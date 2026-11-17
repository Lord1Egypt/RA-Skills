#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(git -C "$SKILL_DIR" rev-parse --show-toplevel 2>/dev/null || realpath "$SKILL_DIR/../..")"
HOOKS_JSON="${PROJECT_ROOT}/.trae/hooks.json"
SYNC_SCRIPT="${SKILL_DIR}/scripts/sync.sh"

mkdir -p "$(dirname "$HOOKS_JSON")"
[ -f "$HOOKS_JSON" ] || printf '%s\n' '{}' > "$HOOKS_JSON"

HOOKS_JSON="$HOOKS_JSON" SYNC_SCRIPT="$SYNC_SCRIPT" PROJECT_ROOT="$PROJECT_ROOT" python3 <<'PY'
import json
import os

hooks_path = os.environ["HOOKS_JSON"]
script = os.environ["SYNC_SCRIPT"]
workspace = os.environ["PROJECT_ROOT"]

with open(hooks_path, "r", encoding="utf-8") as source:
    config = json.load(source)
if not isinstance(config, dict):
    raise SystemExit("hooks.json must contain a JSON object")

hooks = config.setdefault("hooks", {})
if not isinstance(hooks, dict):
    raise SystemExit("hooks.json field 'hooks' must contain an object")

for event, mode in (("UserPromptSubmit", "user"), ("Stop", "assistant")):
    command = f'bash "{script}" --event {mode}'
    entries = hooks.setdefault(event, [])
    if not isinstance(entries, list):
        raise SystemExit(f"hooks.{event} must contain an array")
    entries[:] = [
        entry for entry in entries
        if not any(
            any(name in str(hook.get("command", "")) for name in ("session-notebook", "conversation-archive"))
            for hook in entry.get("hooks", []) if isinstance(hook, dict)
        )
    ]
    entries.append({
        "matcher": ".*",
        "hooks": [{"type": "command", "command": command, "timeout": 30}],
    })

with open(hooks_path, "w", encoding="utf-8") as output:
    json.dump(config, output, indent=2, ensure_ascii=False)
    output.write("\n")
PY

chmod +x "$SYNC_SCRIPT"
printf 'Installed conversation-archive hooks in %s\n' "$HOOKS_JSON"
