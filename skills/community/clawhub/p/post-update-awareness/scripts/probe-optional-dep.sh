#!/usr/bin/env bash
# Probe whether an optional native Node dependency is loadable.
#
# Usage: probe-optional-dep.sh <module-name>
#
# Output (stdout):
#   OK              — the module loaded successfully
#   MISSING         — the module is not installed
#   ERROR <message> — the module is present but failed to load
#
# Exit codes:
#   0 — OK
#   1 — MISSING or ERROR
#   2 — bad usage
#
# Design notes:
#   - Non-blocking: never installs, never modifies state.
#   - Wraps in `node -e` with a try/catch so a broken native binding
#     doesn't take down the calling shell.

set -uo pipefail

if [ $# -lt 1 ] || [ -z "${1:-}" ]; then
  echo "ERROR usage: $(basename "$0") <module-name>" >&2
  exit 2
fi

module="$1"

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR node binary not on PATH"
  exit 1
fi

# Use a here-doc so module names with special characters can't break the script.
result=$(node - "$module" <<'NODESCRIPT' 2>&1
const mod = process.argv[2];
try {
  require(mod);
  console.log("OK");
  process.exit(0);
} catch (err) {
  if (err && err.code === "MODULE_NOT_FOUND" && err.message.includes(mod)) {
    console.log("MISSING");
    process.exit(1);
  }
  // The module exists but failed to load (broken native binding, ABI
  // mismatch after Node upgrade, etc.). Surface the actual error.
  const msg = (err && err.message ? err.message : String(err))
    .split("\n")[0]
    .slice(0, 200);
  console.log("ERROR " + msg);
  process.exit(1);
}
NODESCRIPT
)

echo "$result"
case "$result" in
  OK) exit 0 ;;
  *) exit 1 ;;
esac
