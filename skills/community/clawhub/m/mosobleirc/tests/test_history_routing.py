from __future__ import annotations
import sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import mosobleirc_core as core
import gemini_adapter as ga
INV = ROOT / 'tests' / 'fixtures' / 'inventory.fixture.json'

class LocalControlDbTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store=core.StateStore(Path(self.tmp.name)/'data')
        self.store.initialize(core.load_inventory(INV))

    def test_physical_serial_is_independent_from_provider_serial(self):
        self.store.set_meter_identity(1003, physical_serial='PHYSCW02', location_zone='unknown')
        m=self.store.get_meter(1003)
        self.assertEqual(m['serial'], 'TESTCW02')
        self.assertEqual(m['physical_serial'], 'PHYSCW02')

    def test_provider_snapshot_and_photo_observation_are_separate(self):
        payload={'meter':{'id':1003,'lastValue':{'id':77,'total':{'value':865,'consumptionValue':10},'receivedDate':'2026-04-22T18:06:26Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':4},'isAverageValue':False}}}
        self.store.sync_provider_meter(payload, fetched_at='2026-09-15T10:00:00Z')
        self.store.record_photo_reading(1003,881.95,'2026-09-15T09:00:00Z',image_sha256='abc',validation_status='GREEN')
        self.assertEqual(len(self.store.provider_history(1003)),1)
        self.assertEqual(len(self.store.photo_history(1003)),1)
        self.assertEqual(self.store.provider_history(1003)[0]['value'],865)
        self.assertAlmostEqual(self.store.photo_history(1003)[0]['value'],881.95)

    def test_static_inventory_does_not_clobber_newer_live_provider_value(self):
        payload={'meter':{'id':1003,'lastValue':{'id':88,'total':{'value':900,'consumptionValue':5},'receivedDate':'2026-09-15T08:00:00Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':9},'isAverageValue':False}}}
        self.store.sync_provider_meter(payload, fetched_at='2026-09-15T10:00:00Z')
        self.store.initialize(core.load_inventory(INV))
        self.assertEqual(self.store.get_meter(1003)['last_provider_value'],900)

class ConsumptionAssessmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store=core.StateStore(Path(self.tmp.name)/'data')
        self.store.initialize(core.load_inventory(INV))

    def _hist(self,meter_id, values):
        for i,c in enumerate(values,1):
            self.store.add_provider_history(meter_id, provider_value_id=1000+i, value=800+i*10,
                consumption=c, received_date=f'2026-{i:02d}-20T10:00:00Z', settlement_year=2026,
                settlement_month=i, status='PROCESSED', is_average=False, fetched_at='2026-09-15T10:00:00Z')

    def test_assessment_uses_only_same_meter_history(self):
        self._hist(1009,[2,3,2,3,2,3])
        self._hist(1010,[12,14,13,15,14,13])
        a=core.assess_consumption(self.store,1009,205,'2026-09-15',previous_value=189,previous_date='2026-04-22')
        self.assertLess(a['historical_median'],5)
        self.assertEqual(a['meter_id'],1009)

    def test_high_consumption_is_flagged_against_robust_history(self):
        self._hist(1009,[2,3,2,3,2,3])
        a=core.assess_consumption(self.store,1009,260,'2026-09-15',previous_value=189,previous_date='2026-04-22')
        self.assertIn(a['status'],{'WATCH','ANOMALY'})
        self.assertGreater(a['monthly_equivalent'],a['historical_median'])

class PhotoRoutingTests(unittest.TestCase):
    def profiles(self):
        return [
            {'meter_id':1003,'serial':'TESTCW02','physical_serial':'PHYSCW02','meter_type':'ColdWater'},
            {'meter_id':1004,'serial':'TESTHW02','physical_serial':'PHYSHW02','meter_type':'HotWater'},
        ]

    def test_non_meter_photo_stays_generic(self):
        r=ga.route_photo_observation({'is_water_meter':False},self.profiles())
        self.assertEqual(r['route'],'generic_photo')
        self.assertIsNone(r.get('meter_id'))

    def test_unknown_water_meter_stays_generic(self):
        r=ga.route_photo_observation({'is_water_meter':True,'serial_visible':True,'serial':'999999','meter_type':'cold_water'},self.profiles())
        self.assertEqual(r['route'],'generic_photo')

    def test_known_physical_serial_routes_to_meter_without_provider_contact(self):
        r=ga.route_photo_observation({'is_water_meter':True,'serial_visible':True,'serial':'PHYSCW02','meter_type':'cold_water'},self.profiles())
        self.assertEqual(r['route'],'known_meter')
        self.assertEqual(r['meter_id'],1003)
        self.assertFalse(r['provider_contacted'])

        self.assertTrue(r['deep_check_required'])

    def test_unknown_meter_does_not_enter_deep_pipeline(self):
        r=ga.route_photo_observation({'is_water_meter':True,'serial_visible':True,'serial':'999999','meter_type':'cold_water'},self.profiles())
        self.assertEqual(r['route'],'generic_photo')
        self.assertFalse(r['deep_check_required'])

    def test_explicit_user_binding_allows_deep_pipeline_without_visible_serial(self):
        r=ga.route_photo_observation({'is_water_meter':True,'serial_visible':False,'meter_type':'hot_water'},self.profiles(), explicit_meter_id=1004)
        self.assertEqual(r['route'],'known_meter')
        self.assertEqual(r['meter_id'],1004)
        self.assertEqual(r['binding'],'user_explicit')
        self.assertTrue(r['deep_check_required'])

if __name__=='__main__':
    unittest.main(verbosity=2)

class DeterministicSerialIdentificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store=core.StateStore(Path(self.tmp.name)/'data')
        self.store.initialize(core.load_inventory(INV))
        self.store.set_meter_identity(1011, physical_serial='PHYSHW05')
        self.store.set_meter_identity(1012, physical_serial='PHYSHW06')
        self.store.set_meter_identity(1009, physical_serial='PHYSCW05')
        self.store.set_meter_identity(1010, physical_serial='PHYSCW06')

    def test_provider_serial_identifies_fixture_exactly(self):
        m=self.store.identify_meter_by_serial('TESTHW05')
        self.assertEqual(m['meter_id'],1011)
        self.assertEqual(m['apartment'],'Fixture D')

    def test_physical_serial_with_prefix_identifies_same_meter(self):
        m=self.store.identify_meter_by_serial('PHYSHW05')
        self.assertEqual(m['meter_id'],1011)

    def test_unknown_or_empty_serial_does_not_guess(self):
        self.assertIsNone(self.store.identify_meter_by_serial('999999'))
        self.assertIsNone(self.store.identify_meter_by_serial(''))

class ReferenceCannotChooseApartmentTests(unittest.TestCase):
    def test_reference_match_without_serial_does_not_route(self):
        profiles=[{'meter_id':1007,'serial':'TESTHW03','physical_serial':'TESTHW03','meter_type':'HotWater'}]
        r=ga.route_photo_observation({'is_water_meter':True,'serial_visible':False,'meter_type':'hot_water',
                                      'reference_meter_id':1007,'reference_confidence':0.99},profiles)
        self.assertEqual(r['route'],'generic_photo')
        self.assertIsNone(r['meter_id'])
