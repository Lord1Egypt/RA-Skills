"""Regression for unfinished workflow promises; anonymous local fixtures only."""
import copy
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from role_analysis_contract import questions,contract,check_questions
from report_presentation import view
from previous_action_review import load_feedback,feedback_lines,validate_feedback
from report_build_reuse import signature
from report_text_fields import gap_lines

class ClosureTests(unittest.TestCase):
    def test_mechanical_message_preserves_real_state_and_does_not_repeat_analysis(self):
        from return_communication import communication
        receipt={'run_id':'r','agent_id':'ad-profit-optimizer','return_status':'completed',
                 'response':{'gate_status':'BLOCKED'},'handoff_sha256':'a'*64,
                 'contribution_summary':'不要复制完整分析'*2000}
        with tempfile.TemporaryDirectory() as folder:
            card={'host':'workbuddy','paths':{'run_dir':folder}}
            before=copy.deepcopy(receipt)
            result=communication(card,receipt,Path(folder)/'agent-returns/profit/a1.return.json')
            self.assertEqual(receipt,before)
            params=result['native_message_parameters']
            self.assertEqual(params['recipient'],'team-lead');self.assertEqual(params['type'],'message')
            self.assertLess(len(params['content']),600)
            self.assertIn('BLOCKED',params['content']);self.assertIn('报告尚未放行',params['content'])
            self.assertNotIn('不要复制完整分析',params['content'])
            self.assertEqual(json.loads(params['content'])['handoff_sha256'],'a'*64)

    def test_codex_message_does_not_guess_workbuddy_recipient_or_approval(self):
        from return_communication import communication
        receipt={'run_id':'r','agent_id':'delivery-review','return_status':'completed',
                 'review_status':'conditional_pass','handoff_sha256':'b'*64}
        result=communication({'host':'codex'},receipt,Path('a1.return.json'))
        self.assertNotIn('native_message_parameters',result)
        self.assertIn('conditional_pass',result['short_message'])

    def test_mechanism_error_points_to_own_text_without_rewriting_or_bypassing(self):
        from finish_agent_handoff import mechanism_repair_context
        with tempfile.TemporaryDirectory() as folder:
            raw=Path(folder)/'raw.json'
            raw.write_text(json.dumps({'facts':[{'claim':'一份测试来源有 11 列，包括 GMV 字段。'}]},ensure_ascii=False),encoding='utf-8')
            before=raw.read_bytes()
            card={'client_scope':'runtime-acceptance-no-client-data','paths':{'expert_analysis':str(Path(folder)/'own.analysis.json')}}
            hint=mechanism_repair_context(card,'narrative_number_binding_mismatch:facts:0',raw)
            self.assertEqual(hint['field'],'facts[0].claim');self.assertIn('11',hint['rejected_text'])
            self.assertIn('不绕过检查',hint['repair_hint']);self.assertEqual(raw.read_bytes(),before)
            self.assertIn('未知花费/成本不能转移到证据表',hint['repair_hint'])
            card['client_scope']='business-client'
            self.assertEqual(mechanism_repair_context(card,'narrative_number_binding_mismatch:facts:0',raw),{})

    def feedback(self,path):
        body={'run_id':'r','client_scope':'c','team_version':'2.0.3',
              'previous_period':'previous-week','provided_by':'fixture-owner',
              'actions':[{'action_id':'A1','status':'reported_done','feedback':'已提交素材，但尚未核对后台结果。'}]}
        path.write_text(json.dumps(body,ensure_ascii=False),encoding='utf-8')
        return body

    def test_same_id_cannot_replace_hard_questions(self):
        for role in ('data-analyst','platform-ops','content-live-growth','ad-profit-optimizer'):
            for mode in ('business','mechanism'):
                rows=questions(role,mode)
                depth={'question_contract':contract(role,mode),'minimum_analysis_set':rows}
                check_questions(role,depth)
                rows[0]['question']='这次是不是成功了？'
                with self.assertRaisesRegex(ValueError,'question_text_changed'):check_questions(role,depth)

    def test_duplicate_or_missing_ids_do_not_hide_unassigned_findings(self):
        body={'facts':[{'id':'F1','claim':'a','chapter_ids':['C1']},
                       {'id':'F1','claim':'b'},{'claim':'c','chapter_ids':['C1']},{'claim':'d'}],
              'chapter_plan':{'chapters':[{'chapter_id':'C1'}]}}
        result=view(body)
        self.assertEqual([r['claim'] for r in result['unassigned_findings']],['b','d'])
        self.assertEqual(len({r['presentation_key'] for r in result['unassigned_findings']+result['chapters'][0]['items']}),4)

    def test_feedback_keeps_source_and_qualifies_done(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'feedback.json';self.feedback(path)
            result=load_feedback(path,'r','c','2.0.3')
            self.assertEqual(result['actions'][0]['status'],'reported_done')
            self.assertEqual(len(result['source_sha256']),64)
            self.assertIn('未独立验收',' '.join(feedback_lines(result)))
            self.assertIn('未提供',feedback_lines(None)[0])

    def test_feedback_rejects_cross_customer_and_unproved_acceptance(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'feedback.json';body=self.feedback(path)
            with self.assertRaisesRegex(ValueError,'identity_mismatch'):load_feedback(path,'r','other','2.0.3')
            body['actions'][0]['status']='verified_complete';path.write_text(json.dumps(body),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'status_invalid'):load_feedback(path,'r','c','2.0.3')

    def test_feedback_freeze_binding_rejects_edits_and_forged_projection(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);path=root/'feedback.json';body=self.feedback(path)
            result=load_feedback(path,'r','c','2.0.3',root)
            report={'run_id':'r','client_scope':'c','team_version':'2.0.3','previous_action_review':result}
            self.assertEqual(validate_feedback(report,root)[0]['sha256'],result['source_sha256'])
            forged=copy.deepcopy(report);forged['previous_action_review']['actions'][0]['feedback']='已独立验收'
            with self.assertRaisesRegex(ValueError,'source_or_projection_changed'):validate_feedback(forged,root)
            body['actions'][0]['status']='not_done';path.write_text(json.dumps(body),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'source_or_projection_changed'):validate_feedback(report,root)
            with self.assertRaisesRegex(ValueError,'outside_run'):load_feedback(path,'r','c','2.0.3',root/'other')

    def test_changed_feedback_invalidates_build_reuse(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'version-info.json').write_text('{}',encoding='utf-8')
            ledger=root/'claim-ledger.json';ledger.write_text('{"claims":[]}',encoding='utf-8')
            path=root/'feedback.json';body=self.feedback(path)
            args=Namespace(claim_ledger=str(ledger),previous_action_review=str(path),member_handoff=[])
            first=signature(args,root)
            body['actions'][0]['status']='not_done';path.write_text(json.dumps(body),encoding='utf-8')
            self.assertNotEqual(first,signature(args,root))

    def test_business_gaps_keep_authorization_and_unknown_future_fields(self):
        value={'item':'费用缺失','required_input':'仅在另行授权后提供','custom_condition':'不得覆盖原始退款期间'}
        result=' '.join(gap_lines(value))
        self.assertIn(value['required_input'],result);self.assertIn(value['custom_condition'],result)

    def test_pdf_keeps_long_conditions_duplicate_findings_and_feedback(self):
        from generate_pdf_report import build_story,build_doc
        import pymupdf
        long='仅允许在资料齐全并经指定负责人确认后进行核对。'*130
        body={'task_type':'weekly_report','team_version':'2.0.3','report_revision':'R1',
              'title':'匿名排版测试，非客户交付','metrics':[],
              'facts':[{'id':'F1','claim':'已完成字段检查'},{'id':'F1','claim':'另一条独立发现不能消失'}],
              'judgments':[{'claim':'当前不能批准扩大预算','counter_conditions':[long+'反证末尾保留']}],
              'hypotheses':[{'claim':'待验证关联','verification_method':long+'验证末尾保留'}],
              'actions':[{'action':'补齐资料','acceptance':long+'验收末尾保留','stop_condition':long+'停止末尾保留'}],
              'missing_data':[{'item':'缺口','required_input':long+'授权末尾保留'}],
              'risks':[long+'风险末尾保留']}
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'feedback.json';self.feedback(path)
            body['previous_action_review']=load_feedback(path,'r','c','2.0.3')
            output=Path(folder)/'probe.pdf'
            build_doc(str(output),title=body['title']).build(build_story(body,[]))
            with pymupdf.open(output) as doc:
                text=''.join(p.get_text() for p in doc).replace('\n','').replace(' ','')
                for suffix in ('反证','验证','验收','停止','授权','风险'):
                    self.assertIn(suffix+'末尾保留',text)
                self.assertIn('另一条独立发现不能消失',text)
                self.assertIn('反馈已做（未独立验收）',text)
                self.assertGreater(doc.page_count,1)

if __name__=='__main__':unittest.main()
