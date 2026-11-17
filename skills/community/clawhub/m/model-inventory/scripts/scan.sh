#!/usr/bin/env bash
# scan.sh — tier 1-2 detection of locally installed AI CLIs.
# Spends ZERO tokens: binary lookup, --version, and local credential heuristics only.
# Tier-3 live model probes are the calling agent's job (see references/cli-registry.md).
# Output: one JSON document on stdout. Detection failures never break the JSON — they
# land in evidence fields. Evidence names credential signals, never their values.
set -u

TIMEOUT_SECS="${SCAN_TIMEOUT_SECS:-15}"

run_to() {
  if command -v timeout >/dev/null 2>&1; then
    timeout "$TIMEOUT_SECS" "$@" 2>&1
  elif command -v perl >/dev/null 2>&1; then
    perl -e 'alarm shift; exec @ARGV' "$TIMEOUT_SECS" "$@" 2>&1
  else
    "$@" 2>&1
  fi
}

# First line only, control chars stripped, JSON-escaped, capped at 200 chars.
jesc() {
  printf '%s' "$1" | head -n 1 | tr -d '\000-\037' | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' | head -c 200
}

ENTRIES=""
add_entry() { # 1 name, 2 installed, 3 path, 4 version, 5 auth_status, 6 auth_evidence, 7 models_json, 8 invocation, 9 default_model 'id|evidence' (optional)
  local e dm=${9:-}
  e="{\"name\":\"$1\",\"installed\":$2,\"path\":\"$(jesc "$3")\",\"version\":\"$(jesc "$4")\",\"auth\":{\"status\":\"$5\",\"evidence\":\"$(jesc "$6")\"},\"invocation\":\"$8\""
  if [ -n "$dm" ]; then
    e="$e,\"default_model\":{\"id\":\"$(jesc "${dm%%|*}")\",\"evidence\":\"$(jesc "${dm#*|}")\"}"
  fi
  e="$e,\"models\":$7}"
  ENTRIES="${ENTRIES:+$ENTRIES,}$e"
}

seed_models() { # space-separated ids -> JSON array, all unverified
  local out="" id
  for id in $1; do
    out="${out:+$out,}{\"id\":\"$id\",\"status\":\"unverified\",\"evidence\":\"seed alias; not probed\"}"
  done
  printf '[%s]' "$out"
}

auth_none() { printf 'unknown|no auth heuristic for this CLI'; }

auth_claude() {
  if [ -n "${ANTHROPIC_API_KEY:-}" ]; then printf 'likely-authenticated|env ANTHROPIC_API_KEY is set'; return; fi
  if [ -f "$HOME/.claude/.credentials.json" ]; then printf 'likely-authenticated|~/.claude/.credentials.json exists'; return; fi
  if [ -f "$HOME/.claude.json" ] && grep -q '"oauthAccount"' "$HOME/.claude.json" 2>/dev/null; then
    printf 'likely-authenticated|oauthAccount present in ~/.claude.json'; return
  fi
  printf 'unknown|no credentials file, oauthAccount, or env key found'
}

auth_codex() {
  local out
  out=$(run_to codex login status)
  case "$out" in
    *"ot logged in"*) printf 'unauthenticated|codex login status: %s' "$out" | head -c 250; return ;;
    *"ogged in"*)     printf 'likely-authenticated|codex login status: %s' "$out" | head -c 250; return ;;
  esac
  if [ -f "$HOME/.codex/auth.json" ]; then printf 'likely-authenticated|~/.codex/auth.json exists'; return; fi
  if [ -n "${OPENAI_API_KEY:-}" ]; then printf 'likely-authenticated|env OPENAI_API_KEY is set'; return; fi
  printf 'unknown|login status inconclusive; no auth.json or env key'
}

auth_gemini() {
  if [ -n "${GEMINI_API_KEY:-}" ]; then printf 'likely-authenticated|env GEMINI_API_KEY is set'; return; fi
  if [ -n "${GOOGLE_API_KEY:-}" ]; then printf 'likely-authenticated|env GOOGLE_API_KEY is set'; return; fi
  if [ -f "$HOME/.gemini/oauth_creds.json" ]; then printf 'likely-authenticated|~/.gemini/oauth_creds.json exists'; return; fi
  printf 'unknown|no env key or oauth_creds.json found'
}

auth_copilot() {
  if [ -d "$HOME/.copilot" ]; then printf 'unknown|~/.copilot config dir present; live probe needed to confirm'; return; fi
  printf 'unknown|no auth signal found'
}

auth_opencode() {
  if [ -f "$HOME/.local/share/opencode/auth.json" ]; then printf 'likely-authenticated|~/.local/share/opencode/auth.json exists'; return; fi
  printf 'unknown|no auth.json found'
}

auth_qwen() { # Qwen Code (gemini-cli fork): ~/.qwen holds oauth creds
  if [ -f "$HOME/.qwen/oauth_creds.json" ]; then printf 'likely-authenticated|~/.qwen/oauth_creds.json exists'; return; fi
  if [ -n "${DASHSCOPE_API_KEY:-}" ]; then printf 'likely-authenticated|env DASHSCOPE_API_KEY is set'; return; fi
  if [ -n "${QWEN_API_KEY:-}" ]; then printf 'likely-authenticated|env QWEN_API_KEY is set'; return; fi
  printf 'unknown|no oauth_creds.json or env key found'
}

cfg_model() { # 1 file, 2 label -> prints 'id|evidence', rc 1 if not found
  local f=$1 label=$2 m
  [ -f "$f" ] || return 1
  m=$(grep -o '"model"[[:space:]]*:[[:space:]]*"[^"]*"' "$f" 2>/dev/null | head -n 1 | sed 's/.*:[[:space:]]*"\([^"]*\)"/\1/')
  [ -n "$m" ] || return 1
  printf '%s|"model" key in %s' "$m" "$label"
}

default_model() { # 1 cli name -> 'id|evidence' ('unknown|...' when unreadable)
  local m
  case $1 in
    opencode) cfg_model "$HOME/.config/opencode/opencode.json" "~/.config/opencode/opencode.json" && return ;;
    qwen)     cfg_model "$HOME/.qwen/settings.json" "~/.qwen/settings.json" && return ;;
    gemini)   cfg_model "$HOME/.gemini/settings.json" "~/.gemini/settings.json" && return ;;
    copilot)  cfg_model "$HOME/.copilot/config.json" "~/.copilot/config.json" && return ;;
    claude)   cfg_model "$HOME/.claude/settings.json" "~/.claude/settings.json" && return ;;
    codex)
      if [ -f "$HOME/.codex/config.toml" ]; then
        m=$(grep -E '^[[:space:]]*model[[:space:]]*=' "$HOME/.codex/config.toml" 2>/dev/null | head -n 1 | sed -e 's/.*=[[:space:]]*//' -e 's/^"//' -e 's/"[[:space:]]*$//')
        if [ -n "$m" ]; then printf '%s|model= in ~/.codex/config.toml' "$m"; return; fi
      fi ;;
  esac
  printf 'unknown|no model key in local config; CLI built-in default applies (tier-3 probe banner may reveal it)'
}

scan_cli() { # 1 name, 2 auth_fn, 3 seed model ids, 4 invocation
  local name=$1 authfn=$2 seeds=$3 invoc=$4 path ver auth dm
  path=$(command -v "$name" 2>/dev/null || true)
  if [ -z "$path" ]; then
    add_entry "$name" false "" "" "not-installed" "command -v $name: not found" "[]" "$invoc"
    return
  fi
  ver=$(run_to "$name" --version)
  auth=$($authfn)
  dm=$(default_model "$name")
  add_entry "$name" true "$path" "$ver" "${auth%%|*}" "${auth#*|}" "$(seed_models "$seeds")" "$invoc" "$dm"
}

scan_ollama() { # local models need no account: `ollama list` IS the verification
  local path ver list rc models="" id
  path=$(command -v ollama 2>/dev/null || true)
  if [ -z "$path" ]; then
    add_entry ollama false "" "" "not-installed" "command -v ollama: not found" "[]" "bash"
    return
  fi
  ver=$(run_to ollama --version)
  list=$(run_to ollama list); rc=$?
  if [ $rc -ne 0 ]; then
    add_entry ollama true "$path" "$ver" "unknown" "ollama list failed (server not running?): $list" "[]" "bash"
    return
  fi
  for id in $(printf '%s\n' "$list" | tail -n +2 | awk '{print $1}'); do
    models="${models:+$models,}{\"id\":\"$(jesc "$id")\",\"status\":\"verified\",\"evidence\":\"listed by ollama list (local; no account)\"}"
  done
  add_entry ollama true "$path" "$ver" "likely-authenticated" "local server responded to ollama list" "[$models]" "bash"
}

scan_cli claude   auth_claude   "haiku sonnet opus fable" "agent-tool"
scan_cli codex    auth_codex    "default" "bash"
scan_cli gemini   auth_gemini   "default" "bash"
scan_cli copilot  auth_copilot  "default" "bash"
scan_cli opencode auth_opencode "default" "bash"
scan_cli qwen     auth_qwen     "default" "bash"
scan_ollama

printf '{"schema":1,"tier":"1-2","tokens_spent":0,"generated_at":"%s","platform":"%s","clis":[%s]}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(jesc "$(uname -s) $(uname -m)")" "$ENTRIES"
