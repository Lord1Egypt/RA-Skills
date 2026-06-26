#!/usr/bin/env python3
import argparse
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

MODEL_PATTERNS = [
    r'"model"\s*:\s*"([^"]+)"',
    r'"modelName"\s*:\s*"([^"]+)"',
    r'"resolvedModel"\s*:\s*"([^"]+)"',
    r'\bmodel=([\w./:-]+)',
    r'\busing model\s+([\w./:-]+)',
]


def load_cases(path: Path):
    return json.loads(path.read_text())


def extract_actual_model(log_lines):
    text = "\n".join(log_lines)
    for pat in MODEL_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            return matches[-1]
    return None


def extract_tokens(agent_json, log_lines):
    if isinstance(agent_json, dict):
        # Try common usage keys first
        for key in ["tokens", "usage", "tokenUsage"]:
            val = agent_json.get(key)
            if isinstance(val, dict):
                return val
    text = "\n".join(log_lines)
    token_match = re.findall(r'"(prompt|completion|total)?_?tokens?"\s*:\s*(\d+)', text, flags=re.IGNORECASE)
    if not token_match:
        return None
    out = {}
    for kind, num in token_match:
        k = (kind or "tokens").lower()
        out[k] = int(num)
    return out


def start_log_tail(log_q, stop_event):
    cmd = ["openclaw", "logs", "--follow", "--json", "--plain", "--interval", "500", "--limit", "50"]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    except Exception as e:
        log_q.put(f"[log-tail-error] {e}")
        return None

    def _reader():
        try:
            while not stop_event.is_set():
                line = proc.stdout.readline()
                if not line:
                    if proc.poll() is not None:
                        break
                    time.sleep(0.05)
                    continue
                log_q.put(line.rstrip("\n"))
        finally:
            if proc.poll() is None:
                proc.terminate()

    t = threading.Thread(target=_reader, daemon=True)
    t.start()
    return proc


def run_case(case, agent, requested_model, timeout):
    log_q = queue.Queue()
    stop_event = threading.Event()
    log_proc = start_log_tail(log_q, stop_event)

    prompt = (
        "Spawn a subagent to solve this bounded task, then return only the final answer. "
        "Keep it concise.\n\n"
        f"TEST_CASE_ID: {case['id']}\n"
        f"TEST_TASK: {case['prompt']}\n"
    )
    if requested_model:
        prompt = f"Preferred model: {requested_model}. Use it if available.\n" + prompt

    cmd = ["openclaw", "agent", "--json", "--timeout", str(timeout), "--message", prompt]
    if agent:
        cmd += ["--agent", agent]

    start = time.monotonic()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    runtime = round(time.monotonic() - start, 3)

    time.sleep(1.0)
    stop_event.set()
    if log_proc and log_proc.poll() is None:
        log_proc.terminate()

    logs = []
    while not log_q.empty():
        logs.append(log_q.get())

    raw_out = (proc.stdout or "").strip()
    raw_err = (proc.stderr or "").strip()
    agent_json = None
    parse_error = None

    if raw_out:
        try:
            agent_json = json.loads(raw_out)
        except Exception as e:
            parse_error = f"Could not parse agent JSON output: {e}"

    response_text = None
    if isinstance(agent_json, dict):
        for k in ["response", "text", "output", "message"]:
            if isinstance(agent_json.get(k), str):
                response_text = agent_json[k]
                break

    status = "ok" if proc.returncode == 0 else "error"
    errors = []
    if proc.returncode != 0:
        errors.append(f"openclaw exited with code {proc.returncode}")
    if raw_err:
        errors.append(raw_err)
    if parse_error:
        errors.append(parse_error)

    actual_model = extract_actual_model(logs)
    tokens = extract_tokens(agent_json, logs)

    result = {
        "test_case": case["id"],
        "agent": agent,
        "requested_model": requested_model,
        "actual_model": actual_model,
        "status": status,
        "result_summary": (response_text or raw_out or "").strip()[:600],
        "runtime_seconds": runtime,
        "tokens": tokens,
        "errors": errors,
    }
    return result


def print_human_summary(results):
    print("\n=== model-tester summary ===")
    for r in results:
        print(f"- case={r['test_case']} status={r['status']} runtime={r['runtime_seconds']}s")
        print(f"  agent={r.get('agent') or '-'} requested={r.get('requested_model') or '-'} actual={r.get('actual_model') or 'unknown'}")
        if r.get("tokens"):
            print(f"  tokens={json.dumps(r['tokens'])}")
        if r.get("errors"):
            print(f"  errors={'; '.join(r['errors'])}")
        print(f"  result={r.get('result_summary','')[:180]}")


def main():
    parser = argparse.ArgumentParser(description="Test OpenClaw agent/model routing against predefined cases.")
    parser.add_argument("--agent", help="Agent name/id to test (e.g. chat, coder, menial)")
    parser.add_argument("--model", help="Requested model alias/name to test")
    parser.add_argument("--case", default="extract-emails", help="Case id from test-cases.json, or 'all'")
    parser.add_argument("--timeout", type=int, default=120, help="Per-case timeout seconds")
    parser.add_argument("--cases-file", default=str(Path(__file__).resolve().parents[1] / "references" / "test-cases.json"))
    parser.add_argument("--out", help="Write JSON result to this file")
    args = parser.parse_args()

    if not args.agent and not args.model:
        parser.error("Provide at least one of --agent or --model")

    cases = load_cases(Path(args.cases_file))
    if args.case == "all":
        selected = cases
    else:
        selected = [c for c in cases if c["id"] == args.case]
        if not selected:
            parser.error(f"Unknown case id: {args.case}")

    all_results = [run_case(c, args.agent, args.model, args.timeout) for c in selected]

    output = {
        "tool": "model-tester",
        "timestamp": int(time.time()),
        "agent": args.agent,
        "requested_model": args.model,
        "results": all_results,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    print_human_summary(all_results)

    if args.out:
        Path(args.out).write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")

    if any(r["status"] != "ok" for r in all_results):
        sys.exit(2)


if __name__ == "__main__":
    main()
