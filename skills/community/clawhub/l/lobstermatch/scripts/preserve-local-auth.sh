#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"

ACTION="${1:-status}"

fail() {
  printf 'LobsterMatch local auth preservation error: %s\n' "$1" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required"
}

usage() {
  cat >&2 <<'EOF'
Usage:
  bash ./scripts/preserve-local-auth.sh backup
  bash ./scripts/preserve-local-auth.sh restore
  bash ./scripts/preserve-local-auth.sh status

This helper migrates private LobsterMatch agent auth outside the replaceable
ClawHub/OpenClaw skill folder. It never prints raw tokens.
EOF
}

case "$ACTION" in
  backup|pre-update|restore|post-update|status|migrate) ;;
  *)
    usage
    exit 2
    ;;
esac

require_command python3

AUTH_STATE_JSON="$(lm_auth_state_json)"

python3 - "$ACTION" "$AUTH_STATE_JSON" "$(lm_auth_root)" <<'PY'
import json
import os
import shutil
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

action = sys.argv[1]
state = json.loads(sys.argv[2])
root = Path(os.path.expanduser(sys.argv[3])).resolve()
backup_dir = root / "backups"

def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def print_status(**items):
    for key, value in items.items():
        if isinstance(value, bool):
            value = str(value).lower()
        print(f"{key}: {value if value not in (None, '') else '-'}")

def load(path):
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, dict) else None
    except Exception:
        return None

def token_present(data):
    auth = data.get("agentSessionAuth") if isinstance(data.get("agentSessionAuth"), dict) else {}
    return bool(str(data.get("agentSessionToken") or auth.get("agentSessionToken") or "").strip())

def agent_id(data):
    auth = data.get("agentSessionAuth") if isinstance(data.get("agentSessionAuth"), dict) else {}
    return str(data.get("agentId") or auth.get("agentId") or "").strip()

def chmod_private(path):
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

def latest_backup(target_agent_id=""):
    if not backup_dir.exists():
        return None
    candidates = []
    for path in backup_dir.glob("lobstermatch-agent*.json"):
        if not path.is_file():
            continue
        data = load(path)
        if not data:
            continue
        if target_agent_id and agent_id(data) != target_agent_id:
            continue
        candidates.append(path)
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None

config_path = Path(state["configPath"]).resolve() if state.get("configPath") else None
config_data = load(config_path) if config_path and config_path.exists() else None
current_agent_id = agent_id(config_data) if config_data else state.get("agentId", "")

if action in {"backup", "pre-update", "migrate"}:
    if not config_path or not config_path.exists() or not config_data:
        print_status(
            action="backup",
            persistentAuthRoot=root,
            configExists=False,
            backupCreated=False,
            rawTokenPrinted=False,
            nextStep="No local auth config found. If this is an existing agent, run scripts/recover-agent-auth.sh before registering again.",
        )
        raise SystemExit(0)
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"lobstermatch-agent.{current_agent_id}.{utc_stamp()}.json"
    shutil.copy2(config_path, backup_path)
    chmod_private(backup_path)
    print_status(
        action="backup",
        persistentAuthRoot=root,
        configPath=config_path,
        configSource=state.get("configSource", ""),
        agentId=current_agent_id,
        agentIdPresent=bool(current_agent_id),
        tokenPresent=token_present(config_data),
        migrated=state.get("migrated") is True,
        pointerWritten=state.get("pointerWritten") is True,
        rawTokenPrinted=False,
        backupCreated=True,
        backupPath=backup_path,
        backupExists=backup_path.exists(),
    )
    raise SystemExit(0)

if action in {"restore", "post-update"}:
    if config_path and config_path.exists() and config_data:
        print_status(
            action="restore",
            persistentAuthRoot=root,
            configExists=True,
            restored=False,
            reason="persistent-auth-already-present",
            backupPreserved=True,
            agentId=current_agent_id,
            tokenPresent=token_present(config_data),
            rawTokenPrinted=False,
        )
        raise SystemExit(0)
    backup_path = latest_backup(current_agent_id)
    if not backup_path:
        backup_path = latest_backup("")
    if not backup_path:
        print_status(
            action="restore",
            persistentAuthRoot=root,
            backupFound=False,
            restored=False,
            rawTokenPrinted=False,
            nextStep="No backup found. Run scripts/recover-agent-auth.sh --list; do not register a duplicate profile.",
        )
        raise SystemExit(0)
    backup_data = load(backup_path)
    backup_agent_id = agent_id(backup_data or {})
    if not backup_agent_id:
        print_status(action="restore", backupFound=True, restored=False, reason="backup-agent-id-missing")
        raise SystemExit(1)
    target = root / "agents" / backup_agent_id / "agent-auth.json"
    if target.exists() and target.stat().st_mtime >= backup_path.stat().st_mtime:
        print_status(
            action="restore",
            persistentAuthRoot=root,
            backupFound=True,
            restored=False,
            reason="newer-persistent-config-not-overwritten",
            backupPreserved=True,
            agentId=backup_agent_id,
            rawTokenPrinted=False,
        )
        raise SystemExit(0)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup_path, target)
    chmod_private(target)
    print_status(
        action="restore",
        persistentAuthRoot=root,
        backupFound=True,
        backupPath=backup_path,
        configPath=target,
        restored=True,
        agentId=backup_agent_id,
        agentIdPresent=True,
        tokenPresent=token_present(backup_data or {}),
        rawTokenPrinted=False,
    )
    raise SystemExit(0)

print_status(
    action="status",
    persistentAuthRoot=root,
    configPath=config_path or "",
    configSource=state.get("configSource", ""),
    configExists=bool(config_path and config_path.exists()),
    agentId=current_agent_id or "",
    agentIdPresent=bool(current_agent_id),
    tokenPresent=token_present(config_data or {}),
    migrated=state.get("migrated") is True,
    backupDir=backup_dir,
    rawTokenPrinted=False,
    nextStep="Persistent auth is outside the replaceable skill folder. Run backup before skill updates and status after updates.",
)
PY
