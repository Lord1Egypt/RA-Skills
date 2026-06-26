#!/usr/bin/env bash
# Setup inference-optimizer: make scripts executable; optionally wire commands into workspace.
# Default: preview only. Use --apply to modify AGENTS.md and TOOLS.md.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_MAIN="${WORKSPACE_MAIN:-$HOME/clawd}"
WORKSPACE_WHATSAPP="${WORKSPACE_WHATSAPP:-$HOME/.openclaw/workspace-whatsapp}"
APPROVALS_FILE="${APPROVALS_FILE:-$HOME/.openclaw/exec-approvals.json}"

chmod +x "$SKILL_DIR/scripts/openclaw-audit.sh"
chmod +x "$SKILL_DIR/scripts/purge-stale-sessions.sh"
chmod +x "$SKILL_DIR/scripts/preflight.sh"
chmod +x "$SKILL_DIR/scripts/verify.sh"
echo "[OK] Scripts executable"

APPLY=false
[[ "${1:-}" = "--apply" ]] && APPLY=true

AUDIT_PATH="$SKILL_DIR/scripts/openclaw-audit.sh"
PURGE_PATH="$SKILL_DIR/scripts/purge-stale-sessions.sh"
PREFLIGHT_PATH="$SKILL_DIR/scripts/preflight.sh"
SETUP_PATH="$SKILL_DIR/scripts/setup.sh"
VERIFY_PATH="$SKILL_DIR/scripts/verify.sh"
BEGIN_MARKER="<!-- inference-optimizer:begin -->"
END_MARKER="<!-- inference-optimizer:end -->"

AGENTS_BLOCK=$(cat <<EOF
$BEGIN_MARKER
## inference-optimizer commands (managed)

| Command | Action |
| \`/audit\` | Exec \`$AUDIT_PATH\`; include runtime findings and recommended next steps only. Do not run file-changing actions. |
| \`/optimize\` | Exec \`$AUDIT_PATH\`; include output, then propose remediation or optimization actions. Require explicit approval before any file-changing action. |
| \`/preflight\` | Exec \`$PREFLIGHT_PATH\`; create backups, run audit, run setup preview, and return next steps. |
$END_MARKER
EOF
)

TOOLS_BLOCK=$(cat <<EOF
$BEGIN_MARKER
## inference-optimizer (managed)

| App | Use | Example |
| \`/audit\` | Analyze only | exec \`$AUDIT_PATH\`; include runtime findings and recommended next steps only. |
| \`/optimize\` | Analyze + action flow | exec \`$AUDIT_PATH\`; then propose actions; run actions only after approval. |
| \`/preflight\` | Backup and install checks | exec \`$PREFLIGHT_PATH\`; optional apply: \`$PREFLIGHT_PATH --apply-setup\` after approval. |
| purge sessions | Approved action after audit/optimize | exec \`$PURGE_PATH\` (archives by default). |
$END_MARKER
EOF
)

APPROVAL_PATTERNS=(
  "$AUDIT_PATH"
  "$PREFLIGHT_PATH"
  "$PURGE_PATH"
  "$SETUP_PATH"
  "$VERIFY_PATH"
)

update_file() {
  local file="$1"
  local block="$2"

  FILE_PATH="$file" BLOCK_CONTENT="$block" BEGIN_MARKER="$BEGIN_MARKER" END_MARKER="$END_MARKER" python3 <<'PY'
import os
import pathlib
import re

path = pathlib.Path(os.environ["FILE_PATH"])
begin = os.environ["BEGIN_MARKER"]
end = os.environ["END_MARKER"]
block = os.environ["BLOCK_CONTENT"].strip() + "\n"

text = path.read_text() if path.exists() else ""
text = re.sub(re.escape(begin) + r".*?" + re.escape(end) + r"\n?", "", text, flags=re.S)

legacy_substrings = [
    "~/clawdbot/code/scripts/openclaw-audit.sh",
    "~/clawdbot/code/scripts/purge-stale-sessions.sh",
    "/clawd/skills/public/inference-optimizer/",
]

filtered_lines = []
for line in text.splitlines():
    if any(token in line for token in legacy_substrings):
        continue
    filtered_lines.append(line)

cleaned = "\n".join(filtered_lines).rstrip()
if cleaned:
    cleaned += "\n\n"
cleaned += block
path.write_text(cleaned)
PY
}

update_approvals() {
  python3 - "$APPROVALS_FILE" "${APPROVAL_PATTERNS[@]}" <<'PY'
import json
import pathlib
import uuid
import sys

path = pathlib.Path(sys.argv[1])
patterns = sys.argv[2:]
agents = ["main", "whatsapp"]

if not path.exists():
    print(f"[WARN] approvals file not found: {path}")
    raise SystemExit(0)

data = json.loads(path.read_text())
agent_map = data.setdefault("agents", {})
changed = False

for agent in agents:
    section = agent_map.setdefault(agent, {})
    allowlist = section.setdefault("allowlist", [])
    existing = {entry.get("pattern") for entry in allowlist}
    for pattern in patterns:
        if pattern in existing:
            continue
        allowlist.append({
            "pattern": pattern,
            "id": str(uuid.uuid4()),
        })
        changed = True
        print(f"[OK] Added approval pattern for {agent}: {pattern}")

if changed:
    path.write_text(json.dumps(data, indent=2) + "\n")
else:
    print("[OK] Approval patterns already present")
PY
}

if [[ "$APPLY" = false ]]; then
  echo ""
  echo "Preview (no changes made). Run with --apply to modify workspace files."
  echo ""
  echo "Managed AGENTS.md block:"
  echo "$AGENTS_BLOCK"
  echo ""
  echo "Managed TOOLS.md block:"
  echo "$TOOLS_BLOCK"
  echo ""
  echo "This update replaces any prior managed block and removes legacy paths such as:"
  echo "  - ~/clawdbot/code/scripts/openclaw-audit.sh"
  echo "  - ~/clawd/skills/public/inference-optimizer"
  echo ""
  echo "Managed approval patterns (main + whatsapp in $APPROVALS_FILE):"
  for pattern in "${APPROVAL_PATTERNS[@]}"; do
    echo "  - $pattern"
  done
  echo ""
  echo "Workspaces: $WORKSPACE_MAIN, $WORKSPACE_WHATSAPP"
  echo "Usage: bash $0 --apply"
  exit 0
fi

for ws in "$WORKSPACE_MAIN" "$WORKSPACE_WHATSAPP"; do
  [[ -d "$ws" ]] || continue

  if [[ -f "$ws/AGENTS.md" ]]; then
    update_file "$ws/AGENTS.md" "$AGENTS_BLOCK"
    echo "[OK] Updated $ws/AGENTS.md"
  else
    echo "[WARN] $ws/AGENTS.md not found"
  fi

  if [[ -f "$ws/TOOLS.md" ]]; then
    update_file "$ws/TOOLS.md" "$TOOLS_BLOCK"
    echo "[OK] Updated $ws/TOOLS.md"
  else
    echo "[WARN] $ws/TOOLS.md not found"
  fi
done

update_approvals

echo ""
echo "Done. Prefer manual purge: $PURGE_PATH (archives by default)."
echo "Verify: $SKILL_DIR/scripts/verify.sh"
