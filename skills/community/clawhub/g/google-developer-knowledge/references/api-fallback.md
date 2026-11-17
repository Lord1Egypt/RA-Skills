# Developer Knowledge REST API Fallback

Use this reference only when the preferred `mcporter` MCP workflow is unavailable, when testing client integration outside MCP, or when the task specifically asks for direct REST API calls.

Before using REST, verify one supported authentication path: `DEVELOPERKNOWLEDGE_API_KEY`, or both `DEVELOPERKNOWLEDGE_OAUTH_ACCESS_TOKEN` and `GOOGLE_CLOUD_QUOTA_PROJECT`. If neither is available, do not issue a REST request; use the relevant public Google documentation and state that the REST fallback was unavailable.

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

Use this for direct grounded generation.

```bash
curl -X POST "https://developerknowledge.googleapis.com/v1alpha:answerQuery?key=$DEVELOPERKNOWLEDGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I create a BigQuery dataset?"}'
```

Response shape:

- `answer.answerText`
- `answer.citations[]`
- `answer.references[]`

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
- `pageSize`: limit results per page.
- `pageToken`: retrieve later pages.
- `filter`: strict metadata filter.

Filterable fields:

- `data_source`, for example `docs.cloud.google.com`.
- `update_time`, using RFC 3339 timestamps.
- `uri`, for exact document URI matches.

Filtered example:

```bash
curl "https://developerknowledge.googleapis.com/v1/documents:searchDocumentChunks?query=BigQuery&filter=data_source%3D%22docs.cloud.google.com%22&key=$DEVELOPERKNOWLEDGE_API_KEY"
```

Response shape:

- `documentChunks[].parent`
- `documentChunks[].content`
- `documentChunks[].document.uri`

MCP equivalent:

```bash
mcporter call "$gdk_server.$gdk_search_tool" \
  --args '{"query":"BigQuery"}' \
  --output json
```

## GetDocument

Use this to retrieve a single full Markdown document from a search result parent.

```bash
export DOC_NAME="documents/docs.cloud.google.com/bigquery/docs/datasets"

curl "https://developerknowledge.googleapis.com/v1/$DOC_NAME?key=$DEVELOPERKNOWLEDGE_API_KEY"
```

Alternative form from the how-to docs:

```bash
curl "https://developerknowledge.googleapis.com/v1/documents:get?name=$DOC_NAME&key=$DEVELOPERKNOWLEDGE_API_KEY"
```

MCP equivalent:

```bash
mcporter call "$gdk_server.$gdk_get_tool" \
  --args '{"names":["documents/docs.cloud.google.com/bigquery/docs/datasets"]}' \
  --output json
```

## BatchGetDocuments

Use this to retrieve multiple documents directly through REST.

```bash
curl "https://developerknowledge.googleapis.com/v1/documents:batchGet?names=documents/DOCUMENT_ID_1&names=documents/DOCUMENT_ID_2&key=$DEVELOPERKNOWLEDGE_API_KEY"
```

The REST batch method can retrieve up to 100 documents. The MCP `get_documents` tool retrieves up to 20 documents in one call.

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
- Search and retrieve documents: `https://developers.google.com/knowledge/howto`
- AnswerQuery guide: `https://developers.google.com/knowledge/answer-query`
