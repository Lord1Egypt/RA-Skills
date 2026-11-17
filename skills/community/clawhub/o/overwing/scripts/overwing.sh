#!/usr/bin/env bash
# Overwing helper for agents. Requires curl. Prints JSON to stdout; non-2xx
# responses exit 1 with the API's error body on stderr.
#   OVERWING_API_KEY    organization key (ow_live_...): guardrails, Tower setup, higher Atlas limits
#   OVERWING_AGENT_KEY  agent key (ow_agent_...): Tower operations
# `evaluate`, `who`, `agents`, `atlas`, `terms`, `signup` and `recover` need no key.
# Without a key, evaluate runs 10 times a day on inputs up to 2,000 characters, and the text is not stored.
set -euo pipefail

BASE_URL="${OVERWING_BASE_URL:-https://overwing.ai}"
RULE_SET="content-safety"
CONTEXT=""
NO_STORE=""

usage() {
  cat >&2 <<USAGE
Usage:
  overwing.sh evaluate [--rule-set <slug>] [--context '<json>'] [--no-store] "<text>"
                                                        score one text (or read text from stdin with "-")
                                                        (no key needed: 10 a day, up to 2,000 characters)
  overwing.sh batch    [--rule-set <slug>] [--context '<json>'] [--no-store]
                                                        JSON lines on stdin: {"id":"a","input":"..."}
  --context is a JSON object of facts the rules may read (recipient, channel,
  owns_contact_info, sender, purpose); pair it with --rule-set outbound-message.
  --no-store runs the check without keeping the text or the context (with a key;
  without a key the text is never stored).
  overwing.sh usage                                     today's quota and remaining checks
  overwing.sh whoami                                    which organization this key belongs to
  overwing.sh signup                                    create your own account, no email, and print the API key (once)
  overwing.sh signup <email> <password>                 create an account a person signs in to, and print the API key (once)
  overwing.sh domain start <domain>                     prove you control a domain: prints one value to publish there
  overwing.sh domain verify                             look for it; a proved domain lifts the limits and recovers a lost key
  overwing.sh recover start <domain>                    key lost: prints a value to publish at the proved domain (no key)
  overwing.sh recover verify <domain>                   revokes the old keys and prints one new key (once)
  overwing.sh claim <email> <password>                  a person takes charge of an account made with no email
  overwing.sh terms                                     pay-per-request price and network (x402)
  overwing.sh who "<user-agent string>"                 Atlas: what a User-Agent claims to be and whether to trust it
                                                        (no key needed: 10 a day; with OVERWING_API_KEY: 100 a day)
  overwing.sh agents [--q text] [--purpose p] [--operator o] [--limit n]
                                                        Atlas: search the registry of AI crawlers, fetchers and browser agents
  overwing.sh atlas                                     Atlas: registry counts, traffic shares, field-scan headlines (no key)

  Beacon: is a site reachable by agents? (free; no key: the summary; with OVERWING_API_KEY: the full report)
  overwing.sh beacon sample                             a real report in full, to see what a check returns
  overwing.sh beacon start <site>                       start a check; prints an id
  overwing.sh beacon report <id>                        run the check and print the report (status "running": ask again)

  Tower setup (OVERWING_API_KEY):
  overwing.sh tower setup                               load the starter workflow (email PO to order entry)
  overwing.sh tower agent-create <name> <scope,scope>   create an agent; prints its key once ("*" = every operation)
  overwing.sh tower agents                              list agents (keys are never shown)
  overwing.sh tower agent-revoke <agent_id>             revoke an agent at once
  Tower operations (OVERWING_AGENT_KEY):
  overwing.sh tower capabilities                        operations you may call, with JSON Schema inputs
  overwing.sh tower decide <operation> '<input json>'   how it would be ruled; no side effects
  overwing.sh tower submit <operation> '<input json>' --key <idempotency-key> [--dry-run]
                                                        executed, pending (a person must approve) or rejected
  overwing.sh tower get <action_id>                     status and result
  overwing.sh tower compensate <action_id>              undo an executed action, once
  overwing.sh tower receipt <id|sequence>               one signed receipt
  overwing.sh tower verify [from] [to]                  recompute the receipt chain's hashes and signatures
USAGE
  exit 2
}

json_escape() {
  # Escape a string for inclusion in JSON without requiring jq.
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || {
    local s; s=$(cat); s=${s//\\/\\\\}; s=${s//\"/\\\"}; s=${s//$'\n'/\\n}; s=${s//$'\t'/\\t}; printf '"%s"' "$s"
  }
}

store_field() {
  # Emits ,"store":false when --no-store was given.
  [ -z "$NO_STORE" ] || printf ',"store":false'
}

context_field() {
  # Emits ,"context":<json> when --context was given (must be a JSON object).
  [ -z "$CONTEXT" ] && return 0
  case "$CONTEXT" in \{*\}) printf ',"context":%s' "$CONTEXT" ;; *) echo '{"error":"--context must be a JSON object, e.g. {\"recipient\":\"customer\"}"}' >&2; exit 2 ;; esac
}

require_key() {
  if [ -z "${OVERWING_API_KEY:-}" ]; then
    echo '{"error":"OVERWING_API_KEY is not set. Ask your human for a key (https://overwing.ai/login) or run: overwing.sh signup"}' >&2
    exit 1
  fi
}

require_agent_key() {
  if [ -z "${OVERWING_AGENT_KEY:-}" ]; then
    echo '{"error":{"code":"unauthorized","message":"OVERWING_AGENT_KEY is not set","retryable":false,"suggested_fix":"Ask your human for an agent key, or with an organization key run: overwing.sh tower agent-create <name> <scopes>"}}' >&2
    exit 1
  fi
}

require_object() {
  # require_object <json> <what>
  case "$1" in \{*\}) ;; *) printf '{"error":"%s must be a JSON object"}\n' "$2" >&2; exit 2 ;; esac
}

urlencode() {
  python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read(), safe=""))' 2>/dev/null || sed 's/%/%25/g; s/ /%20/g; s/;/%3B/g; s/(/%28/g; s/)/%29/g; s/+/%2B/g; s/&/%26/g; s/#/%23/g; s/?/%3F/g; s/\//%2F/g'
}

# The credential `call` sends. Empty means no Authorization header at all (keyless).
TOKEN="${OVERWING_API_KEY:-}"
# Extra HTTP statuses whose body is an answer, not an error (space separated).
ACCEPT=""

call() {
  # call <method> <path> [json-body]
  local method="$1" path="$2" body="${3:-}" tmp code
  local -a args=(-sS -m 60 -X "$method" "$BASE_URL$path" -H "Accept: application/json" -H "User-Agent: overwing-skill/1.8 (openclaw)")
  [ -n "$TOKEN" ] && args+=(-H "Authorization: Bearer $TOKEN")
  [ -n "$body" ] && args+=(-H "Content-Type: application/json" --data-binary "$body")
  tmp=$(mktemp)
  code=$(curl "${args[@]}" -o "$tmp" -w '%{http_code}')
  if [ "${code:0:1}" = "2" ]; then cat "$tmp"; echo; rm -f "$tmp"; return 0; fi
  case " $ACCEPT " in *" $code "*) cat "$tmp"; echo; rm -f "$tmp"; return 0 ;; esac
  cat "$tmp" >&2; echo >&2; rm -f "$tmp"; return 1
}

cmd="${1:-}"; shift || true
case "$cmd" in
  evaluate)
    # No key needed: the free allowance applies. A key lifts the limits.
    while [ $# -gt 0 ]; do
      case "$1" in
        --rule-set) RULE_SET="$2"; shift 2 ;;
        --context) CONTEXT="$2"; shift 2 ;;
        --no-store) NO_STORE=1; shift ;;
        -) text=$(cat); shift ;;
        *) text="$1"; shift ;;
      esac
    done
    [ -n "${text:-}" ] || usage
    body=$(printf '{"input":%s,"rule_set":%s,"metadata":{"source":"openclaw-skill"}%s}' "$(printf '%s' "$text" | json_escape)" "$(printf '%s' "$RULE_SET" | json_escape)" "$(context_field)$(store_field)")
    call POST /api/v1/evaluate "$body"
    ;;
  batch)
    require_key
    while [ $# -gt 0 ]; do case "$1" in --rule-set) RULE_SET="$2"; shift 2 ;; --context) CONTEXT="$2"; shift 2 ;; --no-store) NO_STORE=1; shift ;; *) usage ;; esac; done
    items=$(grep -v '^\s*$' | paste -sd, -)
    [ -n "$items" ] || usage
    call POST /api/v1/evaluate/batch "{\"rule_set\":$(printf '%s' "$RULE_SET" | json_escape),\"items\":[$items]$(context_field)$(store_field)}"
    ;;
  usage) require_key; call GET "/api/v1/usage?days=1" ;;
  whoami) require_key; call GET /api/v1/me ;;
  signup)
    # No arguments: an account with no email. Nothing is sent to anyone; the key is the account.
    case $# in
      0) body='{"org_name":"OpenClaw agent"}' ;;
      2) body=$(printf '{"email":%s,"password":%s,"org_name":"OpenClaw agent"}' "$(printf '%s' "$1" | json_escape)" "$(printf '%s' "$2" | json_escape)") ;;
      *) usage ;;
    esac
    TOKEN="" call POST /api/v1/signup "$body"
    ;;
  domain)
    require_key
    sub="${1:-}"; shift || true
    case "$sub" in
      start) [ $# -ge 1 ] || usage; call POST /api/v1/org/domain "{\"domain\":$(printf '%s' "$1" | json_escape)}" ;;
      # 422 means the value is not at the domain yet: an answer, not a failure.
      verify) ACCEPT="422" call POST /api/v1/org/domain/verify ;;
      *) usage ;;
    esac
    ;;
  recover)
    sub="${1:-}"; shift || true
    [ $# -ge 1 ] || usage
    case "$sub" in
      start) TOKEN="" call POST /api/v1/signup/recover "{\"domain\":$(printf '%s' "$1" | json_escape)}" ;;
      verify) TOKEN="" ACCEPT="422" call POST /api/v1/signup/recover/verify "{\"domain\":$(printf '%s' "$1" | json_escape)}" ;;
      *) usage ;;
    esac
    ;;
  claim)
    require_key
    [ $# -ge 2 ] || usage
    call POST /api/v1/org/claim "$(printf '{"email":%s,"password":%s}' "$(printf '%s' "$1" | json_escape)" "$(printf '%s' "$2" | json_escape)")"
    ;;
  terms) TOKEN="" call GET /.well-known/x402 ;;
  who)
    # No key needed. A key, when set, raises the daily allowance.
    [ $# -ge 1 ] || usage
    call GET "/api/v1/atlas/lookup?user_agent=$(printf '%s' "$1" | urlencode)"
    ;;
  agents)
    qs="limit=20"
    while [ $# -gt 0 ]; do case "$1" in --q) qs="$qs&q=$(printf '%s' "$2" | urlencode)"; shift 2 ;; --purpose) qs="$qs&purpose=$(printf '%s' "$2" | urlencode)"; shift 2 ;; --operator) qs="$qs&operator=$(printf '%s' "$2" | urlencode)"; shift 2 ;; --limit) qs="${qs/limit=20/limit=$2}"; shift 2 ;; *) usage ;; esac; done
    call GET "/api/v1/atlas/agents?$qs"
    ;;
  atlas) TOKEN="" call GET /api/v1/atlas/summary ;;
  beacon)
    # Free. No key gives the summary; a key, when set, gives the full report and saves the check to that dashboard.
    sub="${1:-}"; shift || true
    case "$sub" in
      sample) TOKEN="" call GET /api/v1/beacon/sample ;;
      start)
        [ $# -ge 1 ] || usage
        call POST /api/v1/beacon/checks "{\"url\":$(printf '%s' "$1" | json_escape)}"
        ;;
      report)
        [ $# -ge 1 ] || usage
        call GET "/api/v1/beacon/checks/$(printf '%s' "$1" | urlencode)"
        ;;
      *) usage ;;
    esac
    ;;
  tower)
    sub="${1:-}"; shift || true
    case "$sub" in
      setup) require_key; call POST /api/v1/tower/template '{}' ;;
      agent-create)
        require_key
        [ $# -ge 2 ] || usage
        scopes=$(printf '%s' "$2" | tr ', ' '\n\n' | grep -v '^$' | while IFS= read -r sc; do printf '%s,' "$(printf '%s' "$sc" | json_escape)"; done)
        [ -n "$scopes" ] || usage
        call POST /api/v1/tower/agents "{\"name\":$(printf '%s' "$1" | json_escape),\"scopes\":[${scopes%,}]}"
        ;;
      agents) require_key; call GET /api/v1/tower/agents ;;
      agent-revoke) require_key; [ $# -ge 1 ] || usage; call DELETE "/api/v1/tower/agents/$(printf '%s' "$1" | urlencode)" ;;
      capabilities) require_agent_key; TOKEN="$OVERWING_AGENT_KEY" call GET /api/v1/tower/capabilities ;;
      decide)
        require_agent_key
        [ $# -ge 2 ] || usage
        require_object "$2" "input"
        TOKEN="$OVERWING_AGENT_KEY" call POST /api/v1/tower/decide "{\"operation\":$(printf '%s' "$1" | json_escape),\"input\":$2}"
        ;;
      submit)
        require_agent_key
        [ $# -ge 2 ] || usage
        op="$1"; input="$2"; shift 2
        idem=""; dry=""
        while [ $# -gt 0 ]; do case "$1" in --key) idem="$2"; shift 2 ;; --dry-run) dry=',"dry_run":true'; shift ;; *) usage ;; esac; done
        require_object "$input" "input"
        if [ -z "$idem" ]; then echo '{"error":{"code":"invalid_request","field":"idempotency_key","message":"--key is required","retryable":false,"suggested_fix":"Pass --key with something stable for this business request, such as the source message id"}}' >&2; exit 2; fi
        # 422 is a ruling (rejected), not a failure: print it and let the caller read status.
        TOKEN="$OVERWING_AGENT_KEY" ACCEPT="422" call POST /api/v1/tower/actions "{\"operation\":$(printf '%s' "$op" | json_escape),\"input\":$input,\"idempotency_key\":$(printf '%s' "$idem" | json_escape)$dry}"
        ;;
      get) require_agent_key; [ $# -ge 1 ] || usage; TOKEN="$OVERWING_AGENT_KEY" call GET "/api/v1/tower/actions/$(printf '%s' "$1" | urlencode)" ;;
      compensate) require_agent_key; [ $# -ge 1 ] || usage; TOKEN="$OVERWING_AGENT_KEY" call POST "/api/v1/tower/actions/$(printf '%s' "$1" | urlencode)/compensate" '{}' ;;
      receipt) require_agent_key; [ $# -ge 1 ] || usage; TOKEN="$OVERWING_AGENT_KEY" call GET "/api/v1/tower/receipts/$(printf '%s' "$1" | urlencode)" ;;
      verify)
        require_agent_key
        qs=""
        [ -n "${1:-}" ] && qs="?from=$(printf '%s' "$1" | urlencode)"
        [ -n "${2:-}" ] && qs="$qs&to=$(printf '%s' "$2" | urlencode)"
        TOKEN="$OVERWING_AGENT_KEY" call GET "/api/v1/tower/receipts/verify$qs"
        ;;
      *) usage ;;
    esac
    ;;
  *) usage ;;
esac
