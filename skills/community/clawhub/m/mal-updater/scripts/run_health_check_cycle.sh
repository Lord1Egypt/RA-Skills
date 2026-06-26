#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

eval "$(PYTHONPATH=src python3 - <<'PY'
from shlex import quote
from mal_updater.config import load_config
config = load_config()
print(f"RUNTIME_ROOT={quote(str(config.runtime_root))}")
print(f"LOCK_DIR={quote(str(config.state_dir / 'locks'))}")
print(f"LOG_DIR={quote(str(config.state_dir / 'logs'))}")
print(f"HEALTH_DIR={quote(str(config.state_dir / 'health'))}")
PY
)"

LOCK_FILE="$LOCK_DIR/health-check.lock"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_LOG="$LOG_DIR/health-check-$STAMP.log"
RUN_JSON="$HEALTH_DIR/health-check-$STAMP.json"
LATEST_JSON="$HEALTH_DIR/latest-health-check.json"
STALE_HOURS="${MAL_UPDATER_HEALTH_STALE_HOURS:-72}"
STRICT_MODE="${MAL_UPDATER_HEALTH_STRICT:-0}"
AUTO_RUN_RECOMMENDED="${MAL_UPDATER_HEALTH_AUTO_RUN_RECOMMENDED:-0}"
AUTO_RUN_REASON_CODES="${MAL_UPDATER_HEALTH_AUTO_RUN_REASON_CODES:-refresh_ingested_snapshot,refresh_full_snapshot}"

mkdir -p "$LOCK_DIR" "$LOG_DIR" "$HEALTH_DIR"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "[$(date -Is)] health-check already running; skipping overlap"
  exit 0
fi

exec > >(tee -a "$RUN_LOG") 2>&1

run_health_check() {
  PYTHONPATH=src python3 -m mal_updater.cli health-check --stale-hours "$STALE_HOURS" | tee "$RUN_JSON" >/dev/null
  cp "$RUN_JSON" "$LATEST_JSON"
}

echo "[$(date -Is)] starting MAL-Updater health-check cycle"
echo "root=$ROOT_DIR"
echo "runtime_root=$RUNTIME_ROOT"
echo "log=$RUN_LOG"
echo "health_json=$RUN_JSON"
echo "stale_hours=$STALE_HOURS"
echo "auto_run_recommended=$AUTO_RUN_RECOMMENDED"
echo "auto_run_reason_codes=$AUTO_RUN_REASON_CODES"

PYTHONPATH=src python3 -m mal_updater.cli init >/dev/null
run_health_check

python3 - "$RUN_JSON" "$AUTO_RUN_RECOMMENDED" "$AUTO_RUN_REASON_CODES" <<'PY'
import json
import shlex
import subprocess
import sys
from pathlib import Path

json_path = Path(sys.argv[1])
auto_run_enabled = sys.argv[2] == "1"
allowed_reason_codes = {
    item.strip()
    for item in sys.argv[3].split(",")
    if item.strip()
}
payload = json.loads(json_path.read_text(encoding="utf-8"))
maintenance = payload.get("maintenance") if isinstance(payload.get("maintenance"), dict) else {}
recommended_commands = maintenance.get("recommended_commands") if isinstance(maintenance.get("recommended_commands"), list) else []
recommended_command = maintenance.get("recommended_command") if isinstance(maintenance.get("recommended_command"), dict) else None
recommended_auto_command = (
    maintenance.get("recommended_automation_command")
    if isinstance(maintenance.get("recommended_automation_command"), dict)
    else None
)

selected = None
if auto_run_enabled:
    for item in recommended_commands:
        if not isinstance(item, dict):
            continue
        reason_code = item.get("reason_code")
        command_args = item.get("command_args")
        automation_safe = item.get("automation_safe") is True
        requires_auth_interaction = item.get("requires_auth_interaction") is True
        if reason_code not in allowed_reason_codes:
            continue
        if not automation_safe or requires_auth_interaction:
            continue
        if not isinstance(command_args, list) or not all(isinstance(part, str) and part for part in command_args):
            continue
        first_arg = command_args[0]
        execution_mode = "cli"
        if first_arg.startswith("/") or "/" in first_arg or first_arg.endswith(".sh"):
            execution_mode = "direct"
        selected = {
            "reason_code": reason_code,
            "command_args": command_args,
            "execution_mode": execution_mode,
        }
        break

if selected is None:
    if auto_run_enabled:
        print("auto_remediation=enabled")
        if isinstance(recommended_command, dict) and recommended_command.get("reason_code"):
            print("auto_remediation_recommended_reason_code=" + str(recommended_command["reason_code"]))
        if isinstance(recommended_auto_command, dict) and recommended_auto_command.get("reason_code"):
            print("auto_remediation_safe_candidate_reason_code=" + str(recommended_auto_command["reason_code"]))
        if isinstance(recommended_auto_command, dict) and recommended_auto_command.get("reason_code") not in allowed_reason_codes:
            print("auto_remediation_action=skipped_not_allowlisted")
        else:
            print("auto_remediation_action=none")
    else:
        print("auto_remediation=disabled")
    sys.exit(0)

env = dict(__import__("os").environ)
execution_mode = selected.get("execution_mode")
if execution_mode == "direct":
    command = selected["command_args"]
    command_display = " ".join(shlex.quote(part) for part in command)
    subprocess_env = env
else:
    command = ["python3", "-m", "mal_updater.cli", *selected["command_args"]]
    command_display = "PYTHONPATH=src " + " ".join(shlex.quote(part) for part in command)
    subprocess_env = {**env, "PYTHONPATH": "src"}

print("auto_remediation=enabled")
print("auto_remediation_reason_code=" + selected["reason_code"])
print("auto_remediation_command=" + command_display)
subprocess.run(command, check=True, env=subprocess_env)
print("auto_remediation_result=completed")
PY

if [[ "$AUTO_RUN_RECOMMENDED" == "1" ]]; then
  echo "[$(date -Is)] re-running health-check after optional remediation"
  run_health_check
fi

python3 - "$RUN_JSON" "$STRICT_MODE" <<'PY'
import json
import sys
from pathlib import Path

json_path = Path(sys.argv[1])
strict_mode = sys.argv[2] == "1"
payload = json.loads(json_path.read_text(encoding="utf-8"))
warnings = payload.get("warnings") if isinstance(payload.get("warnings"), list) else []
warning_codes = [item.get("code") for item in warnings if isinstance(item, dict) and item.get("code")]
review_queue = payload.get("review_queue") if isinstance(payload.get("review_queue"), dict) else {}
recommended_next = review_queue.get("recommended_next") if isinstance(review_queue.get("recommended_next"), dict) else None
recommended_worklist = review_queue.get("recommended_worklist") if isinstance(review_queue.get("recommended_worklist"), list) else []
recommended_apply_worklist = review_queue.get("recommended_apply_worklist") if isinstance(review_queue.get("recommended_apply_worklist"), dict) else None
maintenance = payload.get("maintenance") if isinstance(payload.get("maintenance"), dict) else {}
recommended_commands = maintenance.get("recommended_commands") if isinstance(maintenance.get("recommended_commands"), list) else []
recommended_auto_command = (
    maintenance.get("recommended_automation_command")
    if isinstance(maintenance.get("recommended_automation_command"), dict)
    else None
)

print(f"healthy={bool(payload.get('healthy'))}")
print(f"warning_count={len(warnings)}")
mappings = payload.get("mappings") if isinstance(payload.get("mappings"), dict) else {}
mapping_coverage = mappings.get("coverage") if isinstance(mappings.get("coverage"), dict) else None
if isinstance(mapping_coverage, dict):
    approved_count = mapping_coverage.get("approved_mapping_count")
    provider_series_count = mapping_coverage.get("provider_series_count")
    coverage_ratio = mapping_coverage.get("approved_coverage_ratio")
    if isinstance(approved_count, int) and isinstance(provider_series_count, int):
        if isinstance(coverage_ratio, float):
            print(
                "approved_mapping_coverage="
                + f"{approved_count}/{provider_series_count} ({coverage_ratio * 100:.1f}%)"
            )
        else:
            print(f"approved_mapping_coverage={approved_count}/{provider_series_count}")
if warning_codes:
    print("warnings=" + ", ".join(str(code) for code in warning_codes))
if recommended_commands:
    top_command = recommended_commands[0]
    if isinstance(top_command, dict) and top_command.get("command"):
        print("maintenance_recommended_command=" + str(top_command["command"]))
if isinstance(recommended_auto_command, dict) and recommended_auto_command.get("command"):
    print("maintenance_recommended_auto_command=" + str(recommended_auto_command["command"]))
if recommended_next:
    command = recommended_next.get("drilldown_command")
    if command:
        print("recommended_next=" + str(command))
if recommended_apply_worklist and recommended_apply_worklist.get("command"):
    print("recommended_apply_worklist=" + str(recommended_apply_worklist["command"]))
if recommended_worklist:
    top = recommended_worklist[0]
    if isinstance(top, dict):
        action_command = top.get("action_command")
        if action_command:
            print("recommended_action=" + str(action_command))
        if top.get("resolve_command"):
            print("recommended_resolve=" + str(top["resolve_command"]))

if strict_mode and warnings:
    sys.exit(2)
PY

echo "[$(date -Is)] MAL-Updater health-check cycle completed"
