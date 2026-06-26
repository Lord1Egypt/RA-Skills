#!/usr/bin/env python3
"""Safety wrapper for Meta's official Ads CLI.

This wrapper does not implement the Meta Marketing API. It helps agents run
`meta ads ...` commands safely: JSON-first output, risk classification, specific
approval for writes, stronger gates for budget/activation/destructive actions,
no token arguments, and no persistent logging unless explicitly enabled.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

PINNED_META_ADS_VERSION = "1.0.1"
EXIT_BAD_ARGS = 2
EXIT_API = 4
EXIT_SAFETY = 6
EXIT_CLI_MISSING = 7
EXIT_PLAN = 8
EXIT_TIMEOUT = 9

READ_ACTIONS = {"list", "get", "show", "status", "inspect", "preview", "previews", "help", "search", "find", "info", "describe", "export", "current"}
WRITE_ACTIONS = {"create", "update", "delete", "remove", "connect", "disconnect", "upload", "pause", "activate", "archive", "set", "assign", "assign-user", "unassign", "import", "unshare"}
BUDGET_TOKENS = {"--daily-budget", "--lifetime-budget", "--budget", "--bid-amount", "--bid", "--spend-cap", "daily_budget", "lifetime_budget", "budget", "bid_amount", "spend_cap"}
DESTRUCTIVE_ACTIONS = {"delete", "remove", "unshare"}
SECRET_FLAGS = {"--access-token", "--token", "--app-secret", "--secret", "--password", "--cookie"}
SENSITIVE_ENV_MARKERS = ("TOKEN", "SECRET", "PASSWORD", "COOKIE", "APP_SECRET")
GENERIC_APPROVALS = {"yes", "y", "ok", "okay", "approved", "approve", "go", "go ahead", "do it", "confirmed", "confirm", "run it", "proceed"}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def emit(payload: Dict[str, Any], code: int = 0) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    return code


def known_secret_values() -> List[str]:
    out: List[str] = []
    for key, value in os.environ.items():
        if value and len(value) >= 8 and any(marker in key.upper() for marker in SENSITIVE_ENV_MARKERS):
            out.append(value)
    return out


def redact_text(text: str) -> str:
    if not text:
        return text
    safe = text
    for secret in known_secret_values():
        safe = safe.replace(secret, "<REDACTED>")
    return re.sub(r"(?i)(access[-_]?token|app[-_]?secret|secret|password|cookie)\s*[:=]\s*([^\s,'\"}]+)", r"\1=<REDACTED>", safe)


def redact_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: ("<REDACTED>" if any(m in str(k).upper() for m in SENSITIVE_ENV_MARKERS) and v else redact_payload(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_payload(x) for x in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def command_secret_flags(cmd: Sequence[str]) -> List[str]:
    hits: List[str] = []
    for token in cmd:
        low = token.lower()
        for flag in SECRET_FLAGS:
            if low == flag or low.startswith(flag + "="):
                hits.append(flag)
    return sorted(set(hits))


def redact_command(cmd: Sequence[str]) -> List[str]:
    out: List[str] = []
    redact_next = False
    for token in cmd:
        if redact_next:
            out.append("<REDACTED>")
            redact_next = False
            continue
        low = token.lower()
        if low in SECRET_FLAGS:
            out.append(token)
            redact_next = True
        elif any(low.startswith(flag + "=") for flag in SECRET_FLAGS):
            out.append(token.split("=", 1)[0] + "=<REDACTED>")
        else:
            safe = token
            for secret in known_secret_values():
                if safe == secret:
                    safe = "<REDACTED>"
            out.append(safe)
    return out


def scrub_env() -> Dict[str, str]:
    keys = {"ACCESS_TOKEN", "AD_ACCOUNT_ID", "BUSINESS_ID", "META_ADS_AGENT_LOG"}
    result: Dict[str, str] = {}
    for key, value in os.environ.items():
        if key in keys or any(marker in key.upper() for marker in SENSITIVE_ENV_MARKERS):
            result[key] = "<SET>" if value else "<EMPTY>"
    return result


def split_command(raw: str) -> List[str]:
    return shlex.split(raw)


def command_from_any(value: Any) -> List[str]:
    if isinstance(value, list) and all(isinstance(x, str) for x in value):
        return list(value)
    if isinstance(value, str):
        return split_command(value)
    raise ValueError("Command must be a string or an array of strings")


def strip_remainder_dash(cmd: Sequence[str]) -> List[str]:
    cmd = list(cmd)
    return cmd[1:] if cmd and cmd[0] == "--" else cmd


def has_output_flag(cmd: Sequence[str]) -> bool:
    return "--output" in cmd or "-o" in cmd or any(x.startswith("--output=") for x in cmd)


def normalise_meta_command(cmd: Sequence[str], prefer_json: bool = True) -> List[str]:
    cmd = list(cmd)
    if not cmd:
        raise ValueError("Empty command")
    if cmd[0] != "meta":
        return cmd
    lowered = [x.lower() for x in cmd]
    if "--help" in lowered or "-h" in lowered or "help" in lowered:
        return cmd
    if prefer_json and "ads" in cmd and not has_output_flag(cmd):
        return [*cmd, "--output", "json"]
    return cmd


def find_resource_action(cmd: Sequence[str]) -> Tuple[Optional[str], Optional[str]]:
    if "ads" not in cmd:
        return None, None
    i = list(cmd).index("ads") + 1
    positional: List[str] = []
    flags_with_values = {"--ad-account-id", "--business-id", "--output", "-o", "--limit", "--date-preset", "--fields", "--campaign-id", "--campaign_id", "--adset-id", "--adset_id", "--ad-id", "--ad_id"}
    while i < len(cmd):
        token = cmd[i]
        if token.startswith("-"):
            flag = token.lower().split("=", 1)[0]
            i += 2 if "=" not in token and flag in flags_with_values and i + 1 < len(cmd) else 1
            continue
        positional.append(token)
        if len(positional) == 2:
            break
        i += 1
    return (positional[0] if positional else None, positional[1] if len(positional) > 1 else None)


def classify(cmd: Sequence[str]) -> Dict[str, Any]:
    cmd = list(cmd)
    lowered = [x.lower() for x in cmd]
    resource, action = find_resource_action(cmd)
    action_l = (action or "").lower()
    is_help = any(x in {"--help", "-h", "help"} for x in lowered)
    is_meta_ads = bool(cmd and cmd[0] == "meta" and "ads" in cmd)
    is_meta_diag = bool(cmd and cmd[0] == "meta" and (is_help or lowered in (["meta", "auth", "status"], ["meta", "auth", "--help"], ["meta", "--help"]) or (len(lowered) >= 2 and lowered[1] == "auth")))

    write_signals: List[str] = []
    high_risk: List[str] = []
    if action_l in WRITE_ACTIONS:
        write_signals.append(f"action:{action_l}")
    if action_l in DESTRUCTIVE_ACTIONS:
        high_risk.append("destructive")
    if action_l == "activate":
        high_risk.append("active")

    for idx, token in enumerate(cmd):
        low = token.lower()
        if low in BUDGET_TOKENS or any(low.startswith(b + "=") for b in BUDGET_TOKENS):
            write_signals.append(f"budget-token:{token}")
            high_risk.append("budget")
        if low == "--status" and idx + 1 < len(cmd):
            write_signals.append("status-update")
            if cmd[idx + 1].upper() == "ACTIVE":
                high_risk.append("active")
        if low.startswith("--status="):
            write_signals.append("status-update")
            if low.split("=", 1)[1].upper() == "ACTIVE":
                high_risk.append("active")
        if low == "--force":
            high_risk.append("destructive")
        if low in {"--targeting", "--targeting-countries", "--special-ad-category", "--special-ad-categories"}:
            write_signals.append(f"targeting-token:{token}")
        if low in {"--image", "--video", "--catalog-id", "--dataset-id", "--pixel-id", "--page-id"}:
            write_signals.append(f"asset-or-tracking-token:{token}")

    if not is_meta_ads and not is_meta_diag:
        risk = "non_meta"
    elif is_help or is_meta_diag:
        risk = "read"
    elif write_signals:
        risk = "write"
    elif action_l in READ_ACTIONS or action_l == "":
        risk = "read"
    else:
        risk = "unknown"

    high_risk = sorted(set(high_risk))
    return {
        "command": redact_command(cmd),
        "is_meta_ads": is_meta_ads,
        "resource": resource,
        "action": action,
        "risk": risk,
        "write_signals": sorted(set(write_signals)),
        "high_risk": high_risk,
        "secret_arg_signals": command_secret_flags(cmd),
        "requires_approval": risk in {"write", "unknown"},
        "requires_allow_active": "active" in high_risk,
        "requires_allow_budget": "budget" in high_risk,
        "requires_allow_destructive": "destructive" in high_risk,
    }


def approval_is_specific(text: Optional[str]) -> bool:
    if not text:
        return False
    compact = " ".join(text.strip().split())
    return len(compact) >= 25 and compact.lower() not in GENERIC_APPROVALS


def safety_problem(cls: Dict[str, Any], approved: Optional[str], allow_active: bool, allow_budget: bool, allow_destructive: bool, allow_unknown: bool) -> Optional[str]:
    if cls.get("secret_arg_signals"):
        return "Do not pass access tokens or secrets as CLI arguments. Put credentials in environment variables or official auth storage."
    if cls["risk"] == "non_meta":
        return "Refusing to run non-`meta ads` command through this guard."
    if cls["risk"] == "unknown" and not allow_unknown:
        return "Unknown CLI action. Check `meta ads <resource> <action> --help`; use --allow-unknown only after review."
    if cls["requires_approval"] and not approval_is_specific(approved):
        return "Write or unknown-risk command requires --approved with specific user approval, not a generic yes/ok."
    if cls["requires_allow_active"] and not allow_active:
        return "Activation requires --allow-active plus specific approval."
    if cls["requires_allow_budget"] and not allow_budget:
        return "Budget/bid/spend change requires --allow-budget plus specific approval."
    if cls["requires_allow_destructive"] and not allow_destructive:
        return "Destructive command requires --allow-destructive plus specific approval."
    return None


def parse_stdout(stdout: str) -> Tuple[Any, str]:
    text = stdout.strip()
    if not text:
        return None, "empty"
    try:
        return redact_payload(json.loads(text)), "json"
    except json.JSONDecodeError:
        return redact_text(text), "text"


def log_path(args: argparse.Namespace) -> Optional[Path]:
    value = getattr(args, "log_file", None) or os.getenv("META_ADS_AGENT_LOG")
    if not value or value.lower() in {"off", "none", "false", "0"}:
        return None
    return Path(value)


def append_log(record: Dict[str, Any], path: Optional[Path]) -> None:
    if path is None:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(path.read_text(encoding="utf-8") + json.dumps(redact_payload(record), sort_keys=True, ensure_ascii=False) + "\n" if path.exists() else json.dumps(redact_payload(record), sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception:
        pass


def run_subprocess(cmd: Sequence[str], timeout: int) -> Dict[str, Any]:
    started = time.time()
    try:
        proc = subprocess.run(list(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout, check=False)
        parsed, stdout_type = parse_stdout(proc.stdout)
        return {"exit_code": proc.returncode, "stdout_type": stdout_type, "stdout": parsed, "stderr": redact_text(proc.stderr.strip()), "duration_seconds": round(time.time() - started, 3)}
    except subprocess.TimeoutExpired as exc:
        return {"exit_code": EXIT_TIMEOUT, "stdout_type": "timeout", "stdout": redact_text(exc.stdout or ""), "stderr": redact_text(exc.stderr or f"Timed out after {timeout} seconds"), "duration_seconds": round(time.time() - started, 3)}
    except FileNotFoundError:
        return {"exit_code": EXIT_CLI_MISSING, "stdout_type": "missing_cli", "stdout": None, "stderr": "`meta` executable was not found on PATH.", "duration_seconds": round(time.time() - started, 3)}


def cmd_doctor(args: argparse.Namespace) -> int:
    meta_path = shutil.which("meta")
    payload: Dict[str, Any] = {"ok": bool(meta_path), "meta_path": meta_path, "checked_at": now_iso(), "expected_cli_package": f"meta-ads=={PINNED_META_ADS_VERSION}", "sensitive_env_presence": scrub_env(), "persistent_log_enabled": bool(os.getenv("META_ADS_AGENT_LOG")), "next_steps": []}
    if not meta_path:
        payload["next_steps"].append("Install the pinned CLI: python3.12 -m pip install -r requirements-meta-ads-cli.txt")
        return emit(payload, EXIT_CLI_MISSING)
    for label, command in [("meta_help", ["meta", "--help"]), ("ads_help", ["meta", "ads", "--help"]), ("auth_status", ["meta", "auth", "status"])] :
        result = run_subprocess(command, args.timeout)
        payload[label] = {"command": command, "exit_code": result["exit_code"], "stdout_type": result["stdout_type"], "stdout_preview": str(result["stdout"])[:800] if result["stdout"] is not None else None, "stderr_preview": str(result["stderr"])[:800] if result["stderr"] else ""}
    if payload.get("auth_status", {}).get("exit_code") not in (0, None):
        payload["next_steps"].append("Resolve auth before writes. Check ACCESS_TOKEN, AD_ACCOUNT_ID, token permissions, and official setup docs.")
    return emit(payload)


def cmd_classify(args: argparse.Namespace) -> int:
    raw = strip_remainder_dash(args.command)
    if not raw:
        return emit({"ok": False, "error": "No command supplied after --"}, EXIT_BAD_ARGS)
    command = normalise_meta_command(raw, prefer_json=not args.no_json)
    payload = classify(command)
    payload["ok"] = True
    payload["normalised_command"] = redact_command(command)
    return emit(payload)


def cmd_run(args: argparse.Namespace) -> int:
    raw = strip_remainder_dash(args.command)
    if not raw:
        return emit({"ok": False, "error": "No command supplied after --"}, EXIT_BAD_ARGS)
    command = normalise_meta_command(raw, prefer_json=not args.no_json)
    cls = classify(command)
    approved = args.approved or os.getenv("META_ADS_AGENT_APPROVED")
    problem = safety_problem(cls, approved, args.allow_active, args.allow_budget, args.allow_destructive, args.allow_unknown)
    if problem:
        return emit({"ok": False, "error": problem, "classification": cls, "would_run": redact_command(command)}, EXIT_SAFETY)
    result = run_subprocess(command, args.timeout)
    lp = log_path(args)
    payload = {"ok": result["exit_code"] == 0, "ran_at": now_iso(), "command": redact_command(command), "classification": cls, "result": result, "log_file": str(lp) if lp else None}
    append_log({"ran_at": payload["ran_at"], "command": payload["command"], "classification": cls, "exit_code": result["exit_code"], "duration_seconds": result["duration_seconds"], "approved": approval_is_specific(approved)}, lp)
    if args.output_file:
        out = Path(args.output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(redact_payload(payload), indent=2, ensure_ascii=False), encoding="utf-8")
        payload["saved_to"] = str(out)
    return emit(redact_payload(payload), result["exit_code"] if result["exit_code"] else 0)


def load_plan(path: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("commands"), list):
        raise ValueError("Plan must be a JSON object with a commands array")
    return data


def lint_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    commands: List[Dict[str, Any]] = []
    write_steps = 0
    high_risk: List[str] = []
    for idx, step in enumerate(plan.get("commands", [])):
        if not isinstance(step, dict):
            issues.append({"step": idx, "severity": "error", "message": "Each step must be an object"})
            continue
        try:
            command = normalise_meta_command(command_from_any(step.get("command")), prefer_json=step.get("prefer_json", True))
            cls = classify(command)
        except Exception as exc:
            issues.append({"step": idx, "severity": "error", "message": str(exc)})
            continue
        if cls["risk"] in {"write", "unknown"}:
            write_steps += 1
        high_risk += cls.get("high_risk", [])
        commands.append({"step": idx, "id": step.get("id", f"step-{idx}"), "intent": step.get("intent"), "command": redact_command(command), "classification": cls})
        if cls["risk"] == "non_meta":
            issues.append({"step": idx, "severity": "error", "message": "Non-meta command in plan"})
        if cls.get("secret_arg_signals"):
            issues.append({"step": idx, "severity": "error", "message": "Secret/token argument in plan"})
        if cls["risk"] == "unknown" and not step.get("allow_unknown"):
            issues.append({"step": idx, "severity": "warning", "message": "Unknown action; verify with CLI help"})
        if cls["requires_allow_active"] and not (plan.get("allow_active") or step.get("allow_active")):
            issues.append({"step": idx, "severity": "error", "message": "Activation step needs allow_active"})
        if cls["requires_allow_budget"] and not (plan.get("allow_budget") or step.get("allow_budget")):
            issues.append({"step": idx, "severity": "error", "message": "Budget/bid step needs allow_budget"})
        if cls["requires_allow_destructive"] and not (plan.get("allow_destructive") or step.get("allow_destructive")):
            issues.append({"step": idx, "severity": "error", "message": "Destructive step needs allow_destructive"})
    if write_steps > 1 and not plan.get("allow_multi_write", False):
        issues.append({"step": None, "severity": "error", "message": "Plan has multiple write/unknown steps. Run one approved write step at a time."})
    if write_steps and not plan.get("requires_user_approval", True):
        issues.append({"step": None, "severity": "error", "message": "Write plan cannot disable user approval"})
    return {"ok": not any(i["severity"] == "error" for i in issues), "goal": plan.get("goal"), "risk_summary": {"write_or_unknown_steps": write_steps, "high_risk": sorted(set(high_risk))}, "issues": issues, "commands": commands}


def cmd_lint_plan(args: argparse.Namespace) -> int:
    try:
        result = lint_plan(load_plan(args.plan))
    except Exception as exc:
        return emit({"ok": False, "error": redact_text(str(exc))}, EXIT_PLAN)
    return emit(result, 0 if result["ok"] else EXIT_PLAN)


def cmd_run_plan(args: argparse.Namespace) -> int:
    try:
        plan = load_plan(args.plan)
        lint = lint_plan(plan)
    except Exception as exc:
        return emit({"ok": False, "error": redact_text(str(exc))}, EXIT_PLAN)
    if not lint["ok"]:
        return emit({"ok": False, "error": "Plan failed lint", "lint": lint}, EXIT_PLAN)
    write_steps = lint["risk_summary"]["write_or_unknown_steps"]
    if write_steps and not args.allow_write_plan:
        return emit({"ok": False, "error": "run-plan is read-only by default. For mutations, lint the plan, then run one approved write command at a time; use --allow-write-plan only in controlled automation.", "lint": lint}, EXIT_SAFETY)
    approved = args.approved or os.getenv("META_ADS_AGENT_APPROVED")
    if write_steps and not approval_is_specific(approved):
        return emit({"ok": False, "error": "Write plan requires specific --approved text", "lint": lint}, EXIT_SAFETY)
    results: List[Dict[str, Any]] = []
    overall_ok = True
    lp = log_path(args)
    for idx, step in enumerate(plan.get("commands", [])):
        command = normalise_meta_command(command_from_any(step["command"]), prefer_json=step.get("prefer_json", True))
        cls = classify(command)
        problem = safety_problem(cls, approved, args.allow_active or plan.get("allow_active", False) or step.get("allow_active", False), args.allow_budget or plan.get("allow_budget", False) or step.get("allow_budget", False), args.allow_destructive or plan.get("allow_destructive", False) or step.get("allow_destructive", False), args.allow_unknown or step.get("allow_unknown", False))
        if problem:
            overall_ok = False
            results.append({"step": idx, "id": step.get("id"), "ok": False, "error": problem, "classification": cls})
            if args.stop_on_error:
                break
            continue
        result = run_subprocess(command, args.timeout)
        ok = result["exit_code"] == 0
        overall_ok = overall_ok and ok
        item = {"step": idx, "id": step.get("id", f"step-{idx}"), "intent": step.get("intent"), "ok": ok, "command": redact_command(command), "classification": cls, "result": result}
        results.append(item)
        append_log({"ran_at": now_iso(), "plan": args.plan, "step": idx, "id": item["id"], "command": item["command"], "classification": cls, "exit_code": result["exit_code"], "duration_seconds": result["duration_seconds"], "approved": approval_is_specific(approved)}, lp)
        if args.stop_on_error and not ok:
            break
    payload = {"ok": overall_ok, "plan": args.plan, "lint": lint, "results": results, "log_file": str(lp) if lp else None}
    if args.output_file:
        out = Path(args.output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(redact_payload(payload), indent=2, ensure_ascii=False), encoding="utf-8")
        payload["saved_to"] = str(out)
    return emit(redact_payload(payload), 0 if overall_ok else EXIT_API)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe agent wrapper for Meta Ads CLI")
    sub = parser.add_subparsers(dest="command_name", required=True)
    p = sub.add_parser("doctor")
    p.add_argument("--timeout", type=int, default=20)
    p.set_defaults(func=cmd_doctor)
    p = sub.add_parser("classify")
    p.add_argument("--no-json", action="store_true")
    p.add_argument("command", nargs=argparse.REMAINDER)
    p.set_defaults(func=cmd_classify)
    p = sub.add_parser("run")
    p.add_argument("--approved")
    p.add_argument("--allow-active", action="store_true")
    p.add_argument("--allow-budget", action="store_true")
    p.add_argument("--allow-destructive", action="store_true")
    p.add_argument("--allow-unknown", action="store_true")
    p.add_argument("--no-json", action="store_true")
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--output-file")
    p.add_argument("--log-file", help="Optional redacted JSONL log path. Default: disabled unless META_ADS_AGENT_LOG is set.")
    p.add_argument("command", nargs=argparse.REMAINDER)
    p.set_defaults(func=cmd_run)
    p = sub.add_parser("lint-plan")
    p.add_argument("plan")
    p.set_defaults(func=cmd_lint_plan)
    p = sub.add_parser("run-plan")
    p.add_argument("plan")
    p.add_argument("--approved")
    p.add_argument("--allow-write-plan", action="store_true")
    p.add_argument("--allow-active", action="store_true")
    p.add_argument("--allow-budget", action="store_true")
    p.add_argument("--allow-destructive", action="store_true")
    p.add_argument("--allow-unknown", action="store_true")
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--output-file")
    p.add_argument("--log-file", help="Optional redacted JSONL log path. Default: disabled unless META_ADS_AGENT_LOG is set.")
    p.add_argument("--stop-on-error", action=argparse.BooleanOptionalAction, default=True)
    p.set_defaults(func=cmd_run_plan)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return emit({"ok": False, "error": "Interrupted"}, 130)
    except Exception as exc:
        return emit({"ok": False, "error": redact_text(str(exc))}, EXIT_BAD_ARGS)


if __name__ == "__main__":
    raise SystemExit(main())
