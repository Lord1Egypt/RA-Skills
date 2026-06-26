#!/usr/bin/env python3
"""
langsmith-cli — Query and analyze LangSmith traces.
Usage: python3 langsmith.py <command> [options]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

import requests

API_BASE = "https://api.smith.langchain.com"


def get_api_key():
    key = os.environ.get("LANGSMITH_API_KEY")
    if not key:
        print("Error: LANGSMITH_API_KEY not set. Add it to your env or ~/.zshrc.", file=sys.stderr)
        sys.exit(1)
    return key


def api_headers():
    return {"x-api-key": get_api_key(), "Content-Type": "application/json"}


def parse_since(since: str) -> datetime:
    """Parse '2h', '7d', '30m', or ISO date string into a UTC datetime."""
    since = since.strip()
    now = datetime.now(timezone.utc)
    if since.endswith("h"):
        return now - timedelta(hours=int(since[:-1]))
    if since.endswith("d"):
        return now - timedelta(days=int(since[:-1]))
    if since.endswith("m"):
        return now - timedelta(minutes=int(since[:-1]))
    # Try ISO parse
    try:
        dt = datetime.fromisoformat(since)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        print(f"Error: Cannot parse --since value: {since}", file=sys.stderr)
        sys.exit(1)


def resolve_session_id(project_name: str) -> str:
    """Resolve project name to session ID."""
    resp = requests.get(
        f"{API_BASE}/api/v1/sessions",
        headers=api_headers(),
        params={"name": project_name},
    )
    if resp.status_code != 200:
        print(f"Error: Could not resolve project '{project_name}': {resp.status_code}", file=sys.stderr)
        sys.exit(1)
    sessions = resp.json()
    if not sessions:
        print(f"Error: Project '{project_name}' not found.", file=sys.stderr)
        sys.exit(1)
    return sessions[0]["id"]


def get_runs(project: str, since: str = "24h", status: str = None, limit: int = 50) -> list:
    """Fetch runs from LangSmith API using POST query endpoint."""
    start_time = parse_since(since)
    session_id = resolve_session_id(project)

    payload = {
        "session": [session_id],
        "start_time": start_time.isoformat(),
        "filter": "eq(is_root, true)",
        "limit": limit,
    }
    if status:
        payload["status"] = [status]

    all_runs = []
    cursor = None
    while True:
        if cursor:
            payload["cursor"] = cursor
        resp = requests.post(f"{API_BASE}/api/v1/runs/query", headers=api_headers(), json=payload)
        if resp.status_code != 200:
            print(f"Error: LangSmith API returned {resp.status_code}: {resp.text}", file=sys.stderr)
            sys.exit(1)
        data = resp.json()
        runs = data.get("runs", data) if isinstance(data, dict) else data
        if not runs:
            break
        all_runs.extend(runs)
        if len(all_runs) >= limit:
            break
        next_cursor = data.get("cursors", {}).get("next") if isinstance(data, dict) else None
        if not next_cursor:
            break
        cursor = next_cursor
    return all_runs[:limit]


def get_run_by_id(run_id: str) -> dict:
    resp = requests.get(f"{API_BASE}/api/v1/runs/{run_id}", headers=api_headers())
    if resp.status_code != 200:
        print(f"Error: Run {run_id} not found ({resp.status_code})", file=sys.stderr)
        sys.exit(1)
    return resp.json()


def compress_run(run: dict) -> dict:
    """Compress a run to essential fields for LLM context."""
    inputs = run.get("inputs", {})
    outputs = run.get("outputs", {})
    # Truncate long strings
    def trunc(v, n=300):
        s = str(v)
        return s[:n] + "…" if len(s) > n else s

    return {
        "id": run.get("id", ""),
        "name": run.get("name", ""),
        "status": run.get("status", ""),
        "start_time": run.get("start_time", ""),
        "latency_ms": (
            round((
                datetime.fromisoformat(run["end_time"].replace("Z", "+00:00")) -
                datetime.fromisoformat(run["start_time"].replace("Z", "+00:00"))
            ).total_seconds() * 1000)
            if run.get("end_time") and run.get("start_time") else None
        ),
        "total_tokens": run.get("total_tokens"),
        "prompt_tokens": run.get("prompt_tokens"),
        "error": run.get("error"),
        "inputs_summary": trunc(inputs),
        "outputs_summary": trunc(outputs),
        "feedback_stats": run.get("feedback_stats"),
    }


def cmd_runs(args):
    """List recent runs."""
    runs = get_runs(args.project, args.since, args.status, args.limit)
    if not runs:
        print(f"No runs found for project '{args.project}' in last {args.since}.")
        return

    print(f"\n{'ID':<36}  {'Name':<30}  {'Status':<10}  {'Tokens':>8}  {'Start'}")
    print("-" * 100)
    for r in runs:
        run_id = r.get("id", "")[:36]
        name = (r.get("name") or "")[:30]
        status = r.get("status", "")[:10]
        tokens = r.get("total_tokens", "-")
        start = r.get("start_time", "")[:19]
        print(f"{run_id:<36}  {name:<30}  {status:<10}  {str(tokens):>8}  {start}")
    print(f"\nTotal: {len(runs)} runs")


def cmd_cost(args):
    """Show token spend broken down by run name."""
    runs = get_runs(args.project, args.since, limit=100)
    if not runs:
        print(f"No runs found for project '{args.project}' in last {args.since}.")
        return

    costs = {}
    for r in runs:
        name = r.get("name", "unknown")
        costs.setdefault(name, {"count": 0, "prompt": 0, "completion": 0, "total": 0})
        costs[name]["count"] += 1
        costs[name]["prompt"] += r.get("prompt_tokens") or 0
        costs[name]["completion"] += r.get("completion_tokens") or 0
        costs[name]["total"] += r.get("total_tokens") or 0

    print(f"\nToken cost breakdown for '{args.project}' (last {args.since}):\n")
    print(f"{'Run Name':<40}  {'Runs':>5}  {'Prompt':>10}  {'Completion':>12}  {'Total':>10}")
    print("-" * 85)
    for name, c in sorted(costs.items(), key=lambda x: -x[1]["total"]):
        print(f"{name[:40]:<40}  {c['count']:>5}  {c['prompt']:>10,}  {c['completion']:>12,}  {c['total']:>10,}")

    grand_total = sum(c["total"] for c in costs.values())
    print(f"\nGrand total: {grand_total:,} tokens across {len(runs)} runs")


def cmd_latency(args):
    """Show latency percentiles per run name."""
    runs = get_runs(args.project, args.since, limit=100)
    if not runs:
        print(f"No runs found for project '{args.project}' in last {args.since}.")
        return

    from collections import defaultdict
    latencies = defaultdict(list)
    for r in runs:
        name = r.get("name", "unknown")
        # LangSmith returns latency in various places
        latency = r.get("latency")
        if latency is None and r.get("end_time") and r.get("start_time"):
            try:
                end = datetime.fromisoformat(r["end_time"].replace("Z", "+00:00"))
                start = datetime.fromisoformat(r["start_time"].replace("Z", "+00:00"))
                latency = (end - start).total_seconds()
            except Exception:
                pass
        if latency is not None:
            latencies[name].append(latency)

    print(f"\nLatency breakdown for '{args.project}' (last {args.since}):\n")
    print(f"{'Run Name':<40}  {'Runs':>5}  {'p50 (s)':>8}  {'p95 (s)':>8}  {'p99 (s)':>8}")
    print("-" * 80)

    import statistics
    for name, lats in sorted(latencies.items(), key=lambda x: -statistics.median(x[1])):
        lats_sorted = sorted(lats)
        n = len(lats_sorted)
        p50 = lats_sorted[int(n * 0.50)]
        p95 = lats_sorted[min(int(n * 0.95), n - 1)]
        p99 = lats_sorted[min(int(n * 0.99), n - 1)]
        print(f"{name[:40]:<40}  {n:>5}  {p50:>8.2f}  {p95:>8.2f}  {p99:>8.2f}")


def cmd_diff(args):
    """Compare runs before vs after a date."""
    before_dt = parse_since(args.before)
    after_dt = parse_since(args.after)

    session_id = resolve_session_id(args.project)
    # Runs BEFORE the pivot (look back 7d from pivot)
    before_start = before_dt - timedelta(days=7)

    def fetch(start, end=None):
        payload = {
            "session": [session_id],
            "start_time": start.isoformat(),
            "filter": "eq(is_root, true)",
            "limit": 100,
        }
        if end:
            payload["end_time"] = end.isoformat()
        r = requests.post(f"{API_BASE}/api/v1/runs/query", headers=api_headers(), json=payload)
        if r.status_code != 200:
            print(f"Error: {r.status_code} {r.text}", file=sys.stderr)
            sys.exit(1)
        data = r.json()
        return data.get("runs", data if isinstance(data, list) else [])

    before_runs = fetch(before_start, before_dt)
    after_runs = fetch(after_dt)

    def stats(runs):
        if not runs:
            return {"count": 0, "error_rate": 0, "avg_tokens": 0, "avg_latency_s": 0}
        errors = sum(1 for r in runs if r.get("status") == "error")
        tokens = [r.get("total_tokens") or 0 for r in runs]
        lats = []
        for r in runs:
            lat = r.get("latency")
            if lat is None and r.get("end_time") and r.get("start_time"):
                try:
                    end = datetime.fromisoformat(r["end_time"].replace("Z", "+00:00"))
                    start = datetime.fromisoformat(r["start_time"].replace("Z", "+00:00"))
                    lat = (end - start).total_seconds()
                except Exception:
                    pass
            if lat is not None:
                lats.append(lat)
        return {
            "count": len(runs),
            "error_rate": round(errors / len(runs) * 100, 1),
            "avg_tokens": round(sum(tokens) / len(runs)) if tokens else 0,
            "avg_latency_s": round(sum(lats) / len(lats), 2) if lats else 0,
        }

    bs = stats(before_runs)
    as_ = stats(after_runs)

    def delta(a, b, pct=False):
        if pct:
            return f"{b - a:+.1f}%"
        return f"{b - a:+}"

    print(f"\nDiff for '{args.project}'")
    print(f"BEFORE: up to {args.before}  |  AFTER: from {args.after}\n")
    print(f"{'Metric':<20}  {'Before':>10}  {'After':>10}  {'Delta':>10}")
    print("-" * 55)
    print(f"{'Runs':<20}  {bs['count']:>10}  {as_['count']:>10}  {delta(bs['count'], as_['count'])}")
    print(f"{'Error rate':<20}  {bs['error_rate']:>9}%  {as_['error_rate']:>9}%  {delta(bs['error_rate'], as_['error_rate'], pct=True)}")
    print(f"{'Avg tokens':<20}  {bs['avg_tokens']:>10,}  {as_['avg_tokens']:>10,}  {delta(bs['avg_tokens'], as_['avg_tokens'])}")
    print(f"{'Avg latency (s)':<20}  {bs['avg_latency_s']:>10}  {as_['avg_latency_s']:>10}  {delta(bs['avg_latency_s'], as_['avg_latency_s'])}")


def cmd_prompt_diff(args):
    """Show side-by-side prompt + output for two runs."""
    a = get_run_by_id(args.run_id_a)
    b = get_run_by_id(args.run_id_b)

    def extract_system(run):
        inputs = run.get("inputs", {})
        msgs = inputs.get("messages", [])
        for m in msgs:
            if isinstance(m, dict) and m.get("role") == "system":
                return m.get("content", "")
        return inputs.get("system", "") or str(inputs)[:500]

    def extract_output(run):
        outputs = run.get("outputs", {})
        if isinstance(outputs, dict):
            return outputs.get("output") or outputs.get("content") or str(outputs)[:500]
        return str(outputs)[:500]

    print(f"\n{'='*50} RUN A: {args.run_id_a[:8]} {'='*50}")
    print(f"Status: {a.get('status')}  |  Tokens: {a.get('total_tokens')}")
    print(f"\n--- System Prompt ---\n{extract_system(a)}")
    print(f"\n--- Output ---\n{extract_output(a)}")

    print(f"\n{'='*50} RUN B: {args.run_id_b[:8]} {'='*50}")
    print(f"Status: {b.get('status')}  |  Tokens: {b.get('total_tokens')}")
    print(f"\n--- System Prompt ---\n{extract_system(b)}")
    print(f"\n--- Output ---\n{extract_output(b)}")


def cmd_ask(args):
    """Fetch and format traces as structured context for the agent to analyze."""
    print(f"Fetching runs from '{args.project}' (last {args.since}, limit {args.limit})...", file=sys.stderr)
    runs = get_runs(args.project, args.since, limit=args.limit)

    if not runs:
        print(f"No runs found for project '{args.project}' in last {args.since}.")
        return

    compressed = [compress_run(r) for r in runs]

    print(f"# LangSmith Trace Context")
    print(f"Project: {args.project} | Period: last {args.since} | Runs: {len(runs)}")
    print(f"\n## Question\n{args.question}")
    print(f"\n## Traces ({len(runs)} runs)\n")
    print(json.dumps(compressed, indent=2))


def cmd_cluster_failures(args):
    """Group failed runs by input pattern (stub)."""
    print("cluster-failures: coming soon. Will use embeddings to group error runs by input similarity.")
    print(f"Project: {args.project}, since: {args.since}")


def cmd_replay(args):
    """Re-run a specific run's inputs against current code (stub)."""
    run = get_run_by_id(args.run_id)
    print(f"Replay stub for run {args.run_id}")
    print(f"Status: {run.get('status')}")
    print(f"Inputs: {json.dumps(run.get('inputs', {}), indent=2)[:1000]}")
    print("\nTo replay: copy the inputs above and send them to your chain/agent manually.")


def main():
    parser = argparse.ArgumentParser(description="LangSmith CLI — query and analyze traces")
    sub = parser.add_subparsers(dest="command")

    # ask
    p_ask = sub.add_parser("ask", help="LLM Q&A over your traces")
    p_ask.add_argument("question", help="Natural language question about your traces")
    p_ask.add_argument("--project", "-p", required=True, help="LangSmith project name")
    p_ask.add_argument("--since", default="24h", help="Time window (e.g. 2h, 7d, 30m). Default: 24h")
    p_ask.add_argument("--limit", type=int, default=50, help="Max runs to fetch. Default: 50")

    # runs
    p_runs = sub.add_parser("runs", help="List recent runs")
    p_runs.add_argument("project", help="LangSmith project name")
    p_runs.add_argument("--since", default="24h")
    p_runs.add_argument("--status", choices=["error", "success", "pending"], help="Filter by status")
    p_runs.add_argument("--limit", type=int, default=20)

    # cost
    p_cost = sub.add_parser("cost", help="Token spend by chain/node")
    p_cost.add_argument("project")
    p_cost.add_argument("--since", default="7d")

    # latency
    p_lat = sub.add_parser("latency", help="Latency percentiles per run name")
    p_lat.add_argument("project")
    p_lat.add_argument("--since", default="24h")

    # diff
    p_diff = sub.add_parser("diff", help="Compare runs before vs after a date")
    p_diff.add_argument("project")
    p_diff.add_argument("--before", required=True, help="Pivot date (ISO or relative like 7d)")
    p_diff.add_argument("--after", required=True, help="Start of 'after' window (ISO or relative)")

    # prompt-diff
    p_pdiff = sub.add_parser("prompt-diff", help="Side-by-side prompt+output for two runs")
    p_pdiff.add_argument("run_id_a")
    p_pdiff.add_argument("run_id_b")

    # cluster-failures
    p_cf = sub.add_parser("cluster-failures", help="Group failed runs by input pattern")
    p_cf.add_argument("project")
    p_cf.add_argument("--since", default="7d")

    # replay
    p_replay = sub.add_parser("replay", help="Show inputs for a specific run (for manual replay)")
    p_replay.add_argument("run_id")

    args = parser.parse_args()

    dispatch = {
        "ask": cmd_ask,
        "runs": cmd_runs,
        "cost": cmd_cost,
        "latency": cmd_latency,
        "diff": cmd_diff,
        "prompt-diff": cmd_prompt_diff,
        "cluster-failures": cmd_cluster_failures,
        "replay": cmd_replay,
    }

    if args.command not in dispatch:
        parser.print_help()
        sys.exit(1)

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
