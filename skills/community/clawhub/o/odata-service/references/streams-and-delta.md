# Streams, media entities, and delta synchronization

## Media entities and stream properties

Read a media entity's default stream at `{entity-url}/$value`; named stream properties use `{entity-url}/{stream-property}` and may expose read/edit links in JSON annotations. Check `Content-Type`, `Content-Length`, media ETag, and provider size limits. Save binary data as bytes, never decode it as JSON or text.

Create/update stream content only when advertised and authorized. Send the real media type and an `If-Match` condition for replacement when an ETag is available. Metadata and stream ETags can differ. A media read may redirect to object storage; never forward credentials across origins. Follow a cross-origin public/signed URL only when no secret headers or mutation body will be forwarded.

## Delta tracking

Request change tracking with the provider-supported mechanism, commonly `Prefer: odata.track-changes`, on a collection query. Fully consume every `@odata.nextLink` first. Persist the final `@odata.deltaLink` verbatim only after the complete initial/delta response has been processed successfully.

Later, GET the stored delta link without rebuilding its query or interpreting `$deltatoken`. Process all pages before replacing the prior checkpoint with the new final delta link. Updating the checkpoint early can lose changes.

Delta entries can represent:

- added or changed entities;
- removed/deleted entities (`@odata.removed` in 4.01; v4.0 has different deleted-entity control information);
- added or deleted relationships;
- nested changes for expanded relationships in 4.01.

Apply changes idempotently by canonical identity and model keys. Preserve event ordering within the response, distinguish deletion from “no longer matches filter,” and handle schema/version changes. If a delta link expires (`404`/`410`) or becomes invalid, perform a fresh bounded baseline rather than guessing a token.

## Synchronization invariants

- Store data changes and the new delta checkpoint atomically where possible.
- Never advance the checkpoint after partial processing.
- Deduplicate replayed changes safely.
- Treat a delta feed as scoped to its original defining query, expansion, permissions, tenant, and schema version.
- Do not use `$top`/`$skip` to manufacture delta semantics.
