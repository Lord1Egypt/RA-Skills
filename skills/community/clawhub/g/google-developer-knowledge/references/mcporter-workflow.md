# Google Developer Knowledge via mcporter

This reference defines a runtime-neutral workflow for Google Developer Knowledge MCP tools. It discovers capability instead of assuming a server name, gateway, or credentials.

## Capability Discovery

Accepted tool-name sets are either gateway-prefixed:

- `GoogleDeveloperKnowledge-search_documents`
- `GoogleDeveloperKnowledge-get_documents`
- `GoogleDeveloperKnowledge-answer_query`

or direct MCP names:

- `search_documents`
- `get_documents`
- `answer_query`

`GOOGLE_DEVELOPER_KNOWLEDGE_MCP_SERVER` optionally prefers one configured server. `GOOGLE_DEVELOPER_KNOWLEDGE_MCPORTER_CONFIG` optionally selects an isolated mcporter config. Neither bypasses capability verification.

```bash
#!/usr/bin/env bash
set -euo pipefail

gdk_timeout_ms="${GDK_MCP_TIMEOUT_MS:-7000}"
gdk_preferred_server="${GOOGLE_DEVELOPER_KNOWLEDGE_MCP_SERVER:-}"
gdk_config="${GOOGLE_DEVELOPER_KNOWLEDGE_MCPORTER_CONFIG:-}"

mcporter_cmd() {
  if [[ -n "$gdk_config" ]]; then
    mcporter --config "$gdk_config" "$@"
  else
    mcporter "$@"
  fi
}

servers_json="$(mcporter_cmd config list --json)" || {
  echo "gdk-discovery: mcporter-config-unavailable" >&2
  exit 1
}

mapfile -t configured_servers < <(jq -r '.servers[]?.name' <<<"$servers_json")
if [[ -n "$gdk_preferred_server" ]]; then
  candidates=("$gdk_preferred_server")
  for server in "${configured_servers[@]}"; do
    [[ "$server" == "$gdk_preferred_server" ]] || candidates+=("$server")
  done
else
  candidates=("${configured_servers[@]}")
fi

failures=()
for server in "${candidates[@]}"; do
  if [[ -n "$gdk_config" ]]; then
    schema="$(mcporter --config "$gdk_config" list "$server" --schema --json --timeout "$gdk_timeout_ms" 2>/dev/null)" || {
      failures+=("$server:schema-unavailable")
      continue
    }
  else
    schema="$(mcporter list "$server" --schema --json --timeout "$gdk_timeout_ms" 2>/dev/null)" || {
      failures+=("$server:schema-unavailable")
      continue
    }
  fi
  if jq -e '
    [.tools[]?.name] as $tools |
    ($tools | index("GoogleDeveloperKnowledge-search_documents")) and
    ($tools | index("GoogleDeveloperKnowledge-get_documents")) and
    ($tools | index("GoogleDeveloperKnowledge-answer_query"))
  ' >/dev/null <<<"$schema"; then
    jq -nc --arg server "$server" '{server: $server, tools: {search: "GoogleDeveloperKnowledge-search_documents", get: "GoogleDeveloperKnowledge-get_documents", answer: "GoogleDeveloperKnowledge-answer_query"}}'
    exit 0
  fi
  if jq -e '
    [.tools[]?.name] as $tools |
    ($tools | index("search_documents")) and
    ($tools | index("get_documents")) and
    ($tools | index("answer_query"))
  ' >/dev/null <<<"$schema"; then
    jq -nc --arg server "$server" '{server: $server, tools: {search: "search_documents", get: "get_documents", answer: "answer_query"}}'
    exit 0
  fi
  failures+=("$server:missing-required-tools")
done

echo "gdk-discovery: no-healthy-google-developer-knowledge-server configured=${candidates[*]:-none} failures=${failures[*]:-none}" >&2
exit 1
```

The command writes only the selected route JSON to stdout. Capture it and use its server and tool names for every call in the same task:

```bash
gdk_route="$(./discover-google-developer-knowledge-server.sh)"
gdk_server="$(jq -r '.server' <<<"$gdk_route")"
gdk_search_tool="$(jq -r '.tools.search' <<<"$gdk_route")"
gdk_get_tool="$(jq -r '.tools.get' <<<"$gdk_route")"
gdk_answer_tool="$(jq -r '.tools.answer' <<<"$gdk_route")"
```

If discovery fails, retain its stderr reason. Do not guess a server name. Follow the Failure Matrix below.

## Default Research Flow

Use `search_documents` first for source-backed documentation lookup:

```bash
mcporter call "$gdk_server.$gdk_search_tool" \
  --args '{"query":"Vertex AI Feature Store online serving point in time correctness"}' \
  --output json
```

Inspect `results[]`:

- `parent`: document resource name for `get_documents`
- `id`: chunk id inside the document; not globally stable
- `content`: matched documentation chunk

Then fetch only the strongest parent documents:

```bash
mcporter call "$gdk_server.$gdk_get_tool" \
  --args '{"names":["documents/docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview"]}' \
  --output json
```

Use `documents[]` fields:

- `name`: document resource name
- `uri`: public source URL
- `title`: document title
- `description`: document description
- `content`: full Markdown content

## Direct Answer Flow

Use `answer_query` only for a concise first pass:

```bash
mcporter call "$gdk_server.$gdk_answer_tool" \
  --args '{"query":"How should I choose between Cloud Run and Cloud Functions for an HTTP API?"}' \
  --output json
```

Its `answerText` and `references[]` are useful synthesis aids. For version-sensitive, pricing, quota, security, migration, or implementation claims, retrieve the referenced documents with `get_documents` before responding.

## Query Patterns

Use focused public documentation questions; do not include credentials, proprietary code, or private incident details.

```bash
mcporter call "$gdk_server.$gdk_search_tool" \
  --args '{"query":"Cloud Run minimum instances billing request based instance based"}' \
  --output json

mcporter call "$gdk_server.$gdk_search_tool" \
  --args '{"query":"Firebase Cloud Messaging Android 13 POST_NOTIFICATIONS permission"}' \
  --output json
```

If results are broad, add the canonical product name, exact setting or API symbol, and task shape such as `pricing`, `quota`, `troubleshooting`, `Python example`, or `migration`.

## Failure Matrix

| Trigger | First action | Fallback or stop |
| --- | --- | --- |
| `mcporter` unavailable or config lookup fails | Report `mcporter-config-unavailable`. | Use REST only after API key preflight; otherwise retrieve the relevant official Google page. |
| No capable server, timeout, or schema drift | Report `no-healthy-google-developer-knowledge-server` and configured candidate names. | Do not guess an alias; use the same REST-or-official-document fallback. |
| `answer_query` returns 429 | Honor a valid `Retry-After` once; otherwise wait one second, then retry once. | On a second failure, use `search_documents` plus `get_documents`. |
| `answer_query` times out or references are insufficient | Stop using `answer_query` for this task. | Use `search_documents` plus `get_documents`. |
| MCP or REST returns 401 or 403 | Stop; do not retry with alternate credentials. | Report authentication or authorization failure; use public official pages if sufficient. |
| Search is empty or irrelevant | Simplify the query once and use the canonical product name. | If still empty, state the corpus gap and use the product's official docs. |
| Full document is large | Retrieve only the returned parents needed for the question. | Ask before broad extraction or offline use. |
| REST fallback selected without an API key or OAuth token plus quota project | Do not construct a REST request. | Use public official Google documentation and disclose the fallback reason. |

## Answering Pattern

1. State the practical answer.
2. State whether the evidence came from MCP, REST, or an official-document fallback.
3. Include official source URLs from `documents[].uri` when behavior is current or version-sensitive.
4. Call out gaps when retrieved documents do not establish a requested detail.

## Official Setup References

- Developer Knowledge API: `https://developers.google.com/knowledge/api`
- Quickstart: `https://developers.google.com/knowledge/quickstart`
- MCP setup: `https://developers.google.com/knowledge/mcp`
- MCP reference: `https://developers.google.com/knowledge/reference/mcp`
- Corpus reference: `https://developers.google.com/knowledge/reference/corpus-reference`
