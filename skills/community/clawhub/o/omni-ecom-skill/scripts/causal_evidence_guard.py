"""Review causal judgments in expert handoffs; correlation is not causation."""
from __future__ import annotations

import re

from adjudication_guard import require
from artifact_contract import native_analysis_identity


CAUSAL_WORDS=re.compile(r'原因|导致|归因|主要来自|因为|驱动')
TENTATIVE_WORDS=re.compile(r'可能|初步|相关|待验证|假设|尚不能确认')
STRENGTHS={'hypothesis','observational_association','quasi_experimental','experimental'}
STATUSES={'hypothesis_only','association_supported','causal_supported'}


def _strings(value,reason):
    require(isinstance(value,list) and bool(value) and
            all(isinstance(item,str) and item.strip() for item in value),reason)
    return value


def review_handoffs(handoffs,run_id,client_scope,team_version,reviewed_at=None):
    reviews=[]
    for agent_id,handoff in handoffs.items():
        evidence={item.get('id'):item for item in handoff.get('evidence_ledger',[])
                  if isinstance(item,dict) and isinstance(item.get('id'),str)}
        for judgment in handoff.get('judgments',[]):
            if not isinstance(judgment,dict): continue
            text=str(judgment.get('claim') or '')
            analysis=judgment.get('causal_analysis')
            if not CAUSAL_WORDS.search(text) and analysis is None: continue
            require(isinstance(analysis,dict),'causal_analysis_required:'+agent_id)
            for key in ('outcome_metric','cause_variable','period','mechanism','falsification_test','identification_method'):
                require(isinstance(analysis.get(key),str) and analysis[key].strip(),
                        'causal_field_missing:'+key)
            require(analysis.get('claim_strength') in STRENGTHS,'causal_strength_invalid')
            require(analysis.get('inference_status') in STATUSES,'causal_inference_status_invalid')
            require(isinstance(analysis.get('primary_cause'),bool),'causal_primary_flag_missing')
            require(analysis.get('temporal_order') in ('verified','not_verified'),
                    'causal_temporal_order_invalid')
            alternatives=_strings(analysis.get('alternative_explanations'),'causal_alternatives_required')
            confounders=_strings(analysis.get('confounders'),'causal_confounders_required')
            ids=_strings(analysis.get('evidence_ids'),'causal_evidence_ids_required')
            require(set(ids)==set(judgment.get('evidence_ids',[])) and all(key in evidence for key in ids),
                    'causal_evidence_binding_mismatch')
            require(all(evidence[key].get('status')=='verified' for key in ids),
                    'causal_evidence_not_verified')
            strength=analysis['claim_strength']; status=analysis['inference_status']
            if strength in ('hypothesis','observational_association'):
                require(status!='causal_supported','causal_observational_overclaim')
                require(not CAUSAL_WORDS.search(text) or TENTATIVE_WORDS.search(text),
                        'causal_language_overstated')
            if status=='causal_supported':
                require(strength in ('quasi_experimental','experimental') and
                        analysis['temporal_order']=='verified','causal_identification_insufficient')
                design_ids=_strings(analysis.get('design_evidence_ids'),'causal_design_evidence_required')
                require(all(key in evidence and evidence[key].get('status')=='verified' for key in design_ids),
                        'causal_design_evidence_invalid')
                require(isinstance(analysis.get('control_group'),str) and analysis['control_group'].strip() and
                        isinstance(analysis.get('treatment_timing'),str) and analysis['treatment_timing'].strip() and
                        analysis.get('pretrend_status')=='passed','causal_design_controls_incomplete')
            reviews.append(dict(agent_id=agent_id,judgment_id=judgment.get('id'),claim=text,
                outcome_metric=analysis['outcome_metric'],cause_variable=analysis['cause_variable'],
                period=analysis['period'],primary_cause=analysis['primary_cause'],
                claim_strength=strength,inference_status=status,evidence_ids=ids,
                alternative_explanations=alternatives,confounders=confounders,
                conclusion_boundary=('causal_supported' if status=='causal_supported' else
                    'association_or_hypothesis_not_causally_proven')))
    result = {**native_analysis_identity('causal_review',team_version),
              'run_id':run_id,'client_scope':client_scope,'team_version':team_version,
              'status':'causal_review_passed','reviews':reviews}
    if reviewed_at is not None:
        result['reviewed_at'] = reviewed_at
    return result


def causal_conflicts(review):
    buckets={}
    for row in review.get('reviews',[]):
        if row.get('primary_cause'):
            buckets.setdefault((row['outcome_metric'],row['period']),[]).append(row)
    conflicts=[]
    for (metric,period),rows in buckets.items():
        if len({row['agent_id'] for row in rows})<2 or len({row['cause_variable'] for row in rows})<2:
            continue
        index=len(conflicts)+1
        hard=any(row['inference_status']=='causal_supported' for row in rows)
        conflicts.append({'conflict_id':f'X-ATTR-{index:03d}','type':'attribution',
            'metric':metric,'period':period,'severity':'hard' if hard else 'soft',
            'topic':f'{metric} 的首要原因存在互斥主张',
            'positions':[{'agent_id':row['agent_id'],
                'position':f"{row['cause_variable']}（{row['conclusion_boundary']}）",
                'evidence_ids':row['evidence_ids']} for row in rows],
            'needs_challenge_round':hard,'lead_recomputation_required':True})
    return conflicts
