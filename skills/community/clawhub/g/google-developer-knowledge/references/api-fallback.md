# Developer Knowledge REST API Fallback

Use this reference only when the preferred `mcporter` MCP workflow is unavailable, when testing client integration outside MCP, or when the task specifically asks for direct REST API calls.

Before using REST, verify one supported authentication path: `DEVELOPERKNOWLEDGE_API_KEY`, or both `DEVELOPERKNOWLEDGE_OAUTH_ACCESS_TOKEN` and `GOOGLE_CLOUD_QUOTA_PROJECT`. If neither is available, do not issue a REST request; use the relevant public Google documentation and state that the REST fallback was unavailable.

The MCP and REST response fields are not interchangeable. These examples use REST v1; the live smoke tests exercised MCP only. Use approved credentials from the environment, never literal keys in files or chat. Do not echo authenticated commands or enable shell tracing.

## Authentication

The Developer Knowledge REST API uses an API key in the `key` query parameter.

```bash
export DEVELOPERKNOWLEDGE_API_KEY="YOUR_API_KEY"
```

Requirements:

- Enable `developerknowledge.googleapis.com` in the Google Cloud project.
- Restrict the API key to Developer Knowledge API when possible.
- If the same key is reused for Gemini model calls, also allow Generative Language API.

## OAuth with a Quota Project

Use this alternative when an OAuth access token and quota project are available. Do not persist a short-lived access token in an MCP configuration.

```bash
export DEVELOPERKNOWLEDGE_OAUTH_ACCESS_TOKEN="ACCESS_TOKEN"
export GOOGLE_CLOUD_QUOTA_PROJECT="YOUR_PROJECT_ID"

curl --get "https://developerknowledge.googleapis.com/v1/documents:searchDocumentChunks" \
  --data-urlencode "query=Cloud Run minimum instances billing" \
  -H "Authorization: Bearer $DEVELOPERKNOWLEDGE_OAUTH_ACCESS_TOKEN" \
  -H "x-goog-user-project: $GOOGLE_CLOUD_QUOTA_PROJECT"
```

The quota project must be permitted to consume Developer Knowledge API quota. A missing quota project can return a quota-project error even when the OAuth token itself is valid.

## AnswerQuery

Use this for direct grounded generation. The current endpoint is `POST /v1:answerQuery` (not the old `v1alpha` example). If it returns 429 / `RESOURCE_EXHAUSTED`, switch to document search instead of retrying the generative endpoint.

```bash
curl -X POST "https://developerknowledge.googleapis.com/v1:answerQuery?key=$DEVELOPERKNOWLEDGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I create a BigQuery dataset?"}'
```

Response shape:

- `answer.answerText`
- `answer.citations[]`
- `answer.references[]` is an array of objects, unlike MCP’s array of resource-name strings. Use `answer.references[].documentReference.documentChunk.parent` for full-document lookup. REST accepts an optional `filter` in the request body.

MCP equivalent:

```bash
mcporter call "$gdk_server.$gdk_answer_tool" \
  --args '{"query":"How do I create a BigQuery dataset?"}' \
  --output json
```

## SearchDocumentChunks

Use this to find matching documentation snippets.

```bash
curl "https://developerknowledge.googleapis.com/v1/documents:searchDocumentChunks?query=BigQuery&key=$DEVELOPERKNOWLEDGE_API_KEY"
```

Useful query parameters:

- `query`: raw search query.
- `pageSize`: defaults to at most 5 results and accepts up to 100.
- `pageToken`: use the preceding response’s `nextPageToken` with the same query and filter.
- `filter`: strict metadata filter.

Filterable fields:

- `data_source`, for example `docs.cloud.google.com`.
- `update_time`, using RFC 3339 timestamps.
- `uri`, for exact document URI matches.
- `content_length_bytes`, for document size.

Filtered example:

```bash
curl "https://developerknowledge.googleapis.com/v1/documents:searchDocumentChunks?query=BigQuery&filter=data_source%3D%22docs.cloud.google.com%22&key=$DEVELOPERKNOWLEDGE_API_KEY"
```

Response shape:

- `results[].parent`
- `results[].content`
- `results[].document.uri`

MCP equivalent:

```bash
mcporter call "$gdk_server.$gdk_search_tool" \
  --args '{"query":"BigQuery"}' \
  --output json
```

## GetDocument

Use this to retrieve a single full Markdown document from a search result parent.

```bash
: "${DOC_NAME:?Set DOC_NAME to an exact parent returned by search or answer}"

curl "https://developerknowledge.googleapis.com/v1/$DOC_NAME?key=$DEVELOPERKNOWLEDGE_API_KEY"
```

MCP equivalent:

```bash
mcporter call "$gdk_server.$gdk_get_tool" \
  --args "$(jq -nc --arg name "$DOC_NAME" '{names:[$name]}')" \
  --output json
```

## BatchGetDocuments

Use this to retrieve multiple documents directly through REST.

```bash
curl "https://developerknowledge.googleapis.com/v1/documents:batchGet?names=documents/DOCUMENT_ID_1&names=documents/DOCUMENT_ID_2&key=$DEVELOPERKNOWLEDGE_API_KEY"
```

Use exact resource names returned by the corpus, not the example placeholders. Both current REST `batchGet` and MCP `get_documents` are limited to 20 documents per call, in request order. The skill’s default research budget is three. The 100 limit applies to REST search page size, not batch retrieval.

## Fallback Decision

Prefer `mcporter` unless one of these is true:

- Capability discovery finds no healthy Google Developer Knowledge-capable server.
- The MCP client integration itself is under test.
- The task requires REST request examples for another application.
- Need REST-only parameters such as `filter`, `pageSize`, or `pageToken`.

After a REST fallback succeeds, keep the same source-backed answering rules:

1. Search first when the target document is unknown.
2. Retrieve full documents before making version-sensitive claims.
3. Include official source URIs when reporting final answers.
4. State clearly when retrieved documents do not contain the requested detail.

## Official References

- Developer Knowledge API: `https://developers.google.com/knowledge/api`
- Quickstart: `https://developers.google.com/knowledge/quickstart`
- Search and retrieve documents: `https://developers.google.com/knowledge/search-retrieve`
- REST search schema: `https://developers.google.com/knowledge/reference/rest/v1/documents/searchDocumentChunks`
- REST batch get schema: `https://developers.google.com/knowledge/reference/rest/v1/documents/batchGet`
- REST answer schema: `https://developers.google.com/knowledge/reference/rest/v1/TopLevel/answerQuery`
- AnswerQuery guide: `https://developers.google.com/knowledge/answer-query`

