#!/usr/bin/env python3
"""Environment and config doctor for OpenClaw autopilot."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
from urllib import error as urlerror
from urllib import request as urlrequest


@dataclass
class CheckItem:
    name: str
    ok: bool
    detail: str
    level: str = "info"


def run_cmd(cmd: List[str], timeout: int = 15) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return p.returncode, (p.stdout or "").strip()
    except subprocess.TimeoutExpired:
        return 124, f"timeout after {timeout}s"


def first_meaningful_line(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        lower = s.lower()
        if "deprecationwarning" in lower:
            continue
        if "trace-deprecation" in lower:
            continue
        if lower.startswith("(node:"):
            continue
        return s
    return text.splitlines()[0].strip() if text.splitlines() else ""


def load_config(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_config_keys(cfg: Dict[str, Any]) -> List[CheckItem]:
    required = ["repo_url", "branch", "cli_tools", "timeouts", "report_min_pass_rate"]
    out: List[CheckItem] = []
    for key in required:
        ok = key in cfg
        out.append(CheckItem(name=f"config.key.{key}", ok=ok, detail="present" if ok else "missing", level="error"))
    cli_tools = cfg.get("cli_tools", [])
    out.append(
        CheckItem(
            name="config.cli_tools.type",
            ok=isinstance(cli_tools, list),
            detail=f"type={type(cli_tools).__name__}",
            level="error",
        )
    )
    repo_url = str(cfg.get("repo_url", "")).strip()
    repo_ok = repo_url.startswith("https://github.com/") and ("<" not in repo_url) and (">" not in repo_url)
    out.append(
        CheckItem(
            name="config.repo_url.valid",
            ok=repo_ok,
            detail=repo_url if repo_url else "empty",
            level="error",
        )
    )
    return out


def check_cli_binaries(cfg: Dict[str, Any]) -> List[CheckItem]:
    out: List[CheckItem] = []
    cli_tools = cfg.get("cli_tools", [])
    if not isinstance(cli_tools, list):
        return [CheckItem(name="cli_tools.invalid", ok=False, detail="cli_tools is not list", level="error")]

    for item in cli_tools:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "Unnamed CLI"))
        cmd = str(item.get("command", "")).strip()
        enabled = bool(item.get("enabled", True))
        try:
            parts = shlex.split(cmd)
        except ValueError:
            parts = []
        binary = parts[0] if parts else ""
        exists = bool(binary) and (shutil.which(binary) is not None)
        lvl = "error" if enabled else "warning"
        out.append(
            CheckItem(
                name=f"cli.binary.{name}",
                ok=(exists or not enabled),
                detail=f"enabled={enabled}, binary={binary or 'N/A'}, found={exists}",
                level=lvl,
            )
        )

        if exists:
            code, version_out = run_cmd([binary, "--version"], timeout=10)
            first = first_meaningful_line(version_out)[:200] if version_out else ""
            out.append(
                CheckItem(
                    name=f"cli.version.{name}",
                    ok=(code == 0),
                    detail=(first if first else f"exit={code}"),
                    level="warning",
                )
            )
    return out


def check_known_logins() -> List[CheckItem]:
    out: List[CheckItem] = []

    if shutil.which("codex"):
        # Override local config edge cases (for example invalid model_reasoning_effort)
        # so login checks do not produce false warnings.
        code, text = run_cmd(["codex", "-c", "model_reasoning_effort=high", "login", "status"], timeout=10)
        ok = code == 0 and ("logged in" in text.lower())
        out.append(CheckItem(name="login.codex", ok=ok, detail=text[:200], level="warning"))

    if shutil.which("gemini"):
        code, text = run_cmd(["gemini", "--list-sessions"], timeout=20)
        ok = code == 0
        first = first_meaningful_line(text)[:200] if text else ""
        out.append(CheckItem(name="login.gemini", ok=ok, detail=first, level="warning"))

    return out


def check_github_token(token: str) -> CheckItem:
    req = urlrequest.Request(
        "https://api.github.com/user",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "openclaw-doctor",
        },
    )
    try:
        with urlrequest.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8", errors="ignore"))
        login = str(body.get("login", "")).strip()
        return CheckItem(name="token.github", ok=bool(login), detail=f"login={login or 'unknown'}", level="error")
    except urlerror.HTTPError as e:
        return CheckItem(name="token.github", ok=False, detail=f"http_{e.code}", level="error")
    except Exception as e:  # noqa: BLE001
        return CheckItem(name="token.github", ok=False, detail=f"request_failed:{e}", level="error")


def summarize(items: List[CheckItem]) -> Dict[str, Any]:
    errors = [x for x in items if (not x.ok and x.level == "error")]
    warnings = [x for x in items if (not x.ok and x.level == "warning")]
    return {
        "ok": len(errors) == 0,
        "errors": len(errors),
        "warnings": len(warnings),
        "items": [asdict(x) for x in items],
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Doctor for OpenClaw autopilot")
    p.add_argument("--config", default="openclaw_config.json", help="Path to config JSON")
    p.add_argument("--token-env", default="GITHUB_TOKEN", help="Env var name for GitHub token")
    p.add_argument("--check-github-token", action="store_true", help="Validate GitHub token via API")
    p.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    p.add_argument("--strict", action="store_true", help="Return non-zero when warnings exist")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    cfg_path = Path(args.config).resolve()
    if not cfg_path.exists():
        out = {"ok": False, "errors": 1, "warnings": 0, "items": [{"name": "config.path", "ok": False, "detail": f"missing: {cfg_path}", "level": "error"}]}
        print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else f"[ERROR] missing config: {cfg_path}")
        return 2

    cfg = load_config(cfg_path)

    items: List[CheckItem] = []
    items.extend(check_config_keys(cfg))
    items.extend(check_cli_binaries(cfg))
    items.extend(check_known_logins())

    token_val = os.environ.get(args.token_env, "")
    if args.check_github_token:
        if token_val:
            items.append(check_github_token(token_val.strip()))
        else:
            items.append(CheckItem(name="token.github", ok=False, detail=f"env {args.token_env} is empty", level="error"))

    result = summarize(items)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Doctor result: ok={result['ok']} errors={result['errors']} warnings={result['warnings']}")
        for item in result["items"]:
            state = "OK" if item["ok"] else item["level"].upper()
            print(f"- [{state}] {item['name']}: {item['detail']}")

    if not result["ok"]:
        return 3
    if args.strict and result["warnings"] > 0:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
