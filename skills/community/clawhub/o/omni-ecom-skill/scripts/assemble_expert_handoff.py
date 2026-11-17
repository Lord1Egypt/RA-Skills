"""Assemble only mechanical fields around the expert's own analysis."""
import copy
import json
from pathlib import Path
from role_analysis_contract import contract, check_questions

FIELDS = {'gate_status','status','contribution_summary','facts','judgments','hypotheses',
          'actions','risks','missing_data','evidence_ledger','analysis_depth'}
DEPTH_FIELDS = {'baseline_ack','depth_ladder','decomposition','minimum_analysis_set','self_check'}

def assemble(card, analysis):
    if not isinstance(analysis,dict) or set(analysis)-FIELDS:
        raise ValueError('expert_analysis_fields_invalid')
    if not FIELDS.issubset(analysis):
        raise ValueError('expert_analysis_fields_missing')
    depth=analysis['analysis_depth']
    if not isinstance(depth,dict) or set(depth)-DEPTH_FIELDS or not DEPTH_FIELDS.issubset(depth):
        raise ValueError('expert_analysis_depth_fields_invalid')
    raw=copy.deepcopy(card['raw_handoff_template'])
    for key in FIELDS-{'analysis_depth'}:
        raw[key]=copy.deepcopy(analysis[key])
    raw['analysis_depth'].update(copy.deepcopy(depth))
    raw['analysis_depth']['question_contract']=copy.deepcopy(card['analysis_question_contract'])
    check_questions(card['agent_id'],raw['analysis_depth'])
    # Schema identities, client/run/scope and actual task binding never come from
    # the model's business fields. No answer or review decision is synthesized.
    return raw

def assemble_file(card):
    analysis_path=Path(card['paths']['expert_analysis'])
    if not analysis_path.is_file():
        return False
    if Path(card['paths']['return_file']).exists():
        raise ValueError('member_return_already_committed')
    raw=assemble(card,json.loads(analysis_path.read_text(encoding='utf-8-sig')))
    path=Path(card['paths']['raw_handoff'])
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return True

