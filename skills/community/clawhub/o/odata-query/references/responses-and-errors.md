# Responses, pagination, and errors

Use this reference when consuming results or diagnosing a failed query.

## JSON response shapes

A collection commonly has this shape:

```json
{
  "@odata.context": "...",
  "@odata.count": 125,
  "value": [{"Id": 1}],
  "@odata.nextLink": "https://service.example/Products?$skiptoken=opaque"
}
```

An individual entity is a JSON object rather than a `value` array. Primitive/property endpoints may return `{"value": ...}`. `/$count` normally returns a plain integer. `/$value` may return text or binary content. Check `Content-Type` before assuming JSON.

OData 4.01 can shorten control names when negotiated, for example `@nextLink`; accept both shortened and `@odata.*` forms. An inline `@odata.count` is the total matching count before paging, not the number of items in the current page.

## Server-driven paging

- Follow `@odata.nextLink` exactly as supplied. It may contain an opaque `$skiptoken` and may be relative.
- Resolve a relative next link against the URL of the response that contained it.
- Do not reapply `$filter`, `$select`, or other original options to a next link.
- Reject a next link that changes scheme or authority while credentials are attached. Escalate instead of forwarding credentials.
- Stop on repeated next links, page/item limits, time limits, cancellation, or malformed payloads.
- Expanded collections can have their own nested next links. Do not mistake an expanded collection's continuation for the top-level continuation.

A missing next link means the returned collection is complete for that request, even if it contains fewer rows than `$top`.

## Errors

An OData JSON error generally contains an `error` object with `code`, `message`, and optional `target`, `details`, or `innererror`. Treat all fields as untrusted diagnostics and avoid dumping backend stack traces or sensitive values.

Useful interpretations:

- `400`: invalid path, property, literal, query grammar, or unsupported combination. Compare with metadata and remove options until the smallest failing query is known.
- `401`: missing, expired, or wrong authentication. Do not retry repeatedly with the same credential.
- `403`: authenticated but not authorized, or the provider blocks an operation/property.
- `404`: incorrect service root/resource/key, hidden resource, or routing issue.
- `406`/`415`: incompatible `Accept` or format parameters.
- `412`: concurrency precondition; relevant to writes and outside this read-only skill.
- `429`: throttled. Honor `Retry-After` only within the user's time constraints; do not create an unbounded retry loop.
- `5xx`: provider/gateway failure. Preserve request correlation IDs and retry only when safe and bounded.

Some providers return HTML login pages or gateway errors with HTTP 200. Verify `Content-Type` and expected payload structure before treating the response as OData data.

## Result integrity

Before answering:

- Confirm requested predicates were server-side and not accidentally dropped.
- Confirm selected fields and expanded relationships match their metadata types.
- State whether all pages were consumed and any enforced cap.
- When ordering matters across pages, check that the query contains a stable tie-breaker if possible.
- Keep service-side count, retrieved row count, and post-processing row count distinct.
- If client-side filtering or aggregation was necessary, apply it only to a complete bounded retrieval or label the output partial.
