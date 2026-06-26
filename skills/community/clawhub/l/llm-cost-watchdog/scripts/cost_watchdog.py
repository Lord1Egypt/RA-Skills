#!/usr/bin/env python3
"""
Unified CLI for the cost-watchdog skill.

Dispatches the slash commands documented in SKILL.md:

    session        — spend summary for the current process session log.
    tail           — watch OpenClaw sessions and log every assistant turn.
    detect         — report which model the agent is using, via layered probes.
    audit <file>   — static-analyze a Python file for cost risks (AST).
    price <model>  — show live pricing (LiteLLM/OpenRouter/static).
    estimate       — cost estimate for a hypothetical call.
    alternatives   — cheaper models with the same billing unit.
    report         — daily/weekly breakdown from usage.jsonl.
    reset          — wipe the usage log.

Usage:
    python3 scripts/cost_watchdog.py <command> [args]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _fmt_age(ts: float) -> str:
    age = max(0, time.time() - ts)
    for unit, seconds in (("d", 86400), ("h", 3600), ("m", 60)):
        if age >= seconds:
            return f"{age/seconds:.1f}{unit}"
    return f"{age:.0f}s"


def cmd_session(args) -> int:
    import usage_log
    totals = usage_log.session_total()
    if totals["calls"] == 0:
        print("No usage recorded yet.")
        return 0
    print(f"Calls:          {totals['calls']:>10,}")
    print(f"Input tokens:   {totals['input_tokens']:>10,}")
    print(f"Output tokens:  {totals['output_tokens']:>10,}")
    print(f"Cache read:     {totals['cache_read_tokens']:>10,}")
    print(f"Cache write:    {totals['cache_write_tokens']:>10,}")
    print(f"Total cost:     ${totals['cost_total']:>9.4f}")
    if totals["by_model"]:
        print("\nBy model:")
        for model, stats in sorted(totals["by_model"].items(),
                                   key=lambda x: -x[1]["cost"])[:15]:
            print(f"  {model:<35s} {stats['calls']:>6,} calls   ${stats['cost']:>8.4f}")
    return 0


def cmd_tail(args) -> int:
    import openclaw_tailer
    if args.once:
        rows = openclaw_tailer.tail_once()
        print(f"Logged {rows} row(s).")
        return 0
    try:
        openclaw_tailer.watch(poll_interval=args.interval)
    except KeyboardInterrupt:
        pass
    return 0


def cmd_detect(args) -> int:
    import detect_model
    results = detect_model.detect_all()
    if args.json:
        from dataclasses import asdict
        print(json.dumps({
            "results": [asdict(r) for r in results],
            "best_guess": asdict(detect_model.best_guess(results)) if detect_model.best_guess(results) else None,
        }, indent=2))
    else:
        print(detect_model._render_table(results))
    return 0 if results else 1


def cmd_audit(args) -> int:
    import code_audit
    any_risks = False
    for path in args.files:
        risks = code_audit.audit_file(path)
        if risks:
            any_risks = True
        print(code_audit.format_report(path, risks))
    return 1 if any_risks else 0


def cmd_price(args) -> int:
    import _pricing
    p = _pricing.get_price(args.model)
    if p is None:
        print(f"No price found for {args.model!r}.")
        return 1
    age = _fmt_age(p.fetched_at) if p.fetched_at else "static"
    print(f"Model:     {p.display_name}  ({p.slug})")
    print(f"Mode:      {p.mode}")
    print(f"Unit:      {p.unit}")
    print(f"Input:     ${p.input_per_1m:.4f} per 1M {p.unit}s")
    print(f"Output:    ${p.output_per_1m:.4f} per 1M {p.unit}s")
    print(f"Provider:  {p.provider}")
    print(f"Source:    {p.source} ({age} old)")
    return 0


def cmd_estimate(args) -> int:
    import _pricing
    p = _pricing.get_price(args.model)
    if p is None:
        print(f"No price for {args.model!r}; can't estimate.", file=sys.stderr)
        return 1
    if p.unit != "token":
        print(f"Model uses unit {p.unit}; this command estimates token-based calls.")
        return 1
    cost_in = (args.input_tokens / 1_000_000) * p.input_per_1m
    cost_out = (args.output_tokens / 1_000_000) * p.output_per_1m
    total = (cost_in + cost_out) * args.iterations
    print(f"Model:          {args.model}")
    print(f"Input tokens:   {args.input_tokens:>10,} × {args.iterations} = {args.input_tokens * args.iterations:,}")
    print(f"Output tokens:  {args.output_tokens:>10,} × {args.iterations} = {args.output_tokens * args.iterations:,}")
    print(f"Per call:       ${cost_in + cost_out:.4f}")
    print(f"Total:          ${total:.4f}")
    return 0


def cmd_alternatives(args) -> int:
    import _pricing
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "optimized_calculator",
        Path(__file__).resolve().parent / "optimized-calculator.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    alts = mod.find_cheaper_alternatives(
        args.model, args.input_tokens, args.output_tokens,
        min_savings=args.min_savings,
    )
    if not alts:
        print(f"No same-unit alternatives cheaper than {args.model} by ≥{args.min_savings:.0%}.")
        return 0
    print(f"Cheaper alternatives to {args.model} (same unit, ≥{args.min_savings:.0%} savings):\n")
    for a in alts:
        print(f"  {a['model']:<40s} save {a['savings_percent']:>5.1f}%   ${a['alternative_cost']:.4f} vs ${a['current_cost']:.4f}")
    return 0


def cmd_report(args) -> int:
    import usage_log
    now = time.time()
    windows = [("24h", 86400), ("7d", 7 * 86400), ("30d", 30 * 86400)]
    print(f"{'Window':<6s} {'Calls':>7s} {'Cost':>10s}  {'Top model':<35s} {'(calls)':>8s}")
    print("-" * 72)
    for label, seconds in windows:
        since = now - seconds
        totals = usage_log.session_total(since=since)
        if totals["by_model"]:
            top_model, top_stats = max(totals["by_model"].items(), key=lambda x: x[1]["cost"])
            top_label = f"{top_model[:35]:<35s}"
            top_calls = f"{top_stats['calls']:>8,}"
        else:
            top_label = "-".ljust(35)
            top_calls = "0".rjust(8)
        print(f"{label:<6s} {totals['calls']:>7,} ${totals['cost_total']:>9.4f}  {top_label} {top_calls}")
    return 0


def cmd_reset(args) -> int:
    import usage_log
    if not args.yes:
        print("This will delete the usage log. Pass --yes to confirm.")
        return 1
    if args.all:
        usage_log.clear_all()
        print("Usage log + rolled files cleared.")
    else:
        usage_log.clear()
        print("Current-day usage log cleared (rolled files preserved).")
    return 0


def cmd_errors(args) -> int:
    import errors
    entries = errors.read_recent(limit=args.limit)
    if not entries:
        print("No errors recorded.")
        return 0
    for e in entries:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.get("ts", 0)))
        print(f"{ts}  [{e.get('component', '?')}] {e.get('error', '?')}")
        if e.get("hint"):
            print(f"    hint: {e['hint']}")
    print(f"\nTotal (24h): {errors.count_since(time.time() - 86400)}")
    return 0


def cmd_validate_tokens(args) -> int:
    """
    Compare our heuristic token count against the provider's authoritative
    count API for the same text. Surfaces drift %.
    """
    import tokenizer
    text = args.text or _DEFAULT_VALIDATION_TEXT
    heuristic, method = tokenizer.count_tokens(text, args.model)

    authoritative = None
    how = ""
    family = tokenizer._provider_family(args.model)
    try:
        if family == "anthropic":
            import anthropic
            client = anthropic.Anthropic()
            resp = client.messages.count_tokens(
                model=args.model,
                messages=[{"role": "user", "content": text}],
            )
            authoritative = resp.input_tokens
            how = "anthropic.messages.count_tokens"
        elif family == "openai":
            import tiktoken
            try:
                enc = tiktoken.encoding_for_model(args.model)
            except KeyError:
                enc = tiktoken.get_encoding("cl100k_base")
            authoritative = len(enc.encode(text))
            how = f"tiktoken ({enc.name})"
        else:
            print(f"No authoritative tokenizer wired for family '{family}' yet.")
            print(f"Heuristic: {heuristic} tokens ({method})")
            return 1
    except ImportError as e:
        print(f"Missing SDK: {e}. Install the provider's SDK to validate.")
        return 1
    except Exception as e:
        print(f"Authoritative count failed: {e}")
        print(f"Heuristic only: {heuristic} tokens ({method})")
        return 1

    drift = (heuristic - authoritative) / authoritative if authoritative else 0.0
    print(f"Model:          {args.model}")
    print(f"Text length:    {len(text)} chars, {len(text.split())} words")
    print(f"Heuristic:      {heuristic:>6,} tokens  ({method})")
    print(f"Authoritative:  {authoritative:>6,} tokens  ({how})")
    print(f"Drift:          {drift:+.1%}")
    return 0


_DEFAULT_VALIDATION_TEXT = """
The cost-watchdog is a diagnostic layer for LLM-based agents.
It tracks spend across providers, detects runaway loops at write time,
and surfaces a unified report. Typical overhead is a few hundred
microseconds per call for local logging, and a 24-hour cached fetch
from LiteLLM for live pricing.
""".strip()


def main() -> int:
    p = argparse.ArgumentParser(description="cost-watchdog CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("session", help="show spend totals from usage.jsonl").set_defaults(fn=cmd_session)

    t = sub.add_parser("tail", help="watch OpenClaw sessions and log turns")
    t.add_argument("--once", action="store_true")
    t.add_argument("--interval", type=float, default=2.0)
    t.set_defaults(fn=cmd_tail)

    d = sub.add_parser("detect", help="detect which model the agent is using")
    d.add_argument("--json", action="store_true")
    d.set_defaults(fn=cmd_detect)

    a = sub.add_parser("audit", help="AST-analyze Python for cost risks")
    a.add_argument("files", nargs="+")
    a.set_defaults(fn=cmd_audit)

    pr = sub.add_parser("price", help="show live price for a model")
    pr.add_argument("model")
    pr.set_defaults(fn=cmd_price)

    es = sub.add_parser("estimate", help="cost for n iterations")
    es.add_argument("model")
    es.add_argument("--input-tokens", type=int, required=True)
    es.add_argument("--output-tokens", type=int, required=True)
    es.add_argument("--iterations", type=int, default=1)
    es.set_defaults(fn=cmd_estimate)

    al = sub.add_parser("alternatives", help="cheaper models (same billing unit)")
    al.add_argument("model")
    al.add_argument("--input-tokens", type=int, default=100000)
    al.add_argument("--output-tokens", type=int, default=20000)
    al.add_argument("--min-savings", type=float, default=0.5)
    al.set_defaults(fn=cmd_alternatives)

    rp = sub.add_parser("report", help="usage summary windows")
    rp.set_defaults(fn=cmd_report)

    rs = sub.add_parser("reset", help="clear the usage log")
    rs.add_argument("--yes", action="store_true")
    rs.add_argument("--all", action="store_true", help="also delete rolled daily files")
    rs.set_defaults(fn=cmd_reset)

    er = sub.add_parser("errors", help="show recent swallowed exceptions")
    er.add_argument("--limit", type=int, default=20)
    er.set_defaults(fn=cmd_errors)

    vt = sub.add_parser("validate-tokens",
                        help="compare heuristic token count to provider's API")
    vt.add_argument("model")
    vt.add_argument("--text", help="text to tokenize (uses a default if omitted)")
    vt.set_defaults(fn=cmd_validate_tokens)

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
