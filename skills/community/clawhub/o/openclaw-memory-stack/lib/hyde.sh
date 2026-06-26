#!/usr/bin/env bash
# OpenClaw Memory Stack — HyDE (Hypothetical Document Embeddings)
# Generates a hypothetical answer document to improve vector search recall.
# Sourced by wrappers; not run standalone.

HYDE_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HYDE_LIB_DIR/platform.sh"

# Default config (overridable via env vars or config.json)
HYDE_MODEL="${HYDE_MODEL:-qwen2.5:7b}"
HYDE_ENDPOINT="${HYDE_ENDPOINT:-http://localhost:11434}"
HYDE_MAX_TOKENS="${HYDE_MAX_TOKENS:-300}"
HYDE_TEMPERATURE="${HYDE_TEMPERATURE:-0.7}"

# Load HyDE config from a config.json file if available
# Usage: hyde_load_config <config_json_path>
hyde_load_config() {
  local config_file="$1"
  [ ! -f "$config_file" ] && return 0

  if has_command python3; then
    local _val
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('hyde',{}); v=cfg.get('model',''); print(v) if v else exit(1)" 2>/dev/null) && HYDE_MODEL="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('hyde',{}); v=cfg.get('endpoint',''); print(v) if v else exit(1)" 2>/dev/null) && HYDE_ENDPOINT="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('hyde',{}); v=cfg.get('max_tokens',''); print(v) if v else exit(1)" 2>/dev/null) && HYDE_MAX_TOKENS="$_val"
    _val=$(python3 -c "import json; cfg=json.load(open('$config_file')).get('hyde',{}); v=cfg.get('temperature',''); print(v) if v else exit(1)" 2>/dev/null) && HYDE_TEMPERATURE="$_val"
  fi
}

# Check if HyDE is enabled
# Returns 0 if enabled, 1 if disabled
hyde_is_enabled() {
  [ "${HYDE_ENABLED:-false}" = "true" ] || [ "${HYDE_ENABLED:-0}" = "1" ]
}

# Generate a hypothetical document that answers the query
# Usage: hyde_expand <query>
# Output: hypothetical document text on stdout
hyde_expand() {
  local query="$1"

  if [ -z "$query" ]; then
    echo "$query"
    return 0
  fi

  # Check Ollama is reachable
  if ! curl -sf "${HYDE_ENDPOINT}/api/tags" >/dev/null 2>&1; then
    # Ollama not available — fall back to raw query
    echo "$query" >&2
    echo "hyde: Ollama not reachable at $HYDE_ENDPOINT, using raw query" >&2
    echo "$query"
    return 0
  fi

  local prompt="Write a short technical passage (~200 words) that directly answers this question. Be specific and use concrete details. Do not include preamble or meta-commentary.\n\nQuestion: ${query}"

  local payload
  payload=$(python3 -c "
import json
print(json.dumps({
    'model': '$HYDE_MODEL',
    'prompt': '''$prompt''',
    'stream': False,
    'options': {
        'num_predict': int('$HYDE_MAX_TOKENS'),
        'temperature': float('$HYDE_TEMPERATURE')
    }
}))
" 2>/dev/null) || {
    echo "$query"
    return 0
  }

  local response
  response=$(curl -sf --max-time 30 \
    -X POST "${HYDE_ENDPOINT}/api/generate" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || {
    # Timeout or error — fall back to raw query
    echo "hyde: Ollama request failed, using raw query" >&2
    echo "$query"
    return 0
  }

  # Extract the generated text
  local hypothetical
  hypothetical=$(python3 -c "
import json, sys
try:
    data = json.loads('''$response''')
    text = data.get('response', '').strip()
    if text:
        print(text)
    else:
        print('$query')
except:
    print('$query')
" 2>/dev/null) || {
    echo "$query"
    return 0
  }

  if [ -z "$hypothetical" ]; then
    echo "$query"
  else
    echo "$hypothetical"
  fi
}
