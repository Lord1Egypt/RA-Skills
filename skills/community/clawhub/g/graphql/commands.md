# Commands — The Toolkit

Things you run against a live endpoint or a schema file. Tool names vary by ecosystem; the shapes do not. Nothing here is required to use the skill — these are the moves that shorten an investigation. Every example uses placeholder hosts and a placeholder `$TOKEN`: substitute your own endpoint and run them yourself.

Contents: Send A Query Without A Client · Read The Response Correctly · Dump The Schema · Diff Two Schemas · Validate Documents · Compute A Persisted-Query Hash · Probe The Limits · Check The CSRF And Transport Posture · Check For The Suggestion Leak · Federation · Count Statements Per Operation · Measure The Payload

## Send A Query Without A Client

```bash
curl -s https://api.example.com/graphql \
  -H 'content-type: application/json' \
  -H "authorization: Bearer $TOKEN" \
  -d '{"query":"query U($id:ID!){ user(id:$id){ id name } }","variables":{"id":"42"},"operationName":"U"}'
```

- Always send `operationName` — production endpoints should reject anonymous operations (`production.md`).
- Pipe through a JSON formatter and read `errors` first, `data` second.
- A response with HTTP 200 and an `errors` array is the normal failure shape; `curl -f` will not catch it.

## Read The Response Correctly

```bash
# did any field fail, and where?
... | jq '.errors[]? | {path, code: .extensions.code, message}'
# what came back despite the errors?
... | jq '.data'
```

- `path` names the failing field; `extensions.code` names the layer (SKILL.md Error Codes).
- Distinguish request-level from field-level failure with one check: `jq 'has("data")'` — request-level failures have no `data` key at all.

## Dump The Schema

```bash
# from a live endpoint (needs introspection enabled)
npx get-graphql-schema https://api.example.com/graphql > schema.graphql
# from source, code-first servers usually expose a print/emit command of their own
```

- Introspection is disabled on most hardened production endpoints by design (`security.md`) — pull from the schema registry instead.
- Never generate clients from a locally-dumped dev schema; use the registry artifact (`codegen.md`).

## Diff Two Schemas

```bash
npx graphql-inspector diff old.graphql new.graphql
```

- Classifies each change as safe, dangerous or breaking. Run it in CI against the *deployed* schema, not the previous commit (`schema-evolution.md`).
- With a directory of client operations attached, a technically-breaking change that no recorded operation selects can be approved automatically.

## Validate Documents Against A Schema

```bash
npx graphql-inspector validate './src/**/*.graphql' schema.graphql
```

- Catches fragments spread on the wrong type, unknown fields and missing variables at build time instead of at runtime (`client.md`).
- Also the cheapest way to find out which of your documents a proposed schema change would break.

## Compute A Persisted-Query Hash

```bash
printf '%s' "$QUERY_TEXT" | shasum -a 256
```

- The hash covers the exact document text: whitespace and comment changes produce a different hash. A `PersistedQueryNotFound` loop is usually this (`caching.md`).
- Send it as `extensions={"persistedQuery":{"version":1,"sha256Hash":"…"}}`; over `GET` for queries, `POST` for anything else.

## Probe The Limits

```bash
# depth: nest a recursive edge until it is rejected, and read which limit fired
# aliases: repeat one field under many aliases in a single document
# tokens: send a large document of nested braces and confirm it dies before parse
```

- Assert both directions: the abusive document is rejected *and* your largest legitimate operation passes (`testing.md`).
- Read the rejection's `extensions.code` — a generic error means the limiter is not reporting which limit fired, which makes production rejections unactionable.

## Check The CSRF And Transport Posture

```bash
# must be rejected: a simple request that skips preflight
curl -s -X POST https://api.example.com/graphql -H 'content-type: text/plain' -d '{"query":"{__typename}"}'
# must be rejected: a mutation over GET
curl -s -G https://api.example.com/graphql --data-urlencode 'query=mutation{deleteThing(id:"1"){ok}}'
```

- Both returning data is a finding, not a style question (`security.md`).

## Check For The Suggestion Leak

```bash
curl -s -X POST https://api.example.com/graphql -H 'content-type: application/json' -d '{"query":"{ user { passwordHsh } }"}' | jq -r '.errors[0].message'
```

- A response containing "Did you mean …" means field suggestions are on. With introspection disabled this is still a full schema disclosure channel (`security.md`).

## Federation

```bash
rover subgraph check <graph>@<variant> --name <subgraph> --schema ./schema.graphql
rover supergraph compose --config ./supergraph.yaml > supergraph.graphql
```

- Run the check in every subgraph's CI, not only the gateway's, or the break surfaces in another team's deploy (`federation.md`).
- Read the query plan for your top operations; an unexpected extra fetch step is usually a missing `@provides` or a key that forces a round trip.

## Count Statements Per Operation

- Turn on statement logging in the database for one request, run the operation, count. Latency that scales with page size and identical statements with different bind parameters is the N+1 signature (`n-plus-one.md`).
- Make it permanent: log statement count per operation in development and assert a page-size-independent ceiling in tests (`testing.md`).

## Measure The Payload

```bash
curl -s -o /dev/null -w '%{size_download} bytes in %{time_total}s\n' -X POST https://api.example.com/graphql -H 'content-type: application/json' -d "$BODY"
```

- Measure uncompressed size: compression flatters repetitive JSON while parse and memory on the client stay uncompressed (`performance.md`).
