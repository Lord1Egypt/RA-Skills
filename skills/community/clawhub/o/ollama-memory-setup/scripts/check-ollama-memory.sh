#!/usr/bin/env bash
set -euo pipefail

INSTALL=false
APPLY_CONFIG=false
QUALITY_TEST=false
MODEL="${OLLAMA_MEMORY_MODEL:-nomic-embed-text}"
BASE_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"
QUALITY_QUERIES=()
TEMP_PATHS=()
cleanup() {
  if [ ${#TEMP_PATHS[@]} -gt 0 ]; then
    rm -rf -- "${TEMP_PATHS[@]}" 2>/dev/null || true
  fi
}
trap cleanup EXIT


for arg in "$@"; do
  case "$arg" in
    --install) INSTALL=true ;;
    --apply-config) APPLY_CONFIG=true ;;
    --quality-test) QUALITY_TEST=true ;;
    --model=*) MODEL="${arg#*=}" ;;
    --base-url=*) BASE_URL="${arg#*=}" ;;
    --query=*) QUALITY_QUERIES+=("${arg#*=}") ;;
    -h|--help)
      cat <<HELP
Usage: bash scripts/check-ollama-memory.sh [options]

Options:
  --install                  Install/start Ollama when possible and pull the embedding model.
  --apply-config             Write OpenClaw memorySearch config using openclaw config set.
  --quality-test             Run real OpenClaw memory searches and classify result quality.
  --query="text"             Add a quality-test query. Repeatable. Defaults to generic agent-memory queries.
  --model=nomic-embed-text   Embedding model to use.
  --base-url=http://localhost:11434
                             Ollama base URL.

Default mode is diagnostic only. It does not install software, start services, or change config unless explicit flags are provided.
HELP
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

step() { printf '\n\033[1m%s\033[0m\n' "$1"; }
ok() { printf '✅ %s\n' "$1"; }
warn() { printf '⚠️  %s\n' "$1"; }
fail() { printf '❌ %s\n' "$1"; }

validate_inputs() {
  case "$MODEL" in
    *[$'\n\r\t']*|"") fail "Invalid model name"; exit 2 ;;
  esac
  if ! [[ "$MODEL" =~ ^[A-Za-z0-9._:-]+$ ]]; then
    fail "Invalid model name. Allowed characters: letters, numbers, dot, underscore, colon, hyphen."
    exit 2
  fi

  case "$BASE_URL" in
    http://localhost:*|http://127.0.0.1:*|http://[::1]:*|http://localhost|http://127.0.0.1|http://[::1]) ;;
    http://10.*|http://172.16.*|http://172.17.*|http://172.18.*|http://172.19.*|http://172.20.*|http://172.21.*|http://172.22.*|http://172.23.*|http://172.24.*|http://172.25.*|http://172.26.*|http://172.27.*|http://172.28.*|http://172.29.*|http://172.30.*|http://172.31.*|http://192.168.*)
      warn "Using private-LAN Ollama base URL: $BASE_URL"
      ;;
    http://*.local:*|http://*.local)
      warn "Using .local Ollama base URL: $BASE_URL"
      ;;
    *)
      fail "Refusing non-local/private Ollama base URL: $BASE_URL"
      echo "Use localhost/private LAN only, or edit the script after reviewing the security risk." >&2
      exit 2
      ;;
  esac
}

validate_inputs

step "1. Checking commands"
if command -v ollama >/dev/null 2>&1; then
  ok "ollama found: $(ollama --version 2>/dev/null || echo unknown)"
elif $INSTALL; then
  warn "ollama missing — installing because --install was provided"
  if [[ "${OSTYPE:-}" == darwin* ]]; then
    command -v brew >/dev/null 2>&1 || { fail "Homebrew missing. Install Ollama manually: https://ollama.com"; exit 1; }
    brew install ollama
  else
    command -v curl >/dev/null 2>&1 || { fail "curl missing. Install curl or Ollama manually."; exit 1; }
    curl -fsSL https://ollama.com/install.sh | sh
  fi
else
  fail "ollama missing. Re-run with --install or install from https://ollama.com"
  exit 1
fi

if command -v openclaw >/dev/null 2>&1; then
  ok "openclaw found: $(openclaw --version 2>/dev/null || echo unknown)"
else
  warn "openclaw CLI not found in PATH — config/index validation will be skipped"
fi

step "2. Checking Ollama server at $BASE_URL"
if curl -fsS -- "$BASE_URL/api/tags" >/tmp/ollama-tags.json 2>/dev/null; then
  ok "Ollama API reachable"
elif $INSTALL; then
  warn "Ollama not reachable — trying to start it because --install was provided"
  if [[ "${OSTYPE:-}" == darwin* ]] && command -v brew >/dev/null 2>&1; then
    brew services start ollama >/dev/null 2>&1 || true
  else
    (ollama serve >/tmp/ollama-memory-setup.log 2>&1 &)
  fi
  sleep 3
  curl -fsS -- "$BASE_URL/api/tags" >/tmp/ollama-tags.json || { fail "Ollama still not reachable. Try: ollama serve"; exit 1; }
  ok "Ollama API reachable after start"
else
  fail "Ollama API not reachable. Re-run with --install or start Ollama manually."
  exit 1
fi

step "3. Checking embedding model: $MODEL"
if ollama list | awk '{print $1}' | grep -qx "$MODEL"; then
  ok "$MODEL already pulled"
elif $INSTALL; then
  warn "$MODEL missing — pulling now because --install was provided"
  ollama pull "$MODEL"
  ok "$MODEL pulled"
else
  fail "$MODEL missing. Re-run with --install or run: ollama pull $MODEL"
  exit 1
fi

step "4. Testing embedding endpoint"
OLLAMA_MEMORY_MODEL="$MODEL" OLLAMA_BASE_URL="$BASE_URL" python3 - <<'PY'
import json, os, urllib.request
base_url = os.environ["OLLAMA_BASE_URL"].rstrip("/")
model = os.environ["OLLAMA_MEMORY_MODEL"]
url = f"{base_url}/api/embeddings"
payload = json.dumps({"model": model, "prompt": "semantic memory test"}).encode()
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.load(r)
emb = data.get("embedding")
if not isinstance(emb, list) or len(emb) < 10:
    raise SystemExit("invalid embedding response")
print(f"✅ embedding ok: dimensions={len(emb)}")
PY

step "5. OpenClaw config"
if command -v openclaw >/dev/null 2>&1; then
  if $APPLY_CONFIG; then
    batch_file="$(mktemp)"
    TEMP_PATHS+=("$batch_file")
    OLLAMA_MEMORY_MODEL="$MODEL" OLLAMA_BASE_URL="$BASE_URL" python3 - "$batch_file" <<'PY'
import json, os, sys
model = os.environ["OLLAMA_MEMORY_MODEL"]
base_url = os.environ["OLLAMA_BASE_URL"]
ops = [
    {"path": "agents.defaults.memorySearch.enabled", "value": True},
    {"path": "agents.defaults.memorySearch.provider", "value": "ollama"},
    {"path": "agents.defaults.memorySearch.model", "value": model},
    {"path": "agents.defaults.memorySearch.remote.baseUrl", "value": base_url},
]
with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(ops, f)
PY
    openclaw config set --batch-file "$batch_file" --strict-json
    rm -f "$batch_file"
    ok "OpenClaw memorySearch config written"
  else
    warn "Not applying config. To apply, run with --apply-config. Current config:"
    openclaw config get agents.defaults.memorySearch || true
  fi

  step "6. Memory status"
  openclaw memory status --deep || true
else
  warn "Skipping OpenClaw checks because CLI is missing"
fi

if $QUALITY_TEST; then
  step "7. Quality test: real semantic searches"
  if ! command -v openclaw >/dev/null 2>&1; then
    fail "Cannot run quality test because openclaw CLI is missing"
    exit 1
  fi

  if [ ${#QUALITY_QUERIES[@]} -eq 0 ]; then
    QUALITY_QUERIES=(
      "important project decision"
      "bug fix learning"
      "open todo or next action"
    )
  fi

  tmpdir="$(mktemp -d)"
  TEMP_PATHS+=("$tmpdir")
  warn "Quality-test output is stored temporarily and will be deleted on exit. Avoid sensitive queries if your terminal/logs are captured."
  total=${#QUALITY_QUERIES[@]}
  passed=0
  noisy=0
  broken=0

  for i in "${!QUALITY_QUERIES[@]}"; do
    q="${QUALITY_QUERIES[$i]}"
    out="$tmpdir/search-$i.txt"
    printf '\nQuery: %s\n' "$q"
    if openclaw memory search "$q" --max-results 5 >"$out" 2>&1; then
      if grep -Eiq 'disabled|no results|0 results|error|failed' "$out"; then
        warn "Search ran but looks weak/noisy"
        noisy=$((noisy+1))
      elif grep -Eiq 'Source:|score|MEMORY|memory/' "$out"; then
        ok "Search returned memory-like results"
        passed=$((passed+1))
      else
        warn "Search returned output, but quality is unclear"
        noisy=$((noisy+1))
      fi
      sed -n '1,12p' "$out" | sed 's/^/  /'
    else
      fail "Search command failed"
      broken=$((broken+1))
      sed -n '1,12p' "$out" | sed 's/^/  /'
    fi
  done

  printf '\nQuality summary: %s OK / %s noisy / %s broken / %s total\n' "$passed" "$noisy" "$broken" "$total"
  if [ "$broken" -gt 0 ]; then
    fail "Memory search is broken. Check config, restart gateway, then reindex."
    exit 1
  elif [ "$passed" -eq 0 ]; then
    warn "Memory search runs, but quality is weak. Reindex and test with known memory topics."
  else
    ok "Memory search quality test passed enough to use."
  fi
fi

cat <<NEXT

✅ Done.

Next recommended commands:
  openclaw gateway restart
  openclaw memory index --force
  openclaw memory status --deep
  bash scripts/check-ollama-memory.sh --quality-test --query="known memory topic"
NEXT
