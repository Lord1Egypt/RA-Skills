#!/bin/sh
# homebase — the single supported entry point into the household data layer.
#
#   homebase.sh <tool_name> '<json_args>'
#   homebase.sh get_morning_briefing '{}'
#   homebase.sh get_weather_context '{"start_hour":8,"end_hour":17}'
#
# Non-agent callers (shell scripts, schedulers, launchd runners) should use
# this rather than invoking tools.py directly: it pins the interpreter to
# homebase's own venv, so nothing outside homebase needs to know where the
# venv lives or that there is one.
#
# Why the venv matters: the venv carries `requests` and `pypdf`. It is NOT
# about credentials — homebase holds none, and `gog` resolves its own Google
# token per invocation. (This comment said "keyring access the Google and
# portal credentials need" until 2026-09-20; keyring was dropped on
# 2026-09-07.)
#
# tools.py can also self-heal by re-execing under the venv, but only when the
# calling interpreter lacks `pypdf` AND resolves to a different binary than
# .venv/bin/python. A Homebrew python3.12 resolves to the same binary the venv
# symlinks to, so the self-heal does NOT fire there. This shim is the reliable
# path; the self-heal is the backstop.
#
# The sibling `bin/homebase` forwards here. This file carries the `.sh`
# extension because ClawHub only publishes known text extensions — an
# extensionless script is silently dropped from the published package.

set -e

HERE="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$HERE")"
VENV_PYTHON="$SKILL_DIR/.venv/bin/python3"

if [ ! -x "$VENV_PYTHON" ]; then
    # stdout, not stderr: callers capture stdout and match a leading ❌.
    echo "❌ homebase venv missing at $VENV_PYTHON"
    exit 1
fi

# tools.py resolves feature imports relative to its own directory.
cd "$SKILL_DIR"
exec "$VENV_PYTHON" tools.py "$@"
