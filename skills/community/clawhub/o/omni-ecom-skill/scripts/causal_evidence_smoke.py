"""Tests for evidence-bounded causal judgments and structured conflicts."""
import unittest

from causal_evidence_guard import review_handoffs, causal_conflicts


class CausalTests(unittest.TestCase):
    def setUp(self):
        self.version='2.0.3-candidate.1'; self.run='run-causal'; self.client='synthetic'
        self.evidence=[{'id':'E1','status':'verified'},{'id':'E2','status':'verified'}]
        self.base={'evidence_ledger':self.evidence,'judgments':[]}

    def analysis(self,**extra):
        value=dict(outcome_metric='转化率',cause_variable='流量质量',period='2026-07',primary_cause=True,
            claim_strength='observational_association',inference_status='association_supported',
            temporal_order='not_verified',mechanism='低意向流量降低支付概率',
            alternative_explanations=['页面承接变化'],confounders=['活动结构变化'],
            falsification_test='同商品同页面分渠道复核',identification_method='分渠道同期观察',evidence_ids=['E1'])
        value.update(extra); return value

    def review(self,handoffs):
        return review_handoffs(handoffs,self.run,self.client,self.version)

    def test_no_causal_claim_is_clean_native_review(self):
        result=self.review({'data-analyst':self.base})
        self.assertEqual(result['contract_name'],'omni-ecom.causal-evidence-review')
        self.assertEqual(result['reviews'],[])

    def test_assertive_causal_language_requires_analysis(self):
        handoff={**self.base,'judgments':[{'id':'J1','claim':'流量质量导致转化下降','evidence_ids':['E1']}]}
        with self.assertRaisesRegex(ValueError,'causal_analysis_required'): self.review({'data-analyst':handoff})

    def test_observation_must_use_tentative_language(self):
        handoff={**self.base,'judgments':[{'id':'J1','claim':'流量质量导致转化下降','evidence_ids':['E1'],
            'causal_analysis':self.analysis()}]}
        with self.assertRaisesRegex(ValueError,'causal_language_overstated'): self.review({'data-analyst':handoff})

    def test_observational_hypothesis_keeps_noncausal_boundary(self):
        handoff={**self.base,'judgments':[{'id':'J1','claim':'转化下降可能主要来自流量质量，待验证',
            'evidence_ids':['E1'],'causal_analysis':self.analysis()}]}
        result=self.review({'data-analyst':handoff})
        self.assertEqual(result['reviews'][0]['conclusion_boundary'],'association_or_hypothesis_not_causally_proven')

    def test_causal_supported_requires_control_design(self):
        analysis=self.analysis(claim_strength='experimental',inference_status='causal_supported',temporal_order='verified')
        handoff={**self.base,'judgments':[{'id':'J1','claim':'实验显示流量质量导致转化下降','evidence_ids':['E1'],
            'causal_analysis':analysis}]}
        with self.assertRaisesRegex(ValueError,'causal_design_evidence_required'): self.review({'data-analyst':handoff})

    def test_competing_supported_primary_causes_are_hard_conflict(self):
        def row(agent,cause):
            analysis=self.analysis(cause_variable=cause,claim_strength='quasi_experimental',
                inference_status='causal_supported',temporal_order='verified',design_evidence_ids=['E2'],
                control_group='未调整渠道',treatment_timing='2026-07-10',pretrend_status='passed')
            return {**self.base,'judgments':[{'id':'J-'+agent,'claim':cause+'导致转化变化',
                'evidence_ids':['E1'],'causal_analysis':analysis}]}
        review=self.review({'data-analyst':row('a','流量质量'),'platform-ops':row('b','页面承接')})
        conflicts=causal_conflicts(review)
        self.assertEqual(conflicts[0]['severity'],'hard')
        self.assertTrue(conflicts[0]['needs_challenge_round'])


if __name__=='__main__': unittest.main()
