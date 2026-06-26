#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

INPUT=$(cat)

TRANSCRIPT_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('transcript_path', ''))
except:
    print('')
" 2>/dev/null || echo "")

TRIGGER=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('trigger', 'unknown'))
except:
    print('unknown')
" 2>/dev/null || echo "unknown")

# --- Backup existente (sin cambios) ---
if [ -n "$TRANSCRIPT_PATH" ] && [ -f "$TRANSCRIPT_PATH" ]; then
  BACKUP_DIR="${PROJECT_DIR}/thinking/session-logs"
  mkdir -p "$BACKUP_DIR"
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  cp "$TRANSCRIPT_PATH" "$BACKUP_DIR/session_${TRIGGER}_${TIMESTAMP}.jsonl"
  ls -t "$BACKUP_DIR"/session_*.jsonl 2>/dev/null | tail -n +31 | xargs rm -f 2>/dev/null || true
fi

# --- Resume Card: estado operativo real ---
OUT="${PROJECT_DIR}/.claude/session-resume-card.md"
TRANSCRIPT="$TRANSCRIPT_PATH"

if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
  # fallback: buscar el más reciente en .claude/
  TRANSCRIPT=$(ls -t "${PROJECT_DIR}/.claude/"*.jsonl 2>/dev/null | head -n 1 || echo "")
fi

{
  echo "## Resume Card — $(date '+%Y-%m-%d %H:%M')"
  echo ""

  # Proyecto activo
  echo "### Proyecto activo"
  BRANCH=$(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null || echo "N/A")
  COMMIT=$(git -C "$PROJECT_DIR" rev-parse --short HEAD 2>/dev/null || echo "N/A")
  echo "branch: $BRANCH"
  echo "commit: $COMMIT"
  echo ""

  # Estado git
  echo "### Cambios en curso"
  git -C "$PROJECT_DIR" status --short 2>/dev/null | head -n 8 || echo "(limpio)"
  echo ""

  # Última intención + última acción (extraídas del transcript con Python)
  if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
    python3 - "$TRANSCRIPT" <<'PYEOF'
import sys, json

path = sys.argv[1]
messages = []
try:
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict) and obj.get('role') in ('user', 'assistant'):
                    messages.append(obj)
            except:
                pass
except:
    pass

def extract_text(msg):
    c = msg.get('content', '')
    if isinstance(c, str):
        return c[:200]
    if isinstance(c, list):
        for block in c:
            if isinstance(block, dict) and block.get('type') == 'text':
                return block.get('text', '')[:200]
    return ''

last_user = next((extract_text(m) for m in reversed(messages) if m['role'] == 'user'), 'N/A')
last_asst = next((extract_text(m) for m in reversed(messages) if m['role'] == 'assistant'), 'N/A')

print("### Última intención (user)")
print(last_user.replace('\n', ' ').strip())
print("")
print("### Última acción (assistant)")
print(last_asst.replace('\n', ' ').strip())
print("")

# Modo: heurística sobre texto combinado
combined = (last_user + " " + last_asst).lower()
mode = "coding"
if any(w in combined for w in ["error", "fail", "bug", "roto", "arregla", "fix"]):
    mode = "debugging"
elif any(w in combined for w in ["deploy", "vercel", "railway", "push", "produccion"]):
    mode = "deploy"
elif any(w in combined for w in ["idea", "brainstorm", "diseña", "concepto", "que opinas"]):
    mode = "ideation"
elif any(w in combined for w in ["commit", "git", "merge", "branch"]):
    mode = "git workflow"

print("### Modo")
print(mode)
print("")
PYEOF
  else
    echo "### Última intención (user)"
    echo "N/A (transcript no disponible)"
    echo ""
    echo "### Última acción (assistant)"
    echo "N/A"
    echo ""
    echo "### Modo"
    echo "unknown"
    echo ""
  fi

  # Next step
  echo "### Next step"
  if [ -f "${PROJECT_DIR}/.claude/current-task.md" ]; then
    head -n 3 "${PROJECT_DIR}/.claude/current-task.md"
  else
    echo "Continuar última acción del assistant"
  fi

} > "$OUT" 2>/dev/null || true

exit 0
