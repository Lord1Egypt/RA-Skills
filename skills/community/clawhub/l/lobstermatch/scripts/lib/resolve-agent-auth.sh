#!/usr/bin/env bash
# Shared local auth resolver for LobsterMatch ClawHub/OpenClaw skill scripts.
# It never prints raw runtime tokens.

lm_script_dir() {
  local source_path="${BASH_SOURCE[0]}"
  local dir
  dir="$(cd "$(dirname "$source_path")/.." && pwd)"
  printf '%s\n' "$dir"
}

lm_skill_dir() {
  local scripts_dir
  scripts_dir="$(lm_script_dir)"
  cd "$scripts_dir/.." && pwd
}

lm_workspace_root() {
  if [ -n "${LOBSTERMATCH_WORKSPACE_ROOT:-}" ]; then
    printf '%s\n' "$LOBSTERMATCH_WORKSPACE_ROOT"
    return 0
  fi
  local skill_dir parent grandparent
  skill_dir="$(lm_skill_dir)"
  parent="$(dirname "$skill_dir")"
  grandparent="$(dirname "$parent")"
  if [ "$(basename "$parent")" = "skills" ]; then
    printf '%s\n' "$grandparent"
    return 0
  fi
  printf '%s\n' "$(pwd)"
}

lm_auth_root() {
  if [ -n "${LOBSTERMATCH_AUTH_ROOT:-}" ]; then
    printf '%s\n' "$LOBSTERMATCH_AUTH_ROOT"
    return 0
  fi
  printf '%s/.lobstermatch\n' "$(lm_workspace_root)"
}

lm_legacy_auth_path() {
  if [ -n "${LOBSTERMATCH_LEGACY_AGENT_CONFIG:-}" ]; then
    printf '%s\n' "$LOBSTERMATCH_LEGACY_AGENT_CONFIG"
    return 0
  fi
  printf '%s/.lobstermatch-agent.json\n' "$(lm_skill_dir)"
}

lm_explicit_auth_path() {
  if [ -n "${LOBSTERMATCH_AGENT_AUTH_PATH:-}" ]; then
    printf '%s\n' "$LOBSTERMATCH_AGENT_AUTH_PATH"
    return 0
  fi
  if [ -n "${LOBSTERMATCH_AGENT_CONFIG:-}" ]; then
    printf '%s\n' "$LOBSTERMATCH_AGENT_CONFIG"
    return 0
  fi
  printf '\n'
}

lm_auth_state_json() {
  python3 - "$(lm_auth_root)" "$(lm_legacy_auth_path)" "$(lm_explicit_auth_path)" <<'PY'
import json
import os
import shutil
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(os.path.expanduser(sys.argv[1])).resolve()
legacy_path = Path(os.path.expanduser(sys.argv[2])).resolve()
explicit_raw = str(sys.argv[3] or "").strip()
explicit_path = Path(os.path.expanduser(explicit_raw)).resolve() if explicit_raw else None
backup_dir = root / "backups"

def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def load_json(path):
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            return None, "json-not-object"
        return data, ""
    except FileNotFoundError:
        return None, "missing"
    except Exception as exc:
        return None, f"json-invalid:{exc.__class__.__name__}"

def token_from(data):
    auth = data.get("agentSessionAuth") if isinstance(data.get("agentSessionAuth"), dict) else {}
    return str(data.get("agentSessionToken") or auth.get("agentSessionToken") or "").strip()

def is_pointer(data):
    return str(data.get("type") or "").startswith("lobstermatch-agent-auth-pointer")

def agent_id_from(data):
    return str(data.get("agentId") or (data.get("agentSessionAuth") or {}).get("agentId") or "").strip()

def valid_auth(data):
    return bool(data and agent_id_from(data) and token_from(data) and not is_pointer(data))

def persistent_path(agent_id):
    return root / "agents" / agent_id / "agent-auth.json"

def chmod_private(path):
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass

def write_json_private(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_umask = os.umask(0o177)
    try:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    finally:
        os.umask(previous_umask)
    chmod_private(path)

def copy_private(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    chmod_private(target)

def maybe_migrate(source_path, source_data, source_kind):
    result = {
        "migrated": False,
        "backupCreated": False,
        "pointerWritten": False,
        "reason": "",
    }
    agent_id = agent_id_from(source_data)
    target = persistent_path(agent_id)
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"lobstermatch-agent.{agent_id}.{utc_stamp()}.json"
    if source_path.exists() and valid_auth(source_data):
        copy_private(source_path, backup_path)
        result["backupCreated"] = True
    should_copy = True
    if target.exists():
        try:
            should_copy = source_path.stat().st_mtime > target.stat().st_mtime
        except Exception:
            should_copy = False
    if should_copy:
        copy_private(source_path, target)
        result["migrated"] = True
    else:
        result["reason"] = "persistent-config-is-newer-or-equal"
    if source_kind == "legacy" and source_path.exists() and source_path.resolve() != target.resolve():
        pointer = {
            "type": "lobstermatch-agent-auth-pointer",
            "agentId": agent_id,
            "statePath": os.path.relpath(target, source_path.parent),
            "migratedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "message": "Private LobsterMatch agent auth moved outside the replaceable skill folder.",
        }
        write_json_private(source_path, pointer)
        result["pointerWritten"] = True
    result["targetPath"] = str(target)
    return result

def candidate_from_path(path, kind):
    if not path or not path.exists():
        return None
    data, error = load_json(path)
    if not data:
        return {"path": str(path), "kind": kind, "ok": False, "error": error}
    if is_pointer(data):
        state_path = str(data.get("statePath") or data.get("persistentAuthPath") or "").strip()
        if state_path:
            pointed = Path(state_path)
            if not pointed.is_absolute():
                pointed = (path.parent / pointed).resolve()
            pointed_data, pointed_error = load_json(pointed)
            return {
                "path": str(pointed),
                "kind": "pointer",
                "ok": valid_auth(pointed_data),
                "error": pointed_error if not valid_auth(pointed_data) else "",
                "data": pointed_data,
                "sourcePath": str(path),
            }
    return {
        "path": str(path),
        "kind": kind,
        "ok": valid_auth(data),
        "error": "" if valid_auth(data) else "auth-incomplete",
        "data": data,
    }

changes = {"migrated": False, "backupCreated": False, "pointerWritten": False}

source_candidates = []
if explicit_path:
    source_candidates.append(candidate_from_path(explicit_path, "explicit"))
source_candidates.append(candidate_from_path(legacy_path, "legacy"))
source_candidates = [item for item in source_candidates if item]

for item in source_candidates:
    if not item.get("ok"):
        continue
    source_path = Path(item.get("sourcePath") or item["path"])
    source_kind = "legacy" if source_path.resolve() == legacy_path.resolve() else item["kind"]
    if source_kind in {"legacy", "explicit"}:
        migrated = maybe_migrate(source_path, item["data"], source_kind)
        for key in changes:
            changes[key] = changes[key] or migrated.get(key, False)
        break

persistent_candidates = []
agents_dir = root / "agents"
if agents_dir.exists():
    for path in agents_dir.glob("*/agent-auth.json"):
        item = candidate_from_path(path, "persistent")
        if item and item.get("ok"):
            persistent_candidates.append(item)

for item in source_candidates:
    if item.get("ok"):
        agent_id = agent_id_from(item["data"])
        target = persistent_path(agent_id)
        persistent = candidate_from_path(target, "persistent")
        if persistent and persistent.get("ok"):
            persistent_candidates.append(persistent)

seen = {}
for item in persistent_candidates:
    seen[item["path"]] = item
persistent_candidates = list(seen.values())
persistent_candidates.sort(key=lambda item: Path(item["path"]).stat().st_mtime if Path(item["path"]).exists() else 0, reverse=True)

selected = persistent_candidates[0] if persistent_candidates else None
if selected:
    data = selected["data"]
    print(json.dumps({
        "ok": True,
        "configPath": selected["path"],
        "configSource": selected["kind"],
        "persistentAuthRoot": str(root),
        "legacyPath": str(legacy_path),
        "agentId": agent_id_from(data),
        "baseUrl": str(data.get("baseUrl") or "https://lobstermatch.com").rstrip("/"),
        "tokenPresent": bool(token_from(data)),
        "migrated": changes["migrated"],
        "backupCreated": changes["backupCreated"],
        "pointerWritten": changes["pointerWritten"],
        "rawTokenPrinted": False,
        "nextStep": "Use LobsterMatch runtime helpers with the persistent local auth config.",
    }))
    raise SystemExit(0)

print(json.dumps({
    "ok": False,
    "configPath": "",
    "configSource": "missing",
    "persistentAuthRoot": str(root),
    "legacyPath": str(legacy_path),
    "agentId": "",
    "tokenPresent": False,
    "migrated": changes["migrated"],
    "backupCreated": changes["backupCreated"],
    "pointerWritten": changes["pointerWritten"],
    "rawTokenPrinted": False,
    "nextStep": "No local LobsterMatch agent auth config was found. If this is an existing agent, run scripts/recover-agent-auth.sh before registering again.",
}))
PY
}

lm_resolve_agent_auth_path() {
  lm_auth_state_json | python3 -c 'import json,sys; data=json.load(sys.stdin); print(data.get("configPath") or "")'
}

lm_print_auth_recovery_instructions() {
  cat >&2 <<'EOF'
No local LobsterMatch runtime auth was found.

If this is an existing agent, do not register a duplicate profile.
Try:
  bash ./scripts/recover-agent-auth.sh --list
  bash ./scripts/recover-agent-auth.sh --restore --agent-id <agent-id>
  bash ./scripts/agent-auth-status.sh
EOF
}
