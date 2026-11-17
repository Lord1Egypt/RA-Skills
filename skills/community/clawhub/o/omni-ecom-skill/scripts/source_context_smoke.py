"""Real local synthetic context cells; no real-store or acquisition claims."""
import copy
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from claim_guard import validate_claims
from claim_source_guard import validate_sources, validate_report_sources
import source_context_guard as context


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name); self.path=self.root/'source.csv'
        self.rows=[['金额','期间','平台','店铺','渠道','单位'],
                   [100,'2026-07','tmall','synthetic','search','元'],
                   [200,'2026-07','tmall','synthetic','search','元']]
        self.claim=dict(claim_id='C-sales',metric='gmv',value=300,unit='元',status='verified',
            period='2026-07',dimensions={'channel':'search'},source_ref=dict(source_id='synthetic',
                source_file='source.csv',field='金额',range='A2:A3',aggregation='sum',source_sha256='0'*64,
                contexts={key:dict(column=column,field=field) for key,column,field in (
                    ('period','B','期间'),('platform','C','平台'),('store','D','店铺'),
                    ('dimensions.channel','E','渠道'),('unit','F','单位'))}))
        self.data=dict(**__import__('artifact_contract').native_claim_identity('2.0.3'),run_id='synthetic',client_scope='synthetic',period='2026-07',
            source_context_policy='required',scope={'platform':'tmall','store':'synthetic'},claims=[self.claim])
        self.save()

    def save(self):
        with self.path.open('w',encoding='utf-8',newline='') as file: csv.writer(file).writerows(self.rows)
        self.claim['source_ref']['source_sha256']=hashlib.sha256(self.path.read_bytes()).hexdigest()

    def check(self):
        self.assertEqual(validate_claims(self.data)[0],[])
        return validate_sources(self.data,self.root)[0]['source_context']

    def test_all_selected_rows_and_context_columns(self):
        result=self.check()
        self.assertEqual(result['status'],'source_context_verified')
        self.assertEqual(result['observed']['dimensions.channel'],['search'])
        self.assertIn('not_authenticity_or_period_coverage',result['evidence_kind'])

    def test_root_dimension_and_currency_are_not_dropped(self):
        del self.claim['dimensions']
        self.data['scope'].update(dimensions={'channel':'search'},currency='CNY')
        self.rows[0].append('币种'); self.rows[1].append('CNY'); self.rows[2].append('CNY')
        self.claim['source_ref']['contexts']['currency']=dict(column='G',field='币种')
        self.save()
        result=self.check()
        self.assertEqual(result['observed']['dimensions.channel'],['search'])
        self.assertEqual(result['observed']['currency'],['CNY'])

    def test_claim_cannot_override_root_dimension(self):
        self.data['scope']['dimensions']={'channel':'organic'}
        with self.assertRaisesRegex(ValueError,'source_context_scope_conflict'): self.check()

    def test_same_number_other_store_blocked(self):
        self.rows[2][3]='other'; self.save()
        with self.assertRaisesRegex(ValueError,'value_mismatch:store'): self.check()

    def test_same_number_other_channel_blocked(self):
        self.rows[2][4]='recommendation'; self.save()
        with self.assertRaisesRegex(ValueError,'value_mismatch:dimensions.channel'): self.check()

    def test_other_period_blocked(self):
        self.rows[2][1]='2026-06'; self.save()
        with self.assertRaisesRegex(ValueError,'value_mismatch:period'): self.check()

    def test_unit_not_silently_converted(self):
        self.rows[2][5]='万元'; self.save()
        with self.assertRaisesRegex(ValueError,'value_mismatch:unit'): self.check()

    def test_missing_context_strict_block_and_legacy_visible(self):
        self.claim['source_ref'].pop('contexts')
        with self.assertRaisesRegex(ValueError,'source_context_required'): self.check()
        self.data['source_context_policy']='legacy_unbound'
        self.assertEqual(self.check(),{'status':'source_context_unbound'})

    def test_partial_context_cannot_claim_verified(self):
        self.claim['source_ref']['contexts'].pop('store')
        with self.assertRaisesRegex(ValueError,'keys_mismatch'): self.check()

    def test_wrong_context_header_blocked(self):
        self.claim['source_ref']['contexts']['store']['field']='其他列'
        with self.assertRaisesRegex(ValueError,'field_mismatch'): self.check()

    def test_duplicate_context_header_blocked(self):
        self.rows[0][2]='店铺'; self.save()
        self.claim['source_ref']['contexts']['platform']['field']='店铺'
        with self.assertRaisesRegex(ValueError,'field_mismatch'): self.check()

    def test_daily_containment_requires_explicit_mode(self):
        self.data['period']=self.claim['period']='2026-07-01至2026-07-02'
        self.rows[1][1]='2026-07-01'; self.rows[2][1]='2026-07-02'; self.save()
        with self.assertRaisesRegex(ValueError,'value_mismatch:period'): self.check()
        self.claim['source_ref']['period_mode']='contained'
        with self.assertRaisesRegex(ValueError,'period_coverage_required'): self.check()
        self.claim['source_ref']['period_coverage']={'frequency':'daily','status':'complete_no_missing_dates'}
        result=self.check()
        self.assertEqual(result['observed']['period'],['2026-07-01','2026-07-02'])
        self.assertEqual(result['period_coverage']['status'],'complete_daily_period_verified')

    def test_contained_period_missing_day_is_blocked(self):
        self.data['period']=self.claim['period']='2026-07-01至2026-07-03'
        self.rows[1][1]='2026-07-01'; self.rows[2][1]='2026-07-03'
        self.claim['source_ref'].update(period_mode='contained',
            period_coverage={'frequency':'daily','status':'complete_no_missing_dates'})
        self.save()
        with self.assertRaisesRegex(ValueError,'source_context_period_incomplete'): self.check()

    def test_contained_period_duplicate_day_is_blocked(self):
        self.data['period']=self.claim['period']='2026-07-01至2026-07-02'
        self.rows[1][1]=self.rows[2][1]='2026-07-01'
        self.claim['source_ref'].update(period_mode='contained',
            period_coverage={'frequency':'daily','status':'complete_no_missing_dates'})
        self.save()
        with self.assertRaisesRegex(ValueError,'source_context_period_duplicate_date'): self.check()

    def test_opaque_period_labels_are_not_proof(self):
        self.data['period']=self.claim['period']='本期'
        self.rows[1][1]=self.rows[2][1]='本期'; self.save()
        with self.assertRaisesRegex(ValueError,'period_unparsed'): self.check()

    def metadata_fixture(self):
        self.rows=[['报告期','2026-07'],['单位','元'],['金额','平台','店铺','渠道'],
                   [300,'tmall','synthetic','search']]
        self.claim['source_ref'].update(range='A4',header_row=3,contexts={
            'period':dict(cell='B1',label_cell='A1',field='报告期'),
            'unit':dict(cell='B2',label_cell='A2',field='单位'),
            'platform':dict(column='B',field='平台'),'store':dict(column='C',field='店铺'),
            'dimensions.channel':dict(column='D',field='渠道')})
        self.save()

    def test_explicit_source_header_metadata(self):
        self.metadata_fixture(); self.check()
        self.rows[0][0]='非报告期'; self.save()
        with self.assertRaisesRegex(ValueError,'metadata_label_mismatch'): self.check()

    def test_data_row_cannot_masquerade_as_global_metadata(self):
        self.metadata_fixture()
        self.claim['source_ref']['contexts']['period']['cell']='B4'
        with self.assertRaisesRegex(ValueError,'metadata_must_precede_header'): self.check()

    def test_excel_actual_sheet_metadata_and_columns(self):
        import openpyxl
        self.metadata_fixture()
        path=self.root/'source.xlsx'; book=openpyxl.Workbook(); sheet=book.active; sheet.title='数据'
        for row in self.rows: sheet.append(row)
        book.save(path); book.close()
        self.claim['source_ref'].update(source_file=path.name,sheet='数据',
            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        self.check()

    def json_fixture(self):
        path=self.root/'source.json'
        path.write_text(json.dumps({'records':[dict(value=300,period='2026-07',unit='元',
            platform='tmall',store='synthetic',channel='search')]}),encoding='utf-8')
        self.claim['source_ref'].update(source_file=path.name,pointer='/records/0/value',
            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),contexts={
                key:dict(field=key.split('.')[-1]) for key in self.claim['source_ref']['contexts']})

    def test_json_context_is_sibling_of_actual_numeric_record(self):
        self.json_fixture(); self.check()
        self.claim['source_ref']['contexts']['store']={'pointer':'/records/1/store'}
        with self.assertRaisesRegex(ValueError,'json_sibling_required'): self.check()

    def test_conflicting_declared_scope_blocked(self):
        self.claim['store']='synthetic'; self.claim['scope']={'store':'other'}
        with self.assertRaisesRegex(ValueError,'scope_conflict'): self.check()

    def test_source_change_during_context_read_blocked(self):
        original=context.read_values
        def changed(*args):
            result=original(*args); self.path.write_text('changed',encoding='utf-8'); return result
        with patch.object(context,'read_values',changed):
            with self.assertRaisesRegex(ValueError,'changed_during_read'): self.check()

    def test_context_schema(self):
        from jsonschema import Draft202012Validator
        schema=json.loads((Path(__file__).resolve().parents[1]/'schemas'/'claim-ledger.schema.json').read_text(encoding='utf-8'))
        validator=Draft202012Validator(schema)
        self.assertEqual(list(validator.iter_errors(self.data)),[])
        self.claim['source_ref']['contexts']['store']={'column':'D'}
        self.assertTrue(list(validator.iter_errors(self.data)))

    def test_required_policy_cannot_omit_declared_store(self):
        self.data['scope'].pop('store')
        self.claim['source_ref']['contexts'].pop('store')
        with self.assertRaisesRegex(ValueError,'store_platform_required'): self.check()

    def test_summary_does_not_call_legacy_or_empty_verified(self):
        self.check()
        checked=validate_sources(self.data,self.root)
        self.assertEqual(context.summary(checked)['status'],'all_verified_source_labels_checked')
        self.data['source_context_policy']='legacy_unbound'; self.claim['source_ref'].pop('contexts')
        unchecked=validate_sources(self.data,self.root)
        self.assertEqual(context.summary(unchecked)['context_unbound'],1)
        self.assertEqual(context.summary([])['status'],'no_verified_source_labels')

    def report_fixture(self):
        path=self.root/'claims.json'; path.write_text(json.dumps(self.data),encoding='utf-8')
        _,counts=validate_claims(self.data)
        return dict(run_id=self.data['run_id'],client_scope=self.data['client_scope'],period=self.data['period'],
            scope=copy.deepcopy(self.data['scope']),claim_ledger=dict(file=path.name,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),claims=self.data['claims'],
                source_checks=validate_sources(self.data,self.root),**counts))

    def test_report_cannot_relabel_a_verified_source_store(self):
        report=self.report_fixture()
        validate_report_sources(report,self.root,'C-sales')
        report['scope']['store']='other'
        with self.assertRaisesRegex(ValueError,'claim_report_source_context_mismatch'):
            validate_report_sources(report,self.root,'C-sales')

    def test_nested_claim_dimension_is_not_lost_in_display_matching(self):
        from report_metric_guard import validate_delivery_metrics
        self.claim['scope']={'dimensions':self.claim.pop('dimensions')}
        report=self.report_fixture()
        report['metrics']=[dict(period='2026-07',inputs={'gmv':300})]
        with self.assertRaises(ValueError): validate_delivery_metrics(report)
        report['metrics'][0]['dimensions']={'channel':'search'}
        validate_delivery_metrics(report)


if __name__=='__main__': unittest.main()
