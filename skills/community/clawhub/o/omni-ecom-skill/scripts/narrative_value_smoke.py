"""Narrative number bindings use synthetic report values, not business advice."""
import json
import unittest
from pathlib import Path

import quality_gate_smoke as fixture
from narrative_value_guard import validate_narrative_numbers,business_numbers
from quality_gate import validate_quality


class NarrativeTests(unittest.TestCase):
    def setUp(self):
        self.fx=fixture.QualityTests(); self.fx.setUp(); self.addCleanup(self.fx.tearDown)
        self.report=self.fx.report
        self.claim=self.report['claim_ledger']['claims'][0]
        self.report.update(facts=[],judgments=[],hypotheses=[],actions=[])

    def bind(self,field,token,claim_id='C-fixture',occurrence=1):
        return dict(field=field,token=token,occurrence=occurrence,kind='claim',claim_id=claim_id)

    def proposal(self,field,token,**extra):
        value=dict(field=field,token=token,occurrence=1,kind='proposal',label='target',
                   basis_claim_ids=['C-fixture'],rationale='以已核验基线做小范围测试，不代表历史事实')
        value.update(extra); return value

    def test_fact_number_must_bind_actual_claim(self):
        self.report['facts']=[dict(claim='合成成交为100',number_bindings=[self.bind('claim','100')])]
        self.assertEqual(validate_narrative_numbers(self.report)['checked'],1)
        self.report['facts'][0].pop('number_bindings')
        with self.assertRaisesRegex(ValueError,'number_binding_mismatch'): validate_narrative_numbers(self.report)

    def test_same_token_occurrences_are_individually_bound(self):
        self.report['facts']=[dict(claim='本期100，对账仍为100',number_bindings=[
            self.bind('claim','100',occurrence=1),self.bind('claim','100',occurrence=2)])]
        self.assertEqual(validate_narrative_numbers(self.report)['checked'],2)
        self.report['facts'][0]['number_bindings'].pop()
        with self.assertRaisesRegex(ValueError,'number_binding_mismatch'): validate_narrative_numbers(self.report)

    def test_wrong_value_id_or_unit_blocked(self):
        self.report['facts']=[dict(claim='花费8131元',number_bindings=[self.bind('claim','8131元')])]
        with self.assertRaisesRegex(ValueError,'claim_value_mismatch'): validate_narrative_numbers(self.report)
        self.report['facts'][0]['number_bindings'][0]['claim_id']='C-missing'
        with self.assertRaisesRegex(ValueError,'claim_id_missing'): validate_narrative_numbers(self.report)
        self.report['facts'][0].update(claim='花费100元',number_bindings=[self.bind('claim','100元')])
        with self.assertRaisesRegex(ValueError,'claim_unit_mismatch'): validate_narrative_numbers(self.report)

    def test_percent_and_wanyuan_compare_canonical_value(self):
        self.claim.update(claim_id='C-rate',value=20,unit='%')
        self.report['facts']=[dict(claim='转化率20%',number_bindings=[self.bind('claim','20%','C-rate')])]
        validate_narrative_numbers(self.report)
        self.claim.update(claim_id='C-gmv',value=10000,unit='元')
        self.report['facts']=[dict(claim='成交1万元',number_bindings=[self.bind('claim','1万元','C-gmv')])]
        validate_narrative_numbers(self.report)

    def test_dates_durations_ids_and_due_are_not_business_values(self):
        text='R001 在2026-07复查，观察7天，T+2完成，版本v2.0'
        self.assertEqual(business_numbers(text),[])
        self.report['actions']=[dict(action=text,due='T+2',number_bindings=[])]
        validate_narrative_numbers(self.report)

    def test_proposal_cannot_disguise_fact_or_baseline(self):
        self.report['facts']=[dict(claim='花费500元',number_bindings=[self.proposal('claim','500元')])]
        with self.assertRaisesRegex(ValueError,'proposal_location_forbidden'): validate_narrative_numbers(self.report)
        self.report.update(facts=[],actions=[dict(baseline='当前500元',approval_required=True,approval_state='pending',
            number_bindings=[self.proposal('baseline','500元')])])
        with self.assertRaisesRegex(ValueError,'proposal_location_forbidden'): validate_narrative_numbers(self.report)

    def test_proposal_needs_basis_reason_and_type(self):
        row=dict(action='测试目标500元',approval_required=True,approval_state='pending',
                 number_bindings=[self.proposal('action','500元')])
        self.report['actions']=[row]; validate_narrative_numbers(self.report)
        for key in ('basis_claim_ids','rationale','label'):
            old=row['number_bindings'][0].pop(key)
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'proposal_'):
                validate_narrative_numbers(self.report)
            row['number_bindings'][0][key]=old

    def test_financial_proposal_requires_approval(self):
        row=dict(action='小测预算500元',approval_required=False,approval_state='not_required',
                 number_bindings=[self.proposal('action','500元')])
        self.report['actions']=[row]
        with self.assertRaisesRegex(ValueError,'requires_approval'): validate_narrative_numbers(self.report)
        row.update(approval_required=True,approval_state='pending')
        validate_narrative_numbers(self.report)

    def test_extra_binding_without_number_is_blocked(self):
        self.report['facts']=[dict(claim='没有经营数值',number_bindings=[self.bind('claim','100')])]
        with self.assertRaisesRegex(ValueError,'number_binding_mismatch'): validate_narrative_numbers(self.report)

    def test_quality_gate_includes_narrative_result(self):
        self.report['facts']=[dict(claim='来源冻结值100',number_bindings=[self.bind('claim','100')])]
        fixture.write(self.fx.root/'report.json',self.report)
        (self.fx.root/'report.md').write_text('R001 交易.csv；C-fixture；来源冻结值100',encoding='utf-8')
        result=validate_quality(self.fx.root,self.report)
        self.assertEqual(result['narrative_value_gate']['status'],'narrative_numbers_bound')

    def test_binding_shapes_are_declared_in_both_schemas(self):
        from jsonschema import Draft202012Validator
        schemas=Path(__file__).resolve().parents[1]/'schemas'
        binding=self.bind('claim','100')
        handoff=json.loads((schemas/'handoff.schema.json').read_text(encoding='utf-8'))
        report=json.loads((schemas/'report-package.schema.json').read_text(encoding='utf-8'))
        self.assertEqual(list(Draft202012Validator(handoff['$defs']['number_bindings']).iter_errors([binding])),[])
        self.assertEqual(list(Draft202012Validator(report['$defs']['narrative_item']).iter_errors(
            {'number_bindings':[binding]})),[])


if __name__=='__main__': unittest.main()
