#!/usr/bin/env bash
# No.0 v0.3.0 integration test suite.
#
# Covers spec §7.1 (Core-only / DLC-only / linked) and §7.2 edge cases.
# Runs installers to fresh temp dirs, exercises CLI, drives event-bus
# linkage end-to-end, verifies audit + archive state.
#
# Usage:  ./tests/integration_test.sh [--keep-temp]

set -uo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
SRC_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
KEEP_TEMP=0
[ "${1:-}" = "--keep-temp" ] && KEEP_TEMP=1

PY="${NO0_PYTHON:-python3}"
TMP_ROOT=""
RUNTIME_BACKUP=""

# Tests must never fire real openclaw system events at the user agent.
export NO0_DLC_DISABLE_PUSH=1
# Pin language to zh for most tests — assertions grep localized strings.
# Test 11 overrides this to exercise English output.
export NO0_LANG=zh
PASS=0
FAIL=0
FAIL_NOTES=()

red() { printf '\033[31m%s\033[0m' "$*"; }
green() { printf '\033[32m%s\033[0m' "$*"; }
dim() { printf '\033[2m%s\033[0m' "$*"; }

pass() { PASS=$((PASS+1)); printf '  %s %s\n' "$(green '[PASS]')" "$1"; }
fail() { FAIL=$((FAIL+1)); FAIL_NOTES+=("$1"); printf '  %s %s\n' "$(red '[FAIL]')" "$1"; }

check() {
  local label="$1"; shift
  if "$@" >/dev/null 2>&1; then
    pass "$label"
  else
    fail "$label ($*)"
  fi
}

section() { printf '\n%s\n' "$(dim "── $* ──")"; }

cleanup() {
  if [ -n "${RUNTIME_BACKUP}" ] && [ -d "$RUNTIME_BACKUP" ]; then
    rm -rf "$HOME/.openclaw/no0" 2>/dev/null
    mv "$RUNTIME_BACKUP" "$HOME/.openclaw/no0" 2>/dev/null || true
  elif [ -n "${RUNTIME_BACKUP}" ]; then
    rm -rf "$HOME/.openclaw/no0" 2>/dev/null || true
  fi
  if [ "$KEEP_TEMP" -eq 0 ] && [ -n "${TMP_ROOT}" ] && [ -d "$TMP_ROOT" ]; then
    rm -rf "$TMP_ROOT"
  else
    [ -n "${TMP_ROOT}" ] && echo "temp kept: $TMP_ROOT"
  fi
}
trap cleanup EXIT

# --- preserve any real runtime state ---
if [ -d "$HOME/.openclaw/no0" ]; then
  RUNTIME_BACKUP="$HOME/.openclaw/no0.testbak.$$"
  mv "$HOME/.openclaw/no0" "$RUNTIME_BACKUP"
else
  RUNTIME_BACKUP="$HOME/.openclaw/no0.testbak.$$"  # sentinel; no dir to restore
fi

TMP_ROOT="$(mktemp -d)"
echo "temp root: $TMP_ROOT"

# =====================================================================
section "Test 1 — Core standalone install"
# =====================================================================
CORE_TARGET="$TMP_ROOT/core-only"
"$SRC_DIR/install.sh" "$CORE_TARGET" >/dev/null
check "install.sh exits 0"                         test $? -eq 0
check "dispatcher exists"                          test -x "$CORE_TARGET/no0"
check "no0-core/ present"                          test -d "$CORE_TARGET/no0-core"
check "scripts/skill_launcher.py present"          test -f "$CORE_TARGET/no0-core/scripts/skill_launcher.py"
check "scripts/event_emitter.py present"           test -f "$CORE_TARGET/no0-core/scripts/event_emitter.py"
check "no0-dlc-internal-control/ absent"           test ! -d "$CORE_TARGET/no0-dlc-internal-control"
check "runtime events/pending/ created"            test -d "$HOME/.openclaw/no0/events/pending"

# Core commands work
"$CORE_TARGET/no0" help >/dev/null 2>&1
check "./no0 help exits 0"                         test $? -eq 0

# DLC command gives friendly upsell (exit 2, not 1)
"$CORE_TARGET/no0" classify get /tmp >/dev/null 2>&1
rc=$?
if [ "$rc" -eq 2 ]; then pass "DLC command upsells (exit 2)"
else fail "DLC command upsell wrong rc=$rc"; fi

# Daemon lifecycle sanity — just start/stop
"$CORE_TARGET/no0" start >/dev/null 2>&1
sleep 2
"$CORE_TARGET/no0" status 2>&1 | grep -qi "monitor"
check "status shows monitor line"                  test $? -eq 0
"$CORE_TARGET/no0" stop >/dev/null 2>&1
check "start/stop cycle clean"                     test $? -eq 0

# =====================================================================
section "Test 2 — DLC standalone install"
# =====================================================================
rm -rf "$HOME/.openclaw/no0"
DLC_ONLY_TARGET="$TMP_ROOT/dlc-only"
"$SRC_DIR/install-dlc.sh" "$DLC_ONLY_TARGET" >/dev/null 2>&1 || true
check "install-dlc.sh produced target"             test -d "$DLC_ONLY_TARGET/no0-dlc-internal-control"
check "dispatcher copied for standalone"           test -x "$DLC_ONLY_TARGET/no0"
check "no0-core/ absent"                           test ! -d "$DLC_ONLY_TARGET/no0-core"
check "dlc_cli.py present"                         test -f "$DLC_ONLY_TARGET/no0-dlc-internal-control/cli/dlc_cli.py"
check "event_listener present"                     test -f "$DLC_ONLY_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py"
check "dlc runtime dir created"                    test -d "$HOME/.openclaw/no0/dlc"

# DLC audit/init work without Core
"$DLC_ONLY_TARGET/no0" audit log >/dev/null 2>&1
check "dlc audit log runs"                         test $? -eq 0
"$DLC_ONLY_TARGET/no0" auth pending >/dev/null 2>&1
check "dlc auth pending runs"                      test $? -eq 0

# Core command gracefully errors (unknown from DLC-only perspective but dispatcher routes to no0-core which doesn't exist)
"$DLC_ONLY_TARGET/no0" status >/dev/null 2>&1
# exit non-zero expected because no0-core/scripts/skill_launcher.py missing
rc=$?
if [ "$rc" -ne 0 ]; then pass "Core cmd fails cleanly when Core absent"
else fail "Core cmd unexpectedly succeeded"; fi

# =====================================================================
section "Test 3 — Linked Core + DLC"
# =====================================================================
rm -rf "$HOME/.openclaw/no0"
LINK_TARGET="$TMP_ROOT/linked"
"$SRC_DIR/install.sh"     "$LINK_TARGET" >/dev/null
"$SRC_DIR/install-dlc.sh" "$LINK_TARGET" >/dev/null 2>&1 || true
check "both packages present"                      test -d "$LINK_TARGET/no0-core" -a -d "$LINK_TARGET/no0-dlc-internal-control"

# Emit a synthetic Level-5 event (bypassing the monitor timer for speed).
# This is the same path heartbeat_processor uses after classify() — validates
# the seam between Core event_emitter and DLC event_handler.
"$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={
        'file_name': 'SOUL.md',
        'source': '/fake/SOUL.md',
        'old_hash': 'aaa111', 'new_hash': 'bbb222',
        'diff': {'unified_diff': '+ exec(untrusted)'},
    },
    level=5, reason='integration-test',
    rule_hits=['安全机制绕过', '自动执行外部命令'],
    added=1, removed=0, target_path='/fake/SOUL.md',
)
PYEOF
check "Core emitted event"                         test "$(ls "$HOME/.openclaw/no0/events/pending/" | wc -l | tr -d ' ')" = "1"

# Run DLC handler once
"$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1
rc=$?
check "DLC handler --once exits 0"                 test "$rc" -eq 0
check "pending drained"                            test "$(ls "$HOME/.openclaw/no0/events/pending/" | wc -l | tr -d ' ')" = "0"
check "processed/ has archived event"              test "$(find "$HOME/.openclaw/no0/events/processed" -type f | wc -l | tr -d ' ')" = "1"
check "audit.csv has a data row"                   test "$(wc -l <"$HOME/.openclaw/no0/dlc/audit.csv" | tr -d ' ')" -ge "2"

# Verify audit row captured severity + rule hits
grep -q "level_5" "$HOME/.openclaw/no0/dlc/audit.csv"
check "audit row mentions level_5"                 test $? -eq 0
grep -q "安全机制绕过" "$HOME/.openclaw/no0/dlc/audit.csv"
check "audit row captures rule_hits"               test $? -eq 0

# L5 push-decision flow: lock written, push skipped by env var
check "pending_decision lock created"              test -f "$HOME/.openclaw/no0/dlc/pending_decisions/SOUL.md.lock"
grep -q "pushed_decision_request" "$HOME/.openclaw/no0/dlc/audit.csv"
check "audit records pushed_decision_request"      test $? -eq 0
grep -q "push=push_skipped_env" "$HOME/.openclaw/no0/dlc/audit.csv"
check "push suppressed by NO0_DLC_DISABLE_PUSH"    test $? -eq 0

# Dedupe: second L5 event for same file while lock exists
"$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={
        'file_name': 'SOUL.md',
        'source': '/fake/SOUL.md',
        'old_hash': 'bbb222', 'new_hash': 'ccc333',
        'diff': {'unified_diff': '+ another tamper'},
    },
    level=5, reason='integration-test-dedupe',
    rule_hits=['安全机制绕过'],
    added=1, removed=0, target_path='/fake/SOUL.md',
)
PYEOF
"$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1
grep -q "deduped_pending_decision" "$HOME/.openclaw/no0/dlc/audit.csv"
check "second L5 deduped against lock"             test $? -eq 0

# decide: status shows lock, keep removes it
"$LINK_TARGET/no0" decide SOUL.md status >/dev/null 2>&1
check "./no0 decide status exits 0"                test $? -eq 0
"$LINK_TARGET/no0" decide SOUL.md keep >/dev/null 2>&1
check "./no0 decide keep exits 0"                  test $? -eq 0
check "lock removed after keep"                    test ! -f "$HOME/.openclaw/no0/dlc/pending_decisions/SOUL.md.lock"
"$LINK_TARGET/no0" decide SOUL.md status >/dev/null 2>&1
check "decide status after keep is clean"          test $? -eq 0

# =====================================================================
section "Test 4 — §7.2 edge: half-written event (.tmp_ ignored)"
# =====================================================================
rm -rf "$HOME/.openclaw/no0/events/processed"
mkdir -p "$HOME/.openclaw/no0/events/pending"
# Drop a tmp-prefixed file (simulating a write in progress) + an orphan .txt
echo '{"not":"ready"}' > "$HOME/.openclaw/no0/events/pending/.tmp_half_written.json"
echo 'garbage'         > "$HOME/.openclaw/no0/events/pending/not_an_event.txt"
"$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1
# Both should still be there — handler ignores non-*.json and .tmp_ files
check ".tmp_ file still present"                   test -f "$HOME/.openclaw/no0/events/pending/.tmp_half_written.json"
check "non-json file still present"                test -f "$HOME/.openclaw/no0/events/pending/not_an_event.txt"

# =====================================================================
section "Test 5 — §7.2 edge: schema version mismatch"
# =====================================================================
rm -f "$HOME/.openclaw/no0/events/pending"/*
rm -rf "$HOME/.openclaw/no0/events/processed"
mkdir -p "$HOME/.openclaw/no0/events/processed"
cat >"$HOME/.openclaw/no0/events/pending/future_schema.json" <<'JSON'
{
  "event_id": "2099-01-01T00:00:00Z_zzzzzz",
  "event_type": "cognitive_file_tampering",
  "schema_version": "2.0",
  "timestamp": "2099-01-01T00:00:00Z",
  "source": "no0-core",
  "severity": "level_5",
  "severity_numeric": 5,
  "target_file": "SOUL.md",
  "rule_hits": ["安全机制绕过"],
  "dlc_request": {"require_authorization": true, "require_mfa": true}
}
JSON
"$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1
check "schema-mismatch event archived"             test "$(find "$HOME/.openclaw/no0/events/processed" -type f | wc -l | tr -d ' ')" = "1"
grep -q "rejected_schema_mismatch" "$HOME/.openclaw/no0/dlc/audit.csv"
check "audit records rejection reason"             test $? -eq 0

# =====================================================================
section "Test 6 — 真实端到端：真 monitor + 真改 .md + 真 poll"
# =====================================================================
# 前几个测试用伪造 JSON 直接塞给 DLC handler。这条测试启动真正的 Core
# monitor，复制 baseline 到一个 watch dir，真实 tamper（追加 exec(...) 一行，
# 应该命中"自动执行外部命令"→ L5），让 monitor + heartbeat_processor
# 自己走完完整链路，最后由 ./no0 decide 收尾。
rm -rf "$HOME/.openclaw/no0/events/pending"/* 2>/dev/null
rm -rf "$HOME/.openclaw/no0/events/processed" 2>/dev/null
rm -f "$HOME/.openclaw/no0/dlc/audit.csv" 2>/dev/null
rm -rf "$HOME/.openclaw/no0/dlc/pending_decisions"/* 2>/dev/null
mkdir -p "$HOME/.openclaw/no0/events/pending" \
         "$HOME/.openclaw/no0/events/processed" \
         "$HOME/.openclaw/no0/dlc/pending_decisions"

# Reset Core baseline state in the linked install so this run is clean
rm -f "$LINK_TARGET/no0-core/change_log.json" "$LINK_TARGET/no0-core/change_log.md" 2>/dev/null
rm -rf "$LINK_TARGET/no0-core/cognitive_file_backups" 2>/dev/null

WATCH_DIR="$TMP_ROOT/watch"
mkdir -p "$WATCH_DIR"
for f in SOUL.md USER.md HEARTBEAT.md MEMORY.md TOOLS.md AGENTS.md; do
  if [ -f "$LINK_TARGET/no0-core/${f}.v1" ]; then
    cp "$LINK_TARGET/no0-core/${f}.v1" "$WATCH_DIR/${f}"
    chmod u+w "$WATCH_DIR/${f}"   # baselines are r--; a real workspace is writable
  fi
done

# Pass 1 — baseline establishment. Should produce no events.
"$PY" "$LINK_TARGET/no0-core/scripts/monitor.py" \
  --monitor-dir "$WATCH_DIR" \
  --output-dir "$LINK_TARGET/no0-core" \
  --run-once >/dev/null 2>&1
check "monitor pass 1 (baseline) produced no events" \
    test "$(ls "$HOME/.openclaw/no0/events/pending/" 2>/dev/null | wc -l | tr -d ' ')" = "0"

# Real tamper: append a line that hits 自动执行外部命令 → Level 5
echo '+exec(untrusted_payload)  # injected tamper' >> "$WATCH_DIR/SOUL.md"

# Pass 2 — detect + write change_log entry
"$PY" "$LINK_TARGET/no0-core/scripts/monitor.py" \
  --monitor-dir "$WATCH_DIR" \
  --output-dir "$LINK_TARGET/no0-core" \
  --run-once >/dev/null 2>&1

# Classifier runs, emits via event_emitter hook
"$PY" "$LINK_TARGET/no0-core/scripts/heartbeat_processor.py" >/dev/null 2>&1

check "pending/ has real tamper event" \
    test "$(ls "$HOME/.openclaw/no0/events/pending/" 2>/dev/null | wc -l | tr -d ' ')" -ge "1"

# DLC consumes
"$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1

check "L5 lock from real tamper"                   test -f "$HOME/.openclaw/no0/dlc/pending_decisions/SOUL.md.lock"
grep -q "自动执行外部命令" "$HOME/.openclaw/no0/dlc/audit.csv"
check "real tamper hit exec-rule in audit"         test $? -eq 0
grep -q "pushed_decision_request" "$HOME/.openclaw/no0/dlc/audit.csv"
check "real tamper produced decision request"      test $? -eq 0

# Clean up via decide keep (rollback would work too but needs real backup plumbing)
"$LINK_TARGET/no0" decide SOUL.md keep >/dev/null 2>&1
check "decide keep released real-tamper lock"      test ! -f "$HOME/.openclaw/no0/dlc/pending_decisions/SOUL.md.lock"

# =====================================================================
section "Test 7 — Core 独立运行：pending/ 自清理 (TTL + 上限)"
# =====================================================================
# 当 DLC 没有消费 pending/ 的时候，Core 每次 emit 前会自清一次：
#   - 超过 TTL 的事件 → events/expired/<date>/
#   - 超过上限的最老事件 → events/expired/<date>/
# 这一项确保 Core 独立运行（DLC 缺位或 handler 挂了）也不会把磁盘撑爆。
rm -rf "$HOME/.openclaw/no0/events/pending"/* 2>/dev/null
rm -rf "$HOME/.openclaw/no0/events/expired" 2>/dev/null
mkdir -p "$HOME/.openclaw/no0/events/pending"

# Fabricate an old pending event (mtime 10 days ago) — should be expired by TTL.
OLD_EVENT="$HOME/.openclaw/no0/events/pending/2099-01-01T00:00:00Z_oldfake.json"
printf '{"event_id":"2099-01-01T00:00:00Z_oldfake","schema_version":"1.0","severity_numeric":4,"target_file":"SOUL.md"}' > "$OLD_EVENT"
# Set mtime to 10 days ago (TTL is 7 days)
python3 -c "import os,time; os.utime('$OLD_EVENT', (time.time()-10*86400, time.time()-10*86400))"

# Trigger a fresh emit — this should both write the new event AND expire the old one.
"$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={'file_name':'SOUL.md','source':'/fake/SOUL.md','old_hash':'a','new_hash':'b','diff':{'unified_diff':'+ x'}},
    level=4, reason='ttl-test', rule_hits=['安全机制绕过'],
    added=1, removed=0, target_path='/fake/SOUL.md',
)
PYEOF

check "old event expired by TTL"                   test ! -f "$OLD_EVENT"
check "expired/ directory populated"               test "$(find "$HOME/.openclaw/no0/events/expired" -type f 2>/dev/null | wc -l | tr -d ' ')" -ge "1"
check "fresh event remains in pending/"            test "$(ls "$HOME/.openclaw/no0/events/pending/" | wc -l | tr -d ' ')" = "1"

# Cap overflow: create 210 synthetic events (cap is 200), emit once more,
# verify at least 11 get expired (10 overflow + the newly emitted puts us at 211).
rm -rf "$HOME/.openclaw/no0/events/pending"/* "$HOME/.openclaw/no0/events/expired" 2>/dev/null
mkdir -p "$HOME/.openclaw/no0/events/pending"
for i in $(seq 1 210); do
  printf '{"event_id":"fake_%03d","schema_version":"1.0"}' "$i" > "$HOME/.openclaw/no0/events/pending/fake_$(printf %03d $i).json"
done
"$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={'file_name':'SOUL.md','source':'/fake/SOUL.md','old_hash':'a','new_hash':'b','diff':{'unified_diff':'+ y'}},
    level=5, reason='cap-test', rule_hits=['安全机制绕过'],
    added=1, removed=0, target_path='/fake/SOUL.md',
)
PYEOF
pending_count=$(ls "$HOME/.openclaw/no0/events/pending/" | wc -l | tr -d ' ')
check "pending count after cap-overflow is <= 200" test "$pending_count" -le "200"
check "overflow moved to expired/"                 test "$(find "$HOME/.openclaw/no0/events/expired" -type f 2>/dev/null | wc -l | tr -d ' ')" -ge "1"

# Status command surfaces the warning when pending is high.
# Seed 60 events to exceed WARN threshold (50) but stay under cap.
rm -rf "$HOME/.openclaw/no0/events/pending"/* "$HOME/.openclaw/no0/events/expired" 2>/dev/null
mkdir -p "$HOME/.openclaw/no0/events/pending"
for i in $(seq 1 60); do
  printf '{"event_id":"warn_%03d"}' "$i" > "$HOME/.openclaw/no0/events/pending/warn_$(printf %03d $i).json"
done
# status needs the monitor_dir arg; use the watch dir from Test 6 or re-create minimal
"$LINK_TARGET/no0" status --monitor-dir "$WATCH_DIR" --output-dir "$LINK_TARGET/no0-core" 2>&1 | grep -q "事件队列 pending: 60"
check "status shows pending count"                 test $? -eq 0
"$LINK_TARGET/no0" status --monitor-dir "$WATCH_DIR" --output-dir "$LINK_TARGET/no0-core" 2>&1 | grep -q "⚠️"
check "status warns when pending over threshold"   test $? -eq 0

# =====================================================================
section "Test 8 — Hourly conditional report"
# =====================================================================
# Fresh state - delete cursor, empty audit + pending, no locks.
rm -f "$HOME/.openclaw/no0/hourly_cursor.json"
rm -f "$HOME/.openclaw/no0/dlc/audit.csv"
rm -rf "$HOME/.openclaw/no0/dlc/pending_decisions"/* 2>/dev/null
rm -rf "$HOME/.openclaw/no0/events/pending"/* 2>/dev/null
rm -f "$HOME/.openclaw/no0/change_log.json" 2>/dev/null

# With no data, report should be silent
out=$("$LINK_TARGET/no0" report 2>&1)
check "empty state → silent"                       test -z "$out"

# Seed an L5 event and process it so audit + lock show up
"$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={'file_name':'USER.md','source':'/fake/USER.md','old_hash':'a','new_hash':'b','diff':{'unified_diff':'+ exec(x)'}},
    level=5, reason='report-test', rule_hits=['自动执行外部命令'],
    added=1, removed=0, target_path='/fake/USER.md',
)
PYEOF
"$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1

# Now report should emit a non-empty summary
out=$("$LINK_TARGET/no0" report 2>&1)
echo "$out" | grep -q "L5 决策已推送"
check "report surfaces L5 pushed decision"         test $? -eq 0
echo "$out" | grep -q "USER.md"
check "report lists outstanding lock"              test $? -eq 0

# Second call should be silent (cursor advanced, no new delta)
out2=$("$LINK_TARGET/no0" report 2>&1)
# Locks are still outstanding though, so the report will still print them.
# Verify: only the "outstanding" section remains, no "new …" bullets.
echo "$out2" | grep -q "未处置 L5 锁"
check "second call still shows unresolved locks"   test $? -eq 0
echo "$out2" | grep -q "新变更记录\|L5 决策已推送\|L5 去重"
# grep -q returns 0 on match — we want NO match here
if [ $? -ne 0 ]; then pass "second call has no \"new\" delta lines"
else fail "second call still shows \"new\" delta"; fi

# After user resolves the lock, third call should be fully silent
"$LINK_TARGET/no0" decide USER.md keep >/dev/null 2>&1
out3=$("$LINK_TARGET/no0" report 2>&1)
check "report silent after decide keep"            test -z "$out3"

# JSON mode works
json_out=$("$LINK_TARGET/no0" report --json 2>&1)
echo "$json_out" | python3 -c "import json,sys; json.loads(sys.stdin.read())" >/dev/null 2>&1
check "report --json is valid JSON"                test $? -eq 0

# =====================================================================
section "Test 9 — Push failure visibility + retry"
# =====================================================================
# Reset state
rm -f "$HOME/.openclaw/no0/dlc/audit.csv" "$HOME/.openclaw/no0/dlc/push_failures.log"
rm -rf "$HOME/.openclaw/no0/dlc/pending_decisions"/* 2>/dev/null
rm -rf "$HOME/.openclaw/no0/events/pending"/* 2>/dev/null

# Install a stub `openclaw` on PATH that always exits 1 to simulate gateway failure.
STUB_DIR="$TMP_ROOT/stub-bin"
mkdir -p "$STUB_DIR"
cat > "$STUB_DIR/openclaw" <<'STUB'
#!/usr/bin/env sh
exit 1
STUB
chmod +x "$STUB_DIR/openclaw"

# Emit an L5 event with push enabled (turn off the test-wide disable), but via the stub.
"$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={'file_name':'TOOLS.md','source':'/fake/TOOLS.md','old_hash':'a','new_hash':'b','diff':{'unified_diff':'+ exec()'}},
    level=5, reason='push-fail-test', rule_hits=['自动执行外部命令'],
    added=1, removed=0, target_path='/fake/TOOLS.md',
)
PYEOF
env -u NO0_DLC_DISABLE_PUSH PATH="$STUB_DIR:/usr/bin:/bin" \
  "$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1

check "push_failures.log written"                  test -f "$HOME/.openclaw/no0/dlc/push_failures.log"
grep -q "TOOLS.md" "$HOME/.openclaw/no0/dlc/push_failures.log"
check "push failure logged with target"            test $? -eq 0
grep -q "push_failed_rc1" "$HOME/.openclaw/no0/dlc/audit.csv"
check "audit records push_failed_rc1"              test $? -eq 0
# decide status surfaces the failure
out=$("$LINK_TARGET/no0" decide TOOLS.md status 2>&1)
echo "$out" | grep -qE "prior push failure|推送失败"
check "decide status surfaces failure"             test $? -eq 0

# Now make the stub succeed — next sweep should retry and recover.
cat > "$STUB_DIR/openclaw" <<'STUB'
#!/usr/bin/env sh
exit 0
STUB
chmod +x "$STUB_DIR/openclaw"

env -u NO0_DLC_DISABLE_PUSH PATH="$STUB_DIR:/usr/bin:/bin" \
  "$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1

check "push_failures.log drained after recovery"   test ! -f "$HOME/.openclaw/no0/dlc/push_failures.log"

# Cleanup — release the lock so later tests stay clean
"$LINK_TARGET/no0" decide TOOLS.md keep >/dev/null 2>&1

# =====================================================================
section "Test 10 — Core-only direct push + decide rollback error UX"
# =====================================================================
# Verify NO0_CORE_DIRECT_PUSH=1 actually invokes openclaw. Use a capturing
# stub so we can assert what was called.
rm -rf "$HOME/.openclaw/no0/events/pending"/* 2>/dev/null
STUB_OUT="$TMP_ROOT/stub.log"
cat > "$STUB_DIR/openclaw" <<STUB
#!/usr/bin/env sh
printf 'CALL: %s\n' "\$*" >> "$STUB_OUT"
exit 0
STUB
chmod +x "$STUB_DIR/openclaw"
: > "$STUB_OUT"

NO0_CORE_DIRECT_PUSH=1 PATH="$STUB_DIR:/usr/bin:/bin" "$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={'file_name':'AGENTS.md','source':'/fake/AGENTS.md','old_hash':'a','new_hash':'b','diff':{'unified_diff':'+ exec()'}},
    level=5, reason='direct-push-test', rule_hits=['自动执行外部命令'],
    added=1, removed=0, target_path='/fake/AGENTS.md',
)
PYEOF
grep -q "system event" "$STUB_OUT"
check "Core direct push invoked openclaw"          test $? -eq 0
grep -q -- "--mode now" "$STUB_OUT"
check "direct push used --mode now"                test $? -eq 0

# Default (no env var) should NOT invoke openclaw
: > "$STUB_OUT"
PATH="$STUB_DIR:/usr/bin:/bin" "$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={'file_name':'MEMORY.md','source':'/fake/MEMORY.md','old_hash':'a','new_hash':'b','diff':{'unified_diff':'+ exec()'}},
    level=5, reason='direct-push-off', rule_hits=['自动执行外部命令'],
    added=1, removed=0, target_path='/fake/MEMORY.md',
)
PYEOF
check "no direct push without env gate"            test ! -s "$STUB_OUT"

# decide rollback with bogus version: should fail AND print available versions
# First recreate a fake lock for a real file (AGENTS.md is in baseline)
rm -rf "$HOME/.openclaw/no0/dlc/pending_decisions"/* 2>/dev/null
"$PY" - <<PYEOF
import json, os
from pathlib import Path
d = Path(os.path.expanduser('~/.openclaw/no0/dlc/pending_decisions'))
d.mkdir(parents=True, exist_ok=True)
(d / 'AGENTS.md.lock').write_text(json.dumps({
    'event_id':'test','target_file':'AGENTS.md','severity':'level_5',
    'pushed_at':'2026-04-20T00:00:00Z','rule_hits':['自动执行外部命令'],
    'versions_blob':'v1 v2',
}, ensure_ascii=False))
PYEOF
out=$("$LINK_TARGET/no0" decide AGENTS.md rollback v999 2>&1 || true)
echo "$out" | grep -qE "rollback failed|回滚失败"
check "bogus rollback fails clearly"               test $? -eq 0
check "lock still present after failed rollback"   test -f "$HOME/.openclaw/no0/dlc/pending_decisions/AGENTS.md.lock"
# Cleanup
rm -f "$HOME/.openclaw/no0/dlc/pending_decisions/AGENTS.md.lock"

# =====================================================================
section "Test 11 — EN/ZH i18n (NO0_LANG switch)"
# =====================================================================
# Seed a fresh L5 lock so decide/report have something to render.
rm -rf "$HOME/.openclaw/no0/dlc/pending_decisions"/* 2>/dev/null
"$PY" - <<PYEOF
import json, os
from pathlib import Path
d = Path(os.path.expanduser('~/.openclaw/no0/dlc/pending_decisions'))
d.mkdir(parents=True, exist_ok=True)
(d / 'SOUL.md.lock').write_text(json.dumps({
    'event_id':'i18n-test','target_file':'SOUL.md','severity':'level_5',
    'pushed_at':'2026-04-20T00:00:00Z','rule_hits':['自动执行外部命令'],
    'versions_blob':'v1 v2',
}, ensure_ascii=False))
PYEOF

# EN path: NO0_LANG=en, LANG ignored.
out_en=$(NO0_LANG=en "$LINK_TARGET/no0" decide SOUL.md status 2>&1)
echo "$out_en" | grep -q "No pending decision" && fail "decide status should find lock (en path broken)" || pass "decide status sees lock regardless of lang"
# decide status for an un-locked file should show EN wording
out_en2=$(NO0_LANG=en "$LINK_TARGET/no0" decide NOT_A_FILE.md status 2>&1)
echo "$out_en2" | grep -q "No pending decision"
check "decide status renders English when NO0_LANG=en"    test $? -eq 0

# ZH path for the same file.
out_zh=$(NO0_LANG=zh "$LINK_TARGET/no0" decide NOT_A_FILE.md status 2>&1)
echo "$out_zh" | grep -q "无待处置决定"
check "decide status renders Chinese when NO0_LANG=zh"    test $? -eq 0

# hourly report in English.
"$LINK_TARGET/no0" report --reset >/dev/null 2>&1
report_en=$(NO0_LANG=en "$LINK_TARGET/no0" report 2>&1)
echo "$report_en" | grep -q "outstanding L5 lock"
check "hourly report renders English"                     test $? -eq 0
echo "$report_en" | grep -q "Resolve with: ./no0 decide"
check "hourly report hint line English"                   test $? -eq 0

# LANG fallback: unset NO0_LANG, set LANG=en_US → still English.
"$LINK_TARGET/no0" report --reset >/dev/null 2>&1
report_lang=$(env -u NO0_LANG LANG=en_US.UTF-8 "$LINK_TARGET/no0" report 2>&1)
echo "$report_lang" | grep -q "outstanding L5 lock"
check "LANG=en_US fallback → English"                     test $? -eq 0

# LANG=zh_CN fallback → Chinese.
"$LINK_TARGET/no0" report --reset >/dev/null 2>&1
report_lang_zh=$(env -u NO0_LANG LANG=zh_CN.UTF-8 "$LINK_TARGET/no0" report 2>&1)
echo "$report_lang_zh" | grep -q "未处置 L5 锁"
check "LANG=zh_CN fallback → Chinese"                     test $? -eq 0

# L5 push alert text picks up NO0_LANG=en
rm -rf "$HOME/.openclaw/no0/events/pending"/* 2>/dev/null
rm -rf "$HOME/.openclaw/no0/dlc/pending_decisions"/* 2>/dev/null
PUSH_CAPTURE="$TMP_ROOT/push_en.log"
cat > "$STUB_DIR/openclaw" <<STUB
#!/usr/bin/env sh
printf '%s\n' "\$*" >> "$PUSH_CAPTURE"
exit 0
STUB
chmod +x "$STUB_DIR/openclaw"
: > "$PUSH_CAPTURE"

NO0_LANG=en "$PY" - <<PYEOF
import sys
sys.path.insert(0, r'$LINK_TARGET/no0-core/scripts')
from event_emitter import emit_tamper_event
emit_tamper_event(
    event_payload={'file_name':'HEARTBEAT.md','source':'/fake/HEARTBEAT.md','old_hash':'a','new_hash':'b','diff':{'unified_diff':'+ exec()'}},
    level=5, reason='i18n-en-test', rule_hits=['自动执行外部命令'],
    added=1, removed=0, target_path='/fake/HEARTBEAT.md',
)
PYEOF
env -u NO0_DLC_DISABLE_PUSH NO0_LANG=en PATH="$STUB_DIR:/usr/bin:/bin" \
  "$PY" "$LINK_TARGET/no0-dlc-internal-control/event_listener/cognitive_event_handler.py" --once >/dev/null 2>&1

grep -q "URGENT: L5 cognitive file tampering" "$PUSH_CAPTURE"
check "L5 push uses English header under NO0_LANG=en"     test $? -eq 0
grep -q "Reply 'rollback v" "$PUSH_CAPTURE"
check "L5 push uses English prompt under NO0_LANG=en"     test $? -eq 0
# Cleanup
rm -f "$HOME/.openclaw/no0/dlc/pending_decisions/HEARTBEAT.md.lock"
rm -f "$HOME/.openclaw/no0/dlc/pending_decisions/SOUL.md.lock"

# =====================================================================
# Summary
# =====================================================================
echo
printf 'Results: %s / %d passed\n' "$(green "$PASS")" "$((PASS+FAIL))"
if [ "$FAIL" -gt 0 ]; then
  echo "Failures:"
  for note in "${FAIL_NOTES[@]}"; do echo "  - $note"; done
  exit 1
fi
exit 0
