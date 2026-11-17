#!/usr/bin/env bash
# kb-search.sh — query a JishuDB knowledge base from inside an OpenClaw agent.
#
# Runs inside the OpenClaw container; reaches the KB container over the panel's
# cross-container path (host.docker.internal:<host-port>). No jq required; uses
# python3 to format if present, otherwise prints raw JSON for the agent to read.
#
# Usage:
#   kb-search.sh list                          # list available knowledge bases
#   kb-search.sh search "<query>" [kb] [topK]
#   kb-search.sh "<query>"                     # search default KB (JISHUDB_DEFAULT_KB)
#
# Env (the panel bind hook templates JISHUDB_URL / JISHUDB_DEFAULT_KB; both have
# sensible defaults so the skill also works when run by hand):
#   JISHUDB_URL         base URL of the KB service   (default http://host.docker.internal:18089)
#   JISHUDB_DEFAULT_KB  kb id used when none is given (optional)
#   JISHUDB_TOKEN       bearer token if the KB has auth enabled (optional)
set -uo pipefail

BASE="${JISHUDB_URL:-http://host.docker.internal:18089}"; BASE="${BASE%/}"
AUTH=(); [ -n "${JISHUDB_TOKEN:-}" ] && AUTH=(-H "authorization: Bearer ${JISHUDB_TOKEN}")
die() { echo "kb-search: $*" >&2; exit 1; }
command -v curl >/dev/null 2>&1 || die "curl not found in this environment"
HAVE_PY=0; command -v python3 >/dev/null 2>&1 && HAVE_PY=1

cmd="${1:-}"; case "$cmd" in search|list) shift;; *) cmd="search";; esac

if [ "$cmd" = "list" ]; then
  resp=$(curl -sS --max-time 15 "${AUTH[@]}" "$BASE/api/kb") \
    || die "cannot reach KB at $BASE — is the 知识库 (JishuDB) app running in the panel?"
  if [ "$HAVE_PY" = 1 ]; then
    JSON="$resp" python3 <<'PY' || printf '%s\n' "$resp"
import os, json
try: kbs = json.loads(os.environ["JSON"])
except Exception as e: print("(could not parse KB list:", e, ")"); raise SystemExit
if not kbs: print("(no knowledge bases yet — create one in the panel)"); raise SystemExit
print('Available knowledge bases (use the id with: kb-search.sh search "<query>" <id>):')
for k in kbs:
    print(f"  - {k.get('id')}  \"{k.get('name')}\"  ({k.get('chunks', 0)} chunks)")
PY
  else printf '%s\n' "$resp"; fi
  exit 0
fi

# ── search ──────────────────────────────────────────────────────────────────
QUERY="${1:-}"; KB="${2:-${JISHUDB_DEFAULT_KB:-}}"; TOPK="${3:-6}"
[ -n "$QUERY" ] || die "no query. usage: kb-search.sh search \"<query>\" [kb] [topK]"
[ -n "$KB" ]    || die "no knowledge base. run 'kb-search.sh list' then pass an id, or set JISHUDB_DEFAULT_KB"

if [ "$HAVE_PY" = 1 ]; then
  payload=$(QUERY="$QUERY" TOPK="$TOPK" python3 -c 'import os,json;print(json.dumps({"query":os.environ["QUERY"],"topK":int(os.environ["TOPK"])}))')
else
  payload="{\"query\":\"${QUERY//\"/\\\"}\",\"topK\":${TOPK}}"
fi

resp=$(curl -sS --max-time 40 "${AUTH[@]}" -H 'content-type: application/json' \
  -X POST "$BASE/api/kb/$KB/search" -d "$payload") \
  || die "cannot reach KB at $BASE — is the 知识库 app running?"

if [ "$HAVE_PY" = 1 ]; then
  JSON="$resp" python3 <<'PY' || printf '%s\n' "$resp"
import os, json
try: d = json.loads(os.environ["JSON"])
except Exception as e: print("(could not parse search response:", e, ")"); raise SystemExit
cites = d.get("citations") or d.get("hits") or []
if not cites: print("No matching passages found in this knowledge base."); raise SystemExit
print(f"Top {len(cites)} passages (cite the source filename in your answer):\n")
for i, c in enumerate(cites, 1):
    title = c.get("docTitle") or c.get("path") or c.get("docId") or "?"
    s = c.get("score")
    rel = "high" if isinstance(s,(int,float)) and s>=0.75 else "medium" if isinstance(s,(int,float)) and s>=0.5 else "low"
    t = (c.get("text") or c.get("snippet") or "").strip().replace("\n", " ")
    if len(t) > 600: t = t[:600] + " …"
    print(f"[{i}] {title}  (relevance: {rel})\n    {t}\n")
PY
else printf '%s\n' "$resp"; fi
