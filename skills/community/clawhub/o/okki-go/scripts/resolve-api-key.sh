#!/bin/sh
# Compatibility wrapper for OKKI Go API key resolution.
#
# The credential implementation lives in okki-auth.js to avoid shell-specific
# stat/JQ behavior across Linux, macOS, containers, and agent runtimes.

set -eu

MODE="${1:---check}"
SKILL_VERSION="${OKKIGO_SKILL_VERSION:-1.3.3}"
export OKKIGO_SKILL_VERSION="$SKILL_VERSION"

if [ "$MODE" != "--check" ] && [ "$MODE" != "--source" ] && [ "$MODE" != "--print" ]; then
  echo "Usage: $0 [--check|--source|--print]" >&2
  exit 2
fi

script_dir() {
  CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd
}

dir="$(script_dir || pwd)"

if command -v node >/dev/null 2>&1; then
  exec node "$dir/okki-auth.js" resolve "$MODE"
fi

echo "NO_KEY"
echo "OKKI Go API key resolver requires node to read the user credential cache." >&2
exit 1
