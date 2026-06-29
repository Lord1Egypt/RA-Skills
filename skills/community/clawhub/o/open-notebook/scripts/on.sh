#!/usr/bin/env bash
# Open Notebook  -  bridge client for OpenClaw agents
# Bridge: http://127.0.0.1:5077 → open-notebook API at 127.0.0.1:5055
set -euo pipefail

BRIDGE_URL="${OPEN_NOTEBOOK_BRIDGE_URL:-http://127.0.0.1:5077}"
API_KEY="${OPEN_NOTEBOOK_API_KEY:?OPEN_NOTEBOOK_API_KEY not set  -  add it to ~/.openclaw/.env and restart the gateway}"

call() {
  local method="$1" path="$2" body="${3:-}"
  if [[ -n "$body" ]]; then
    curl -sf --max-time 120 -X "$method" \
      -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
      -d "$body" "${BRIDGE_URL}${path}"
  else
    curl -sf --max-time 120 -X "$method" \
      -H "X-API-Key: $API_KEY" "${BRIDGE_URL}${path}"
  fi
}

# Build JSON: tries jq first, falls back to python3
# Formats: notebook-create, source-add, search, ask
jq_or_py() {
  local fmt="$1"; shift
  if command -v jq &>/dev/null; then
    case "$fmt" in
      notebook-create) jq -nc --arg n "${n:-}" --arg d "${d:-}" '{"name":$n,"description":$d}' ;;
      source-add)     jq -nc --arg t "${t:-}" --arg v "${v:-}" --arg ti "${ti:-}" '{"type":$t,"content":$v,"title":$ti}' ;;
      search)         jq -nc --arg q "${q:-}" '{"query":$q}' ;;
      ask)            jq -nc --arg q "${q:-}" '{"question":$q}' ;;
    esac
  else
    case "$fmt" in
      notebook-create) python3 -c "import sys,json; print(json.dumps({'name':sys.argv[1],'description':sys.argv[2]},ensure_ascii=False))" "${n:-}" "${d:-}" ;;
      source-add)     python3 -c "import sys,json; print(json.dumps({'type':sys.argv[1],'content':sys.argv[2],'title':sys.argv[3]},ensure_ascii=False))" "${t:-}" "${v:-}" "${ti:-}" ;;
      search)         python3 -c "import sys,json; print(json.dumps({'query':sys.argv[1]},ensure_ascii=False))" "${q:-}" ;;
      ask)            python3 -c "import sys,json; print(json.dumps({'question':sys.argv[1]},ensure_ascii=False))" "${q:-}" ;;
    esac
  fi
}

case "${1:-help}" in
  health)
    call GET /v1/health
    ;;

  list-notebooks)
    call GET /v1/notebooks
    ;;

  get-notebook)
    [[ $# -ge 2 ]] || { echo "usage: $0 get-notebook ID" >&2; exit 1; }
    call GET "/v1/notebooks/$2"
    ;;

  create-notebook)
    [[ $# -ge 2 ]] || { echo "usage: $0 create-notebook NAME [DESC]" >&2; exit 1; }
    call POST /v1/notebooks "$(n="$2" d="${3:-}"; jq_or_py notebook-create)"
    ;;

  add-source)
    nb="$2"; shift 2
    title=""; input_type=""; input=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --text)  input_type="text";  input="$2"; shift 2 ;;
        --url)   input_type="url";   input="$2"; shift 2 ;;
        --file)  input_type="file";  input="$2"; shift 2 ;;
        --title) title="$2"; shift 2 ;;
        *) echo "unknown flag: $1" >&2; exit 1 ;;
      esac
    done
    [[ -n "$input_type" ]] || { echo "need --text, --url, or --file" >&2; exit 1; }
    call POST "/v1/notebooks/$nb/sources" "$(t="$input_type" v="$input" ti="$title"; jq_or_py source-add)"
    ;;

  get-source)
    [[ $# -ge 2 ]] || { echo "usage: $0 get-source ID" >&2; exit 1; }
    call GET "/v1/sources/$2"
    ;;

  search)
    [[ $# -ge 2 ]] || { echo "usage: $0 search QUERY" >&2; exit 1; }
    call POST /v1/search "$(q="$2"; jq_or_py search)"
    ;;

  ask)
    [[ $# -ge 3 ]] || { echo "usage: $0 ask NOTEBOOK_ID QUESTION" >&2; exit 1; }
    call POST "/v1/notebooks/$2/chat" "$(q="$3"; jq_or_py ask)"
    ;;

  delete-source)
    [[ $# -ge 2 ]] || { echo "usage: $0 delete-source ID" >&2; exit 1; }
    call DELETE "/v1/sources/$2"
    ;;

  delete-notebook)
    [[ $# -ge 2 ]] || { echo "usage: $0 delete-notebook ID" >&2; exit 1; }
    call DELETE "/v1/notebooks/$2"
    ;;

  *)
    cat <<EOF >&2
on.sh  -  open-notebook bridge client (v1.3.2)

Commands:
  health                                       bridge + open-notebook liveness
  list-notebooks                               list allowed notebooks
  get-notebook ID                              notebook details
  create-notebook NAME [DESC]                  create a new notebook
  add-source NB --text|--url|--file VAL [--title T]
                                               add a source to a notebook
  get-source ID                                source status (poll while processing)
  search QUERY                                 cross-notebook vector search
  ask NB QUESTION                              RAG answer from one notebook
  delete-source ID                             ⚠️ remove a source (irreversible)
  delete-notebook ID                           remove a notebook (irreversible)

Env:
  OPEN_NOTEBOOK_BRIDGE_URL   default http://127.0.0.1:5077
  OPEN_NOTEBOOK_API_KEY      required, per-agent from bridge/agents.json
EOF
    exit 1
    ;;
esac
