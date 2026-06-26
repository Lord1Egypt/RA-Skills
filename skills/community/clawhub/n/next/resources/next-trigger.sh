#!/bin/bash
# next-trigger.sh — Stop hook for next skill
#
# Detects task completion keywords in the last assistant message and emits
# a skill-trigger marker so that the LLM invokes the `next` skill in its
# follow-up response.
#
# Trigger condition: Stop hook fires when Claude finishes a response.
# Input (stdin): JSON { session_id, transcript_path, stop_hook_active }
# Output (stdout): on match, a JSON Stop-hook decision object of the form
#   {"decision":"block","reason":"<skill-trigger name=\"next\">…</skill-trigger>"}
# (the skill-trigger marker is embedded inside the JSON `reason` field — it is
# NOT emitted as a bare standalone marker, because Stop hooks deliver stdout to
# the debug log only; the `decision:"block"` envelope is what surfaces the
# `reason` text to the LLM. See ~/.claude/skills/hook/SKILL.md "Output channel
# spec per event"). On no match, output is empty.
#
# Responsibility: next skill (per automation.md "Hook responsibility policy").
# Install: copy to ~/.claude/hooks/next-trigger.sh and register in
# ~/.claude/settings.json under "Stop" matcher (see next/SKILL.md Install).

set -euo pipefail

INPUT="$(cat)"

TRANSCRIPT=$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    d = json.load(sys.stdin)
    print(d.get("transcript_path",""))
except Exception:
    print("")' 2>/dev/null || echo "")

STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    d = json.load(sys.stdin)
    print("true" if d.get("stop_hook_active") else "false")
except Exception:
    print("false")' 2>/dev/null || echo "false")

# Prevent infinite loops: do not re-trigger when this hook itself caused the stop
if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
  exit 0
fi

if [[ -z "$TRANSCRIPT" || ! -f "$TRANSCRIPT" ]]; then
  exit 0
fi

# Extract concatenated text of the most recent assistant message from JSONL.
# IMPORTANT: A single response is split into multiple text blocks (between tool_use
# blocks). We must concatenate ALL text blocks of the LAST message — not overwrite
# with each block, which captures only the trailing fragment (often non-completion).
# See ~/.agents/rules/failed-attempts.md "Hook last_text missed multiple text-blocks".
LAST_TEXT=$(python3 - "$TRANSCRIPT" <<'PY' 2>/dev/null || echo ""
import json, sys
path = sys.argv[1]
last_blocks = []
current_blocks = []
last_uuid = None
try:
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except Exception:
                continue
            if obj.get("type") != "assistant":
                continue
            uuid = obj.get("uuid", "")
            # Each assistant JSONL line = a discrete message turn. Accumulate every text block
            # within this message, then commit to last_blocks when a NEW message arrives.
            if uuid != last_uuid:
                if current_blocks:
                    last_blocks = current_blocks
                current_blocks = []
                last_uuid = uuid
            msg = obj.get("message", {}) or {}
            content = msg.get("content", []) or []
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    t = c.get("text", "")
                    if t:
                        current_blocks.append(t)
        # Final commit if file ends mid-message
        if current_blocks:
            last_blocks = current_blocks
except Exception:
    pass
print("\n".join(last_blocks))
PY
)

if [[ -z "$LAST_TEXT" ]]; then
  exit 0
fi

# Completion keyword detection (case-insensitive).
# Patterns are loaded from data/*.regex files — each non-empty, non-comment line
# is concatenated into a single egrep -E alternation. The data/ directory is
# git-ignored (skills/next/.gitignore) and publish-ignored (.clawhubignore),
# so each user adds their own locale patterns (en.regex, ko.regex, ja.regex…).
# If no data files exist, fall back to a built-in English default.
DATA_DIR="$(dirname "$0")/../data"
if compgen -G "$DATA_DIR/*.regex" > /dev/null 2>&1; then
  PATTERN=$(cat "$DATA_DIR"/*.regex | sed 's/#.*$//' | awk 'NF' | paste -sd'|' -)
else
  PATTERN='Fix complete:|✅|all done|^[[:space:]]*done\.|task (complete|completed|finished)|completed[\.\!\)\*,[:space:]]|finished[\.\!\)\*,[:space:]]|wrapped up'
fi

if echo "$LAST_TEXT" | grep -qiE "$PATTERN"; then
  # Output JSON decision:"block" — Stop hook spec: stdout goes to debug log only;
  # JSON decision:"block" prevents stop and feeds reason to Claude as a follow-up signal.
  # See ~/.claude/skills/hook/SKILL.md "Output channel spec per event".
  echo '{"decision":"block","reason":"<skill-trigger name=\"next\">Task completion signal detected. Invoke the `next` skill to suggest follow-up actions.</skill-trigger>"}'
fi

exit 0
