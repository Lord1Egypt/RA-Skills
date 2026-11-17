"""Presentation tests; synthetic numbers and roles are explicitly not host proof."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import decision_display as display
from artifact_contract import native_analysis_identity


class DisplayTests(unittest.TestCase):
    def setUp(self):
        self.package=dict(run_id='synthetic-display',client_scope='synthetic',team_version='2.0.3',report_revision='R1')
        self.payload=dict(**native_analysis_identity('conflict_verdict',self.package['team_version']),
            **self.package,adjudicated_claims={'X-DIR-001':dict(metric='转化率',unit='%',value=20,
            period='2026-07',previous_period='2026-06',previous_value=10,direction='up',absolute_change=10,
            current_days=31,previous_days=30,comparability_note='自然月天数不同，不能据此断言原因')},
            verdicts=[dict(conflict_id='X-DIR-001',decision='采用同期间支付买家与去重访客',
                not_adopted_disposition='未采用销售额除以访客',residual_risk='合成测试，不是真实经营结论',
                inputs={'private_path':'E:/private/internal.json'},challenge_review=[dict(role='data-analyst',
                disposition='adopted',reason='原始数据重算一致',return_event_hash='a'*64)])])

    def test_public_projection_does_not_copy_raw_input_paths(self):
        display.attach(self.package,self.payload)
        self.assertNotIn('private_path',json.dumps(self.package))
        self.assertNotIn('inputs',self.package['adjudication_summary'][0])
        self.assertEqual(self.package['decision_presentation_status'],'candidate_requires_quality_and_review')

    def test_cross_client_cannot_import_decisions(self):
        self.payload['client_scope']='other'
        with self.assertRaisesRegex(ValueError,'identity_mismatch'): display.attach(self.package,self.payload)

    def test_unknown_conflict_claim_cannot_be_imported(self):
        self.payload['adjudicated_claims']['unknown']={}
        with self.assertRaisesRegex(ValueError,'conflict_mismatch'): display.attach(self.package,self.payload)

    def test_markdown_shows_disposition_limits_and_percentage_points(self):
        display.attach(self.package,self.payload)
        value='\n'.join(display.markdown(self.package))
        for expected in ('百分点','未采用销售额除以访客','自然月天数不同','原始数据重算一致','候选裁决'):
            self.assertIn(expected,value)

    def test_markup_in_claims_is_not_active_html(self):
        self.payload['verdicts'][0]['decision']='<script>bad</script> **假标题**'
        display.attach(self.package,self.payload)
        value='\n'.join(display.markdown(self.package))
        self.assertNotIn('<script>',value); self.assertIn('&lt;script&gt;',value)

    def test_display_does_not_mutate_source(self):
        before=copy.deepcopy(self.payload); display.attach(self.package,self.payload)
        display.sections(self.package)
        self.assertEqual(self.payload,before)

    def test_display_cannot_misrepresent_the_checked_verdict(self):
        import quality_gate_smoke as fixtures
        from quality_gate import validate_quality
        fx=fixtures.QualityTests(); fx.setUp()
        try:
            verdict=fx.verdict_fixture()
            display.attach(fx.report,dict(verdict,adjudicated_claims=fx.report['adjudicated_claims']))
            fx.report['adjudication_summary'][0]['decision']='改写总监结论'
            fixtures.write(fx.root/'report.json',fx.report)
            with self.assertRaisesRegex(ValueError,'decision_display_stale'): validate_quality(fx.root,fx.report)
        finally: fx.tearDown()

    def test_actual_pdf_contains_complete_decision_text(self):
        import generate_pdf_report as pdf
        import pymupdf as fitz
        display.attach(self.package,self.payload)
        self.package.update(title='合成裁决展示测试',gate_status='WARN',period='2026-07',status='draft',
            expert_participation=[dict(agent_id='data-analyst',display_name='合成数据岗位',profession='数据核对',
            participation_status='synthetic_fixture',agent_task_ids=['agent-synthetic'],contribution_summary='仅合成展示测试')])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'report.json'
            from pdf_source_smoke import attach_synthetic_sources
            attach_synthetic_sources(root,self.package)
            source.write_text(json.dumps(self.package,ensure_ascii=False),encoding='utf-8')
            result=pdf.generate(source,root/'report.pdf',root/'pdf-delivery.json',root/'pages')
            with fitz.open(root/'report.pdf') as doc:
                text=''.join(page.get_text() for page in doc).replace(' ','').replace('\n','')
            self.assertIn('未采用销售额除以访客',text)
            self.assertIn('百分点',text)
            self.assertIn('原始数据重算一致',text)
            self.assertEqual(result['blank_pages'],[])
            self.assertGreaterEqual(result['chart_count'],3)

    def test_no_actions_cannot_be_plotted_as_one_invented_action(self):
        import generate_pdf_report as pdf
        from matplotlib.axes import Axes
        from unittest.mock import patch
        values=[]; original=Axes.bar
        def capture(self,x,height,*args,**kwargs):
            values.extend(height); return original(self,x,height,*args,**kwargs)
        with tempfile.TemporaryDirectory() as tmp, patch.object(Axes,'bar',capture):
            pdf.chart_actions({'actions':[],'missing_data':['costs','visits']},Path(tmp)/'actions.png')
        self.assertEqual(values,[0])


if __name__=='__main__': unittest.main()
