from __future__ import annotations
import contextlib, importlib.util, io, json, tempfile, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _posix import requires_fcntl
MODULE=ROOT/'scripts'/'mosobleirc.py'; INV=ROOT/'tests'/'fixtures'/'inventory.fixture.json'
spec=importlib.util.spec_from_file_location('mosobleirc_cli_workflow',MODULE)
cli=importlib.util.module_from_spec(spec); spec.loader.exec_module(cli)

class WorkflowCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.data=Path(self.tmp.name)/'data'
    def run_cli(self,*args):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            rc=cli.main(['--data-root',str(self.data),'--inventory',str(INV),*args])
        return rc,json.loads(out.getvalue())
    @requires_fcntl
    def test_local_analysis_never_needs_yandex_credentials(self):
        rc,p=self.run_cli('local','analyze','--meter-id','1003','--value','881','--observed-at','2026-09-15')
        self.assertEqual(rc,0); self.assertFalse(p['provider_contacted'])
        self.assertEqual(p['meter_id'],1003); self.assertEqual(p['previous_provider_value'],865)
        self.assertGreater(p['consumption']['delta'],0)
    @requires_fcntl
    def test_send_prepare_requires_explicit_user_confirmation_before_relay(self):
        rc,p=self.run_cli('send','prepare','--meter-id','1003','--value','881','--observed-at','2026-09-15','--operation-id','op-confirm')
        self.assertNotEqual(rc,0)
        self.assertEqual(p['error'],'CONFIRMATION_REQUIRED')

    @requires_fcntl
    def test_send_execute_requires_matching_prepared_operation(self):
        rc,p=self.run_cli('send','execute','--meter-id','1003','--value','881','--operation-id','op-missing','--confirmed-by-user')
        self.assertNotEqual(rc,0)
        self.assertEqual(p['error'],'PREPARE_REQUIRED')
        self.assertFalse(p['provider_contacted'])

    @requires_fcntl
    def test_send_execute_requires_explicit_confirmation(self):
        rc,p=self.run_cli('send','execute','--meter-id','1003','--value','881','--operation-id','op-1')
        self.assertNotEqual(rc,0)
        self.assertEqual(p['error'],'CONFIRMATION_REQUIRED')
        self.assertFalse(p['provider_contacted'])



    @requires_fcntl
    def test_pre_send_photo_cannot_be_persisted(self):
        rc,p=self.run_cli('local','record-photo','--meter-id','1003','--value','881.95','--observed-at','2026-09-15T09:00:00Z','--status','GREEN')
        self.assertNotEqual(rc,0)
        self.assertEqual(p['error'],'PERSIST_BEFORE_VERIFICATION_FORBIDDEN')
        self.assertEqual(len(cli.StateStore(self.data).photo_history(1003)),0)

    @requires_fcntl
    def test_prepare_does_not_mutate_provider_history_or_meter_snapshot(self):
        class FakeRelay:
            def call(self,action,**payload):
                self_outer.assertEqual(action,'meters')
                return {'ok':True,'data':[{'meter':{'id':1003,'lastValue':{'id':99,'total':{'value':900,'consumptionValue':7},'receivedDate':'2026-09-15T10:00:00Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':9},'isAverageValue':False}},'valueSendInfo':{'isAbleToSendMeterValues':True,'isInAllowedPeriod':True,'isValueSentForCurrentPeriod':False}}]}
        self_outer=self
        old=cli._relay; cli._relay=lambda args: FakeRelay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','prepare','--meter-id','1003','--value','901','--photo-value','901.234','--observed-at','2026-09-15','--operation-id','op-nomutate','--confirmed-by-user')
        self.assertEqual(rc,0)
        store=cli.StateStore(self.data)
        self.assertEqual(store.get_meter(1003)['last_provider_value'],865)
        self.assertEqual(store.provider_history(1003),[])
        self.assertEqual(store.photo_history(1003),[])

    @requires_fcntl
    def test_verified_execute_uses_fresh_preflight_then_commits_once_from_relay_readback(self):
        calls=[]
        before={'meter':{'id':1003,'lastValue':{'id':10,'total':{'value':865,'consumptionValue':10},'receivedDate':'2026-04-22T18:00:00Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':4},'isAverageValue':False}},'valueSendInfo':{'isAbleToSendMeterValues':True,'isInAllowedPeriod':True,'isValueSentForCurrentPeriod':False}}
        after={'meter':{'id':1003,'lastValue':{'id':11,'total':{'value':881,'consumptionValue':16},'receivedDate':'2026-09-15T15:10:00Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':9},'isAverageValue':False}},'valueSendInfo':{'isAbleToSendMeterValues':True,'isInAllowedPeriod':True,'isValueSentForCurrentPeriod':True}}
        class FakeRelay:
            def call(self,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[before]}
                if action=='submit': return {'ok':True,'provider_contacted':True,'operation_id':payload['operation_id'],'status':'VERIFIED','value':881,'readback_meter':after}
                raise AssertionError(action)
        old=cli._relay; cli._relay=lambda args:FakeRelay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,_=self.run_cli('send','prepare','--meter-id','1003','--value','881','--photo-value','881.95','--observed-at','2026-09-15T09:00:00Z','--operation-id','op-atomic','--confirmed-by-user')
        self.assertEqual(rc,0)
        rc,q=self.run_cli('send','execute','--meter-id','1003','--value','881','--operation-id','op-atomic','--confirmed-by-user')
        self.assertEqual(rc,0); self.assertEqual(q['status'],'VERIFIED')
        self.assertEqual(calls,['meters','meters','submit'])
        store=cli.StateStore(self.data)
        self.assertEqual(store.get_meter(1003)['last_provider_value'],881)
        self.assertEqual(len(store.provider_history(1003)),1)
        self.assertEqual(len(store.photo_history(1003)),1)
        self.assertAlmostEqual(store.photo_history(1003)[0]['value'],881.95)


class SkillTextTests(unittest.TestCase):
    def test_image_only_routing_and_provider_guard_are_explicit(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('фото без текста',text)
        self.assertIn('обычн',text)
        self.assertIn('не обращайся в мособлеирц',text)
        self.assertIn('явн',text)
        self.assertIn('отправ',text)
    def test_four_meter_apartments_are_never_aggregated_for_anomaly_stats(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('каждому прибору отдельно',text)
        self.assertIn('не сумм',text)


class ReconcileWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.data=Path(self.tmp.name)/'data'
    def run_cli(self,*args):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            rc=cli.main(['--data-root',str(self.data),'--inventory',str(INV),*args])
        return rc,json.loads(out.getvalue())
    def _prepare(self,op='op-r',value='881'):
        before={'meter':{'id':1003,'lastValue':{'id':10,'total':{'value':865,'consumptionValue':10},'receivedDate':'2026-04-22T18:00:00Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':4},'isAverageValue':False}},'valueSendInfo':{'isAbleToSendMeterValues':True,'isInAllowedPeriod':True,'isValueSentForCurrentPeriod':False}}
        class Relay:
            def call(self,action,**payload): return {'ok':True,'data':[before]}
        old=cli._relay; cli._relay=lambda args:Relay()
        try:
            rc,p=self.run_cli('send','prepare','--meter-id','1003','--value',value,'--photo-value','881.95','--observed-at','2026-09-15T09:00:00Z','--operation-id',op,'--confirmed-by-user')
        finally: cli._relay=old
        self.assertEqual(rc,0)
        return cli.StateStore(self.data)
    @requires_fcntl
    def test_prepare_refuses_new_operation_when_same_value_is_executing(self):
        store=self._prepare('op-old','881')
        store.update_operation('op-old','EXECUTING',updated_at='2026-09-15T09:01:00Z')
        class NeverRelay:
            def call(self,*a,**k): raise AssertionError('provider must not be contacted before reconcile')
        old=cli._relay; cli._relay=lambda args:NeverRelay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','prepare','--meter-id','1003','--value','881','--photo-value','881.95','--observed-at','2026-09-15T09:02:00Z','--operation-id','op-new','--confirmed-by-user')
        self.assertNotEqual(rc,0)
        self.assertEqual(p['error'],'RECONCILE_REQUIRED')
        self.assertEqual(p['existing_operation_id'],'op-old')
        self.assertFalse(p['provider_contacted'])
    @requires_fcntl
    def test_reconcile_closes_executing_when_provider_has_same_processed_value(self):
        store=self._prepare('op-r','881'); store.update_operation('op-r','EXECUTING',updated_at='2026-09-15T09:01:00Z')
        after={'meter':{'id':1003,'lastValue':{'id':11,'total':{'value':881,'consumptionValue':16},'receivedDate':'2026-09-15T15:10:00Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':9},'isAverageValue':False}},'valueSendInfo':{'isAbleToSendMeterValues':True,'isInAllowedPeriod':True,'isValueSentForCurrentPeriod':True}}
        calls=[]
        class Relay:
            def call(self,action,**payload): calls.append(action); return {'ok':True,'data':[after]}
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','reconcile','--operation-id','op-r')
        self.assertEqual(rc,0); self.assertEqual(p['status'],'VERIFIED'); self.assertEqual(calls,['meters'])
        self.assertEqual(cli.StateStore(self.data).get_operation('op-r')['status'],'VERIFIED')
        self.assertEqual(cli.StateStore(self.data).get_meter(1003)['last_provider_value'],881)
    @requires_fcntl
    def test_reconcile_never_posts_and_keeps_uncertain_when_provider_still_old(self):
        store=self._prepare('op-r2','881'); store.update_operation('op-r2','EXECUTING',updated_at='2026-09-15T09:01:00Z')
        old={'meter':{'id':1003,'lastValue':{'id':10,'total':{'value':865,'consumptionValue':10},'receivedDate':'2026-04-22T18:00:00Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':4},'isAverageValue':False}},'valueSendInfo':{'isAbleToSendMeterValues':True,'isInAllowedPeriod':True,'isValueSentForCurrentPeriod':False}}
        calls=[]
        class Relay:
            def call(self,action,**payload): calls.append(action); return {'ok':True,'data':[old]}
        oldrelay=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',oldrelay))
        rc,p=self.run_cli('send','reconcile','--operation-id','op-r2')
        self.assertNotEqual(rc,0); self.assertEqual(p['status'],'UNCERTAIN_NO_RETRY'); self.assertEqual(calls,['meters'])
        self.assertEqual(cli.StateStore(self.data).get_operation('op-r2')['status'],'UNCERTAIN_NO_RETRY')

class SingleTurnSendContractTests(unittest.TestCase):
    def test_skill_uses_one_confirmed_send_command(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('send readings',text)
        self.assertIn('одного подтверждения',text)
        self.assertIn('не создавай и не выбирай `operation_id`',text)
        self.assertNotIn('не выполняй send execute в том же turn',text)
        self.assertNotIn('следующего отдельного сообщения пользователя',text)

class UncertainStateTests(WorkflowCliTests):
    def _seed_uncertain(self, opid='op-u'):
        store=cli.StateStore(self.data); store.initialize(cli.load_inventory(INV))
        store.prepare_operation(opid,meter_id=1003,value=881,observed_at='2026-09-15T09:00:00Z',
            provider_snapshot={'provider_value':865},consumption={'status':'NORMAL'},ready=True,created_at='2026-09-15T09:00:00Z',photo_value=881.95)
        store.update_operation(opid,'UNCERTAIN_NO_RETRY',result={'ok':False,'status':'UNCERTAIN_NO_RETRY'},updated_at='2026-09-15T09:01:00Z')

    @requires_fcntl
    def test_prepare_refuses_new_operation_when_same_value_is_uncertain(self):
        self._seed_uncertain()
        class NeverRelay:
            def call(self,*a,**k): raise AssertionError('provider must not be contacted before reconcile')
        old=cli._relay; cli._relay=lambda args:NeverRelay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','prepare','--meter-id','1003','--value','881','--photo-value','881.95','--observed-at','2026-09-15T09:02:00Z','--operation-id','op-new','--confirmed-by-user')
        self.assertNotEqual(rc,0); self.assertEqual(p['error'],'RECONCILE_REQUIRED'); self.assertEqual(p['existing_operation_id'],'op-u')

    @requires_fcntl
    def test_reconcile_accepts_uncertain_no_retry_and_never_posts(self):
        self._seed_uncertain()
        after={'meter':{'id':1003,'lastValue':{'id':11,'total':{'value':881,'consumptionValue':16},'receivedDate':'2026-09-15T15:10:00Z','status':'PROCESSED','settlementPeriod':{'year':2026,'month':9},'isAverageValue':False}},'valueSendInfo':{'isAbleToSendMeterValues':True,'isInAllowedPeriod':True,'isValueSentForCurrentPeriod':True}}
        calls=[]
        class FakeRelay:
            def call(self,action,**payload): calls.append(action); return {'ok':True,'data':[after]}
        old=cli._relay; cli._relay=lambda args:FakeRelay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','reconcile','--operation-id','op-u')
        self.assertEqual(rc,0); self.assertEqual(p['status'],'VERIFIED'); self.assertEqual(calls,['meters']); self.assertFalse(p['post_attempted'])

    def test_skill_hides_low_level_send_state_machine_from_model(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('send readings',text)
        self.assertIn('не создавай и не выбирай `operation_id`',text)
        self.assertIn('не вызывай `send prepare`',text)
        self.assertIn('слепого повторного post нет',text)


class SingleCommandSendWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.data=Path(self.tmp.name)/'data'
    def run_cli(self,*args):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            rc=cli.main(['--data-root',str(self.data),'--inventory',str(INV),*args])
        return rc,json.loads(out.getvalue())
    @staticmethod
    def entry(meter_id,value,sent=False,status='PROCESSED'):
        return {'meter':{'id':meter_id,'lastValue':{'id':100+meter_id,'total':{'value':value,'consumptionValue':1},'receivedDate':'2026-09-15T10:00:00Z','status':status,'settlementPeriod':{'year':2026,'month':9},'isAverageValue':False}},'valueSendInfo':{'isAbleToSendMeterValues':True,'isInAllowedPeriod':True,'isValueSentForCurrentPeriod':sent}}
    @requires_fcntl
    def test_readings_requires_confirmation_before_provider_contact(self):
        class NeverRelay:
            def call(self,*a,**k): raise AssertionError('provider must not be contacted')
        old=cli._relay; cli._relay=lambda args:NeverRelay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--observed-at','2026-09-15T09:00:00Z')
        self.assertNotEqual(rc,0); self.assertEqual(p['error'],'CONFIRMATION_REQUIRED'); self.assertFalse(p['provider_contacted'])
    @requires_fcntl
    def test_readings_runs_preflight_submit_and_commits_verified_result(self):
        calls=[]; before=self.entry(1003,865,False); after=self.entry(1003,881,True)
        class Relay:
            def call(_,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[before]}
                if action=='submit': return {'ok':True,'provider_contacted':True,'operation_id':payload['operation_id'],'status':'VERIFIED','value':881,'readback_meter':after}
                raise AssertionError(action)
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--observed-at','2026-09-15T09:00:00Z','--confirmed-by-user')
        self.assertEqual(rc,0); self.assertEqual(calls,['meters','submit']); self.assertEqual(p['results'][0]['status'],'VERIFIED')
        store=cli.StateStore(self.data); self.assertEqual(store.get_meter(1003)['last_provider_value'],881); self.assertEqual(len(store.photo_history(1003)),1)
    @requires_fcntl
    def test_verified_override_preserves_photo_value_and_marks_manual_override(self):
        calls=[]; before=self.entry(1003,882,False); after=self.entry(1003,883,True)
        class Relay:
            def call(_,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[before]}
                if action=='submit': return {'ok':True,'provider_contacted':True,'operation_id':payload['operation_id'],'status':'VERIFIED','value':883,'readback_meter':after}
                raise AssertionError(action)
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,payload=self.run_cli('send','readings','--reading','1003:883:881.95','--observed-at','2026-09-15T09:00:00Z','--confirmed-by-user')
        self.assertEqual(rc,0)
        self.assertEqual(payload['results'][0]['value'],883)
        self.assertEqual(payload['results'][0]['photo_value'],881.95)
        hist=cli.StateStore(self.data).photo_history(1003)
        self.assertEqual(hist[-1]['value'],881.95)
        self.assertEqual(hist[-1]['payload']['submitted_value'],883)
        self.assertTrue(hist[-1]['payload']['manual_override'])

    @requires_fcntl
    def test_readings_preserves_partial_results_when_submit_network_fails(self):
        before1=self.entry(1003,865,False); before2=self.entry(1004,430,False); after1=self.entry(1003,881,True)
        class Relay:
            def call(_,action,**payload):
                if action=='meters': return {'ok':True,'data':[before1,before2]}
                if action=='submit' and payload['meter_id']==1003:
                    return {'ok':True,'provider_contacted':True,'operation_id':payload['operation_id'],'status':'VERIFIED','value':881,'readback_meter':after1}
                if action=='submit' and payload['meter_id']==1004:
                    raise cli.RelayNetworkError('relay timeout')
                raise AssertionError(action)
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,payload=self.run_cli('send','readings',
            '--reading','1003:881:881.95','--reading','1004:445:445.2',
            '--observed-at','2026-09-15T09:00:00Z','--confirmed-by-user')
        self.assertNotEqual(rc,0)
        self.assertEqual([x['status'] for x in payload['results']],['VERIFIED','UNCERTAIN_NO_RETRY'])
        self.assertEqual(payload['results'][0]['photo_value'],881.95)
        self.assertEqual(payload['results'][1]['photo_value'],445.2)
        self.assertTrue(payload['results'][1]['post_attempted'])
        store=cli.StateStore(self.data)
        self.assertEqual(len(store.photo_history(1003)),1)
        self.assertEqual(len(store.photo_history(1004)),0)

    @requires_fcntl
    def test_readings_batches_preflight_for_two_meters_of_same_apartment(self):
        calls=[]; before1=self.entry(1003,865,False); before2=self.entry(1004,430,False)
        after1=self.entry(1003,881,True); after2=self.entry(1004,445,True)
        class Relay:
            def call(_,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[before1,before2]}
                if action=='submit':
                    rb=after1 if payload['meter_id']==1003 else after2
                    return {'ok':True,'provider_contacted':True,'operation_id':payload['operation_id'],'status':'VERIFIED','value':payload['value'],'readback_meter':rb}
                raise AssertionError(action)
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--reading','1004:445:445.2','--observed-at','2026-09-15T09:00:00Z','--confirmed-by-user')
        self.assertEqual(rc,0); self.assertEqual(calls,['meters','submit','submit']); self.assertEqual([x['status'] for x in p['results']],['VERIFIED','VERIFIED'])
    @requires_fcntl
    def test_readings_does_not_post_when_same_value_already_sent(self):
        calls=[]; current=self.entry(1003,881,True)
        class Relay:
            def call(_,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[current]}
                raise AssertionError('submit must not be called')
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--observed-at','2026-09-15T09:00:00Z','--confirmed-by-user')
        self.assertEqual(rc,0); self.assertEqual(calls,['meters']); self.assertEqual(p['results'][0]['status'],'ALREADY_SENT')

class SingleCommandSendRecoveryTests(SingleCommandSendWorkflowTests):
    def seed_uncertain(self, opid='old-u', value=881):
        store=cli.StateStore(self.data); store.initialize(cli.load_inventory(INV))
        store.prepare_operation(opid,meter_id=1003,value=value,observed_at='2026-09-15T09:00:00Z',
            provider_snapshot={'provider_value':865},consumption={'status':'NORMAL'},ready=True,
            created_at='2026-09-15T09:00:00Z',photo_value=881.95)
        store.update_operation(opid,'UNCERTAIN_NO_RETRY',result={'ok':False,'status':'UNCERTAIN_NO_RETRY'},updated_at='2026-09-15T09:01:00Z')
        return store

    @requires_fcntl
    def test_readings_reconciles_uncertain_as_already_sent_without_post(self):
        store=self.seed_uncertain(); calls=[]; current=self.entry(1003,881,True)
        class Relay:
            def call(_,action,**payload): calls.append(action); return {'ok':True,'data':[current]}
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--observed-at','2026-09-15T10:00:00Z','--confirmed-by-user')
        self.assertEqual(rc,0); self.assertEqual(calls,['meters']); self.assertEqual(p['results'][0]['status'],'ALREADY_SENT')
        self.assertEqual(store.get_operation('old-u')['status'],'VERIFIED'); self.assertEqual(len(store.photo_history(1003)),1)

    @requires_fcntl
    def test_readings_never_retries_uncertain_after_single_negative_readback(self):
        store=self.seed_uncertain(); calls=[]; before=self.entry(1003,865,False)
        class Relay:
            def call(_,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[before]}
                raise AssertionError('submit must not be called while previous outcome is unresolved')
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--observed-at','2026-09-15T10:00:00Z','--confirmed-by-user')
        self.assertNotEqual(rc,0); self.assertEqual(calls,['meters']); self.assertEqual(p['results'][0]['status'],'RECONCILE_REQUIRED')
        self.assertEqual(store.get_operation('old-u')['status'],'UNCERTAIN_NO_RETRY')

    @requires_fcntl
    def test_readings_never_retries_uncertain_submit(self):
        calls=[]; before=self.entry(1003,865,False)
        class Relay:
            def call(_,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[before]}
                if action=='submit': return {'ok':False,'provider_contacted':True,'operation_id':payload['operation_id'],'status':'UNCERTAIN_NO_RETRY','value':881}
                raise AssertionError(action)
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--observed-at','2026-09-15T10:00:00Z','--confirmed-by-user')
        self.assertNotEqual(rc,0); self.assertEqual(calls,['meters','submit']); self.assertEqual(p['results'][0]['status'],'UNCERTAIN_NO_RETRY')
        self.assertEqual(len(cli.StateStore(self.data).photo_history(1003)),0)

    @requires_fcntl
    def test_blocked_meter_does_not_block_other_meter_in_same_batch(self):
        calls=[]; blocked=self.entry(1003,870,True); before2=self.entry(1004,430,False); after2=self.entry(1004,445,True)
        class Relay:
            def call(_,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[blocked,before2]}
                if action=='submit': return {'ok':True,'provider_contacted':True,'operation_id':payload['operation_id'],'status':'VERIFIED','value':445,'readback_meter':after2}
                raise AssertionError(action)
        old=cli._relay; cli._relay=lambda args:Relay(); self.addCleanup(lambda:setattr(cli,'_relay',old))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--reading','1004:445:445.2','--observed-at','2026-09-15T10:00:00Z','--confirmed-by-user')
        self.assertNotEqual(rc,0); self.assertEqual(calls,['meters','submit']); self.assertEqual([x['status'] for x in p['results']],['BLOCKED','VERIFIED'])

    @requires_fcntl
    def test_consumption_anomaly_is_warning_not_write_blocker_after_confirmation(self):
        calls=[]; before=self.entry(1003,865,False); after=self.entry(1003,881,True)
        class Relay:
            def call(_,action,**payload):
                calls.append(action)
                if action=='meters': return {'ok':True,'data':[before]}
                if action=='submit': return {'ok':True,'provider_contacted':True,'operation_id':payload['operation_id'],'status':'VERIFIED','value':881,'readback_meter':after}
                raise AssertionError(action)
        oldrelay=cli._relay; oldassess=cli.assess_consumption
        cli._relay=lambda args:Relay(); cli.assess_consumption=lambda *a,**k:{'status':'ANOMALY','delta':16}
        self.addCleanup(lambda:setattr(cli,'_relay',oldrelay)); self.addCleanup(lambda:setattr(cli,'assess_consumption',oldassess))
        rc,p=self.run_cli('send','readings','--reading','1003:881:881.95','--observed-at','2026-09-15T10:00:00Z','--confirmed-by-user')
        self.assertEqual(rc,0); self.assertEqual(calls,['meters','submit']); self.assertEqual(p['results'][0]['status'],'VERIFIED'); self.assertIn('consumption_anomaly',p['results'][0]['warnings'])
class SingleCommandSendInterfaceTests(unittest.TestCase):
    def test_cli_accepts_send_readings_action(self):
        parser=cli.build_parser()
        try:
            args=parser.parse_args(['send','readings','--reading','1003:881:881.95','--observed-at','2026-09-15T09:00:00Z','--confirmed-by-user'])
        except SystemExit:
            self.fail('send readings must be a supported CLI action')
        self.assertEqual(args.send_action,'readings')

    def test_skill_uses_one_user_confirmation_for_write_flow(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8').lower()
        self.assertIn('send readings',text)
        self.assertIn('одного',text)
        self.assertIn('отправляй',text)
        self.assertNotIn('не выполняй send execute в том же turn',text)
        self.assertNotIn('следующего отдельного сообщения пользователя',text)

if __name__=='__main__': unittest.main(verbosity=2)
