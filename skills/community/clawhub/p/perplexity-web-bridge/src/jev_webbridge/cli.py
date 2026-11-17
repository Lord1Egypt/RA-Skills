"""jevw CLI: `jevw run` — dry-run, session derivation, escalation bridge, exit codes.

Exit codes: 0 done/dry_run, 3 exhausted, 4 blocked, 2 usage (argparse), 1 unexpected
error (message on stderr). Final stdout of a real run is exactly ONE JSON line
{status, answer, cycles, turns, wall_ms, session}.

Escalation bridge (plan Task 7): payload JSON on stdin -> decision JSON on stdout is
the DEFAULT — the CLI prints the payload as one JSON line (request) and reads ONE
JSON line from stdin as the decision (the calling agent answers). `--escalate-cmd
CMD` runs `sh -c CMD` with the payload JSON on stdin and parses the command's stdout
as the decision; malformed output raises with context, never guesses a decision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections.abc import Callable

from .driver import WebBridgeDriver
from .loop import MAX_CYCLES
from .loop import run as run_loop
from .policy import JevClient
from .promptpack import enhance

DEFAULT_RECEIPTS = "~/.jev-webbridge/runs.jsonl"
EXIT_CODES = {"done": 0, "dry_run": 0, "exhausted": 3, "blocked": 4}


def derive_session(goal: str) -> str:
    """Stable prefixed session: "jev-" + sha1(goal)[:12]."""
    return "jev-" + hashlib.sha1(goal.encode("utf-8")).hexdigest()[:12]


def _parse_decision(raw: str, source: str) -> dict:
    try:
        decision = json.loads(raw)
    except ValueError as e:
        raise ValueError(f"{source}: malformed decision JSON ({e}): {raw.strip()[:200]!r}") from e
    if not isinstance(decision, dict):
        raise TypeError(f"{source}: decision must be a JSON object, got {type(decision).__name__}")
    return decision


def build_escalate_fn(cmd: str | None) -> Callable[[dict], dict]:
    """Build the escalation bridge: payload dict -> decision dict.

    cmd is None (default): print the payload as ONE JSON line on stdout (the
    request), then read ONE JSON line from stdin and parse it as the decision.
    cmd is set: run `sh -c CMD` with the payload JSON on stdin, parse the
    command's stdout as the decision; malformed/missing output raises with
    context (exit code + stderr) — a decision is never guessed.
    """
    if cmd is None:

        def _interactive(payload: dict) -> dict:
            print(json.dumps(payload, ensure_ascii=False), flush=True)
            line = sys.stdin.readline()
            if not line.strip():
                raise ValueError("escalation bridge: no decision JSON on stdin (EOF)")
            return _parse_decision(line, "escalation bridge (stdin)")

        return _interactive

    def _subprocess(payload: dict) -> dict:
        proc = subprocess.run(
            ["sh", "-c", cmd],
            input=json.dumps(payload, ensure_ascii=False),
            capture_output=True,
            text=True,
            check=False,
        )
        try:
            return _parse_decision(proc.stdout, f"escalate-cmd {cmd!r} (rc={proc.returncode})")
        except (ValueError, TypeError) as e:  # malformed decision gets cmd/rc/stderr context
            raise ValueError(f"{e}; stderr={proc.stderr.strip()[:300]!r}") from e

    return _subprocess


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jevw",
        description="Generic jev-ultrafast-style decision loop over kimi-webbridge.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run_p = sub.add_parser("run", help="run the observe/decide/act loop to a terminal status")
    run_p.add_argument("--goal", required=True, help="goal sentence for the decision head")
    run_p.add_argument("--site", required=True, help="site name selecting the settle predicate")
    run_p.add_argument("--max-cycles", type=int, default=MAX_CYCLES, help="cycle cap (default 20)")
    run_p.add_argument("--escalate-cmd", default=None,
                       help="shell command bridging payload JSON (stdin) -> decision JSON (stdout)")
    run_p.add_argument("--session", default=None, help="webbridge session name (default: derived)")
    run_p.add_argument("--url", default=None,
                       help="start URL for the run (required unless --dry-run; "
                            "the CLI never hardcodes site URLs)")
    run_p.add_argument("--text", default=None,
                       help="text to TYPE_TEXT (default: the recipe-enhanced goal)")
    run_p.add_argument("--recipe", default="default",
                       choices=["default", "finance", "tech", "research"],
                       help="prompt-quality recipe layered onto the goal (v1.1)")
    run_p.add_argument("--receipts", default=DEFAULT_RECEIPTS, help="JSONL receipt file path")
    run_p.add_argument("--dry-run", action="store_true",
                       help="print session/goal/site as one JSON line; no driver, no daemon")
    return parser


def resolve_text(goal: str, text: str | None, recipe: str) -> str:
    """v1.1 prompt-quality seam: explicit ``--text`` wins; else the goal wrapped
    by the recipe's community-validated answer rules (goal stays verbatim)."""
    if text is not None:
        return text
    return enhance(goal, recipe)


def _cmd_run(args: argparse.Namespace) -> int:
    session = args.session or derive_session(args.goal)
    if not args.dry_run and not args.url:
        print("jevw run: --url is required unless --dry-run", file=sys.stderr)
        return 2
    if args.dry_run:
        print(json.dumps(
            {"status": "dry_run", "session": session, "goal": args.goal, "site": args.site},
            ensure_ascii=False,
        ))
        return 0
    try:
        driver = WebBridgeDriver(session=session)
        driver.call("navigate", url=args.url)  # open/reuse this session's tab on the target
        client = JevClient()  # reads TYPESAFE_API_KEY via vendored _api_key at call time
        result = run_loop(
            driver,
            goal=args.goal,
            site=args.site,
            client=client,
            escalate_fn=build_escalate_fn(args.escalate_cmd),
            max_cycles=args.max_cycles,
            receipt_path=args.receipts,
            text=resolve_text(args.goal, args.text, args.recipe),  # v1.1: --text wins else recipe-enhanced goal
            wait_free=True,  # v2: WAIT never exhausts the cycle budget (wall cap bounds runaway)
            stuck_escalates=True,  # spec §4.3 stuck trigger (loop default False is the test seam)
        )
    except Exception as e:  # noqa: BLE001 — CLI top level: report the error, exit 1, never traceback
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(json.dumps(
        {
            "status": result["status"],
            "answer": result["answer"],
            "cycles": result["cycles"],
            "turns": result["turns"],
            "wall_ms": result["wall_ms"],
            "session": session,
        },
        ensure_ascii=False,
    ))
    return EXIT_CODES.get(result["status"], 1)


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    return _cmd_run(args)
