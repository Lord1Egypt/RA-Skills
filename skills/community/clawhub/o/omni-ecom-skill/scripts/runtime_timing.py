"""Read native traces for measured latency; no completion or business authority."""
import argparse
import hashlib
import json
from pathlib import Path


def phase(call):
    name = call.get('name')
    if name in ('Read', 'Glob', 'Grep'):
        return 'input_read'
    if name == 'Agent':
        return 'expert_dispatch'
    if name in ('TaskOutput', 'TaskStop'):
        return 'expert_wait_or_control'
    if name in ('Bash', 'exec_command'):
        raw = call.get('arguments', '')
        try:
            args = json.loads(raw) if isinstance(raw, str) else raw
            command = args.get('command', args.get('cmd', '')) if isinstance(args, dict) else ''
        except (ValueError, TypeError):
            command = ''
        # Only known program names are classified; never persist arguments or data.
        groups = (
            ('wait_for_agent_returns.py', 'expert_wait_or_control'),
            ('generate_pdf_report.py', 'report_and_pdf'),
            ('build_report_package.py', 'report_and_pdf'),
            ('prepare_workbuddy_acceptance_review.py', 'review_preparation'),
            ('check_review_inputs.py', 'review_input_check'),
            ('finalize_workbuddy_acceptance_review.py', 'review_and_completion'),
            ('completion_gate.py', 'completion_check'),
            ('finish_agent_handoff.py', 'handoff_validation_and_return'),
            ('claim_guard.py', 'numeric_verification'),
            ('quality_recompute.py', 'numeric_verification'),
        )
        for program, group in groups:
            if program in command:
                return group
    return 'other'


def summarize(trace):
    trace = Path(trace)
    rows = [json.loads(line) for line in trace.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    times = [r['timestamp'] for r in rows if isinstance(r.get('timestamp'), (int,float))]
    calls = [r for r in rows if r.get('type')=='function_call']
    results = {r.get('callId'):r for r in rows if r.get('type')=='function_call_result'}
    from trace_usage import summarize_usage
    counts = {}; spans = []; phase_counts = {}; phase_seconds = {}
    for call in calls:
        name=call.get('name'); counts[name]=counts.get(name,0)+1
        group = phase(call)
        phase_counts[group] = phase_counts.get(group, 0) + 1
        result=results.get(call.get('callId'))
        if result and isinstance(call.get('timestamp'),(int,float)) and isinstance(result.get('timestamp'),(int,float)):
            seconds = round((result['timestamp']-call['timestamp'])/1000,3)
            spans.append(dict(tool=name,seconds=seconds))
            phase_seconds[group] = round(phase_seconds.get(group, 0) + seconds, 3)
    return dict(file=trace.name,sha256=hashlib.sha256(trace.read_bytes()).hexdigest(),
        elapsed_seconds=round((max(times)-min(times))/1000,3) if times else None,
        tool_calls=len(calls),tool_counts=counts,tool_spans=spans,
        token_usage=summarize_usage(rows),
        tool_phase_counts=phase_counts,tool_phase_seconds=phase_seconds,
        timing_note='Tool spans only; model reasoning and network queue time are not phase-attributed. Parallel spans may overlap and must not be summed as total report time.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--trace',required=True); p.add_argument('--output')
    a=p.parse_args(); trace=Path(a.trace).resolve()
    result=dict(artifact_type='runtime_timing_diagnostic',current_completion_authority=False,
        traces=[summarize(trace),*[summarize(f) for f in sorted((trace.parent/trace.stem/'subagents').glob('*.jsonl'))]])
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if a.output:
        out=Path(a.output).resolve()
        if out==trace or out.suffix!='.json': raise ValueError('timing_output_invalid')
        out.write_text(text+'\n',encoding='utf-8')
    print(text)
