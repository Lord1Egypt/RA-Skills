"""CLI entry point for perplexity-toolkit."""

import argparse
import logging
import json
import sys
from typing import Optional

from ..config import set_config
from ..routing import select_route

logger = logging.getLogger(__name__)


def cmd_route(args) -> int:
    """Select a route from the original user wording only."""
    decision = select_route(args.request)
    if args.format == "json":
        print(json.dumps(decision, ensure_ascii=False))
    else:
        print(f"route: {decision['route']}")
        if decision["matched_terms"]:
            print("matched_terms: " + ", ".join(decision["matched_terms"]))
        print("reason: " + decision["reason"])
    return 0


def _console_error_payload(exc) -> dict:
    """Machine-readable failure payload (gate + error_code + evidence)."""
    return {"ok": False, "gate": exc.gate, "error": exc.message,
            "error_code": getattr(exc, "code", None),
            "evidence": exc.evidence, "gates": exc.gates}


def _console_fail(exc, fmt: str) -> None:
    hint = None
    try:
        from ..console_judge import route_hint
        candidate = route_hint(exc.gate, getattr(exc, "code", None), exc.message)
        if candidate.get("status") == "ok":
            hint = candidate
    except Exception:  # noqa: BLE001 — the optional judge must never break failure reporting
        hint = None
    payload = _console_error_payload(exc)
    if hint:
        payload["jev_hint"] = hint
    if fmt == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"FAILED at gate: {exc.gate}")
        print(f"  {exc.message}")
        if getattr(exc, "code", None):
            print(f"  code: {exc.code}")
        if exc.evidence:
            print(f"  evidence: {exc.evidence}")
        if hint:
            print(f"  hint (Jev): {hint['route']}  (confidence {hint['confidence']:.2f})")


def _console_run_step(fn, fmt: str, *, args=(), kwargs=None,
                      text_lines=None) -> Optional[dict]:
    """Run one granular console step; unified error output + exit handling."""
    from ..console import ConsoleError
    try:
        payload = fn(*args, **(kwargs or {}))
    except ConsoleError as exc:
        _console_fail(exc, fmt)
        return None
    if fmt == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        lines = text_lines(payload) if text_lines else [json.dumps(payload, ensure_ascii=False)]
        for line in lines:
            print(line)
    return payload


def _t_drift(payload: dict) -> list:
    """Human-readable rendering of the read-only probe drift report."""
    counts = payload.get("counts") or {}
    lines = [f"drift report: {counts.get('total', 0)} probes "
             f"({counts.get('executed', 0)} read-only executed, "
             f"{counts.get('action', 0)} action-class static-only)  "
             f"locale={payload.get('locale')}"]
    for name, entry in (payload.get("probes") or {}).items():
        if entry.get("error"):
            lines.append(f"  {name:<13} read   ERROR {entry['error']}")
        elif entry.get("mode") == "action":
            mark = "markers-ok" if entry.get("markers_ok") else "MARKERS-LOST"
            found = ("" if entry.get("found") is None
                     else f"  found={str(entry.get('found')).lower()}")
            lines.append(f"  {name:<13} action static-only [{mark}]{found} "
                         f"— {entry.get('reason')}")
        else:
            summary = json.dumps(entry.get("summary") or {}, ensure_ascii=False)
            lines.append(f"  {name:<13} read   found={entry.get('found')}  {summary}")
    if payload.get("missing_found"):
        lines.append("missing_found: " + ", ".join(payload["missing_found"]))
    for note in payload.get("anomalies") or []:
        lines.append(f"  ⚠ {note}")
    fb = payload.get("fallbacks") or {}
    by_rung = fb.get("by_rung") or {}
    head = f"fallbacks: {fb.get('total', 0)} total"
    if by_rung:
        head += " (" + ", ".join(f"{k}×{v}" for k, v in by_rung.items()) + ")"
    lines.append(head)
    for ev in fb.get("recent") or []:
        lines.append(f"  recent: {ev.get('ts', '')} {ev.get('rung', '')} "
                     f"ok={str(ev.get('ok')).lower()} {ev.get('summary', '')}")
    lines.append("verdict: " + (f"clean — no drift detected" if payload.get("ok")
                                else f"{counts.get('anomalies', 0)} anomaly(ies)"))
    return lines


def cmd_console(args) -> int:
    """Resident Perplexity console actions."""
    from ..console import (ConsoleError, console_ask, console_attach, console_detach,
                           console_drift, console_extract, console_files, console_fill,
                           console_models, console_open, console_selfcheck,
                           console_send, console_set_model, console_status,
                           console_submit, console_threads, console_wait)
    action = getattr(args, "console_action", None)
    fmt = getattr(args, "format", "text")

    if action in ("models", "model"):
        try:
            payload = (console_models() if action == "models"
                       else console_set_model(args.name))
        except ConsoleError as exc:
            _console_fail(exc, fmt)
            return 1
        if fmt == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            if action == "models":
                print(f"current: {payload['current']}")
                for m in payload["models"]:
                    mark = "*" if m["checked"] else " "
                    badges = f"  [{'/'.join(m['badges'])}]" if m["badges"] else ""
                    sub = "  (submenu)" if m["submenu"] else ""
                    print(f"{mark} {m['name']}{badges}{sub}")
                print(f"menu_closed: {payload.get('menu_closed')}")
            else:
                print(f"switched: {payload['from']} -> {payload['to']} "
                      f"(attempts={payload['attempts']})")
        return 0

    if action == "ask":
        try:
            result = console_ask(args.query, task=args.task,
                                 new_thread=args.new_thread,
                                 wait_budget=args.wait_budget,
                                 files=getattr(args, "file", None),
                                 judge=getattr(args, "judge", None),
                                 model=getattr(args, "model", None))
        except ConsoleError as exc:
            _console_fail(exc, fmt)
            return 1
        if fmt == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result["answer"])
            print("\n--- console ---")
            print(f"task: {result['task']}  session: {result['session']}"
                  f"  new_thread: {result['new_thread']}  elapsed: {result['elapsed_s']}s")
            print(f"url: {result['url']}")
            print(f"model: {result.get('model') or '-'}  "
                  f"attachments: {', '.join(result.get('attachments') or []) or '-'}")
            j = result.get("judge") or {}
            if j.get("enabled"):
                if j.get("status") in {"ok", "review", "concern"}:
                    print(f"judge: {j['status']} (answers_question="
                          f"{j.get('answers_question'):.2f}, complete={j.get('complete'):.2f})")
                else:
                    print(f"judge: {j.get('status')} ({j.get('reason', '')})")
            print(f"sources: {len(result['sources'])}")
            gate_bits = []
            for name, value in result["gates"].items():
                gate_bits.append(f"{name}={'ok' if isinstance(value, dict) else value}")
            print("gates: " + ", ".join(gate_bits))
        return 0

    if action == "status":
        payload = console_status()
        if fmt == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"session: {payload['session']}  group: {payload['group_title']}")
            print(f"active_task: {payload['active_task']}")
            for name, entry in payload["threads"].items():
                print(f"  - {name}: {entry.get('url', '')}  (turns={entry.get('turns', '?')})")
            pend = payload.get("pending")
            if pend:
                print(f"pending: {pend.get('status')}  "
                      f"query={str(pend.get('query'))[:50]!r}  "
                      f"files={', '.join(pend.get('files') or []) or '-'}")
            print(f"live: {json.dumps(payload.get('live'), ensure_ascii=False)}")
        return 0

    if action == "threads":
        payload = console_threads()
        if fmt == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            for name, entry in payload["threads"].items():
                marker = "*" if name == payload.get("active_task") else " "
                print(f"{marker} {name}: {entry.get('label', '')} "
                      f"[turns={entry.get('turns', '?')}] {entry.get('url', '')}")
        return 0

    if action == "drift" or (action == "selfcheck" and getattr(args, "drift", False)):
        # Read-only probe drift report. `selfcheck --drift` is the alias: the
        # bare `selfcheck` action keeps its original meaning (run the full
        # gate pipeline on a canned query).
        payload = _console_run_step(console_drift, fmt, text_lines=_t_drift)
        return 0 if payload and payload.get("ok") else 1

    if action == "selfcheck":
        result = console_selfcheck(wait_budget=args.wait_budget)
        if fmt == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if result.get("ok"):
                print("SELFCHECK PASSED")
                print(f"answer: {result['answer'][:200]}")
                for name, value in result["gates"].items():
                    print(f"  gate {name}: {json.dumps(value, ensure_ascii=False)}")
                print(f"elapsed: {result['elapsed_s']}s")
            else:
                print("SELFCHECK FAILED")
                print(f"  gate: {result.get('gate')}")
                print(f"  error: {result.get('error')}")
                if result.get("evidence"):
                    print(f"  evidence: {result['evidence']}")
        return 0 if result.get("ok") else 1

    if action == "open":
        ok = _console_run_step(
            console_open, fmt, args=(args.target,),
            kwargs={"new_thread": args.new_thread},
            text_lines=lambda p: [f"opened: {p['url']} (task={p['target']}, "
                                  f"new_thread={p['new_thread']})"])
        return 0 if ok else 1

    if action == "fill":
        def _t_fill(p):
            pend = p["pending"]
            files = ", ".join(pend.get("files") or []) or "-"
            lines = [f"staged: task={pend['task']} query={pend['query'][:60]!r} files={files}",
                     f"gates: {', '.join(k + '=ok' for k in p['gates'])}"]
            jr = (p.get("gates") or {}).get("jev_recovery")
            if jr:
                lines.append(f"jev recovery: {jr.get('route')} "
                             f"(applied, attempts={jr.get('attempts', 1)})")
            return lines
        ok = _console_run_step(
            console_fill, fmt, args=(args.query,),
            kwargs={"task": args.task, "new_thread": args.new_thread,
                    "files": getattr(args, "file", None),
                    "judge": getattr(args, "judge", None)},
            text_lines=_t_fill)
        return 0 if ok else 1

    if action == "submit":
        def _t_submit(p):
            g = p["gates"]["submit"]
            return [f"submitted: mechanism={g.get('mechanism')} "
                    f"recovered={g.get('recovered', '-')}"]
        ok = _console_run_step(console_submit, fmt,
                               kwargs={"submit_timeout": args.submit_timeout},
                               text_lines=_t_submit)
        return 0 if ok else 1

    if action == "wait":
        def _t_wait(p):
            g = p["gates"]["complete"]
            lines = [f"completed: chars={g.get('chars')} method={g.get('method')}"]
            jr = (p.get("gates") or {}).get("jev_recovery")
            if jr:
                lines.append(f"jev recovery: {jr.get('route')} "
                             f"(applied, attempts={jr.get('attempts', 1)})")
            return lines
        ok = _console_run_step(console_wait, fmt,
                               kwargs={"wait_budget": args.wait_budget,
                                       "judge": getattr(args, "judge", None)},
                               text_lines=_t_wait)
        return 0 if ok else 1

    if action == "extract":
        def _t_extract(p):
            lines = [p.get("answer") or "(empty answer)"]
            lines.append(f"url: {p.get('url')}  model: {p.get('model') or '-'}  "
                         f"sources: {len(p.get('sources') or [])}")
            if (p.get("gates") or {}).get("send"):
                lines.append(f"send: chips_cleared={p['gates']['send'].get('chips_cleared')}")
            jr = (p.get("gates") or {}).get("jev_recovery")
            if jr:
                lines.append(f"jev recovery: {jr.get('route')} "
                             f"(applied, attempts={jr.get('attempts', 1)})")
            j = p.get("judge") or {}
            if j.get("enabled"):
                if j.get("status") in {"ok", "review", "concern"}:
                    lines.append(f"judge: {j['status']} (answers_question="
                                 f"{j.get('answers_question'):.2f}, complete={j.get('complete'):.2f})")
                else:
                    lines.append(f"judge: {j.get('status')} ({j.get('reason', '')})")
            scroll = (p.get("gates") or {}).get("scroll") or {}
            if scroll.get("settled") is False:
                lines.append("⚠️ scroll unsettled（懒渲染可能未完成，"
                             "extract --peek 复核）")
            if "consumed" in p:
                lines.append(f"consumed: {str(bool(p['consumed'])).lower()}")
            if p.get("truncation_risk") is True:
                lines.append("⚠️ 可能截断（尾部无终止符且仍在生成）")
            return lines
        ok = _console_run_step(console_extract, fmt,
                               kwargs={"judge": getattr(args, "judge", None),
                                       "strict": getattr(args, "strict", False),
                                       "peek": getattr(args, "peek", False),
                                       "again": getattr(args, "again", False)},
                               text_lines=_t_extract)
        return 0 if ok else 1

    if action == "send":
        def _t_send(p):
            g = p["gates"]["submit"]
            return [f"sent: task={p['task']} mechanism={g.get('mechanism')} "
                    f"recovered={g.get('recovered', '-')}",
                    "next: `perplexity console wait` then `perplexity console extract`"]
        ok = _console_run_step(
            console_send, fmt, args=(args.query,),
            kwargs={"task": args.task, "new_thread": args.new_thread,
                    "files": getattr(args, "file", None)},
            text_lines=_t_send)
        return 0 if ok else 1

    if action == "attach":
        def _t_attach(p):
            return [f"attached: {', '.join(p['pending_files']) or '-'}",
                    f"chips: {', '.join(p['gates']['files'].get('chips') or []) or '-'}"]
        ok = _console_run_step(console_attach, fmt, kwargs={"files": args.file},
                               text_lines=_t_attach)
        return 0 if ok else 1

    if action == "files":
        def _t_files(p):
            return [f"chips: {', '.join(p['chips']) or '-'}",
                    f"staged: {', '.join(p['pending_files']) or '-'} "
                    f"({p.get('pending_status')})"]
        ok = _console_run_step(console_files, fmt, text_lines=_t_files)
        return 0 if ok else 1

    if action == "detach":
        ok = _console_run_step(
            console_detach, fmt, args=(args.name,),
            text_lines=lambda p: [f"detached: {p['detached']}",
                                  f"chips: {', '.join(p['chips']) or '-'}"])
        return 0 if ok else 1

    print("usage: perplexity console {ask,send,fill,submit,wait,extract,attach,files,"
          "detach,open,models,model,status,threads,drift,selfcheck} ...")
    return 2


def cmd_search(args):
    """Single search."""
    from ..search import search, deep_research, model_council, step_by_step
    modes = {"search": search, "deep_research": deep_research,
             "model_council": model_council, "step_by_step": step_by_step}
    fn = modes.get(args.mode, search)
    result = fn(args.query, new_tab=None, verify=args.verify)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"URL: {result.get('url', 'N/A')}")
        print(f"Answer:\n{result.get('answer', 'No answer')}")
        print(f"\nSources ({len(result.get('sources', []))}):")
        for i, s in enumerate(result.get("sources", []), 1):
            print(f"  {i}. {s.get('text', '')[:80]} → {s.get('href', '')}")

        # Show verification results only in human-readable mode. JSON mode
        # must remain one valid JSON document on stdout.
        quality = result.get("quality")
        if quality:
            print(f"\n--- Quality Check ---")
            ac = quality.get("answer_check", {})
            sc = quality.get("source_check", {})
            print(f"Answer score: {ac.get('score', '?')}/100")
            if ac.get("issues"):
                for issue in ac["issues"]:
                    print(f"  ⚠ {issue}")
            if sc.get("total", 0) > 0:
                print(f"Sources: {sc['valid']}/{sc['total']} reachable")
                for b in sc.get("broken_urls", []):
                    print(f"  ✗ [{b['status']}] {b['href']}")
            print(f"Verdict: {quality.get('verdict', '?')} — {quality.get('suggestion', '')}")

    return 1 if result.get("error") else 0


def cmd_batch(args):
    """Batch search."""
    from ..batch import load_queries, run_batch
    queries = []
    if args.input:
        queries = load_queries(args.input)
    for q in (args.queries or []):
        queries.append({"query": q, "mode": args.mode})
    if not queries:
        logger.warning("No queries provided.")
        sys.exit(1)
    run_batch(queries, output_file=args.output, resume=args.resume,
              progress_file=args.progress if args.resume else None,
              delay=args.delay, verify=args.verify)


def cmd_aggregate(args):
    """Aggregate results."""
    from ..aggregator import aggregate, to_markdown
    import json
    results = []
    for f in args.files:
        with open(f) as fh:
            data = json.load(fh)
            results.extend(data if isinstance(data, list) else [data])
    report = aggregate(results)
    if args.format == "markdown":
        print(to_markdown(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))


def cmd_history(args):
    """Manage search history."""
    from ..history import list_conversations, find_conversation, delete_conversations
    if args.action == "list":
        from ..config import get_config
        from ..drivers import create_driver
        drv = create_driver(get_config())
        from ..config import get_config as gc
        drv.navigate(gc().base_url, new_tab=True)
        import time; time.sleep(gc().page_load_wait)
        convos = list_conversations(drv, args.limit)
        for i, c in enumerate(convos, 1):
            print(f"{i}. {c['title'][:60]}  [{c['href'][:20]}...]")
        print(f"\nTotal: {len(convos)} conversations")

    elif args.action == "search":
        from ..config import get_config
        from ..drivers import create_driver
        drv = create_driver(get_config())
        drv.navigate(get_config().base_url, new_tab=True)
        import time; time.sleep(get_config().page_load_wait)
        if not args.query:
            logger.warning("Error: provide a search query")
            sys.exit(1)
        convos = find_conversation(drv, args.query)
        for i, c in enumerate(convos, 1):
            print(f"{i}. {c['title'][:60]}  [{c['href'][:20]}...]")
        print(f"\nFound: {len(convos)} matching '{args.query}'")

    elif args.action == "delete":
        if not args.query and not args.href:
            logger.warning("Error: provide --query or --href")
            sys.exit(1)
        result = delete_conversations(query=args.query, hrefs=args.href,
                                       limit=args.limit, dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser with all subcommands."""
    # Imported here rather than at module scope to keep CLI startup lazy, in
    # line with the other driver imports in this file.
    from ..drivers import DRIVER_REGISTRY

    backends = sorted(DRIVER_REGISTRY)

    parser = argparse.ArgumentParser(
        prog="perplexity",
        description="Perplexity Toolkit — automate Perplexity AI search",
    )
    parser.add_argument("-w", "--wait", type=float, help="Search wait time (seconds)")
    parser.add_argument("-r", "--retries", type=int, help="Max retries")
    parser.add_argument("--session-prefix", help="Task-scoped WebBridge session prefix")
    # Choices come from the registry so this flag can never advertise a backend
    # that is not actually implemented, and an unknown value is rejected here
    # rather than silently falling back to webbridge.
    parser.add_argument(
        "-b", "--backend", choices=backends,
        help=f"Driver backend ({', '.join(backends)})",
    )
    parser.set_defaults(verify=True)
    parser.add_argument("--verify", dest="verify", action="store_true",
                        help="Verify sources and answer quality (default)")
    parser.add_argument("--no-verify", dest="verify", action="store_false",
                        help="Skip source and answer-quality verification")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable DEBUG logging")
    sub = parser.add_subparsers(dest="command")

    # search
    p = sub.add_parser("search", help="Single search")
    p.add_argument("query", help="Search query")
    p.add_argument("-m", "--mode", default="search",
                   choices=["search", "deep_research", "model_council", "step_by_step"])
    p.add_argument("-f", "--format", default="text", choices=["text", "json"])
    p.add_argument("--verify", dest="verify", action="store_true", default=argparse.SUPPRESS,
                   help=argparse.SUPPRESS)
    p.add_argument("--no-verify", dest="verify", action="store_false", default=argparse.SUPPRESS,
                   help=argparse.SUPPRESS)

    # batch
    p = sub.add_parser("batch", help="Batch search")
    p.add_argument("queries", nargs="*", help="Inline queries")
    p.add_argument("-i", "--input", help="Input file (json/csv/txt)")
    p.add_argument("-o", "--output", default="batch_results.json")
    p.add_argument("-m", "--mode", default="search")
    p.add_argument("-r", "--resume", action="store_true")
    p.add_argument("--progress", default=".batch_progress")
    p.add_argument("-d", "--delay", type=float, default=3.0)
    p.add_argument("--verify", dest="verify", action="store_true", default=argparse.SUPPRESS,
                   help=argparse.SUPPRESS)
    p.add_argument("--no-verify", dest="verify", action="store_false", default=argparse.SUPPRESS,
                   help=argparse.SUPPRESS)

    # aggregate
    p = sub.add_parser("aggregate", help="Aggregate results")
    p.add_argument("files", nargs="+", help="Result JSON files")
    p.add_argument("-f", "--format", default="json", choices=["json", "markdown"])

    # history
    p = sub.add_parser("history", help="Manage search history")
    p.add_argument("action", choices=["list", "search", "delete"],
                   help="list: show all, search: find by title, delete: remove")
    p.add_argument("query", nargs="?", help="Search query or title to match")
    p.add_argument("--limit", type=int, default=50, help="Max conversations")
    p.add_argument("--dry-run", action="store_true", help="Show what would be deleted")
    p.add_argument("--href", nargs="*", help="Specific conversation UUIDs to delete")

    # route
    p = sub.add_parser("route", help="Select CLI or direct-browser route")
    p.add_argument("request", help="Original user wording, not a search query")
    p.add_argument("-f", "--format", default="json", choices=["json", "text"])

    # console
    p = sub.add_parser("console", help="Resident Perplexity console (fixed tab/group)")
    csub = p.add_subparsers(dest="console_action")
    pc = csub.add_parser("ask", help="Ask the console; creates or continues a task thread")
    pc.add_argument("query")
    pc.add_argument("--model", "-m", help="Switch model before asking (e.g. \"Grok 4.6\")")
    pc.add_argument("--task", default="default", help="Task name; one task = one thread")
    pc.add_argument("--new-thread", action="store_true",
                    help="Start a new Perplexity thread in the same tab")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc.add_argument("--wait", dest="wait_budget", type=float, default=120.0,
                    help="Completion budget in seconds")
    pc.add_argument("--file", action="append", metavar="PATH",
                    help="Attach a local file to the message (repeatable; <=8MB)")
    pc.add_argument("--judge", dest="judge", action="store_true", default=None,
                    help="Ask Jev to judge the extracted answer (advisory; env PERPLEXITY_CONSOLE_JUDGE=1)")
    pc.add_argument("--no-judge", dest="judge", action="store_false",
                    help="Disable the Jev judge for this call")
    pc = csub.add_parser("status", help="Show console state and live tab readback")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("threads", help="List known task threads")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("selfcheck", help="Run the full gate pipeline on a canned query")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc.add_argument("--wait", dest="wait_budget", type=float, default=120.0)
    pc.add_argument("--drift", action="store_true",
                    help="Read-only probe drift report instead of the canned run")
    pc = csub.add_parser("drift",
                         help="Read-only probe drift report (12 probes; never clicks or types)")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("models", help="List selectable Perplexity models")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("model", help="Switch the composer model (verified readback)")
    pc.add_argument("name")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("open", help="Attach the console tab to a task thread or URL")
    pc.add_argument("target", help="Task name, or an https URL")
    pc.add_argument("--new-thread", action="store_true",
                    help="Start a fresh thread for the task")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("fill", help="Stage a turn: attach files + fill the composer (no send)")
    pc.add_argument("query")
    pc.add_argument("--task", default="default")
    pc.add_argument("--new-thread", action="store_true")
    pc.add_argument("--file", action="append", metavar="PATH")
    pc.add_argument("--judge", dest="judge", action="store_true", default=None,
                    help="Allow one bounded Jev-directed recovery on failure (advisory decision, code executes)")
    pc.add_argument("--no-judge", dest="judge", action="store_false",
                    help="Disable the Jev judge for this call")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("submit", help="Submit the staged turn (verified)")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc.add_argument("--submit-timeout", dest="submit_timeout", type=float, default=15.0)
    pc = csub.add_parser("wait", help="Wait for the staged turn's answer to settle")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc.add_argument("--wait", dest="wait_budget", type=float, default=120.0)
    pc.add_argument("--judge", dest="judge", action="store_true", default=None,
                    help="Allow one bounded Jev-directed recovery on failure (advisory decision, code executes)")
    pc.add_argument("--no-judge", dest="judge", action="store_false",
                    help="Disable the Jev judge for this call")
    pc = csub.add_parser("extract", help="Extract the newest answer; consumes the staged turn")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc.add_argument("--judge", dest="judge", action="store_true", default=None,
                    help="Ask Jev to judge the extracted answer (advisory)")
    pc.add_argument("--no-judge", dest="judge", action="store_false",
                    help="Disable the Jev judge for this call")
    pc.add_argument("--strict", action="store_true",
                    help="Fail with extract.truncation-risk when the answer "
                         "looks truncated (advisory flag by default)")
    pc.add_argument("--peek", action="store_true",
                    help="Read the staged turn WITHOUT consuming it "
                         "(read-only re-read; no disk write, no turn count)")
    pc.add_argument("--again", action="store_true",
                    help="Re-read the newest answer without a staged turn "
                         "(read-only; mutually exclusive with --peek)")
    pc = csub.add_parser("send", help="Stage + submit in one call (fill + submit)")
    pc.add_argument("query")
    pc.add_argument("--task", default="default")
    pc.add_argument("--new-thread", action="store_true")
    pc.add_argument("--file", action="append", metavar="PATH")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("attach", help="Attach local files to the composer (verified chips)")
    pc.add_argument("--file", action="append", metavar="PATH", required=True)
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("files", help="List composer attachments and the staged file set")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])
    pc = csub.add_parser("detach", help="Remove one composer attachment by name")
    pc.add_argument("name")
    pc.add_argument("-f", "--format", default="text", choices=["text", "json"])

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    # Apply global config overrides
    cfg_overrides = {}
    if args.wait is not None:
        cfg_overrides["search_wait"] = args.wait
    if args.retries is not None:
        cfg_overrides["max_retries"] = args.retries
    if args.backend:
        cfg_overrides["driver_backend"] = args.backend
    if args.session_prefix:
        cfg_overrides["session_prefix"] = args.session_prefix
    if cfg_overrides:
        set_config(**cfg_overrides)

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(name)s %(levelname)s: %(message)s")

    if args.command == "route":
        return cmd_route(args)
    elif args.command == "console":
        return cmd_console(args)
    elif args.command == "search":
        return cmd_search(args)
    elif args.command == "batch":
        cmd_batch(args)
    elif args.command == "aggregate":
        cmd_aggregate(args)
    elif args.command == "history":
        cmd_history(args)
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
