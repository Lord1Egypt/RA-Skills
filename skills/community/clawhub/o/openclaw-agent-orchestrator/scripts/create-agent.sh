#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 <agent-id> <name> <emoji> [theme] [source-workspace]" >&2
  exit 1
}

[ "${1:-}" ] || usage
[ "${2:-}" ] || usage
[ "${3:-}" ] || usage

AGENT_ID="$1"
AGENT_NAME="$2"
AGENT_EMOJI="$3"
AGENT_THEME="${4:-default}"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
SOURCE_WORKSPACE="${5:-$OPENCLAW_HOME/workspace}"
TARGET_WORKSPACE="${OPENCLAW_HOME}/workspaces/${AGENT_ID}"

if [ ! -d "$SOURCE_WORKSPACE" ]; then
  echo "source workspace not found: $SOURCE_WORKSPACE" >&2
  exit 1
fi

python3 - "$SOURCE_WORKSPACE" "$TARGET_WORKSPACE" "$AGENT_NAME" "$AGENT_EMOJI" "$AGENT_THEME" <<'PY'
import os
import shutil
import sys
from pathlib import Path

src = Path(sys.argv[1]).expanduser()
dst = Path(sys.argv[2]).expanduser()
name = sys.argv[3]
emoji = sys.argv[4]
theme = sys.argv[5]

if dst.exists():
    shutil.rmtree(dst)
dst.mkdir(parents=True, exist_ok=True)

skip_names = {".git", ".DS_Store", "__pycache__"}

def ignored(name: str) -> bool:
    return name.startswith("._") or name.startswith("backup-") or name in skip_names

for current_root, dirnames, filenames in os.walk(src, topdown=True, onerror=lambda e: None):
    current = Path(current_root)
    rel = current.relative_to(src)
    target_dir = dst / rel
    target_dir.mkdir(parents=True, exist_ok=True)

    dirnames[:] = [name for name in dirnames if not ignored(name)]

    for filename in filenames:
        if ignored(filename):
            continue
        source_file = current / filename
        target_file = target_dir / filename
        try:
            shutil.copy2(source_file, target_file)
        except (PermissionError, OSError):
            continue

identity = dst / "IDENTITY.md"
identity.write_text(
    "\n".join(
        [
            "# IDENTITY.md - Who Am I?",
            "",
            f"- **Name:** {name}",
            "- **Creature:** AI assistant, evolving",
            f"- **Vibe:** {theme}",
            f"- **Emoji:** {emoji}",
            "",
        ]
    )
)
PY

if openclaw agents list --json | python3 -c '
import json
import sys
agent_id = sys.argv[1]
data = json.load(sys.stdin)
raise SystemExit(0 if any(item.get("id") == agent_id for item in data) else 1)
' "$AGENT_ID"
then
  echo "agent already exists, refreshing identity only: $AGENT_ID"
else
  openclaw agents add "$AGENT_ID" --workspace "$TARGET_WORKSPACE" --non-interactive --json
fi

openclaw agents set-identity --agent "$AGENT_ID" --workspace "$TARGET_WORKSPACE" --from-identity --json

openclaw agents list --json | python3 -c '
import json
import sys
agent_id = sys.argv[1]
data = json.load(sys.stdin)
for item in data:
    if item.get("id") == agent_id:
        print(json.dumps(item, indent=2))
        raise SystemExit(0)
print(f"agent not visible after add: {agent_id}", file=sys.stderr)
raise SystemExit(1)
' "$AGENT_ID"
