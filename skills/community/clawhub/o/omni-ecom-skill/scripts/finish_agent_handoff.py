"""One member-owned call for unchanged inputs, handoff/depth checks and return."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def verify_packet(card):
    for item in card.get('read_packet', {}).values():
        path = Path(item['path'])
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('task_packet_source_changed')
        actual=json.loads(data.decode('utf-8-sig'))
        if item.get('projection'):
            from task_input_projection import project
            spec=item['projection']
            if spec.get('version')!='1' or spec.get('role')!=card['agent_id']:
                raise ValueError('task_packet_projection_invalid')
            actual=project(spec['kind'],actual,card['agent_id'])
        if actual != item['content']:
            raise ValueError('task_packet_content_changed')


def verify_mechanism_facts(card, raw):
    if card.get('client_scope') != 'runtime-acceptance-no-client-data':
        return
    from mechanism_fact_guard import validate
    run = Path(card['paths']['run_dir'])
    handoff = json.loads(raw.read_text(encoding='utf-8-sig'))
    inventory = json.loads(Path(card['paths']['report_inventory']).read_text(encoding='utf-8-sig'))
    ledger = json.loads((run / 'claim-ledger.json').read_text(encoding='utf-8-sig'))
    validate(handoff.get('facts', []), {'client_scope':card['client_scope'],
                                      'report_inventory':inventory, 'claim_ledger':ledger})


def mechanism_repair_context(card, error, raw):
    """Locate the actual rejected text; never repair or approve it automatically."""
    import re
    match=re.fullmatch(r'narrative_number_binding_mismatch:facts:(\d+)',str(error))
    if card.get('client_scope')!='runtime-acceptance-no-client-data' or not match:
        return {}
    facts=json.loads(Path(raw).read_text(encoding='utf-8-sig')).get('facts',[])
    index=int(match.group(1))
    if index>=len(facts):return {}
    return {'field':'facts['+str(index)+'].claim','rejected_text':str(facts[index].get('claim') or '')[:500],
        'edit_only':card.get('paths',{}).get('expert_analysis') or str(raw),
        'repair_hint':'这条机制事实包含未绑定数字，先核查其真实来源。无来源数字不得保留，未知花费/成本不能转移到证据表冒充已核实；只有本人核实的结构条数/列数可留在 evidence_ledger，facts 用证据编号说明机制状态，不重复经营数值。只改本人未封存分析并重跑同一 finish_command；不猜费用、不更改问题、不删除实际风险、不读无关程序、不绕过检查。'}


def main():
    # A committed return must not look failed merely because a Windows console
    # cannot encode the expert's Chinese contribution summary.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-card', required=True)
    args = parser.parse_args()
    path = Path(args.task_card).resolve()
    card = json.loads(path.read_text(encoding='utf-8-sig'))
    verify_packet(card)
    if card.get('paths',{}).get('expert_analysis'):
        from assemble_expert_handoff import assemble_file
        assemble_file(card)
    root = Path(__file__).resolve().parents[1]
    paths = card['paths']
    raw = Path(paths['raw_handoff'])
    if card.get('analysis_question_contract'):
        from role_analysis_contract import check_questions
        depth=json.loads(raw.read_text(encoding='utf-8-sig'))['analysis_depth']
        if depth.get('question_contract')!=card['analysis_question_contract']:
            raise ValueError('minimum_analysis_contract_mismatch')
        check_questions(card['agent_id'],depth)
    child_env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    commands = [
        [sys.executable, '-B', str(root/'skills/ecom-diagnosis-core/scripts/validate_handoff.py'), str(raw)],
        [sys.executable, '-B', str(root/'scripts/analysis_depth_guard.py'), '--handoff', card['agent_id']+'='+str(raw), '--baseline', paths['baseline'], '--min-level', card['required_result']['minimum_depth'], '--output', str(raw.parent/(card['agent_id']+'-'+card['attempt_id']+'-depth.json'))],
    ]
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', env=child_env)
        if result.returncode:
            print(result.stdout + result.stderr)
            return result.returncode
    verify_packet(card)
    try:
        verify_mechanism_facts(card, raw)
    except ValueError as exc:
        print(json.dumps({'status':'member_return_not_committed','error':str(exc),
                          'next_step':'Correct only the unfrozen raw mechanism handoff; do not bypass this check or overwrite a return.',
                          **mechanism_repair_context(card,exc,raw)}, ensure_ascii=False))
        return 1
    result = subprocess.run([sys.executable, '-B', str(root/'scripts/write_agent_return.py'), '--task-card', str(path)], capture_output=True, text=True, encoding='utf-8', errors='replace', env=child_env)
    print(result.stdout + result.stderr)
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
