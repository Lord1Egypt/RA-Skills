import copy
import unittest
from acceptance_report_view import enrich, markdown, defaults


class AcceptanceViewTests(unittest.TestCase):
    def package(self):
        return {'acceptance_only':True, 'title':'机制验收', 'team_version':'2.0.3-candidate.2',
            'team_version_label':'omni-ecom v2.0.3-candidate.2','report_revision':'R1','run_id':'test',
            'client_scope':'runtime-acceptance-no-client-data','period':'2026-W36','gate_status':'PASS',
            'status':'draft_diagnosis','acceptance_notice':'固定测试值，不是经营表现',
            'metrics':[{'metrics':{'conversion_rate':0.05}}], 'data_gate':{},
            'claim_ledger':{'claims':[{'claim_id':'C-conversion','metric':'conversion_rate','value':5,'unit':'%'}]},
            'chapter_plan':{'chapters':[{'chapter_id':'CH05','title':'验收缺口与限制','data_gaps':[]}]},
            'mechanism_findings':[{'agent_id':'data-analyst','gate_status':'PASS','facts':[],
                'missing_data':['缺原始退款明细',{'item':'投放归因表','impact':'无法复算 ROAS','required_source':'渠道消耗和归因导出'}]}]}

    def test_all_gaps_with_requirements_preserve_original(self):
        package = self.package()
        original = copy.deepcopy(package)
        enrich(package)
        self.assertEqual(len(package['missing_data']), 2)
        self.assertTrue(all(gap['impact'] and gap['required_source'] for gap in package['missing_data']))
        self.assertEqual(package['chapter_plan_source_snapshot'], original['chapter_plan'])
        self.assertEqual(package['mechanism_findings'], original['mechanism_findings'])
        self.assertEqual(package['chapter_plan']['chapters'][0]['data_gaps'], package['missing_data'])
        self.assertFalse(package['chapter_plan_enrichment']['initial_plan_file_modified'])

    def test_internal_ratio_not_rewritten_as_percentage(self):
        package = self.package()
        enrich(package)
        self.assertEqual(package['metrics'][0]['metrics']['conversion_rate'], 0.05)
        self.assertEqual(package['metrics'][0]['metric_units']['conversion_rate'], 'ratio')
        text = markdown(package)
        self.assertIn('| conversion_rate | 5 | % | C-conversion |', text)
        self.assertNotIn('0.05', text)
        for n, title in [('零','数据概览与覆盖'),('一','核心指标速览'),('二','关键图表'),('三','事实、判断与限制'),('四','优先行动'),('五','专家协作与版本凭证'),('六','数字来源与复算索引'),('七','验收缺口与限制')]:
            self.assertIn('## '+n+'、'+title, text)
        self.assertIn('缺原始退款明细', text)
        self.assertIn('渠道消耗和归因导出', text)

    def test_business_reports_not_relabelled_as_mechanism(self):
        package = self.package()
        package['acceptance_only'] = False
        before = copy.deepcopy(package)
        enrich(package)
        self.assertEqual(package, before)

    def test_host_and_phase_gaps_not_business_export_requests(self):
        host = defaults('未提供 WorkBuddy team-bootstrap，当前采用 Codex 原生路径')
        stage = defaults('阶段任务登记及全团实际完成状态不在岗位凭证中')
        self.assertEqual(host[0], 'host_mechanism')
        self.assertIn('不适用', host[2])
        self.assertNotIn('同客户', host[2])
        self.assertEqual(stage[0], 'phase_evidence')
        self.assertIn('当前完成凭证', stage[2])
        self.assertNotIn('原始导出', stage[2])


if __name__ == '__main__': unittest.main()
