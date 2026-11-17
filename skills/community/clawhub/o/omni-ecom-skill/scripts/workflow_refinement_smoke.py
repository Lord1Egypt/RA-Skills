"""Behavioral regression for gaps, compact inputs, full display and reuse safety."""
import copy
import hashlib
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from analysis_depth_guard import check_handoff
from analysis_depth_smoke import GOOD_DEPTH,BODY
from role_analysis_contract import questions,contract
from task_input_projection import project
from assemble_expert_handoff import assemble
from finish_agent_handoff import verify_packet
from report_presentation import view,action_order
from report_build_reuse import existing,record,ARTIFACTS
from trace_usage import summarize_usage
from report_triage import classify
from pdf_layout_policy import page_limit

class RefinementTests(unittest.TestCase):
    def depth(self,folder):
        body=copy.deepcopy(BODY);body['agent_id']='ad-profit-optimizer'
        body['gate_status']='BLOCKED';body['judgments']=[]
        body['facts']=[{'id':'F1','claim':'已核对文件字段清单，未提供推广费用列。','evidence_ids':['E1']}]
        body['evidence_ledger']=[{'id':'E1','source':'source.csv/headers','metric':'费用列是否存在','period':'test','value':'未提供','status':'blocked'}]
        depth=copy.deepcopy(GOOD_DEPTH)
        depth['depth_ladder'].update(reached_level='L1',blocked_below='当前没有广告费和完整成本资料，仅交缺口核查与补数要求。')
        depth['question_contract']=contract('ad-profit-optimizer')
        rows=questions('ad-profit-optimizer')
        for row in rows:row.update(status='unanswerable',blocker='原表字段和授权来源清单没有广告费及成本，不能计算利润或预算。',evidence_ids=['E1'])
        depth['minimum_analysis_set']=rows
        body['analysis_depth']=depth
        path=folder/'raw.json';path.write_text(json.dumps(body,ensure_ascii=False),encoding='utf-8')
        return path,body

    def test_honest_six_gaps_complete_check_but_do_not_approve_profit(self):
        with tempfile.TemporaryDirectory() as f:
            path,body=self.depth(Path(f))
            result=check_handoff('ad-profit-optimizer',path,body,'','L2')
            self.assertEqual(result['status'],'passed',result)
            self.assertEqual(result['gate_status'],'BLOCKED')
            self.assertEqual(body['judgments'],[])
            self.assertEqual(body['evidence_ledger'][0]['value'],'未提供')

    def test_empty_questions_and_duplicated_ids_are_blocked(self):
        with tempfile.TemporaryDirectory() as f:
            path,body=self.depth(Path(f));body['analysis_depth']['minimum_analysis_set']=[]
            result=check_handoff('ad-profit-optimizer',path,body,'','L2')
            self.assertIn('minimum_analysis_set_missing',result['errors'])
            path,body=self.depth(Path(f))
            body['analysis_depth']['minimum_analysis_set'][1]['question_id']=body['analysis_depth']['minimum_analysis_set'][0]['question_id']
            self.assertIn('minimum_analysis_question_identity_invalid',check_handoff('ad-profit-optimizer',path,body,'','L2')['errors'])

    def test_gap_without_known_evidence_cannot_pass(self):
        with tempfile.TemporaryDirectory() as f:
            path,body=self.depth(Path(f));body['analysis_depth']['minimum_analysis_set'][0]['evidence_ids']=['E999']
            self.assertIn('minimum_analysis_evidence_unknown',check_handoff('ad-profit-optimizer',path,body,'','L2')['errors'])

    def test_business_cannot_use_mechanism_questions(self):
        with tempfile.TemporaryDirectory() as f:
            path,body=self.depth(Path(f));body['analysis_depth']['question_contract']=contract('ad-profit-optimizer','mechanism')
            self.assertIn('mechanism_questions_for_business_forbidden',check_handoff('ad-profit-optimizer',path,body,'','L2')['errors'])

    def test_compact_inventory_retains_all_ids_paths_and_reasons(self):
        reports=[{'report_id':'R'+str(i),'file_path':'inputs/'+str(i)+'.csv','verdict_reason':'缺字段需补数',
                  'columns':['unused-'+str(k) for k in range(200)],'rows':['x'*1000]*5} for i in range(50)]
        source={'reports':reports,'report_count':50,'run_id':'r','client_scope':'c','team_version':'2.0.3'}
        output=project('inventory',source,'data-analyst')
        self.assertEqual(len(output['reports']),50)
        self.assertTrue(all(r['file_path'] and r['verdict_reason'] for r in output['reports']))
        self.assertLess(len(json.dumps(output)),len(json.dumps(source))*.2)
        self.assertNotIn('complete_index',output)
        self.assertNotIn('full_detail_in_original',output)

    def test_archived_revision_cannot_continue_writing_but_can_be_read(self):
        from host_runtime import Runtime
        with tempfile.TemporaryDirectory() as f:
            folder=Path(f);runtime=Runtime(folder,'r','c');runtime.init('2.0.3','weekly_report');runtime.close()
            (folder/'report-revision-successor.json').write_text('{"report_revision":"R2"}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'runtime_predecessor_archived_use_successor'):Runtime(folder,'r','c')
            runtime=Runtime(folder,'r','c',read_only=True)
            try:self.assertEqual(runtime.identity()['team_version'],'2.0.3')
            finally:runtime.close()

    def test_projection_tamper_and_source_mutation_are_rejected(self):
        with tempfile.TemporaryDirectory() as f:
            path=Path(f)/'source.json';content={'reports':[{'report_id':'R1','file_path':'source.csv'}]}
            path.write_text(json.dumps(content),encoding='utf-8')
            item={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'projection':{'version':'1','kind':'inventory','role':'data-analyst'},'content':project('inventory',content,'data-analyst')}
            card={'agent_id':'data-analyst','read_packet':{'inventory':item}}
            verify_packet(card);item['content']['reports'][0]['file_path']='other.csv'
            with self.assertRaisesRegex(ValueError,'content_changed'):verify_packet(card)
            path.write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'source_changed'):verify_packet(card)

    def test_mechanical_assembly_preserves_expert_answer_and_rejects_identity_injection(self):
        with tempfile.TemporaryDirectory() as f:
            _,body=self.depth(Path(f));template=copy.deepcopy(body)
            card={'agent_id':'ad-profit-optimizer','analysis_question_contract':contract('ad-profit-optimizer'),'raw_handoff_template':template}
            fields={'gate_status','status','contribution_summary','facts','judgments','hypotheses','actions','risks','missing_data','evidence_ledger','analysis_depth'}
            analysis={k:copy.deepcopy(body.get(k,[])) for k in fields}
            analysis['status']='data_blocked'
            analysis['analysis_depth']={k:v for k,v in analysis['analysis_depth'].items() if k in {'baseline_ack','depth_ladder','decomposition','minimum_analysis_set','self_check'}}
            result=assemble(card,analysis)
            self.assertEqual(result['facts'],body['facts']);self.assertEqual(result['legacy_compatibility'],body['legacy_compatibility'])
            analysis['client_scope']='other'
            with self.assertRaisesRegex(ValueError,'fields_invalid'):assemble(card,analysis)

    def test_full_presentation_retains_findings_actions_and_distinct_report_focus(self):
        p={'task_type':'weekly_report','facts':[{'id':'F'+str(i),'claim':'事实'+str(i)} for i in range(30)],
            'actions':[{'action_id':'A'+str(i),'priority':'P2'} for i in range(15)]}
        w=view(p);self.assertEqual(len(w['unassigned_findings']),30);self.assertEqual(len(w['action_ids']),15)
        p['task_type']='annual_report';self.assertNotEqual(w['focus'],view(p)['focus'])
        self.assertEqual(action_order([{'action_id':'low','priority':'P2'},{'action_id':'high','priority':'P0'}])[0]['action_id'],'high')

    def test_missing_data_projection_preserves_authorization_and_specific_requests(self):
        from acceptance_report_view import enrich
        raw={'item':'客户经营资料','required_input':'另行授权后提供费用，本次不请求业务报表',
             'required_data':'保留原退款期间和归因窗口'}
        package={'acceptance_only':True,'mechanism_findings':[{'agent_id':'ad-profit-optimizer','missing_data':[raw]}],
                 'data_gate':{},'chapter_plan':{'chapters':[{'chapter_id':'CH05'}]}}
        enrich(package)
        gap=package['missing_data'][0]
        self.assertIn(raw['required_input'],gap['required_source'])
        self.assertIn(raw['required_data'],gap['required_source'])
        self.assertEqual(gap['raw_missing_data'],raw)
        self.assertEqual(package['chapter_plan']['chapters'][0]['data_gaps'][0],gap)

    def test_host_evidence_gap_is_not_routed_to_customer_reports(self):
        from acceptance_report_view import enrich
        package={'acceptance_only':True,'mechanism_findings':[{'agent_id':'platform-ops','missing_data':[
            {'missing_fields':['账本中的真实角色启动、完成、消息和封存事件'],
             'required_data':'由团长依据宿主真实回包补齐运行事件与任务绑定'}]}], 'data_gate':{}}
        enrich(package)
        gap=package['missing_data'][0]
        self.assertEqual(gap['gap_kind'],'host_mechanism')
        self.assertIn('由团长',gap['required_source'])
        self.assertNotIn('请提供',gap['required_source'])

    def test_string_gap_keeps_future_authorization_without_new_request(self):
        from acceptance_report_view import enrich
        raw='无客户业务资料。补数要求：仅在另行授权真实客户任务时提供原表，本轮无需补造。'
        p={'acceptance_only':True,'mechanism_findings':[{'agent_id':'platform-ops','missing_data':[raw]}],'data_gate':{}}
        enrich(p)
        self.assertEqual(p['missing_data'][0]['required_source'],'仅在另行授权真实客户任务时提供原表，本轮无需补造。')

    def test_live_funnel_is_not_trade_but_filename_alone_is_not_enough(self):
        self.assertEqual(classify('内容直播.csv',['场次','观看人数','支付买家数','支付金额'])[0],'livestream')
        self.assertNotEqual(classify('直播销售.csv',['支付金额','支付买家数'])[0],'livestream')

    def test_usage_deduplicates_and_does_not_guess_fees_or_missing_cache(self):
        row={'providerData':{'messageId':'one','rawUsage':{'prompt_tokens':100,'completion_tokens':8,'prompt_cache_hit_tokens':90,'prompt_cache_miss_tokens':10}}}
        result=summarize_usage([row,row]);self.assertEqual(result['input_tokens'],100);self.assertEqual(result['usage_records'],1);self.assertIsNone(result['cost'])
        row['providerData']['rawUsage'].pop('prompt_cache_hit_tokens')
        self.assertIsNone(summarize_usage([row])['cache_hit_tokens'])
        self.assertEqual(summarize_usage([])['status'],'not_reported')

    def test_dynamic_page_policy_retains_rich_content_and_is_bounded(self):
        self.assertEqual(page_limit({}),17)
        self.assertGreater(page_limit({'facts':[{}]*72,'judgments':[{}]*72,'hypotheses':[{}]*72,'actions':[{}]*12}),21)
        self.assertEqual(page_limit({'facts':[{}]*10000}),120)

    def test_unchanged_build_reused_but_source_mutation_invalidates(self):
        with tempfile.TemporaryDirectory() as f:
            folder=Path(f);root=folder/'plugin';root.mkdir();out=folder/'run';out.mkdir()
            (root/'version-info.json').write_text('{"team_version":"synthetic"}',encoding='utf-8')
            source=out/'source.csv';source.write_text('amount\n10\n',encoding='utf-8')
            ledger=out/'claim-ledger.json';ledger.write_text(json.dumps({'claims':[{'source_ref':{'source_file':'source.csv'}}]}),encoding='utf-8')
            args=Namespace(claim_ledger=str(ledger),output_dir=str(out),format='all',member_handoff=[],report_revision='R1')
            key,prior=existing(args,root);self.assertIsNone(prior)
            for name in ARTIFACTS:(out/name).write_text('synthetic cache-byte fixture, not a report',encoding='utf-8')
            record(out,key)
            self.assertIsNotNone(existing(args,root)[1])
            source.write_text('amount\n20\n',encoding='utf-8')
            self.assertIsNone(existing(args,root)[1])

    def test_frozen_build_is_not_overwritten_when_artifact_changes(self):
        with tempfile.TemporaryDirectory() as f:
            folder=Path(f);root=folder/'plugin';root.mkdir();out=folder/'run';out.mkdir()
            (root/'version-info.json').write_text('{"team_version":"synthetic"}',encoding='utf-8')
            ledger=out/'claim-ledger.json';ledger.write_text('{"claims":[]}',encoding='utf-8')
            args=Namespace(claim_ledger=str(ledger),output_dir=str(out),format='all',member_handoff=[],report_revision='R1')
            key,_=existing(args,root)
            for name in ARTIFACTS:(out/name).write_text('synthetic only',encoding='utf-8')
            record(out,key);(out/'review-manifest.json').write_text('synthetic freeze sentinel',encoding='utf-8')
            self.assertIsNotNone(existing(args,root)[1])
            (out/'report.md').write_text('changed',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'frozen_report_requires_new_revision'):existing(args,root)

    def test_unclaimed_authorized_source_changes_invalidate_build(self):
        with tempfile.TemporaryDirectory() as f:
            folder=Path(f);root=folder/'plugin';root.mkdir();out=folder/'run';out.mkdir()
            (root/'version-info.json').write_text('{"team_version":"synthetic"}',encoding='utf-8')
            ledger=out/'claim-ledger.json';ledger.write_text('{"claims":[]}',encoding='utf-8')
            (out/'extra.csv').write_text('original',encoding='utf-8')
            (out/'run-scope.json').write_text('{"files":[{"file":"extra.csv"}]}',encoding='utf-8')
            args=Namespace(claim_ledger=str(ledger),output_dir=str(out),format='all',member_handoff=[],report_revision='R1')
            key,_=existing(args,root)
            for name in ARTIFACTS:(out/name).write_text('synthetic only',encoding='utf-8')
            record(out,key);(out/'extra.csv').write_text('changed',encoding='utf-8')
            self.assertIsNone(existing(args,root)[1])

if __name__=='__main__':unittest.main()
