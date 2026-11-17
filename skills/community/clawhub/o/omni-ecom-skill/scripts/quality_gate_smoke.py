#!/usr/bin/env python3
"""Synthetic integration scenarios for final-delivery quality checks, not host proof."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from analysis_depth_smoke import GOOD_DEPTH, BODY, baseline_with
from coverage_guard_smoke import make_inventory, rep, run_pipeline
from quality_gate import ROLES, read, sha, validate_quality, validate_frozen_quality
from adjudication_guard import fingerprint, calculate, cell_value
from claim_guard import validate_claims
from claim_source_guard import validate_sources
import conflict_scan
from artifact_contract import native_analysis_identity


def write(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')


def write_scope_receipt(root,report,source_files):
    rows=[]
    for path in source_files:
        path=Path(path).resolve()
        rows.append(dict(file=path.relative_to(root.resolve()).as_posix(),sha256=sha(path),size_bytes=path.stat().st_size))
    payload=dict(**__import__('artifact_contract').native_run_scope_identity(report['team_version']),
                 run_id=report['run_id'],client_scope=report['client_scope'],team_version=report['team_version'],
                 status='scope_verified',allowed_roots=['.'],input_paths=[row['file'] for row in rows],
                 files=rows,scanned_files=len(rows),errors=[])
    write(root/'run-scope.json',payload)
    return root/'run-scope.json'


def present_verdict(root,report,verdict):
    """Assemble a synthetic visible decision, not a native report-generation proof."""
    from decision_display import attach,markdown
    attach(report,dict(verdict,adjudicated_claims=report.get('adjudicated_claims',{}),
                       adjudicated_downstream=report.get('adjudicated_downstream',{}),
                       unresolved_conflicts=report.get('unresolved_conflicts',[])))
    body=(root/'report.md').read_text(encoding='utf-8').split('## 专家分歧与总监裁决')[0]
    (root/'report.md').write_text(body.rstrip()+'\n\n'+'\n'.join(markdown(report)),encoding='utf-8')
    write(root/'report.json',report)


class QualityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.report=dict(run_id='quality-test',client_scope='synthetic',team_version='2.0.3',
                         report_revision='R1',collaboration_mode='comprehensive')
        inventory=make_inventory([rep('R001','交易.csv','trade_sales','transaction','analyzable')])
        inventory.update(run_id='quality-test',client_scope='synthetic')
        inv,clusters,plan=run_pipeline(self.root,inventory,'quality')
        base=baseline_with(self.root,'')
        baseline=read(base)
        baseline.update(run_id='quality-test',team_version='2.0.3',created_by_team_version='2.0.3')
        write(base,baseline)
        handoffs={}
        for role in ROLES:
            body=copy.deepcopy(BODY)
            body.update(agent_id=role,run_id='quality-test',agent_version='2.0.3',
                        created_by_team_version='2.0.3',judgments=[])
            body['analysis_depth']=copy.deepcopy(GOOD_DEPTH)
            body['analysis_depth']['created_by_team_version']='2.0.3'
            body['analysis_depth']['baseline_ack']['baseline_sha256']=sha(base)
            path=self.root/(role+'.json')
            write(path,body)
            handoffs[role]=path.name
        config=dict(run_id='quality-test',client_scope='synthetic',report_revision='R1',
                    inventory=inv.name,chapter_plan=plan.name,baseline=base.name,handoffs=handoffs)
        write(self.root/'quality-inputs.json',config)
        # A separate synthetic source isolates claim freezing from conflict
        # fixtures. It is not evidence that all business prose is verified.
        self.report['period']=baseline['scope']['period']
        self.report['scope']={'platform':'tmall','store':'s1'}
        source=self.root/'claim-source.csv'
        source.write_text('合成检查值,期间,平台,店铺,单位\n100,'+self.report['period']+',tmall,s1,数值\n',encoding='utf-8')
        claim=dict(claim_id='C-fixture',metric='synthetic_probe',value=100,unit='数值',status='verified',
                   period=self.report['period'],source_ref=dict(source_id='synthetic-probe',source_file=source.name,
                   range='A2',field='合成检查值',source_sha256=sha(source),
                   contexts={key:dict(column=column,field=field) for key,column,field in
                             [('period','B','期间'),('platform','C','平台'),('store','D','店铺'),('unit','E','单位')]}))
        ledger=dict(**__import__('artifact_contract').native_claim_identity(self.report['team_version']),run_id=self.report['run_id'],client_scope=self.report['client_scope'],
                    period=self.report['period'],scope=self.report['scope'],source_context_policy='required',claims=[claim])
        write(self.root/'claims.json',ledger)
        errors,counts=validate_claims(ledger)
        self.assertEqual(errors,[])
        self.report['claim_ledger']=dict(file='claims.json',sha256=sha(self.root/'claims.json'),**counts,
                                        claims=ledger['claims'],source_checks=validate_sources(ledger,self.root))
        scope=write_scope_receipt(self.root,self.report,[source])
        config=self.config(); config['run_scope']=scope.name; write(self.root/'quality-inputs.json',config)
        write(self.root/'report.json',self.report)
        (self.root/'report.md').write_text('合成测试：R001 交易.csv；C-fixture 为来源冻结测试值 100',encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def config(self):
        return read(self.root/'quality-inputs.json')

    def test_valid_full_recomputation(self):
        result=validate_quality(self.root,self.report)
        self.assertEqual(result['status'],'quality_gate_passed')
        self.assertEqual(len(result['depth']),4)

    def test_legacy_baseline_cannot_support_current_report(self):
        config=self.config(); path=self.root/config['baseline']; baseline=read(path)
        baseline['schema_version']='1.0'
        write(path,baseline)
        with self.assertRaisesRegex(ValueError,'baseline_identity_invalid'):
            validate_quality(self.root,self.report)

    def test_legacy_inventory_cannot_support_current_report(self):
        path=self.root/self.config()['inventory']; value=read(path); value['schema_version']='1.0.0'; write(path,value)
        with self.assertRaisesRegex(ValueError,'stage_identity_invalid'):
            validate_quality(self.root,self.report)

    def test_legacy_chapter_plan_cannot_support_current_report(self):
        path=self.root/self.config()['chapter_plan']; value=read(path); value['schema_version']='1.0.0'; write(path,value)
        with self.assertRaisesRegex(ValueError,'stage_identity_invalid'):
            validate_quality(self.root,self.report)

    def test_legacy_run_scope_cannot_support_current_report(self):
        scope=read(self.root/'run-scope.json')
        scope['schema_version']='1.0'
        write(self.root/'run-scope.json',scope)
        with self.assertRaisesRegex(ValueError,'run_scope_identity_invalid'):
            validate_quality(self.root,self.report)

    def test_run_scope_source_change_blocks(self):
        (self.root/'claim-source.csv').write_text('合成检查值\n999\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'quality_run_scope_source_changed'):
            validate_quality(self.root,self.report)

    def test_body_omission_blocks(self):
        (self.root/'report.md').write_text('缺少文件编号的合成报告',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'coverage_blocked'):
            validate_quality(self.root,self.report)

    def test_cross_client_blocks(self):
        config=self.config()
        config['client_scope']='other-customer'
        write(self.root/'quality-inputs.json',config)
        with self.assertRaisesRegex(ValueError,'identity_mismatch'):
            validate_quality(self.root,self.report)

    def test_missing_member_blocks(self):
        config=self.config()
        del config['handoffs']['ad-profit-optimizer']
        write(self.root/'quality-inputs.json',config)
        with self.assertRaisesRegex(ValueError,'members_missing'):
            validate_quality(self.root,self.report)

    def test_changed_baseline_blocks(self):
        path=self.root/self.config()['baseline']
        base=read(path)
        base['metric_contract']['GMV']['definition']='another definition'
        write(path,base)
        with self.assertRaisesRegex(ValueError,'depth_blocked'):
            validate_quality(self.root,self.report)

    def test_hard_numeric_conflict_blocks(self):
        path=self.root/'ad-profit-optimizer.json'
        handoff=read(path)
        handoff['evidence_ledger'][0]['value']=200000
        write(path,handoff)
        with self.assertRaisesRegex(ValueError,'adjudication_required'):
            validate_quality(self.root,self.report)

    def test_empty_inventory_cannot_pass_vacuously(self):
        path=self.root/self.config()['inventory']
        inventory=read(path)
        inventory.update(reports=[],report_count=0)
        write(path,inventory)
        with self.assertRaisesRegex(ValueError,'inventory_empty'):
            validate_quality(self.root,self.report)

    def test_external_reference_blocks(self):
        config=self.config()
        config['baseline']='../another-client.json'
        write(self.root/'quality-inputs.json',config)
        with self.assertRaisesRegex(ValueError,'outside_or_missing'):
            validate_quality(self.root,self.report)

    def test_weak_depth_blocks(self):
        path=self.root/'data-analyst.json'
        body=read(path)
        body['analysis_depth']['depth_ladder']['reached_level']='L1'
        write(path,body)
        with self.assertRaisesRegex(ValueError,'depth_blocked'):
            validate_quality(self.root,self.report)

    def verdict_fixture(self):
        path=self.root/'ad-profit-optimizer.json'
        handoff=read(path)
        handoff['evidence_ledger'][0]['value']=200000
        write(path,handoff)
        bodies={role:read(self.root/(role+'.json')) for role in ROLES}
        evidence=[r for role,body in bodies.items() for r in conflict_scan.evidence_rows(body,role)]
        found=conflict_scan.scan_numeric(evidence,0.02)
        source=self.root/'交易.csv'
        source.write_text('金额\n60000\n40000\n',encoding='utf-8')
        row=dict(conflict_id=found[0]['conflict_id'],method='lead_recomputation',
                 decision='采用原始文件两行合计',not_adopted_disposition=[{'agent_id':'ad-profit-optimizer','reason':'重复计算'}],
                 residual_risk='合成测试，不代表任何真实客户',
                 inputs={'sales':dict(file=source.name,sha256=sha(source),column='金额',rows=[0,1],aggregation='sum')},
                 formula='sales',result='100000',downstream=[],no_downstream_reason='测试无下游经营建议')
        verdict=dict(**native_analysis_identity('conflict_verdict',self.report['team_version']),
                     **{k:self.report[k] for k in ('run_id','client_scope','team_version','report_revision')},
                     conflicts_sha256=fingerprint(found),verdicts=[row])
        config=self.config()
        config['adjudication']='verdict.json'
        write(self.root/'quality-inputs.json',config)
        write(self.root/'verdict.json',verdict)
        self.report['adjudicated_claims']={row['conflict_id']:dict(metric='GMV',period='202607',unit='元',value=100000)}
        present_verdict(self.root,self.report,verdict)
        return verdict

    def test_numeric_verdict_recomputes_source(self):
        self.verdict_fixture()
        result=validate_quality(self.root,self.report)
        self.assertEqual(result['adjudications'][0]['result'],'100000')
        self.assertTrue(any(r['file']=='交易.csv' for r in result['inputs']))

    def test_unsupported_verdict_method(self):
        v=self.verdict_fixture()
        v['verdicts'][0]['method']='综合判断'
        write(self.root/'verdict.json',v)
        with self.assertRaisesRegex(ValueError,'method_invalid'):
            validate_quality(self.root,self.report)

    def test_changed_raw_source(self):
        self.verdict_fixture()
        (self.root/'交易.csv').write_text('金额\n90000\n40000\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'source_changed'):
            validate_quality(self.root,self.report)

    def test_wrong_recomputed_result(self):
        v=self.verdict_fixture()
        v['verdicts'][0]['result']='200000'
        write(self.root/'verdict.json',v)
        with self.assertRaisesRegex(ValueError,'result_mismatch'):
            validate_quality(self.root,self.report)

    def test_dependent_claim_must_be_updated(self):
        v=self.verdict_fixture()
        v['verdicts'][0]['downstream']=[dict(claim_id='dependent',formula='adjudicated * 2',result='200000')]
        write(self.root/'verdict.json',v)
        self.report['adjudicated_downstream']={'dependent':{'value':100000}}
        write(self.root/'report.json',self.report)
        with self.assertRaisesRegex(ValueError,'downstream_report_stale'):
            validate_quality(self.root,self.report)

    def frozen(self, receipt):
        return dict(quality_gate=receipt,artifacts=[],sources=[dict(path=str(self.root/i['file']),sha256=i['sha256']) for i in receipt['inputs']])

    def test_freeze_all_inputs(self):
        receipt=validate_quality(self.root,self.report)
        validate_frozen_quality(self.frozen(receipt),self.root,receipt)

    def test_missing_frozen_source_blocks(self):
        receipt=validate_quality(self.root,self.report)
        manifest=self.frozen(receipt)
        manifest['sources'].pop()
        with self.assertRaisesRegex(ValueError,'missing_or_changed'):
            validate_frozen_quality(manifest,self.root,receipt)

    def test_source_changed_after_freeze(self):
        receipt=validate_quality(self.root,self.report)
        manifest=self.frozen(receipt)
        (self.root/'report.md').write_text('changed R001',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'missing_or_changed'):
            validate_frozen_quality(manifest,self.root,receipt)

    def test_formula_cannot_execute_code(self):
        with self.assertRaisesRegex(ValueError,'operator_not_allowed'):
            calculate('x + __import__("os").getcwd()',{'x':1})

    def test_zero_denominator(self):
        with self.assertRaisesRegex(ValueError,'zero_denominator'):
            calculate('x / 0',{'x':1})

    def test_excel_offset_header(self):
        import openpyxl
        path=self.root/'offset.xlsx'
        book=openpyxl.Workbook()
        sheet=book.active
        sheet.title='Sheet1'
        sheet.append(['导出标题'])
        sheet.append(['金额','订单'])
        sheet.append([12,1])
        sheet.append([18,2])
        book.save(path)
        book.close()
        value,_,_=cell_value(dict(file=path.name,sha256=sha(path),sheet='Sheet1',header_row=2,
                                 column='金额',rows=[0,1],aggregation='sum'),
                             lambda name:self.root/name, {path.name})
        self.assertEqual(value,30)

    def test_formula_cell_without_cache_not_zero(self):
        import openpyxl
        path=self.root/'formula.xlsx'
        book=openpyxl.Workbook()
        sheet=book.active
        sheet.append(['金额'])
        sheet.append(['=1+1'])
        book.save(path)
        book.close()
        with self.assertRaisesRegex(ValueError,'number_invalid'):
            cell_value(dict(file=path.name,sha256=sha(path),sheet='Sheet',header_row=1,
                            column='金额',rows=[0]),lambda name:self.root/name,{path.name})


if __name__=='__main__':
    unittest.main()
