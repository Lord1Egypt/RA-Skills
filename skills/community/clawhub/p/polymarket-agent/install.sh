#!/usr/bin/env bash
# Install polymarket-agent into an isolated virtualenv.
#
# AUDIT FIX (Low — "Supply Chain Issues"): installs from requirements.txt with
# pinned versions, instead of resolving whatever is published at the moment.
#
# `set -euo pipefail`: the original script used only `set -e`, so an undefined
# variable or a failure in the middle of a pipe went unnoticed.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

say()  { printf '%s\n' "$*"; }
fail() { printf '❌ %s\n' "$*" >&2; exit 1; }

say "🎰 polymarket-agent — install"
say ""

command -v python3 >/dev/null 2>&1 || fail \
  "python3 not found. Install it with your package manager (on Debian/Ubuntu, the python3 and python3-venv packages)."

# The package uses 3.10+ type syntax (PEP 604). Failing here beats crashing
# with an obscure SyntaxError on the first `poly` run.
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
  || fail "Python 3.10+ is required (found: $(python3 -V 2>&1))"

if [ ! -d "$VENV_DIR" ]; then
  say "📦 Creating virtualenv in .venv…"
  python3 -m venv "$VENV_DIR" \
    || fail "failed to create the virtualenv. Install the python3-venv package for your distribution."
fi

PIP="$VENV_DIR/bin/pip"
say "📦 Installing dependencies (pinned versions)…"
"$PIP" install --quiet --upgrade pip
"$PIP" install --quiet -r "$SCRIPT_DIR/requirements.txt"
"$PIP" install --quiet -e "$SCRIPT_DIR"

# State directory at 0700 from the start, so the keystore never comes to
# exist under a directory with loose permissions.
STATE_DIR="${POLYMARKET_AGENT_HOME:-$HOME/.openclaw/polymarket-agent}"
mkdir -p "$STATE_DIR"
# Symbolic form of 0700 — same result, and it states the intent directly.
chmod u=rwx,go= "$STATE_DIR" 2>/dev/null || true

say ""
say "✅ Installed."
say ""
say "   CLI:   $VENV_DIR/bin/poly"
say "   State: $STATE_DIR (0700)"
say ""
say "Research works with no credential:"
say "   $VENV_DIR/bin/poly markets --limit 5"
say ""
say "To operate a wallet (optional):"
say "   $VENV_DIR/bin/poly setup     # key read hidden and encrypted"
say "   $VENV_DIR/bin/poly doctor    # check install and limits"
say ""
say "⚠  REAL MONEY: dry-run ships ON. Orders are validated and journaled,"
say "   but not sent, until you deliberately turn it off with:"
say "     poly config --key dry_run --value false"
say ""
say "   Emergency stop at any time: poly halt"
say ""
say "💡 Optional shortcut for ~/.bashrc:"
say "     alias poly='$VENV_DIR/bin/poly'"
