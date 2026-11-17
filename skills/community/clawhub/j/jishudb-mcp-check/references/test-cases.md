# JishuDB MCP Test Cases

Execute cases in the listed phase order. The primary matrix contains every
current `jishudb-mcp-v2` tool exactly once.

Before running cases, compare capabilities with
[contract-baseline.md](contract-baseline.md). Apply its drift policy and carry
the Skill version and baseline digest into the report.

## Shared conventions

- Replace `<runId>`, `<kbId>`, `<noteId>`, `<documentId>`, and `<jobId>` only
  with values recorded in the current run.
- Uploaded filenames are:
  - `mcp-check-<runId>.md`
  - `mcp-check-<runId>.txt`
  - `mcp-check-<runId>.pdf`
- A wrong confirmation value is the correct ID plus `-wrong`, except for
  `note_delete`: its `confirmNoteId` accepts at most 36 characters, so use a
  different valid 36-character UUID.
- Expected errors pass only when the protected resource remains unchanged.
- If the host hides stable MCP error metadata, record `not-exposed`.

## Smoke phase

| Case | Tool | Task and assertions |
| --- | --- | --- |
| CAP-001 | `kb_get_capabilities` | Call with no arguments. Require contract `jishudb-mcp-v2`; record transport, protocol, profile, server version/revision, tools, and upload modes; ensure no secret fields appear. If `mcp.upload.audio` is present, record its enabled state, modes, formats, limits, and speech/decoder readiness separately. Otherwise label audio as not advertised. |
| KB-001 | `kb_list` | Require a `knowledgeBases` array and non-negative document/chunk counts. In all-tools mode repeat after KB creation and require exactly one match for `<kbId>`. |
| SYS-001 | `kb_read_handbook` | Read the full handbook. Request a deliberately missing section, select one returned heading, then request that heading exactly. Require coherent `found` and `truncated` values. |
| SYS-002 | `kb_get_config` | Require the allowlisted config sections and matching profile/contract. Fail on exposed tokens, keys, credentials, provider URLs, local paths, or `providerDataEpoch`. |

Stop here in `smoke` mode. Optionally call `kb_get` only when the user names a
KB to inspect; do not mutate anything.

## Isolated KB phase

| Case | Tool | Task and assertions |
| --- | --- | --- |
| KB-002 | `kb_create` | Create `<kbId>` with a run-scoped name and description. Require the exact ID and metadata. Repeat the same create and require `CONFLICT` or the host-visible equivalent. |
| KB-003 | `kb_get` | Read `<kbId>` after creation and after ingest. Require matching metadata and non-negative document, chunk, and job counts. |
| KB-004 | `kb_update` | Change the run KB name and description, then verify with `kb_get`. Calling with only `kbId` must return `INVALID_ARGUMENT` and leave metadata unchanged. |

## Fixture ingest phase

Use the exact bytes in [fixture-values.md](fixture-values.md).

| Case | Tool | Task and assertions |
| --- | --- | --- |
| DOC-001 | `kb_upload` | Upload Markdown and TXT using `contentBase64`; upload PDF the same way unless DOC-002 completes it. Require exact fixture byte count/SHA-256, non-empty document ID, matching KB, and a searchable canary. Invalid Base64 must return `INVALID_ARGUMENT`. Test `path` only with an explicitly supplied same-host allowed path. |
| DOC-002 | `kb_prepare_upload` | If direct upload is disabled, require `REJECTED`. If enabled and the host supports raw PUT, prepare the PDF with exact size/SHA and a run idempotency key, use the returned method/headers without exposing their values, then repeat preparation and require the committed replay/job. If the host cannot PUT, mark `BLOCKED` without preparing and use DOC-001 for PDF. |
| DOC-003 | `kb_import_url` | Always verify a malformed URI is rejected as `INVALID_ARGUMENT`. Then import the packaged, pre-approved fixture `https://example.com/` asynchronously using a run idempotency key, poll the returned job, and require a document/job in `<kbId>` whose readable text contains `Example Domain`. If the fixture cannot be reached, report the fetch evidence and mark the positive path `BLOCKED`; do not silently substitute another URL. |

If a prepared direct upload fails after returning an `uploadId`, report the ID
without its token. The server expires the single-purpose session; there is no
MCP deletion tool for it.

When the live upload schema includes `externalAssetId`, use the non-secret
association `mcp-check:<runId>` for the Markdown and TXT fixtures and require it
in the corresponding document results. Keep this association unchanged during
DOC-006. An older schema without this optional input leaves association coverage
untested; do not send an unsupported field.

The raw PUT response uses `job.docId`, while native MCP job responses use
`documentId`. Retain the PUT job's `id`, read `kb_get_job`, and use its
`documentId`. A repeated committed preparation must return the same job in the
native MCP shape, not an untyped HTTP job.

## Optional audio phase

Run this only when the user explicitly requests audio coverage and approves one
additional audio document in the run KB. Use an explicitly supplied, small,
supported audio fixture with known spoken content. Do not acquire a recording
from a third-party account or substitute personal material under the default
fixture approval.

Require an enabled `mcp.upload.audio` capability, the requested extension,
appropriate processing readiness, and a host able to issue the returned PUT.
If a prerequisite is absent, record the specific capability as `SKIP` or the
missing host/fixture prerequisite as `BLOCKED`; do not use Base64 for audio.

1. Prepare with exact size, SHA-256, and a run-scoped retry identity. Upload
   actual bytes and retain the job ID.
2. Call `kb_get_job`, then `kb_get_document`. Require `audio.originalSaved`,
   matching `originalBytes` and `originalSha256`, and distinct transcription
   and indexing states. Do not interpret zero duration before decoding as an
   empty recording.
3. Wait for completion within the normal polling budget. Require a ready
   transcript, playback readiness, a completed job, and the known spoken
   content in `kb_read_document_text` and `kb_search`.
4. Repeat preparation with identical arguments and require the same
   `documentId` and job, with no extra document.
5. Report processing failures without repeatedly uploading. Record the audio
   document ID for the existing run-KB cleanup.

## Document phase

| Case | Tool | Task and assertions |
| --- | --- | --- |
| DOC-004 | `kb_list_documents` | List with `limit=1`, follow `nextCursor`, then list without pagination. Require every run document exactly once and no duplicate IDs across pages. |
| DOC-005 | `kb_get_document` | Read the Markdown document. Require matching ID/KB/title/MIME/SHA/bytes/status and valid chunk, FAQ, and job counts. |
| DOC-006 | `kb_update_document` | Rename only the Markdown title. Require the title to persist while SHA, origin, MIME, and bytes remain unchanged. An extra `sourcePath` argument must be rejected as `INVALID_ARGUMENT`. |
| DOC-007 | `kb_list_document_chunks` | Require at least one Markdown chunk after indexing. Require a fixture canary in a returned chunk or in the paired search result when chunk text is capped. |
| DOC-008 | `kb_read_document_text` | Read Markdown and PDF extracted text. Require their exact canaries and coherent character/truncation limits. |
| DOC-009 | `kb_read_document_raw` | Read TXT raw text and require its canary. Reading PDF raw content must return `INVALID_ARGUMENT` and no bytes. |
| DOC-010 | `kb_list_document_faq` | Require a valid `faqs` array. Empty is valid. Existing entries must contain only public ID/question fields. |
| DOC-011 | `kb_reindex_document` | Call Markdown reindex with a wrong confirmation and require `REJECTED`; then use the exact ID with `strategy=auto`. Require the same document, a valid result shape, and successful post-reindex search. |
| SEA-001 | `kb_search` | Search the exact fixture canaries and queries containing the rare terms `苍蓝轨道` and `ORBIT-THURSDAY`. Require the expected run document/fact and no more than `topK` results. |

## Note and job phase

Create Note content containing:

```text
JISHU-MCP-NOTE-<runId>-V1
```

| Case | Tool | Task and assertions |
| --- | --- | --- |
| NOTE-001 | `note_list` | List before creation, after creation/link, and after deletion. Require the run Note exactly once while present; summaries must omit content, attachments, and paths. |
| NOTE-002 | `note_create` | Create with the generated UUID, run title/content, and one saved RFC 3339 `createdAt`. Repeat the identical request and require `replayed=true`. Before linking, `kb_search` must not find the Note canary. |
| NOTE-003 | `note_get` | Require exact title/content/canary, memberships, and timestamps; record the latest `updatedAt`; reject exposed paths or attachments. |
| NOTE-004 | `note_link_to_kb` | Link the current version to `<kbId>`, record membership document/job IDs, poll to completion, and require the Note canary to become searchable. Repeat with the original version and require replay without a second document. |
| JOB-001 | `kb_list_jobs` | List jobs for `<kbId>` and require the Note-link job. Exercise a status or client-item filter when available; require coherent pagination and no unrelated jobs. |
| JOB-002 | `kb_get_job` | Poll the Note-link or another asynchronous run job. Require matching IDs and coherent status, stage, progress, attempts, timestamps, and error code. |
| JOB-003 | `kb_get_job_trace` | Read the same job trace. Require matching job and spans containing only stage/timing fields; fail on paths, URLs, tokens, or arbitrary metadata. Empty spans are valid. |
| JOB-004 | `kb_cancel_job` | If a run job is queued/processing, first require `REJECTED` for a wrong confirmation, then cancel exactly and require `cancel_requested` or `cancelled`. If only terminal jobs exist, verify wrong-confirmation rejection and exact-confirmation no-op, then mark the positive path `BLOCKED`. |
| JOB-005 | `kb_retry_job` | If a run job is failed/cancelled, retry and require the same job/document to return to an active state and eventually complete. Otherwise require an eligible call on a completed job to preserve its status and mark the positive path `BLOCKED`. |
| NOTE-005 | `note_update` | First use a stale `expectedUpdatedAt` and require `CONFLICT`. Then use the latest value and content `JISHU-MCP-NOTE-<runId>-V2`; require a newer timestamp. Without relinking, wait through debounce/processing and require V2 searchability. |
| NOTE-006 | `note_delete` | First require `REJECTED` using a different valid 36-character UUID as `confirmNoteId` (do not append `-wrong`). Then use the latest `updatedAt` and exact UUID. Require deletion/membership details, `note_get` to return `NOT_FOUND`, and the linked knowledge document/canary to disappear. |

If cancelling the first Note-link job, retry it and wait for completion before
continuing NOTE-005.

## Source phase

| Case | Tool | Task and assertions |
| --- | --- | --- |
| SRC-001 | `kb_list_sources` | List sources for `<kbId>`; an empty array is valid. If the user approves an existing KB, it may also be read. Require sanitized IDs/types/status/actions and no credentials, full URLs, or local paths. |
| SRC-002 | `kb_sync_source` | A missing run-scoped source must return `NOT_FOUND`; an extra administration field such as `path` must return `INVALID_ARGUMENT`. With explicit approval for an enabled existing source, trigger one sync/rescan and require preserved ID/type plus valid state/replay. Otherwise mark the positive path `BLOCKED`. |

## Cleanup phase

| Case | Tool | Task and assertions |
| --- | --- | --- |
| DOC-012 | `kb_delete_document` | Delete the TXT document. Wrong confirmation must return `REJECTED`; exact confirmation must return `ok=true`; subsequent read must return `NOT_FOUND`; other run documents must remain. |
| KB-005 | `kb_delete_kb` | Delete `<kbId>` last. Wrong confirmation must return `REJECTED`; exact confirmation must return `ok=true`; subsequent `kb_get` must return `NOT_FOUND`. |

NOTE-006 performs Note cleanup before these cases. If any cleanup step fails,
record the remaining IDs and set the overall result to `FAIL`.

## Profile behavior

- `default`: require the 18 read tools reported by capabilities; write/source
  tools must be absent. `smoke` may pass; `all-tools` is `BLOCKED`.
- `jishudb`: expect the 35 baseline tools. Report additions or removals rather
  than silently using an outdated catalog.

## Runtime preparation extension

Call `kb_get_readiness` for the isolated test KB and record dependency and actual
inference status separately from connection success. Basic text readiness does
not certify OCR/audio/Vault. Do not mutate model settings to make this check pass.

`kb_prepare_runtime` is conditional on explicit onboarding preparation authority,
independent of the read/write profile. Its absence on an ordinary connection is
expected. When present, test idempotent observation of a completed authorized job;
retry a failed download only within its existing authorization and recovery rules.
Reject arbitrary URL/path/model arguments. Record missing preparation authority
as a scoped limitation, not failed ordinary MCP read/write acceptance.
