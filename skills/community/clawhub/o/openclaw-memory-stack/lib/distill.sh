#!/usr/bin/env bash
# OpenClaw Memory Stack — Thread Distillation
# Post-session fact extraction pipeline.
# Sourced by hooks or run via: source distill.sh && distill_session <logfile>

DISTILL_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$DISTILL_LIB_DIR/platform.sh"

# Config defaults
DISTILL_MODEL="${DISTILL_MODEL:-qwen2.5:7b}"
DISTILL_ENDPOINT="${DISTILL_ENDPOINT:-http://localhost:11434}"
DISTILL_MIN_SCORE="${DISTILL_MIN_SCORE:-4}"
DISTILL_MAX_FACTS="${DISTILL_MAX_FACTS:-20}"

# Load config from JSON file if available
# Usage: distill_load_config <config_json_path>
distill_load_config() {
  local config_file="$1"
  [ ! -f "$config_file" ] && return 0

  if has_command python3; then
    local _val
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('distill',{}); v=cfg.get('model',''); print(v) if v else exit(1)" 2>/dev/null) && DISTILL_MODEL="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('distill',{}); v=cfg.get('endpoint',''); print(v) if v else exit(1)" 2>/dev/null) && DISTILL_ENDPOINT="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('distill',{}); v=cfg.get('min_score',''); print(v) if v else exit(1)" 2>/dev/null) && DISTILL_MIN_SCORE="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('distill',{}); v=cfg.get('max_facts',''); print(v) if v else exit(1)" 2>/dev/null) && DISTILL_MAX_FACTS="$_val"
  fi
}

# ── Stage 1: Triage ─────────────────────────────────────────
# Determine if a session log is worth distilling.
# Usage: distill_triage <session_log>
# Returns: score (1-10) on stdout, 0 = not worth distilling
distill_triage() {
  local session_log="$1"

  if [ ! -f "$session_log" ]; then
    echo "0"
    return 0
  fi

  # Quick heuristic: skip very short sessions
  local line_count
  line_count=$(wc -l < "$session_log" | tr -d ' ')
  if [ "$line_count" -lt 5 ]; then
    echo "1"
    return 0
  fi

  # Check Ollama availability
  if ! curl -sf "${DISTILL_ENDPOINT}/api/tags" >/dev/null 2>&1; then
    # No LLM — use heuristic: longer sessions with keywords score higher
    _triage_heuristic "$session_log"
    return 0
  fi

  # Truncate log to fit context window
  local log_content
  log_content=$(head -c 12000 "$session_log" 2>/dev/null)

  local prompt="Rate this conversation on a scale of 1-10 for how much useful, durable knowledge it contains. Consider: decisions made, patterns discovered, preferences stated, architectural choices, bug fixes, configuration details. Respond with ONLY a single integer.\n\nConversation:\n${log_content}"

  local payload
  payload=$(python3 -c "
import json
print(json.dumps({
    'model': '$DISTILL_MODEL',
    'prompt': '''$prompt''',
    'stream': False,
    'options': {'num_predict': 5, 'temperature': 0.1}
}))
" 2>/dev/null) || {
    _triage_heuristic "$session_log"
    return 0
  }

  local response
  response=$(curl -sf --max-time 30 \
    -X POST "${DISTILL_ENDPOINT}/api/generate" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || {
    _triage_heuristic "$session_log"
    return 0
  }

  local score
  score=$(python3 -c "
import json, re
data = json.loads('''$response''')
text = data.get('response', '').strip()
match = re.search(r'\d+', text)
if match:
    s = int(match.group())
    print(min(max(s, 1), 10))
else:
    print(5)
" 2>/dev/null) || echo "5"

  echo "$score"
}

# Heuristic triage when LLM is unavailable
_triage_heuristic() {
  local session_log="$1"

  python3 -c "
from pathlib import Path
import re

content = Path('$session_log').read_text(errors='replace').lower()
score = 3  # base

# Positive signals
keywords = ['decided', 'decision', 'chose', 'prefer', 'pattern', 'architecture',
            'bug', 'fix', 'config', 'workaround', 'important', 'remember']
for kw in keywords:
    if kw in content:
        score += 1

# Length bonus
lines = len(content.split('\n'))
if lines > 50:
    score += 1
if lines > 200:
    score += 1

print(min(score, 10))
" 2>/dev/null || echo "5"
}

# ── Stage 2: Extract atomic facts ───────────────────────────
# Usage: distill_extract <session_log>
# Output: JSON array of facts on stdout
distill_extract() {
  local session_log="$1"

  if [ ! -f "$session_log" ]; then
    echo "[]"
    return 0
  fi

  # Check Ollama
  if ! curl -sf "${DISTILL_ENDPOINT}/api/tags" >/dev/null 2>&1; then
    # Fallback: extract key lines heuristically
    _extract_heuristic "$session_log"
    return 0
  fi

  local log_content
  log_content=$(head -c 12000 "$session_log" 2>/dev/null)

  local prompt
  prompt="Extract durable facts from this conversation. Output as a JSON array:
[{\"fact\": \"...\", \"importance\": 1-10, \"tags\": [\"...\"]}]

Rules:
- Skip ephemeral details (greetings, typos, temporary debugging)
- Focus on: decisions, patterns, preferences, architectural choices, config details, bug causes
- Each fact should be self-contained and understandable without context
- Maximum ${DISTILL_MAX_FACTS} facts
- importance 8-10: critical decisions, hard-won insights
- importance 5-7: useful patterns, preferences
- importance 1-4: minor details

Conversation:
${log_content}"

  local payload
  payload=$(python3 -c "
import json
print(json.dumps({
    'model': '$DISTILL_MODEL',
    'prompt': '''$prompt''',
    'stream': False,
    'options': {'num_predict': 2000, 'temperature': 0.3}
}))
" 2>/dev/null) || {
    _extract_heuristic "$session_log"
    return 0
  }

  local response
  response=$(curl -sf --max-time 60 \
    -X POST "${DISTILL_ENDPOINT}/api/generate" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || {
    _extract_heuristic "$session_log"
    return 0
  }

  # Parse and validate the JSON array
  python3 -c "
import json, re

data = json.loads('''$response''')
text = data.get('response', '')

# Find JSON array in response
match = re.search(r'\[.*\]', text, re.DOTALL)
if not match:
    print('[]')
    exit(0)

try:
    facts = json.loads(match.group())
    # Validate structure
    valid = []
    for f in facts[:${DISTILL_MAX_FACTS}]:
        if isinstance(f, dict) and 'fact' in f:
            valid.append({
                'fact': str(f['fact']),
                'importance': int(f.get('importance', 5)),
                'tags': list(f.get('tags', []))
            })
    print(json.dumps(valid))
except:
    print('[]')
" 2>/dev/null || echo "[]"
}

# Heuristic extraction when LLM is unavailable
_extract_heuristic() {
  local session_log="$1"

  python3 -c "
import json, re
from pathlib import Path

content = Path('$session_log').read_text(errors='replace')
lines = content.split('\n')
facts = []

# Look for decision/preference patterns
patterns = [
    (r'(?i)(decided|chose|choosing|picked|selected|went with)\s+(.{10,200})', 'decision'),
    (r'(?i)(remember|note|important|always|never|must|prefer)\s*:?\s*(.{10,200})', 'preference'),
    (r'(?i)(bug|issue|problem|cause|root cause|fix)\s*:?\s*(.{10,200})', 'bugfix'),
    (r'(?i)(config|configure|set|setting)\s+(.{10,200})', 'config'),
]

seen = set()
for line in lines:
    stripped = line.strip()
    if len(stripped) < 15:
        continue
    for pattern, tag in patterns:
        match = re.search(pattern, stripped)
        if match:
            fact_text = match.group(0)[:300]
            if fact_text not in seen:
                seen.add(fact_text)
                facts.append({
                    'fact': fact_text,
                    'importance': 5,
                    'tags': [tag]
                })
            break

print(json.dumps(facts[:${DISTILL_MAX_FACTS}]))
" 2>/dev/null || echo "[]"
}

# ── Stage 3: Store facts ────────────────────────────────────
# Usage: distill_store <facts_json> [memory_root]
# Stores each fact via Total Recall daily tier.
distill_store() {
  local facts_json="$1"
  local memory_root="${2:-${OPENCLAW_REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || echo "")}}"
  local install_root="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
  local tr_wrapper="$install_root/skills/memory-totalrecall/wrapper.sh"

  if [ -z "$memory_root" ]; then
    echo "Error: no memory root found" >&2
    return 1
  fi

  local stored=0
  python3 -c "
import json
facts = json.loads('''$facts_json''')
for i, f in enumerate(facts):
    print(f'{i}\t{f[\"fact\"]}\t{\",\".join(f.get(\"tags\",[]))}')
" 2>/dev/null | while IFS=$'\t' read -r idx fact tags; do
    local slug="distilled-$(date -u +%Y%m%d)-${idx}"

    # Format as markdown
    local content="# Distilled Fact\n\n${fact}\n\nTags: ${tags}\nExtracted: $(now_iso)"

    if [ -x "$tr_wrapper" ]; then
      OPENCLAW_REPO_ROOT="$memory_root" bash "$tr_wrapper" store daily "$slug" "$content" >/dev/null 2>&1 || true
    else
      # Direct write fallback
      mkdir -p "$memory_root/memory/daily"
      printf '%b\n' "$content" > "$memory_root/memory/daily/$(date -u +%Y-%m-%d)_${slug}.md"
    fi

    stored=$((stored + 1))
  done

  echo "Stored facts to daily tier"
}

# ── Full pipeline ────────────────────────────────────────────
# Usage: distill_session <session_log> [memory_root]
distill_session() {
  local session_log="$1"
  local memory_root="${2:-}"

  if [ ! -f "$session_log" ]; then
    echo "Error: session log not found: $session_log" >&2
    return 1
  fi

  echo "Distilling session: $session_log" >&2

  # Stage 1: Triage
  local score
  score=$(distill_triage "$session_log")
  echo "  Triage score: $score / 10" >&2

  if [ "$score" -lt "$DISTILL_MIN_SCORE" ]; then
    echo "  Score below threshold ($DISTILL_MIN_SCORE), skipping." >&2
    return 0
  fi

  # Stage 2: Extract facts
  local facts
  facts=$(distill_extract "$session_log")
  local fact_count
  fact_count=$(python3 -c "import json; print(len(json.loads('''$facts''')))" 2>/dev/null || echo "0")
  echo "  Extracted $fact_count facts" >&2

  if [ "$fact_count" -eq 0 ]; then
    echo "  No facts extracted, skipping." >&2
    return 0
  fi

  # Stage 3: Store
  distill_store "$facts" "$memory_root"
  echo "  Distillation complete." >&2
}

# ── Hook integration ─────────────────────────────────────────
# To wire as a post-session hook in OpenClaw config:
#
# 1. Add to ~/.openclaw/config.json:
#    {
#      "hooks": {
#        "post_session": "~/.openclaw/memory-stack/lib/distill.sh"
#      }
#    }
#
# 2. Or in a shell hook script:
#    #!/usr/bin/env bash
#    source ~/.openclaw/memory-stack/lib/distill.sh
#    distill_session "$OPENCLAW_SESSION_LOG"
#
# 3. Or call from cron/launchd for batch processing:
#    for log in ~/.openclaw/sessions/*.log; do
#      source ~/.openclaw/memory-stack/lib/distill.sh
#      distill_session "$log"
#    done
