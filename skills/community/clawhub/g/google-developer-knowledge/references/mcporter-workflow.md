# Google Developer Knowledge via mcporter

## Capability discovery

Use the installed `mcporter`. If a flag is unavailable, check `mcporter list --help` or `mcporter call --help` and inspect the live tool schema. Use a configured server; this workflow does not create a server, write config, import editor credentials, or start OAuth. The smoke test used a gateway exposing `GoogleDeveloperKnowledge-*`; direct servers use unprefixed names. Neither is assumed by the workflow. Only probe configured servers you trust.

Run this block in Bash and keep the same shell for the following examples. `GOOGLE_DEVELOPER_KNOWLEDGE_MCP_SERVER` optionally prioritizes a configured alias; `GOOGLE_DEVELOPER_KNOWLEDGE_MCPORTER_CONFIG` optionally chooses a config file for both discovery and calls. Discovery defaults to 8 s per server (`GDK_MCP_TIMEOUT_MS`); calls default to 30 s (`GDK_CALL_TIMEOUT_MS`). These are workflow defaults, not mcporter defaults.

```bash
mcporter_cmd() {
  if [[ -n "${GOOGLE_DEVELOPER_KNOWLEDGE_MCPORTER_CONFIG:-}" ]]; then
    mcporter --config "$GOOGLE_DEVELOPER_KNOWLEDGE_MCPORTER_CONFIG" "$@"
  else
    mcporter "$@"
  fi
}

discover_gdk() {
  local cfg candidates server schema route
  cfg=$(mcporter_cmd config list --json) || return 1
  candidates=$(jq -r --arg preferred "${GOOGLE_DEVELOPER_KNOWLEDGE_MCP_SERVER:-}" '
    [.servers[]?.name | strings] | unique |
    sort_by(if . == $preferred then 0 else 1 end)[]' <<<"$cfg") || return 1
  while IFS= read -r server; do
    [[ -n "$server" ]] || continue
    if ! schema=$(mcporter_cmd list "$server" --schema --json --no-oauth \
        --timeout "${GDK_MCP_TIMEOUT_MS:-8000}" --exit-code); then
      printf 'gdk-discovery: %s: schema unavailable (see CLI diagnostic)\n' "$server" >&2
      continue
    fi
    if route=$(jq -ec --arg server "$server" '
      [.tools[]?.name] as $names |
      ["GoogleDeveloperKnowledge-", ""][] as $p |
      {search: ($p+"search_documents"), get: ($p+"get_documents"), answer: ($p+"answer_query")} as $t |
      select(($t | [.search,.get] - $names | length) == 0) |
      {server: $server, tools: ($t | if ($names | index($t.answer)) == null then del(.answer) else . end)}' <<<"$schema"); then
      printf '%s\n' "${route%%$'\n'*}"
      return 0
    fi
    printf 'gdk-discovery: %s: missing search/get or invalid schema\n' "$server" >&2
  done <<<"$candidates"
  echo "gdk-discovery: no configured server exposes compatible search/get tools" >&2
  return 1
}

gdk_init() {
  gdk_route=$(discover_gdk) || return 1
  gdk_server=$(jq -er '.server' <<<"$gdk_route") || return 1
  gdk_search_tool=$(jq -er '.tools.search' <<<"$gdk_route") || return 1
  gdk_get_tool=$(jq -er '.tools.get' <<<"$gdk_route") || return 1
  gdk_answer_tool=$(jq -r '.tools.answer // empty' <<<"$gdk_route") || return 1
}

gdk_call() {
  [[ -n "${gdk_server:-}" && -n "$1" ]] || return 1
  mcporter_cmd call "$gdk_server.$1" --args "$2" --output json --no-oauth \
    --timeout "${GDK_CALL_TIMEOUT_MS:-30000}"
}

gdk_init
```

If `gdk_init` fails, stop and follow the failure matrix. A tool list proves discovery, not that an upstream call succeeds. A missing answer tool does not disable search and retrieval. For a single known, configured alias, `mcporter list "$server" --schema --json --no-oauth --timeout 8000 --exit-code` shows the exact names and schemas. Do not log the whole config.

## Choose a tool

| MCP tool | Request and result | Use it for |
| --- | --- | --- |
| `search_documents` | `{query: string}` → `results[]` with `parent`, `id`, `content` | Default for exact flags, errors, code, settings, or a document lookup. Chunks are excerpts; `id` is local to a document and may change. |
| `get_documents` | `{names: string[]}` → `documents[]` with `name`, `uri`, `title`, `description`, and full Markdown `content` | Fetch 1–20 exact resource names in request order. The skill checks at most 3 by default. Use only names actually returned in `parent` or `references`; never construct them from a URL. |
| `answer_query` | `{query: string}` → `answerText`, `references: string[]` | Optional conceptual synthesis with limited quota. Deduplicate references and fetch the relevant full source if the claim is consequential. |

The MCP tools listed and tested do not take `filter`, `pageSize`, or `pageToken`. Add the product and exact term to the query, or use the [REST fallback](api-fallback.md) if API-level filtering is necessary and authenticated.

### Search and fetch one source

```bash
gdk_search_and_get() {
  local query="$1" search_json parent docs_json
  search_json=$(gdk_call "$gdk_search_tool" "$(jq -nc --arg query "$query" '{$query}')") || return 1
  jq -e '.isError != true and (.results | type == "array")' <<<"$search_json" >/dev/null || return 1
  jq -r '.results[] | [.parent, (.content | .[:160])] | @tsv' <<<"$search_json" >&2
  # This smoke example uses the first returned result. For research, pick by relevance.
  parent=$(jq -er '.results[0].parent | strings | select(startswith("documents/"))' <<<"$search_json") || return 1
  docs_json=$(gdk_call "$gdk_get_tool" "$(jq -nc --arg name "$parent" '{names:[$name]}')") || return 1
  jq -e --arg name "$parent" '.isError != true and any(.documents[]?; .name == $name and (.content | type == "string" and length > 0))' <<<"$docs_json" >/dev/null || return 1
  jq '.documents[] | {name,uri,title,content}' <<<"$docs_json"
}

gdk_search_and_get "Cloud Run minimum instances request-based billing idle rate"
```

For multiple sources, combine and deduplicate the selected returned resource names into a JSON `names` array. Read `documents[].uri` for citation; use `documents[].content` to verify the claim before summarizing. With `--output json`, the tested batch returned the unwrapped tool object. If another client returns an MCP envelope, pass through `structuredContent` (or decode the JSON text block if present), reject `isError: true`, and validate the expected fields before using it. Exit status 0 alone is not evidence that the requested result exists.

### Conceptual query

```bash
gdk_answer() {
  [[ -n "$gdk_answer_tool" ]] || return 1
  local payload response
  payload=$(jq -nc --arg query "$1" '{$query}') || return 1
  response=$(gdk_call "$gdk_answer_tool" "$payload") || return 1
  jq -e '.isError != true and (.answerText | type == "string" and length > 0) and any(.references[]?; type == "string" and startswith("documents/"))' <<<"$response" >/dev/null || return 1
  jq '.references |= unique | {answerText,references}' <<<"$response"
}

gdk_answer "When should I use Firestore batched writes instead of transactions?"
```

## Failure matrix

- **`answer_query` 429 / `RESOURCE_EXHAUSTED`:** Skip retries of the generative tool on a quota error. Use `search_documents` then `get_documents`, as Google recommends. Do likewise when the answer times out, has no relevant references, or is unavailable.
- **Search has no relevant match:** Refine once using the canonical product name and exact setting or error. If it still misses, report the corpus gap and look for the relevant public official page. `answer_query` uses the same corpus and is not a second search index.
- **Transport/handshake timeout or no compatible schema:** Keep the CLI diagnostic separate from a valid empty search. For a transient read-only failure, at most one retry on the same verified route; then use an authenticated REST fallback or a public official page.
- **401 or 403:** Stop and report authentication/authorization failure. Do not launch OAuth, swap identities, or alter config as part of this lookup. Use official public docs if sufficient.
- **Full-document misses:** Confirm `names` is an array, use the exact returned names, and check the response contains the requested documents. Do not guess replacement resource IDs.

## Official connection and live smoke evidence

Google documents a remote Streamable HTTP endpoint at `https://developerknowledge.googleapis.com/mcp`. A direct client can use `X-Goog-Api-Key` over HTTPS, or separately configured OAuth/ADC per the [setup guide](https://developers.google.com/knowledge/mcp). If your gateway already provides the tools, use that route; do not add a redundant direct server or expose gateway secrets. A schema listing is not evidence that direct Google authentication works.

The live smoke test via `mcporter` and a configured gateway covered:

- Cloud Run minimum-instances billing: 5 chunks; the [full page](https://docs.cloud.google.com/run/docs/configuring/min-instances) confirms the idle rate for minimum instances with request-based billing.
- Firebase Android 13 notifications: 5 chunks; the [full page](https://firebase.google.com/docs/cloud-messaging/android/get-started) confirms the runtime permission requirement for showing notifications.
- Firestore batched writes vs transactions: grounded `answerText` plus 2 unique references; the [standard Firestore page](https://firebase.google.com/docs/firestore/manage-data/transactions) confirms the read dependency and offline distinction. Do not conflate the standard and Enterprise references.
- One `get_documents` call retrieved the above three full documents by their returned resource names, in order. No direct REST credentials or MCP setup changes were needed.

References: [official tool catalog](https://developers.google.com/knowledge/reference/mcp), [search](https://developers.google.com/knowledge/reference/mcp/tools_list/search_documents), [get](https://developers.google.com/knowledge/reference/mcp/tools_list/get_documents), [answer](https://developers.google.com/knowledge/reference/mcp/tools_list/answer_query), [corpus](https://developers.google.com/knowledge/reference/corpus-reference).
