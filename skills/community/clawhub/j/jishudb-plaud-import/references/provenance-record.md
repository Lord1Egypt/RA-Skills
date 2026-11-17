# Recording Provenance Record

Use one source-only Markdown Note with the helper's `manifestNoteId`, then
explicitly link it to the selected KB. The Note contains the stable marker
`jishudb-plaud-import/v1`, the `externalAssetId`, and the actual KB ID.
Read and merge an existing matching record rather than discarding its history.

Keep a small structured block with these fields; use null or an explicit
unknown label when the source does not provide a value:

```text
workflow: jishudb-plaud-import/v1
provider: plaud | user-export
acquisition: plaud-mcp | existing-plaud-cli | user-selected-local-export
externalAssetId: <opaque helper result>
kbId: <returned destination ID>
recordingId: <selected non-secret vendor ID, or approved local source ID>
title: <original recording title>
recordedAt: <source start time with timezone, if available>
sourceCreatedAt: <source creation time, if available>
sourceDurationMs: <source-reported duration, if available>
firstCollectedAt: <first collection timestamp>
lastCollectedAt: <latest collection timestamp>
representations:
  - kind: audio | transcript | summary
    producer: plaud | jishudb | user-export
    contentSha256: <exact bytes for this revision>
    filename: <safe basename, not an absolute path>
    bytes: <actual bytes>
    sourceRevision: <vendor revision if returned, otherwise the content hash>
    idempotencyKey: <stable helper result when direct upload was used>
    transferAttempts: <attempt identities and non-secret returned IDs>
    documentId: <returned saved ID>
    jobId: <returned processing ID, if asynchronous>
    originalSaved: <observed for audio>
    transcriptionState: <observed for audio>
    indexState: <observed>
    readback: pending | confirmed | failed
    collectedAt: <this revision's collection timestamp>
    coverage: <actual material, including missing segments where known>
```

These placeholders are instructions, not source facts. Do not save them as if
they were returned values. Do not persist the raw account identifier, email,
device serial, credentials, temporary download URLs, upload headers, or local
paths. The source association incorporates account scope without publishing it.
Preserve original metadata separately from subsequently measured audio duration.

For audio with existing text, retain separate representation records. A Plaud
summary is not its transcript; Plaud text is not JishuDB-generated speech
recognition. Record disagreements or omissions without overwriting either
source. The externally imported transcript is a separate document, not an
automatic replacement for the audio worker's transcript.

Record new content revisions as additional entries, even when they share the
same source association. Repeated collection of identical bytes updates
collection/status history without reimporting the document. Do not put
changing collection timestamps into the source text itself.

## Concrete persistence

1. `note_get({noteId: manifestNoteId})` establishes whether the matching record
   exists. Only `NOT_FOUND` permits the create branch.
2. On creation, call `note_create` with `noteId`, a readable title, the actual
   Markdown content, and one retained RFC 3339 `createdAt`. On update, call
   `note_update` with the merged content and the last returned
   `expectedUpdatedAt`. A conflict requires rereading and merging, not ignoring
   the precondition.
3. Call `note_link_to_kb` with `noteId`, `kbId`, and the saved current
   `expectedUpdatedAt` when not already linked. Preserve the returned
   membership's `documentId` and `jobId`.
4. Follow `kb_get_job`, then read `note_get` and `kb_read_document_text` for the
   linked snapshot. After updates to an already linked Note, inspect its
   current membership/refresh rather than repeatedly creating links.

## Completion report

Report only safe, task-relevant identifiers and observed coverage:

| Material | Saved document | Coverage | Processing / readback |
| --- | --- | --- | --- |
| Original audio | `<documentId>` | `<format and retained bytes>` | `<retained / normalized / transcribed / indexed separately>` |
| Plaud transcript | `<documentId or unavailable>` | `<timestamps and speaker labels actually provided>` | `<saved/readable or missing>` |
| Plaud summary | `<documentId or not requested>` | `<summary only>` | `<saved/readable or missing>` |
| Provenance record | `<linked documentId>` | `<source and representation associations>` | `<linked and readable or pending>` |

Use `PARTIAL` whenever a requested representation, processing requirement, or
the linked provenance record remains incomplete. Include only the specific
next recovery action. Optional analysis must cite actual saved source passages
and distinguish observations, source-generated summaries, and new conclusions.
