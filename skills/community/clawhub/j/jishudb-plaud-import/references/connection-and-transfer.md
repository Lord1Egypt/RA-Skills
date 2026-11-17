# Connection and Transfer

## Source connection

The vendor references are:

- [Plaud MCP](https://docs.plaud.ai/plaud-mcp-cli/mcp)
- [Plaud CLI](https://docs.plaud.ai/plaud-mcp-cli/cli)

Inspect the installed connector's current catalog and schemas; documentation
is not proof of a connected account. The documented MCP tools include
`login`, `get_current_user`, `list_files`, `get_file`, `get_transcript`, and
`get_note`. They are source tools, not JishuDB tools.

Prefer an existing authorized connector. If configuration is needed, use the
host's supported MCP settings and the vendor's official installation guidance.
Obtain approval for the selected client and package version before installing
or changing configuration. Do not run an auto-configure-all-clients option,
overwrite unrelated MCP entries, introduce a proxy, read stored tokens, or
automatically repair/reinstall under an earlier approval.

The documented local Plaud package requires Node.js 20 or later. WorkBuddy is
not a documented auto-configured client in the vendor reference inspected for
this package. Use its actual supported configuration surface rather than
inventing a settings path. The vendor documents US-hosted transit for its
HTTP-based connector; disclose that route when it is selected. Do not describe
it as local-only or promise mainland accessibility.

The user completes browser authorization. Call `get_current_user` afterward
and obtain the intended account's non-secret stable identifier for the identity
helper. If the tool does not expose one, obtain a stable, user-approved account
alias; do not substitute an email, a token, or a device serial.

For `list_files`, the documented filters are `query`, `date_from`, and `date_to`;
unfiltered listing uses `page` / `page_size`. Filtering can change pagination
behavior. Inspect the actual result and coverage rather than assuming every
page/filter combination is a full account search.

Documented metadata includes `id`, `name`, `created_at`, `start_at`, and
`duration` in milliseconds. `get_file` additionally returns a temporary
`presigned_url` and available source text. A URL is not an archived recording.
Do not save the device serial or assume a documented URL lifetime guarantees
that a particular URL remains valid.

The CLI is an optional already-installed source adapter, not a mandatory second
installation. Its documented commands include `plaud me`, `plaud files`,
`plaud file <id>`, `plaud transcript <id>`, `plaud summary <id>`, and
`plaud audio <id>`. `plaud audio` returns a URL, not the audio bytes. The
documented CLI keyword search scans at most the 500 most recent recordings;
disclose that boundary. Never read the CLI's token files or redirect its
authentication endpoints.

## Destination capability gates

Use the actual JishuDB MCP connector. Reuse the official `jishudb` setup Skill
when connection or installation is needed; do not duplicate its installer,
release selection, endpoint probing, or privilege-escalation logic here.

Call `kb_get_capabilities`, inspect the loaded schemas, and require the needed
write profile and destination access. For audio, require this live capability:

```text
mcp.upload.audio:
  enabled
  modes
  extensions
  speechReady
  compressedAudioReady
  maxSourceBytes
  maxDurationMs
  storageBytes
```

An older service may omit `audio`. In that case, audio support is unavailable
to this workflow until a supported backend is installed. A general upload mode
or a filename extension in an unrelated HTTP UI is insufficient.

`enabled` requires a write-capable HTTP direct-upload connection and an enabled
speech service. WAV is the baseline format; MP3 and M4A require the configured
decoder. M4A processing supports AAC-LC or ALAC. Respect the actual capability
limits instead of hard-coding these formats or a maximum file size.

The ordinary `kb_upload` Base64/path routes remain document-only. Do not call a
private audio HTTP endpoint, impersonate a manual upload, or enable server-side
file reads to avoid this boundary.

## Stable identities

Resolve the helper relative to this installed Skill's root, not the user's
project directory. Run its actual absolute path through the host's shell or
equivalent Node execution:

```text
node "<installed-skill-directory>/scripts/recording-identity.mjs"
```

Supply JSON through stdin, not credentials or command-line secrets:

```json
{
  "accountScope": "stable-non-secret-account-id",
  "recordingId": "selected-recording-id",
  "kbId": "actual-selected-kb-id"
}
```

It returns `externalAssetId` and `manifestNoteId` without echoing the account or
recording ID. After acquiring exact bytes, also supply:

```json
{
  "accountScope": "stable-non-secret-account-id",
  "recordingId": "selected-recording-id",
  "kbId": "actual-selected-kb-id",
  "representation": "transcript",
  "contentSha256": "a2d51f7cb1667127b7e5e36a59d7dac5c46c963785c7ef60b5df8f68a7029ba6"
}
```

The shown digest is illustrative, not a fixture to upload. Compute the actual
file's digest. Representations are `audio`, `transcript`, and `summary`. The
helper then also returns `idempotencyKey`, scoped to source/account, recording,
representation, exact content revision, and destination KB.

An association is not authentication and does not automatically attach an
external transcript to the audio processing row. Store each representation
separately and link their returned IDs in the manifest. Preserve the manifest's
history and use current Note version preconditions when merging updates.

## Transfer sequence

1. Acquire only the selected file with an authorized host downloader. Check
   permitted source/destination URLs and redirects, keep downloads bounded by
   `maxSourceBytes`, and never forward JishuDB credentials to Plaud or its
   download host. Keep signed URLs and upload credentials out of shell command
   histories, persisted provenance, and reports. If the host cannot perform a
   protected transfer, request a user-exported local file instead of leaking
   credentials or bypassing access.
2. Record exact filename, byte count, and SHA-256. Preserve downloaded bytes;
   do not transcode locally and then call the converted file the original.
3. Call `kb_prepare_upload` with the actual values:

```text
kb_prepare_upload({
  kbId,
  filename,
  sizeBytes,
  mime,
  sha256,
  idempotencyKey,
  externalAssetId
})
```

4. If the result is a committed replay, use its existing `job.id` and
   `job.documentId`; no upload is required. The same authenticated receipt can
   be recovered despite later decoder/speech or source-limit changes, without
   granting admission for a new upload. Otherwise send the file's raw bytes
   with exactly the returned `method`, `uploadUrl`, and headers. Do not add the
   general MCP bearer, forward those headers on redirects, send multipart
   encoding, or wrap the bytes in JSON/Base64.
5. The raw HTTP response's job uses `id` and `docId`. Call
   `kb_get_job({kbId, jobId: job.id})` to obtain the native MCP `documentId`.
   All later document reads use that returned ID.
6. Retain `uploadId`, `clientItemId`, and job/document IDs as soon as each is
   known. For an uncertain response, query
   `kb_list_jobs({kbId, clientItemId})`. An interrupted transfer before storage
   may reuse an unconsumed descriptor within its lifetime. Inspect session/job
   state before re-preparing, since preparation can rotate the upload secret.
7. A descriptor is short-lived, and upload replay records are not permanent
   deduplication storage. After expiry, reconcile the durable manifest and
   associated documents first. If nothing was committed and the previous
   identity is no longer retryable, record a distinct transfer-attempt suffix
   under the same stable source/content identity before preparing again.
   Never use a new identity just to suppress a conflict.

For text-only fallback, inspect the live `kb_upload` schema and document limits,
then call it with `kbId`, `filename`, `contentBase64`, and `externalAssetId`.
It returns `document.id`. It has no preparation idempotency key: reconcile the
manifest and paginated document inventory after an uncertain response before
submitting the same bytes again.

On `duplicate_document`, inspect only the authorized destination's document
inventory and compare exact content hashes, using the original-audio hash for
audio. Identical bytes may already exist under another source association.
With an approved reuse, record the additional source association and existing
document ID in the manifest without rewriting immutable document provenance.
If no accessible match can be established, report the unresolved duplicate;
do not change the bytes or filename to evade deduplication.

## Readback and recovery

Use `kb_get_document({kbId, documentId})`. For audio inspect:

```text
audio.originalSaved / originalBytes / originalSha256
audio.format / durationMs / playbackReady
audio.state / transcriptReady / transcriptRevision
audio.jobId / jobStatus / indexStatus / errorCode / indexErrorCode
```

Zero duration before decoding is unknown duration, not evidence of a zero-length
recording. `originalSha256` identifies original audio; the document's `sha256`
can identify its generated transcript. A ready transcript with a failed job
can mean indexing failed; it does not mean the original or transcription was
lost. Read indexed text with `kb_read_document_text` and verify relevant
retrieval with `kb_search`. Inspect the read result's `truncated` flag and label
excerpt-only review honestly; a bounded read cannot establish that later
speech is absent or that the whole meeting was reviewed.

| Condition | Recovery |
| --- | --- |
| Source login expired | Restore browser authorization and confirm the account before resuming selected reads |
| Recording absent from a bounded search | Check coverage, dates/timezone, and vendor sync; do not claim global absence |
| Download URL expired | Obtain a new URL with `get_file` for the same recording |
| Audio capability absent | Use a supported backend/host; do not silently substitute text |
| `audio_upload_busy` | Inspect job state, then retry admission within the valid transfer scope |
| Invalid container or unsupported codec | Preserve any saved original; obtain a supported export rather than relabelling bytes |
| Decoder/model unavailable | Repair the declared prerequisite, then inspect and retry the existing job |
| `audio_storage_full` or transfer-size limit | Resolve capacity or choose an approved supported export; do not delete user data automatically |
| Transcription ready, indexing failed | Retry the existing job; preserve the saved transcript and original |
| Transfer succeeded, provenance write failed | Report partial archival and finish the manifest without re-uploading audio |

Polling timeout is not job failure. Preserve the last observed state and IDs.
Only cancel an active job when the user authorizes cancellation; do not cancel
it merely because the current interaction's waiting budget elapsed.
