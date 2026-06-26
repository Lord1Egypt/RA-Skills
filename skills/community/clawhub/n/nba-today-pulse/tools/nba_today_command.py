#!/usr/bin/env python3
"""Deterministic slash-command dispatcher for NBA today report."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from nba_common import NBAReportError  # noqa: E402
from nba_pulse_core import command_options, detect_lang  # noqa: E402
from timezone_resolver import resolve_timezone  # noqa: E402

REPORT_SCRIPT = CURRENT_DIR / "nba_pulse_router.py"

MISSING_TIMEZONE_MESSAGES = {
    "zh": "无法确定你的时区。请直接告诉我城市或 IANA 时区，例如：上海 / Asia/Shanghai。",
    "en": "I couldn't determine your timezone. Please provide a city or IANA timezone, for example: Shanghai / Asia/Shanghai.",
}

TERMINAL_ERROR_KINDS = {"invalid_timezone", "missing_timezone", "not_found"}
ERROR_LINE_RE = re.compile(r"^\[(?P<kind>[^\]]+)\]\s*(?P<message>.+?)\s*$")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse slash-command args and invoke nba_today_report.py.")
    parser.add_argument("--command", default="", help="Raw slash-command args string")
    parser.add_argument("--tz", default="", help="Optional timezone or city override injected by the runtime")
    parser.add_argument("--command-name", default="", help="Slash command name")
    parser.add_argument("--skill-name", default="", help="Skill name")
    return parser.parse_args(argv)


def build_command(raw_command: str, tz_override: str | None = None) -> list[str]:
    explicit_tz = tz_override
    try:
        resolved_timezone = resolve_timezone(explicit_tz=explicit_tz, command_text=None if explicit_tz else raw_command)
    except NBAReportError as exc:
        if exc.kind == "missing_timezone":
            lang = detect_lang(raw_command)
            raise NBAReportError(MISSING_TIMEZONE_MESSAGES.get(lang, MISSING_TIMEZONE_MESSAGES["en"]), kind="missing_timezone") from exc
        raise

    options = command_options(raw_command, tz_hint=resolved_timezone.name)

    cmd = [
        sys.executable,
        str(REPORT_SCRIPT),
        "--command",
        raw_command,
        "--lang",
        str(options["lang"]),
        "--format",
        "markdown",
        "--analysis-mode",
        str(options["analysis_mode"]),
    ]
    if options.get("intent"):
        cmd.extend(["--intent", str(options["intent"])])
    if options["date"]:
        cmd.extend(["--date", str(options["date"])])
    if options["team"]:
        cmd.extend(["--team", str(options["team"])])
    if options.get("opponent"):
        cmd.extend(["--opponent", str(options["opponent"])])
    if options.get("zh_locale"):
        cmd.extend(["--zh-locale", str(options["zh_locale"])])
    cmd.extend(["--tz", str(resolved_timezone.name)])
    return cmd


def extract_terminal_message(stderr_text: str) -> tuple[str, str] | None:
    for raw_line in reversed(stderr_text.splitlines()):
        line = raw_line.strip()
        if not line:
            continue
        match = ERROR_LINE_RE.match(line)
        if match:
            kind = str(match.group("kind") or "").strip()
            message = str(match.group("message") or "").strip()
            if kind in TERMINAL_ERROR_KINDS and message:
                return kind, message
            return None
    return None


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        command = build_command(args.command or "", tz_override=args.tz or None)
    except NBAReportError as exc:
        message = str(exc).strip()
        if exc.kind in TERMINAL_ERROR_KINDS:
            if message:
                sys.stdout.write(f"{message}\n")
            return 0
        if message:
            sys.stderr.write(f"{message}\n")
        return 1
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    terminal_message = extract_terminal_message(completed.stderr or "")
    if completed.returncode != 0 and terminal_message and not (completed.stdout or "").strip():
        _, message = terminal_message
        sys.stdout.write(f"{message}\n")
        return 0
    if completed.stdout:
        sys.stdout.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
