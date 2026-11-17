"""Automatic decision delivery tests, all business/agent inputs synthetic."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import decision_display as display
import quality_gate_smoke as quality_fixture
from quality_gate import validate_quality
from analysis_depth_smoke import BODY


ROOT=Path(__file__).resolve().parents[1]
PROFILES=json.loads((ROOT/'config/task-profiles.json').read_text(encoding='utf-8'))['profiles']


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')


def prepare_builder_sample(root,task_type):
    """Fixture inputs for the actual builder CLI, not native collaborator evidence."""
    root=Path(root)
    root.mkdir(exist_ok=True)
    version=json.loads((ROOT/'version-info.json').read_text(encoding='utf-8'))['team_version']
    mode=PROFILES[task_type]['default_collaboration_mode']
    period={'weekly_report':'2026-W28','quarterly_report':'2026-Q3','annual_report':'2026',
            'campaign_review':'2026-06-01 至 2026-06-18'}.get(task_type,'2026-07')
    identity=dict(run_id='synthetic-'+task_type,client_scope='synthetic',team_version=version,report_revision='R1')
    source=root/'synthetic-source.csv'
    source.write_text('金额\n60000\n40000\n',encoding='utf-8')
    from quality_gate import sha
    primary=copy.deepcopy(BODY)
    from artifact_contract import native_handoff_identity
    primary.update(native_handoff_identity(version))
    primary.update(run_id=identity['run_id'],agent_version=version,client_scope='synthetic',
                   agent_id='omni-ecom-team-lead' if mode=='comprehensive' else 'data-analyst',
                   gate_status='WARN',judgments=[],facts=[dict(id='F1',claim='合成来源金额合计为 100000 元',evidence_ids=['E1'],
                       number_bindings=[dict(field='claim',token='100000 元',occurrence=1,kind='claim',claim_id='C-gmv')])],
                   contribution_summary='合成输入，仅检查生成链路；无真实专家调用',
                   evidence_kind='synthetic_fixture')
    primary['scope'].update(store='合成测试店铺',period=period)
    primary['evidence_ledger']=[dict(id='E1',metric='GMV',value=100000,unit='元',period=period,
        source=source.name,status='verified',source_sha256=sha(source))]
    primary['risks']=['全部数据、岗位回传和裁决均为合成测试，不代表真实客户或正式 2.0 发布。']
    write(root/'primary.json',primary)
    members=[]
    if mode=='comprehensive':
        for role in quality_fixture.ROLES:
            item=copy.deepcopy(primary)
            item.update(agent_id=role,agent_task_id='agent-synthetic-'+role,agent_return_status='completed',
                        agent_returned_at='2026-09-08T00:00:00Z',agent_return_file=role+'.return.json',
                        agent_return_sha256='a'*64)
            path=root/(role+'.json'); write(path,item); members.extend(['--member-handoff',str(path)])
    claim=dict(claim_id='C-gmv',metric='gmv',value=100000,unit='元',period=period,status='verified',
               source_ref=dict(source_id='synthetic-source',source_file=source.name,sheet='data',range='A2:A3',
                               field='金额',aggregation='sum',source_sha256=sha(source)))
    write(root/'claims.json',dict(**__import__('artifact_contract').native_claim_identity(version),run_id=identity['run_id'],client_scope='synthetic',period=period,claims=[claim]))
    verdict=dict(**__import__('artifact_contract').native_analysis_identity('conflict_verdict',version),
        **identity,verdicts=[dict(conflict_id='X-NUM-001',method='lead_recomputation',
        decision='按合成原始表两行合计采用',not_adopted_disposition='未采纳重复计算后的金额',
        residual_risk='这是合成测试，不是实际经营结论',challenge_review=[dict(role='data-analyst',
        disposition='adopted',reason='合成回复展示测试',return_event_hash='b'*64)])],
        adjudicated_claims={'X-NUM-001':dict(metric='GMV',value=100000,unit='元',period=period)})
    write(root/'adjudication.json',verdict)
    write(root/'quality-inputs.json',dict(run_id=identity['run_id'],client_scope='synthetic',report_revision='R1',
                                        adjudication='adjudication.json'))
    write(root/'report-config.json',dict(title='候选功能合成测试—'+PROFILES[task_type]['display_name']))
    return [sys.executable,str(ROOT/'scripts/build_report_package.py'),'--handoff',str(root/'primary.json'),
            '--client-scope','synthetic','--task-type',task_type,'--collaboration-mode',mode,
            '--claim-ledger',str(root/'claims.json'),'--config',str(root/'report-config.json'),
            '--output-dir',str(root),*members]


class AutomaticDecisionTests(unittest.TestCase):
    def setUp(self):
        self.fx=quality_fixture.QualityTests(); self.fx.setUp()
        self.addCleanup(self.fx.tearDown)
        self.root,self.report=self.fx.root,self.fx.report
        self.verdict=self.fx.verdict_fixture()
        self.verdict['adjudicated_claims']=copy.deepcopy(self.report['adjudicated_claims'])
        write(self.root/'verdict.json',self.verdict)

    def test_default_uses_configured_decision_without_extra_argument(self):
        blank={k:self.report[k] for k in ('run_id','client_scope','team_version','report_revision')}
        self.assertTrue(display.auto_attach(blank,self.root))
        self.assertEqual(blank['adjudicated_claims'],self.verdict['adjudicated_claims'])
        self.assertIn('采用原始文件两行合计','\n'.join(display.markdown(blank)))

    def test_explicit_override_cannot_replace_canonical_decision(self):
        alternate=copy.deepcopy(self.verdict); alternate['verdicts'][0]['decision']='另一结论'
        write(self.root/'other.json',alternate)
        with self.assertRaisesRegex(ValueError,'override_conflicts'):
            display.auto_attach(self.report,self.root,self.root/'other.json')

    def test_missing_canonical_claims_stops_generation(self):
        del self.verdict['adjudicated_claims']; write(self.root/'verdict.json',self.verdict)
        with self.assertRaisesRegex(ValueError,'canonical_claims_missing'):
            display.auto_attach(self.report,self.root)

    def test_legacy_verdict_cannot_be_imported(self):
        self.verdict['schema_version']='1.0'
        write(self.root/'verdict.json',self.verdict)
        with self.assertRaisesRegex(ValueError,'analysis_identity_invalid'):
            display.auto_attach(self.report,self.root)

    def test_other_run_config_and_external_source_are_rejected(self):
        config=self.fx.config(); config['run_id']='another-run'; write(self.root/'quality-inputs.json',config)
        with self.assertRaisesRegex(ValueError,'quality_identity'):
            display.auto_attach(self.report,self.root)
        config['run_id']=self.report['run_id']; config['adjudication']='../another-client.json'
        write(self.root/'quality-inputs.json',config)
        with self.assertRaisesRegex(ValueError,'outside_or_missing'):
            display.auto_attach(self.report,self.root)

    def test_summary_omission_blocks_quality(self):
        del self.report['adjudication_summary']; write(self.root/'report.json',self.report)
        with self.assertRaisesRegex(ValueError,'display_stale_or_missing'):
            validate_quality(self.root,self.report)

    def test_markdown_omission_blocks_even_when_json_is_correct(self):
        (self.root/'report.md').write_text('合成测试 R001 交易.csv',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'markdown_missing_or_stale'):
            validate_quality(self.root,self.report)

    def test_hidden_or_code_only_decision_is_not_delivery(self):
        block='\n'.join(display.markdown(self.report))
        for wrapped in ('<!--\n'+block+'\n-->','<!--\n'+block,'```markdown\n'+block+'\n```',
                        '```markdown\n```not-a-closing-fence\n'+block+'\n```'):
            with self.subTest(wrapper=wrapped[:4]):
                (self.root/'report.md').write_text('合成测试 R001 交易.csv\n'+wrapped,encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'markdown_missing_or_stale'):
                    validate_quality(self.root,self.report)

    def test_stale_decision_cannot_survive_after_conflict_disappears(self):
        path=self.root/'ad-profit-optimizer.json'; handoff=quality_fixture.read(path)
        handoff['evidence_ledger'][0]['value']=100000; write(path,handoff)
        with self.assertRaisesRegex(ValueError,'without_current_conflict'):
            validate_quality(self.root,self.report)

    def test_canonical_claim_mismatch_is_not_silently_accepted(self):
        self.verdict['adjudicated_claims'][next(iter(self.report['adjudicated_claims']))]['value']=99999
        write(self.root/'verdict.json',self.verdict)
        with self.assertRaisesRegex(ValueError,'projection_changed'):
            validate_quality(self.root,self.report)


class BuilderDeliveryTests(unittest.TestCase):
    def test_default_cli_generates_decision_pdf_for_all_eight_report_types(self):
        import pymupdf as fitz
        with tempfile.TemporaryDirectory(prefix='omni-auto-delivery-') as temporary:
            for task_type in PROFILES:
                with self.subTest(task_type=task_type):
                    root=Path(temporary)/task_type
                    command=prepare_builder_sample(root,task_type)
                    self.assertNotIn('--decision-pack',command)
                    self.assertNotIn('--format',command)
                    result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',
                        env={**os.environ,'PYTHONIOENCODING':'utf-8','PYTHONDONTWRITEBYTECODE':'1'},timeout=120)
                    self.assertEqual(0,result.returncode,result.stdout+result.stderr)
                    package=json.loads((root/'report.json').read_text(encoding='utf-8'))
                    self.assertEqual(task_type,package['task_type'])
                    self.assertEqual('未采纳重复计算后的金额',package['adjudication_summary'][0]['not_adopted_disposition'])
                    markdown=(root/'report.md').read_text(encoding='utf-8')
                    self.assertIn('未采纳重复计算后的金额',markdown)
                    self.assertNotIn('已冻结的复核候选稿',markdown)
                    with fitz.open(root/'report.pdf') as doc:
                        text=''.join(page.get_text() for page in doc).replace(' ','').replace('\n','')
                    self.assertIn('未采纳重复计算后的金额',text)
                    self.assertIn('候选功能合成测试',text)
                    receipt=json.loads((root/'pdf-delivery.json').read_text(encoding='utf-8'))
                    self.assertEqual([],receipt['blank_pages'])
                    self.assertGreaterEqual(receipt['chart_count'],3)


if __name__=='__main__': unittest.main()
