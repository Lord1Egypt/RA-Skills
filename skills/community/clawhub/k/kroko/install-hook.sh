#!/usr/bin/env bash
# Install KROKO as a git pre-commit hook in a repository.
#
#   ./install-hook.sh [REPO_PATH]        default: the current directory
#
# The hook checks only the staged Python files, in strict comment mode, so it costs
# a few dozen milliseconds per commit rather than a full-repo sweep.
set -euo pipefail

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${1:-.}"
KROKO_HOME="${KROKO_HOME:-$HOME/.hermes/skills/kroko}"

if [ ! -d "$REPO/.git" ]; then
    echo "kroko: not a git repository: $REPO" >&2
    exit 2
fi
if [ ! -x "$KROKO_HOME/bin/kroko" ]; then
    echo "kroko: gate not found at $KROKO_HOME/bin/kroko" >&2
    echo "kroko: run install.sh first, or set KROKO_HOME" >&2
    exit 2
fi

HOOK="$REPO/.git/hooks/pre-commit"
if [ -f "$HOOK" ] && ! grep -q "KROKO pre-commit hook" "$HOOK" 2>/dev/null; then
    BACKUP="$HOOK.kroko-backup.$(date +%Y%m%d%H%M%S)"
    mv "$HOOK" "$BACKUP"
    echo "kroko: existing hook preserved at $BACKUP"
fi

sed "s|@KROKO_HOME@|$KROKO_HOME|g" "$SOURCE/templates/pre-commit" > "$HOOK"
chmod +x "$HOOK"
echo "kroko: hook installed at $HOOK"
echo "kroko: gate resolved to $KROKO_HOME/bin/kroko"
