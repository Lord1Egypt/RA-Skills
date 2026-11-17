---
name: jishudb-plaud-import
description: >-
  将选定的 Plaud 录音、原始音频、带时间戳的转写或会议纪要导入 JishuDB，
  适用于会议归档、本地导出导入、保留来源关联及导入后的会议对比。 /
  Archive selected Plaud recordings, audio, timestamped transcripts, or meeting
  summaries in JishuDB from an authorized connector or local export. Preserve
  source associations and compare imported meetings with cited project evidence;
  not for recording-device control.
compatibility: Requires authorized JishuDB MCP write tools and either authorized Plaud MCP source tools or an explicitly selected local export. Audio additionally requires HTTP direct upload, the advertised JishuDB audio capability, and a host able to transfer actual binary bytes. The identity helper uses Node.js 20 or later without dependencies. JishuDB setup is included in this package.
metadata:
  author: jishudb
  bundled-setup: jishudb
  version: "0.1.17"
  openclaw:
    homepage: https://github.com/x-aijishu/jishudb-skills/tree/main/skills/jishudb-plaud-import
---

# Plaud Recording Import

Archive selected Plaud audio, timestamped transcripts, and summaries in JishuDB
with stable source associations. Keep each representation distinct and verify
saved material before offering cited comparisons.

## Required first step: JishuDB readiness

Start here before optional preference questions, public research, source
transfer, drafting, rendering, or creating deliverables. Use the request and
existing decisions for this check; apply the task-specific defaults below.
If you make a task list, put JishuDB readiness first and leave dependent work
pending until it passes.

1. Look for the host's JishuDB MCP tools. If available, call
   `kb_get_capabilities({})` through the actual host connector. Reuse the
   selected service and existing authorization when they work.
2. If tools are absent, the connector is unconfigured, or the call fails,
   immediately read the bundled [routine setup path](references/jishudb-setup/references/setup-quickstart.md).
   Missing tools trigger setup without requiring a failed MCP call. Reading
   the guide is not completion: perform its read-only machine, effective
   client-configuration, and supported Desktop-location checks next.
3. On a supported local machine, follow the quickstart's single discovery
   pass. Missing application binaries, even with retained data/preferences,
   lead directly to packaged `check`/`plan`, not another question or a recursive
   directory scan. Read the full installation contract only for a specific
   warning/failure; do not ask whether to generate a read-only plan. Repair an
   existing selected service instead of replacing it.

4. Treat `plan_ready` as internal progress. Reuse existing explicit installation
   or setup authorization when it covers the concrete transaction; do not ask
   again to inspect, plan, resume a bounded download, or continue after a user
   action. If authorization is missing, ask one short confirmation after the
   plan is ready. Keep the full plan, paths and hashes in tool evidence unless
   needed to resolve a discrepancy or requested by the user.
   On both platforms, run bounded `download` calls with the same valid plan
   until `downloaded`, then `execute`. `download_pending` means continue, not
   stop after reporting progress. Honor `download_waiting` retry intervals.
   Pause for actual OS, installer, agreement, OAuth or client-trust prompts;
   after the user acts, verify completion and continue automatically. Ask again
   only for uncovered material changes or genuinely missing authorization.
   Follow the setup guide's expiry and failure rules; never alter signed plans,
   bypass consent or repeatedly execute an installer with an unknown outcome.

5. Begin research, source transfer, or deliverable generation only after a real
   host capability call, required runtime readiness, and the task's destination
   and write authorization pass.
   A healthy endpoint, saved URL, installed app, or remembered KB is insufficient.

After `installed`, continue the quickstart's **Connect after installation**
steps. Verify service health in a separate tool call after launch returns,
then configure and load the connector through supported host controls yourself.
Keep routine configuration work with the Agent when those controls are available;
request user action only for a real presence prompt or a proven missing host
capability. For supported `initial-consent` or `owner-consent`, use native OAuth
without management-password setup. The user completes Trust/OAuth; allow
automatic return before using a manual fallback. Do not start Connect again
while the original callback is pending. A browser success page alone is not readiness. Read only the
relevant onboarding or runtime-preparation section of the full
[setup guide](references/jishudb-setup/setup.md) when those details are needed.

### Reuse setup authorization without a choice menu

Do not offer or recommend a "PDF fast path", "skip JishuDB", "local files
first", or "archive later" choice, including through a question tool. JishuDB
is a prerequisite of this Skill, not optional storage for its deliverables.
A preference for speed or a particular output format does not waive it.

When installation approval is missing, ask whether to execute the concrete
plan just produced; proceeding or postponing setup are valid choices. Do not
replace that approval with an "install DB or produce local files?" menu. Do
not ask about optional format, depth, variants, or style before readiness.
Reuse explicit preferences from the original request; ask later only if a
consequential ambiguity actually prevents the task. Necessary material-selection,
source-access, transfer, and retention consent remain task-specific requirements;
installation approval does not grant them.

Return `USER_ACTION_REQUIRED` for pending approval, OAuth, or a required client
action that the Agent cannot perform through available supported controls.
Return `BLOCKED` for unsupported or declined setup, with the observed reason
and next action. If inspection or plan generation fails, report that exact
failure rather than inventing a plan or offering a local-only substitute.
Do not start research, transfer source material, or generate task deliverables
while this prerequisite is unmet. If the user explicitly declines JishuDB and
requests a different workflow, explain that this Skill is blocked; do not label
a separate local-only workflow as successful execution of this Skill.

## At a glance

| Item | Details |
| --- | --- |
| Use when | Selected Plaud meetings or local exports need archival and optional follow-up comparison. |
| Delivers | Saved representations, verified processing status, provenance records, and requested cited analysis. |
| Requires | JishuDB write access and authorized Plaud/local material; compatible direct upload for audio. |
| Does not | Control recording hardware, access unsynced device-only material, or silently drop requested audio. |

## Use this skill when

- The user wants to archive selected Plaud meetings in a JishuDB knowledge base.
- The user selects a local Plaud audio, transcript, or summary export to import.
- A resumed import needs to preserve the association between meeting representations.
- The user wants to import meetings and then compare their requirements with project documents.

## Do not use this skill when

Do not use this skill to start recordings, control hardware, access unsynced
device-only recordings, or import other vendors' material. If all needed
material is already archived and only retrieval is requested, use
`jishudb-search`; use `jishudb` for destination connection setup.

## Agent workflow

Read [connection and transfer](references/connection-and-transfer.md) before
connecting or uploading, and use the
[provenance record](references/provenance-record.md) for the saved association.
Use the host's actual namespaced tools and live input schemas; tool names below
are the unprefixed vendor and JishuDB names.

Follow the packaged [task execution defaults](references/jishudb-setup/task-execution.md)
for routine choices and bounded recovery; retain the recording-specific consent
and identity rules below.

### Scope and approval

1. Resolve the recording selection, material mode, destination KB, and output
   directory from the request. For an unqualified recording import, propose
   original audio plus any available existing transcript; summaries are a
   separate representation. Reuse an explicit user choice.
2. Reuse explicit transfer authorization when the request already identifies
   the selected material and destination. Otherwise disclose the concrete
   source-to-JishuDB transfer and obtain only the missing scope once. Do not interpret installing this Skill
   as account access, installation approval, or knowledge-base write approval.
3. Use the host's language for questions, reports, and meeting analysis. Ask
   only for ambiguous selections or necessary authorization, not for a resume,
   document pack, or unrelated account information.
4. Do not control hardware, start recordings, access unsynced device-only
   material, add other vendors, publish content, or create external tasks.
   Recurring imports need separately authorized host automation.

### Connect and select

1. Reuse a working JishuDB MCP connection for the user's intended service.
   If missing or unusable, pause the task and follow the included
   [installation and connection guide](references/jishudb-setup/setup.md).
   Its platform helpers and recovery instructions are inside this package;
   no separate `jishudb` Skill or ClawHub download is required. Resolve setup
   paths and run helpers from `references/jishudb-setup/`, not the task root.
   Diagnose the observed failure first. Honor an already selected local or
   remote target; clarify an unresolved target before installing anything.
   Reuse existing installation approval. When this task needs writes, obtain
   that scope explicitly in the initial OAuth flow instead of first creating
   a read-only grant and immediately requesting a second authorization.
   Preserve OS, client-trust, agreement and device-owner prompts for the user.
   Resume only after the real client connection and required runtime are ready.
   Pending user action is `USER_ACTION_REQUIRED`; unsupported or declined
   setup is `BLOCKED`. Do not continue using a local-only persistence substitute.
2. Call `kb_list`, resolve the actual selected KB ID, and check
   `kb_get_config` and live tool schemas for document limits. Use `kb_create`
   only if the user approves creating the named destination. Do not guess a
   KB ID from its display name or silently select an unrelated default.
3. For cloud acquisition, call Plaud `get_current_user`. If authorization is
   missing, guide the browser login through the existing connector. Never ask
   for or read its token files. Confirm the intended account before reading
   recordings.
4. Call `list_files` with the relevant name/date filters, inspect candidate
   metadata, and use `get_file` for the selected ID. Resolve relative dates in
   the user's timezone and retain `start_at` separately from `created_at`.
   Inspect pagination and search coverage; an incomplete list does not prove
   that a meeting does not exist. If the recording has not synced, explain the
   vendor sync step.
5. For an approved local export, skip Plaud calls. Record that acquisition
   route honestly. Associate it with a vendor recording only when the user
   identifies that recording; otherwise use a stable user-approved local
   source identifier instead of inventing a Plaud ID.

### Resolve prior imports before writing

1. Use [the identity helper](scripts/recording-identity.mjs) with the confirmed
   non-secret account scope, recording ID, and KB ID. For a local-only export,
   use the distinct scope `local-export` and its approved stable source ID.
   Its `externalAssetId` associates representations; `manifestNoteId`
   locates the durable provenance record. Do not use an email, device serial,
   bearer, or temporary URL as an identity input.
2. Call `note_get` with `manifestNoteId`. On `NOT_FOUND` only, plan a new
   provenance Note. Propagate authorization or service errors instead of
   treating them as an absent record. Before updating an existing Note, verify
   its Skill marker, source association, and KB match.
3. Follow `kb_list_documents` pagination to reconcile existing associated
   documents, including an interrupted import not yet recorded in the Note.
   Call `kb_get_document` for candidate IDs. Match representation and content
   hash; use `audio.originalSha256` for original audio, not the document's
   potentially transcript-based `sha256`.
4. Reuse unchanged material. Append changed source content as an explicitly
   labelled revision by default; never overwrite or delete an older document
   automatically. If a manifest references a missing/deleted resource, report
   it and obtain approval before recreating it.

### Acquire and import selected material

1. Before downloading audio, require `mcp.upload.audio.enabled`, its `direct`
   mode, the requested extension, and acceptable size/duration. Inspect
   speech and compressed-decoder readiness separately. Missing readiness
   requires repair or explicit approval to retain an original while processing
   remains incomplete; never promise a ready transcript in that case.
2. For audio, obtain the selected recording's current `presigned_url` from
   `get_file` and download actual bytes with a bounded, authorized host
   transfer. Keep the URL transient. Renew it through `get_file` after expiry;
   do not store it as provenance or bypass access restrictions.
3. For existing text, call `get_transcript` and/or `get_note` only for the
   approved representations. Preserve supplied timestamps and speaker labels.
   Store a summary as a summary, not a substitute transcript. Do not invoke
   audio recognition merely to import existing text.
4. Preserve the original downloaded/exported files in the approved output
   directory without overwriting existing files. Hash exact bytes. Keep
   collection times and import status out of the immutable source-text payload
   so reruns do not manufacture a new content revision.
5. Run the identity helper again with the representation and actual content
   SHA-256. Keep its retry identity unchanged for the same bytes and target.
   Execute the transfer sequence in the reference: `kb_prepare_upload`,
   its returned raw PUT, then `kb_get_job`. Use the shared `externalAssetId`
   for the audio and each text representation.
6. When direct upload is unavailable, supported text can use
   `kb_upload({kbId, filename, contentBase64, externalAssetId})`. Inspect its
   live schema first. Audio cannot use this fallback or server-side `path`.
   If the host cannot transfer audio, report the missing capability rather
   than silently switching to transcript-only import.
7. After uncertain completion, query `kb_list_jobs` using the descriptor's
   `clientItemId` before retrying bytes. Reconcile associated documents before
   replacing an expired preparation. A new attempt after a proven failed,
   uncommitted transfer must be recorded explicitly; it is not permission to
   duplicate an already saved recording.

### Persist provenance and complete

1. Poll `kb_get_job` at a reasonable interval, for at most two minutes in the
   current interaction. A still-running job is `PARTIAL`, not failed or
   complete. Retain its ID for continuation instead of resubmitting it.
2. Call `kb_get_document` for each saved representation. For audio, report
   original retention, playback/normalization, transcription, and indexing
   separately. Use `kb_retry_job` only after inspecting the failed/cancelled
   job and addressing its cause. An indexing-only retry should reuse the
   saved transcription.
3. Read saved text with `kb_read_document_text` and confirm the requested
   source content or recognizable passages. Use `kb_search` in the selected
   KB to establish retrieval before promising cited analysis.
4. Save or merge the provenance record with `note_create` or `note_update`,
   using the stable Note ID and the returned `updatedAt` for optimistic
   concurrency. For creation, capture one RFC 3339 `createdAt` and reuse the
   identical request on an uncertain retry.
5. Call `note_link_to_kb` with the saved Note's current `updatedAt`. Follow its
   job, then `note_get` and `kb_read_document_text` for the linked document.
   A source-only Note or a queued link is not completed KB archival. Subsequent
   updates to a linked Note refresh automatically; inspect that refresh instead
   of linking repeatedly.
6. Only if requested, compare the imported material with the user's selected
   existing KB evidence. Cite returned document/chunk IDs and actual source
   timestamps where present. Separate original summaries from new analysis,
   preserve disagreements, and identify missing evidence. Never invent speaker
   labels or meeting commitments.

Return one state with the saved IDs, material coverage, and any required
recovery action:

- `COMPLETE`: all requested material and provenance are saved, required
  processing/indexing and readback succeeded, and requested analysis is cited.
- `PARTIAL`: some material is saved or files are preserved, but a requested
  representation, processing step, or provenance refresh remains incomplete.
- `USER_ACTION_REQUIRED`: login, installation, trust, or another explicit
  user-presence gate is waiting and no partial archival needs reporting.
- `BLOCKED`: a required source/backend/host capability is absent or declined
  before archival.
- `FAILED`: an available operation failed before anything was archived; report
  the actual failure without a success-shaped substitute.

Never print credentials, upload headers, signed URLs, or account/device
identifiers in the completion report. This package does not claim a tested
Plaud account, WorkBuddy integration, or mainland network configuration.

## Discovery

### Keywords

- Chinese: Plaud录音导入、会议归档、音频导入、带时间戳转写、来源关联.
- English: Plaud import, local recording export, meeting transcript, provenance, duplicate reconciliation.

### Example requests

- “把我选中的Plaud录音和已有转写导入指定知识库。”
- “导入这份Plaud本地导出，再对比已归档的项目需求。”
- “Archive selected Plaud meetings while preserving audio and transcript associations.”
- “Resume this interrupted recording import and check what is already saved.”

### Nearby but different

- Read material already archived in JishuDB → `jishudb-search`.
- Repair the destination connection → `jishudb`.
