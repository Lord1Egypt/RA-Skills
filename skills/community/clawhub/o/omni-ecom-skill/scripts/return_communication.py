"""Mechanical short communication from an already validated/committed receipt."""
import json
from pathlib import Path

def communication(card, receipt, return_path):
    # Never copy the long contribution or findings into chat. They stay in the
    # original independently authored handoff/review and the immutable receipt.
    path=Path(return_path).resolve()
    folder=card.get('paths',{}).get('run_dir') or str(Path(card.get('manifest',str(path))).parent)
    root=Path(folder).resolve()
    reference=path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)
    response=receipt.get('response',{})
    state=receipt.get('review_status') or response.get('gate_status') or receipt.get('return_status')
    content=json.dumps({'run_id':receipt['run_id'],'agent_id':receipt['agent_id'],
        'return_status':receipt['return_status'],'gate_or_review_status':state,
        'return_file':reference,'handoff_sha256':receipt['handoff_sha256'],
        'note':'仅本岗回执已生成，报告尚未放行；完整分析、缺口、风险及必改项见原件。'},ensure_ascii=False,separators=(',',':'))
    result={'short_message':content}
    if card.get('host')=='workbuddy':
        result['native_message_parameters']={'type':'message','recipient':'team-lead',
            'summary':receipt['agent_id']+' 回传：'+str(state),'content':content}
    return result
