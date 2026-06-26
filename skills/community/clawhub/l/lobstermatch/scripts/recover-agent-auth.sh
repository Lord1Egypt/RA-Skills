#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"

MODE="list"
AGENT_ID=""
RESTORE_LATEST="0"

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/recover-agent-auth.sh --list
  scripts/recover-agent-auth.sh --restore --agent-id agent-55 --latest

Searches safe local LobsterMatch auth backup locations, prints redacted metadata,
and restores only the requested same agentId. It never prints raw tokens.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --list)
      MODE="list"
      shift
      ;;
    --restore)
      MODE="restore"
      shift
      ;;
    --agent-id)
      AGENT_ID="${2:-}"
      shift 2
      ;;
    --latest)
      RESTORE_LATEST="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      printf 'LobsterMatch auth recovery error: unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
done

python3 - "$MODE" "$AGENT_ID" "$RESTORE_LATEST" "$(lm_auth_root)" "$(lm_workspace_root)" "$(lm_skill_dir)" <<'PY'
import json
import os
import shutil
import stat
import sys
from pathlib import Path

mode, requested_agent_id, restore_latest, auth_root_raw, workspace_raw, skill_raw = sys.argv[1:7]
auth_root = Path(os.path.expanduser(auth_root_raw)).resolve()
workspace = Path(os.path.expanduser(workspace_raw)).resolve()
skill_dir = Path(os.path.expanduser(skill_raw)).resolve()

search_roots = [
    workspace / ".lobstermatch" / "backups",
    auth_root / "backups",
    auth_root / "agents",
    skill_dir / ".lobstermatch" / "backups",
    skill_dir,
]
seen_files = set()

def load(path):
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, dict) else None
    except Exception:
        return None

def is_pointer(data):
    return str(data.get("type") or "").startswith("lobstermatch-agent-auth-pointer")

def agent_id(data):
    auth = data.get("agentSessionAuth") if isinstance(data.get("agentSessionAuth"), dict) else {}
    return str(data.get("agentId") or auth.get("agentId") or "").strip()

def token_present(data):
    auth = data.get("agentSessionAuth") if isinstance(data.get("agentSessionAuth"), dict) else {}
    return bool(str(data.get("agentSessionToken") or auth.get("agentSessionToken") or "").strip())

def candidate_files(root):
    if not root.exists():
        return []
    if root.is_file():
        return [root]
    files = []
    for pattern in ("*.json", "*/agent-auth.json", ".lobstermatch-agent.json"):
        files.extend(root.glob(pattern))
    return [path for path in files if path.is_file()]

def inspect(path):
    data = load(path)
    if data and is_pointer(data):
        state_path = str(data.get("statePath") or data.get("persistentAuthPath") or "").strip()
        pointed = Path(state_path)
        if state_path and not pointed.is_absolute():
            pointed = (path.parent / pointed).resolve()
        pointed_data = load(pointed) if state_path else None
        return {
            "path": str(path),
            "statePath": str(pointed) if state_path else "",
            "agentId": agent_id(pointed_data or data),
            "validJson": True,
            "containsToken": token_present(pointed_data or {}),
            "isPointer": True,
            "mtime": path.stat().st_mtime,
            "restoreSource": str(pointed) if pointed_data else "",
        }
    return {
        "path": str(path),
        "statePath": "",
        "agentId": agent_id(data or {}),
        "validJson": bool(data),
        "containsToken": token_present(data or {}),
        "isPointer": False,
        "mtime": path.stat().st_mtime,
        "restoreSource": str(path) if data else "",
    }

candidates = []
for root in search_roots:
    for path in candidate_files(root):
        resolved = str(path.resolve())
        if resolved in seen_files:
            continue
        seen_files.add(resolved)
        item = inspect(path.resolve())
        if item["validJson"] and item["agentId"]:
            candidates.append(item)

candidates.sort(key=lambda item: item["mtime"], reverse=True)

if mode == "list":
    print("LobsterMatch auth recovery candidates")
    print(f"persistentAuthRoot: {auth_root}")
    print(f"candidateCount: {len(candidates)}")
    for index, item in enumerate(candidates, 1):
        print(f"candidate[{index}].agentId: {item['agentId']}")
        print(f"candidate[{index}].validJson: {str(item['validJson']).lower()}")
        print(f"candidate[{index}].containsToken: {str(item['containsToken']).lower()}")
        print(f"candidate[{index}].isPointer: {str(item['isPointer']).lower()}")
        print(f"candidate[{index}].mtime: {int(item['mtime'])}")
        print(f"candidate[{index}].path: {item['path']}")
    print("rawTokenPrinted: false")
    if candidates:
        print("nextStep: Restore a same-agent candidate with --restore --agent-id <agent-id> --latest; do not register a duplicate profile.")
    else:
        print("nextStep: No local recovery candidates found. Use scripts/bootstrap-agent-auth.sh with same-agent proof, not duplicate registration.")
    raise SystemExit(0)

if not requested_agent_id:
    raise SystemExit("restore requires --agent-id")
matching = [item for item in candidates if item["agentId"] == requested_agent_id and item["containsToken"] and item["restoreSource"]]
if not matching:
    print(json.dumps({
        "restored": False,
        "agentId": requested_agent_id,
        "reason": "no-same-agent-token-candidate-found",
        "rawTokenPrinted": False,
        "nextStep": "Run scripts/bootstrap-agent-auth.sh with same-agent proof; do not register a duplicate profile.",
    }, indent=2))
    raise SystemExit(0)
if len(matching) > 1:
    print(f"warning: multiple same-agent recovery candidates found for {requested_agent_id}; latest selected only because --latest was supplied.")
if restore_latest != "1":
    print(json.dumps({
        "restored": False,
        "agentId": requested_agent_id,
        "reason": "multiple-safe-candidates-require---latest",
        "candidateCount": len(matching),
        "rawTokenPrinted": False,
    }, indent=2))
    raise SystemExit(0)
source = Path(matching[0]["restoreSource"])
target = auth_root / "agents" / requested_agent_id / "agent-auth.json"
if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
    print(json.dumps({
        "restored": False,
        "agentId": requested_agent_id,
        "reason": "newer-persistent-config-not-overwritten",
        "targetPath": str(target),
        "rawTokenPrinted": False,
    }, indent=2))
    raise SystemExit(0)
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(source, target)
os.chmod(target, stat.S_IRUSR | stat.S_IWUSR)
print(json.dumps({
    "restored": True,
    "agentId": requested_agent_id,
    "targetPath": str(target),
    "containsToken": True,
    "mode": oct(target.stat().st_mode & 0o777),
    "rawTokenPrinted": False,
    "nextStep": "Run scripts/agent-auth-status.sh.",
}, indent=2))
PY
