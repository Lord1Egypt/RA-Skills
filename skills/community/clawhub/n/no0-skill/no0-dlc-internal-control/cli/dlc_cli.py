#!/usr/bin/env python3
"""No.0-DLC-Internal Control — unified CLI entrypoint.

Dispatched from top-level ./no0 for subcommands: classify, audit, auth, init.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

DLC_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DLC_ROOT))

from i18n import t  # noqa: E402


DLC_RUNTIME_DIR = Path(os.path.expanduser("~/.openclaw/no0/dlc"))
AUDIT_LOG_PATH = DLC_RUNTIME_DIR / "audit.csv"
PENDING_DECISIONS_DIR = DLC_RUNTIME_DIR / "pending_decisions"
PUSH_FAILURES_LOG = DLC_RUNTIME_DIR / "push_failures.log"


def _lazy_classify():
    try:
        from internal_control import classify_cli
        return classify_cli
    except ModuleNotFoundError as e:
        print(f"[dlc] classify requires DLC dependencies (missing: {e.name}).", file=sys.stderr)
        print(f"      Install: pip install -r {DLC_ROOT / 'requirements.txt'}", file=sys.stderr)
        sys.exit(2)


def _make_classify_dispatcher(name: str):
    def _run(args):
        mod = _lazy_classify()
        return getattr(mod, name)(args)
    return _run


def _build_classify_subparser(parent: argparse._SubParsersAction) -> None:
    classify = parent.add_parser("classify", help="Data classification operations")
    sub = classify.add_subparsers(dest="classify_cmd")

    p_get = sub.add_parser("get", help="Classify a single path")
    p_get.add_argument("path")
    p_get.set_defaults(func=_make_classify_dispatcher("cmd_get"))

    p_dir = sub.add_parser("dir", help="Classify a directory")
    p_dir.add_argument("directory")
    p_dir.add_argument("-r", "--recursive", action="store_true")
    p_dir.add_argument("-d", "--max-depth", type=int, default=10)
    p_dir.add_argument("-v", "--verbose", action="store_true")
    p_dir.set_defaults(func=_make_classify_dispatcher("cmd_dir"))

    p_stats = sub.add_parser("stats", help="Rule and classification statistics")
    p_stats.set_defaults(func=_make_classify_dispatcher("cmd_stats"))

    p_excl = sub.add_parser("exclusions", help="Exclusion rule management")
    p_excl.add_argument("-l", "--list", action="store_true")
    p_excl.add_argument("-c", "--check", metavar="PATH")
    p_excl.set_defaults(func=_make_classify_dispatcher("cmd_exclusions"))

    p_reload = sub.add_parser("reload", help="Reload classification rules")
    p_reload.set_defaults(func=_make_classify_dispatcher("cmd_reload"))


def _cmd_audit_log(args) -> int:
    if not AUDIT_LOG_PATH.exists():
        print(f"[dlc] No audit log yet at {AUDIT_LOG_PATH}")
        return 0
    try:
        lines = AUDIT_LOG_PATH.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        print(f"[dlc] Failed to read audit log: {e}", file=sys.stderr)
        return 1
    tail = lines[-args.last:] if args.last and args.last > 0 else lines
    for line in tail:
        print(line)
    return 0


def _cmd_auth_pending(args) -> int:
    print("[dlc] TODO: wire 'auth pending' to internal_control.http_auth.request_store")
    print(f"      (Spec §3.2 — list pending authorization requests)")
    return 0


def _push_failures_for(basename: str) -> list:
    if not PUSH_FAILURES_LOG.exists():
        return []
    out: list = []
    for line in PUSH_FAILURES_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except Exception:
            continue
        if row.get("target_file") == basename:
            out.append(row)
    return out


def _locate_no0_dispatcher() -> Optional[Path]:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidate = parent.parent / "no0"
        if candidate.exists() and os.access(candidate, os.X_OK):
            return candidate
    return None


def _cmd_decide(args) -> int:
    file_arg = args.file
    basename = Path(file_arg).name
    lock = PENDING_DECISIONS_DIR / f"{basename}.lock"

    if args.action == "status":
        if not lock.exists():
            print(t("decide.no_pending", name=basename))
            return 0
        print(lock.read_text(encoding="utf-8"))
        failures = _push_failures_for(basename)
        if failures:
            print(t("decide.prior_failures", name=basename, n=len(failures)))
            for row in failures:
                reason = row.get("last_reason") or row.get("reason")
                retries = row.get("retry_count", 0)
                print(t("decide.prior_failure_row",
                        reason=reason, retries=retries, ts=row.get("recorded_at")))
        return 0

    if not lock.exists():
        print(t("decide.no_pending_at", name=basename, lock=lock), file=sys.stderr)
        return 1

    if args.action == "rollback":
        if not args.version:
            print(t("decide.rollback_needs_version"), file=sys.stderr)
            return 2
        no0_bin = _locate_no0_dispatcher()
        if no0_bin is None:
            print(t("decide.no_dispatcher"), file=sys.stderr)
            return 3
        result = subprocess.run(
            [str(no0_bin), "rollback", basename, args.version],
            capture_output=True,
            text=True,
        )
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        if result.returncode != 0:
            print(t("decide.rollback_failed", rc=result.returncode), file=sys.stderr)
            versions_result = subprocess.run(
                [str(no0_bin), "versions", basename],
                capture_output=True, text=True,
            )
            if versions_result.returncode == 0 and versions_result.stdout.strip():
                print(t("decide.available_versions"), file=sys.stderr)
                for line in versions_result.stdout.splitlines():
                    print(f"    {line}", file=sys.stderr)
                print(t("decide.retry_hint", name=basename), file=sys.stderr)
            return result.returncode
        lock.unlink()
        print(t("decide.rolled_back", name=basename, version=args.version))
        return 0

    if args.action == "keep":
        lock.unlink()
        print(t("decide.kept", name=basename))
        return 0

    print(t("decide.unknown_action", action=args.action), file=sys.stderr)
    return 2


def _build_decide_subparser(parent: argparse._SubParsersAction) -> None:
    p = parent.add_parser(
        "decide",
        help="Resolve a pending L5 decision (rollback / keep / status)",
    )
    p.add_argument("file", help="Target file basename (e.g. SOUL.md)")
    p.add_argument("action", choices=["rollback", "keep", "status"])
    p.add_argument("version", nargs="?", help="Version for rollback (e.g. v3)")
    p.set_defaults(func=_cmd_decide)


def _cmd_init(args) -> int:
    DLC_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[dlc] Initialized runtime dir: {DLC_RUNTIME_DIR}")
    print("[dlc] TODO: wire TOTP Vault master-key init + classification.db + http_auth.db")
    return 0


def _build_audit_subparser(parent: argparse._SubParsersAction) -> None:
    audit = parent.add_parser("audit", help="Audit log operations")
    sub = audit.add_subparsers(dest="audit_cmd")

    p_log = sub.add_parser("log", help="Show audit log entries")
    p_log.add_argument("--last", type=int, default=0, help="Show last N entries")
    p_log.set_defaults(func=_cmd_audit_log)


def _build_auth_subparser(parent: argparse._SubParsersAction) -> None:
    auth = parent.add_parser("auth", help="Authorization management")
    sub = auth.add_subparsers(dest="auth_cmd")

    p_pending = sub.add_parser("pending", help="List pending authorization requests")
    p_pending.set_defaults(func=_cmd_auth_pending)


def _build_init_subparser(parent: argparse._SubParsersAction) -> None:
    p_init = parent.add_parser("init", help="Initialize DLC runtime state")
    p_init.set_defaults(func=_cmd_init)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="no0 (dlc)",
        description="No.0-DLC-Internal Control CLI",
    )
    subparsers = parser.add_subparsers(dest="command")
    _build_classify_subparser(subparsers)
    _build_audit_subparser(subparsers)
    _build_auth_subparser(subparsers)
    _build_init_subparser(subparsers)
    _build_decide_subparser(subparsers)

    args = parser.parse_args(argv)

    if not getattr(args, "command", None):
        parser.print_help()
        return 1

    func = getattr(args, "func", None)
    if func is None:
        parser.parse_args([args.command, "--help"])
        return 1

    result = func(args)
    return int(result) if isinstance(result, int) else 0


if __name__ == "__main__":
    sys.exit(main())
