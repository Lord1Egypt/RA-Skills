"""Carry scoped, explicitly supplied feedback; never infer action completion."""
import hashlib
import json
from pathlib import Path

LABELS = {'reported_done':'反馈已做（未独立验收）', 'in_progress':'反馈进行中',
          'not_done':'反馈未做', 'unknown':'状态未确认'}
FALLBACK = '未提供已确认的上期执行反馈，本稿不声称行动已执行。'

def load_feedback(value, run_id, client_scope, team_version, root=None):
    if not value:
        return None
    path = Path(value).resolve()
    relative=path.name
    if root is not None:
        root=Path(root).resolve()
        if not path.is_relative_to(root):
            raise ValueError('previous_action_review_outside_run')
        relative=path.relative_to(root).as_posix()
    body = path.read_bytes()
    payload = json.loads(body.decode('utf-8-sig'))
    if not isinstance(payload,dict) or any(payload.get(k)!=v for k,v in (
            ('run_id',run_id),('client_scope',client_scope),('team_version',team_version))):
        raise ValueError('previous_action_review_identity_mismatch')
    if not all(isinstance(payload.get(k),str) and payload[k].strip()
               for k in ('previous_period','provided_by')):
        raise ValueError('previous_action_review_source_missing')
    rows=payload.get('actions')
    if not isinstance(rows,list) or not rows:
        raise ValueError('previous_action_review_actions_missing')
    ids=set()
    for row in rows:
        if not isinstance(row,dict) or row.get('status') not in LABELS:
            raise ValueError('previous_action_review_status_invalid')
        if any(not isinstance(row.get(k),str) or not row[k].strip()
               for k in ('action_id','feedback')) or row['action_id'] in ids:
            raise ValueError('previous_action_review_action_invalid')
        ids.add(row['action_id'])
    if path.read_bytes()!=body:
        raise ValueError('previous_action_review_source_changed')
    return {'status':'provided_feedback_not_independently_accepted',
            'previous_period':payload['previous_period'], 'provided_by':payload['provided_by'],
            'actions':rows, 'source_file':relative,
            'source_sha256':hashlib.sha256(body).hexdigest()}

def validate_feedback(report, root):
    value=report.get('previous_action_review')
    if value is None:
        return []
    if not isinstance(value,dict):
        raise ValueError('previous_action_review_source_binding_required')
    name=value.get('source_file')
    if not isinstance(name,str) or Path(name).is_absolute() or '..' in Path(name).parts:
        raise ValueError('previous_action_review_source_path_invalid')
    expected=load_feedback(Path(root)/name,report['run_id'],report['client_scope'],report['team_version'],root)
    if expected!=value:
        raise ValueError('previous_action_review_source_or_projection_changed')
    return [{'file':name,'sha256':expected['source_sha256']}]

def feedback_lines(value):
    if not value:
        return [FALLBACK]
    # Read-only compatibility with earlier manually prepared report packages.
    if isinstance(value,str):
        return [value]
    if not isinstance(value,dict) or value.get('status')!='provided_feedback_not_independently_accepted':
        raise ValueError('previous_action_review_unqualified')
    result=[f"期间：{value['previous_period']}；反馈提供者：{value['provided_by']}；以下为提供者反馈，不等于独立验收通过。"]
    for row in value['actions']:
        result.append(f"{row['action_id']}：{LABELS[row['status']]}；{row['feedback']}")
    result.append(f"来源：{value['source_file']}；SHA256：{value['source_sha256']}")
    return result
