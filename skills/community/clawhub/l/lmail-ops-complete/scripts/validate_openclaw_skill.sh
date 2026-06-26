#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"

if [[ ! -f "$SKILL_MD" ]]; then
  echo "[ERR] missing SKILL.md at $SKILL_MD" >&2
  exit 1
fi

python3 - "$SKILL_MD" <<'PY'
import re
import sys
from pathlib import Path

skill_md = Path(sys.argv[1]).read_text(encoding="utf-8")
if not skill_md.startswith("---\n"):
    raise SystemExit("[ERR] SKILL.md must start with YAML frontmatter delimiter '---'")

parts = skill_md.split("\n---\n", 1)
if len(parts) != 2:
    raise SystemExit("[ERR] SKILL.md must include closing YAML frontmatter delimiter")

frontmatter = parts[0][4:]

name_match = re.search(r"(?m)^name:\s*([A-Za-z0-9_]+)\s*$", frontmatter)
if not name_match:
    raise SystemExit("[ERR] frontmatter missing required field: name")

name = name_match.group(1)
if not re.fullmatch(r"[a-z0-9_]+", name):
    raise SystemExit("[ERR] name must be snake_case ([a-z0-9_]+)")

if not re.search(r"(?m)^description:\s*.+$", frontmatter):
    raise SystemExit("[ERR] frontmatter missing required field: description")

required_snippets = [
    "metadata:",
    "openclaw:",
    "requires:",
    "bins:",
]
for snippet in required_snippets:
    if snippet not in frontmatter:
        raise SystemExit(f"[ERR] frontmatter missing expected metadata section: {snippet}")

print("[OK] SKILL.md frontmatter is valid")
print(f"[OK] skill name: {name}")
PY

required_files=(
  "scripts/preflight_check.sh"
  "scripts/strict_register.py"
  "scripts/login_verify.py"
  "scripts/inbox_loop.py"
  "scripts/inbox_once.py"
  "scripts/chat_fast.py"
  "scripts/send_message.py"
  "scripts/send_reply.py"
  "scripts/admin_fetch_registration_events.py"
  "scripts/admin_issue_override_permit.py"
)

for rel in "${required_files[@]}"; do
  if [[ -f "$SKILL_DIR/$rel" ]]; then
    echo "[OK] found $rel"
  else
    echo "[ERR] missing $rel" >&2
    exit 1
  fi
done

echo "[DONE] OpenClaw skill validation passed"
