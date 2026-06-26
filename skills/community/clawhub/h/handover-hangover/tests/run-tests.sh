#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "ok - $*"; }

assert_file() { [ -f "$1" ] || fail "missing file: $1"; }
assert_no_file() { [ ! -e "$1" ] || fail "unexpected file: $1"; }
assert_contains() { grep -Fq "$2" "$1" || fail "expected '$2' in $1"; }

make_workspace() {
  local name="$1"
  local ws="$TMP_ROOT/$name"
  mkdir -p "$ws/memory" "$ws/skills"
  printf '%s\n' "$ws"
}

run_watchdog() {
  local ws="$1"
  WORKSPACE="$ws" bash "$ROOT/scripts/handoff.sh" >/tmp/hh-test.out 2>/tmp/hh-test.err
}

# Static checks
bash -n "$ROOT/scripts/handoff.sh" "$ROOT/scripts/install-integration.sh" "$ROOT/scripts/status.sh"
node --input-type=module -e "import('$ROOT/hooks/handover-hangover/handler.js').then(m => { if (typeof m.default !== 'function') process.exit(1) })"
pass "static syntax checks"

# INIT branch: creates bootstrap prev + pending + sealed, no current note remains.
ws="$(make_workspace init)"
run_watchdog "$ws"
assert_file "$ws/memory/handoff-note.prev.md"
assert_file "$ws/memory/.handoff-pending"
assert_file "$ws/memory/.handoff-sealed"
assert_no_file "$ws/memory/handoff-note.md"
assert_contains "$ws/memory/handoff-note.prev.md" "First run of Handover Hangover"
pass "watchdog INIT branch"

# CONFIRMED branch: archives model-written note.
ws="$(make_workspace confirmed)"
cat > "$ws/memory/handoff-note.md" <<'NOTE'
# Handoff Note

## Why you are here
Test confirmed branch.

--- written by test-model at 2026-01-01T00:00:00Z
NOTE
run_watchdog "$ws"
assert_file "$ws/memory/handoff-note.prev.md"
assert_file "$ws/memory/.handoff-pending"
assert_file "$ws/memory/.handoff-sealed"
assert_no_file "$ws/memory/handoff-note.md"
assert_contains "$ws/memory/handoff-note.prev.md" "Test confirmed branch"
pass "watchdog CONFIRMED branch"

# NO-OP branch: sealed prev remains, signal is reasserted.
ws="$(make_workspace noop)"
printf 'existing baton\n' > "$ws/memory/handoff-note.prev.md"
touch "$ws/memory/.handoff-sealed"
run_watchdog "$ws"
assert_file "$ws/memory/.handoff-pending"
assert_contains "$ws/memory/handoff-note.prev.md" "existing baton"
pass "watchdog NO-OP branch"

# DIRTY SWITCH branch: prev without seal is replaced by fallback.
ws="$(make_workspace dirty)"
printf 'old baton\n' > "$ws/memory/handoff-note.prev.md"
run_watchdog "$ws"
assert_file "$ws/memory/.handoff-pending"
assert_file "$ws/memory/.handoff-sealed"
assert_contains "$ws/memory/handoff-note.prev.md" "Possible model switch or continuity break"
assert_contains "$ws/memory/handoff-note.prev.md" "script-generated fallback"
pass "watchdog DIRTY SWITCH branch"

# Managed hook: message:received invokes watchdog before the model turn.
ws="$(make_workspace hook-message)"
node --input-type=module <<NODE
import hook from '$ROOT/hooks/handover-hangover/handler.js';
await hook({ type: 'message', action: 'received', context: { workspaceDir: '$ws', cfg: {} } });
NODE
assert_file "$ws/memory/.handoff-pending"
assert_file "$ws/memory/handoff-note.prev.md"
pass "managed hook message:received invokes watchdog"

# Managed hook: restores executable bit and runs direct script execution path.
ws="$(make_workspace hook-nonexec)"
mkdir -p "$ws/skills/handover-hangover/scripts"
cp "$ROOT/scripts/handoff.sh" "$ws/skills/handover-hangover/scripts/handoff.sh"
chmod 0644 "$ws/skills/handover-hangover/scripts/handoff.sh"
node --input-type=module <<NODE
import hook from '$ROOT/hooks/handover-hangover/handler.js';
await hook({ type: 'message', action: 'received', context: { workspaceDir: '$ws', cfg: {} } });
NODE
assert_file "$ws/memory/.handoff-pending"
[ -x "$ws/skills/handover-hangover/scripts/handoff.sh" ] || fail "hook did not restore executable bit"
pass "managed hook restores executable bit for direct execution"

# Managed hook ignores unrelated events.
ws="$(make_workspace hook-ignore)"
node --input-type=module <<NODE
import hook from '$ROOT/hooks/handover-hangover/handler.js';
await hook({ type: 'message', action: 'sent', context: { workspaceDir: '$ws', cfg: {} } });
NODE
assert_no_file "$ws/memory/.handoff-pending"
pass "managed hook ignores unrelated events"

# Installer: with fake openclaw on PATH, copies managed hook without touching real home.
fake_home="$TMP_ROOT/openclaw-home"
fake_bin="$TMP_ROOT/bin"
mkdir -p "$fake_bin"
cat > "$fake_bin/openclaw" <<'SH'
#!/usr/bin/env bash
if [ "$1" = "hooks" ] && [ "${2:-}" = "--help" ]; then exit 0; fi
if [ "$1" = "hooks" ] && [ "${2:-}" = "enable" ]; then echo "enabled $3"; exit 0; fi
exit 1
SH
chmod +x "$fake_bin/openclaw"
OPENCLAW_HOME="$fake_home" PATH="$fake_bin:$PATH" bash "$ROOT/scripts/install-integration.sh" >/tmp/hh-install.out
assert_file "$fake_home/hooks/handover-hangover/HOOK.md"
assert_file "$fake_home/hooks/handover-hangover/handler.js"
assert_file "$fake_home/hooks/handover-hangover/handoff.sh"
[ -x "$fake_home/hooks/handover-hangover/handoff.sh" ] || fail "installed handoff.sh not executable"
assert_contains /tmp/hh-install.out "enabled OpenClaw hook"
pass "installer copies and enables managed hook"

echo "All tests passed."
