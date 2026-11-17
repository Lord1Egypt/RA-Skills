---
name: "paperless-cloud-intake-hardening"
description: "Harden Paperless cloud-folder intake with staging, provider gates, read checks, and safe retries."
---

# Paperless Cloud Intake Hardening

Use this skill to design, review, or repair Paperless intake workflows where files arrive through a cloud-synced folder or another unreliable filesystem event path.

Keep all examples generic. Do not include real client names, private paths, hostnames, volume names, account names, URLs, secrets, tokens, filenames, or document examples in reusable skill text or public reports.

## Core Principles

Preserve these even when provider commands, operating systems, or deployment details change:

- Stage before Paperless consume.
- Verify readable bytes before staging or delivery.
- Never treat provider metadata, badges, pinning, or filenames as proof of readability.
- Classify the provider before choosing a hydration action.
- Deduplicate before delivery and after retries.
- Atomically deliver only validated files.
- Verify Paperless ingestion through a native signal after delivery.
- Account for leftovers before deleting or moving anything.

## Core Pattern

Use a layered intake path:

1. Source cloud folder receives user files.
2. Optional user-context automation enumerates, enqueues, or requests provider hydration.
3. Intake script reads the source into staging outside Paperless consume.
4. Script validates nonzero and complete staged bytes.
5. Script deduplicates by checksum or another durable identity.
6. Script atomically moves validated files into Paperless consume.
7. Paperless ingestion is verified through tasks, API records, database records, logs, or another native signal.
8. Periodic retry remains available for missed events, delayed sync, provider failures, paused sync clients, files added while no user-facing automation is active, and files that were visible before they were hydrated.

A hydration nudge makes the common path smoother. It does not replace staging, validation, duplicate handling, retry, or Paperless-side verification.

## Relationship To Generic Cloud Hydration Skill

This skill is self-contained for Paperless work. An agent using it should have enough guidance to harden a Paperless intake flow without loading another skill.

For non-Paperless workflows, use the standalone `cloud-file-hydration-nudge` skill. That skill is the generic reusable pattern for visible-but-unreadable cloud files in shared folders, document review, OCR, uploads, batch processing, and other automations.

## Cloud Materialization Preflight

Before handing cloud-backed files to Paperless, verify that files are not merely visible placeholders.

Treat filenames, sizes, Finder metadata, search results, provider badges, provider policy state, and provider state as weaker evidence than a successful byte read.

## Evidence Confidence

Use this ladder when deciding whether a file is safe to deliver:

- High: successful bounded read by a normal process; successful parser/checksum/content validation; Paperless native ingestion success after delivery.
- Medium: provider API or File Provider state reports downloaded/current; file has expected size and stable metadata after a successful read.
- Low: file is visible in Finder, Explorer, a directory listing, search index, or provider UI.
- Very low: filename exists, provider badge appears local, folder is marked available offline, or a policy such as pinning/always-keep-local is set.

Only high-confidence evidence should move a file into Paperless consume.

Preflight workflow:

1. Inventory the source folder without modifying it.
2. Classify the cloud provider for each source path before choosing any hydration routine.
3. Attempt bounded content reads against representative files and every candidate before delivery.
4. Prefer content-aware checks where available: `file`, `pdfinfo`, `unzip -t`, image metadata tools, checksum after hydration, or a bounded byte read.
5. If filenames are visible but reads fail, treat the source as not materialized yet unless other evidence proves corruption.
6. Use the provider's normal local-availability action only when it is supported and approved for the environment.
7. Re-run the same read tests after local availability or hydration.
8. Do not hand files to Paperless until read tests succeed.

## Provider Classification Gate

Provider-specific hydration is only safe after identifying the provider for the actual source path. Do not reuse the last successful nudge from another intake.

Use multiple weak signals where possible:

- iCloud Drive: path under `~/Library/Mobile Documents/com~apple~CloudDocs`, ubiquitous-item metadata, or platform checks for an iCloud ubiquitous item.
- OneDrive: path under a OneDrive or Microsoft File Provider container such as `~/Library/CloudStorage/OneDrive-*`, provider metadata/domain naming Microsoft OneDrive, or a tenant-branded OneDrive mount.
- Other File Provider folders: provider metadata, mount path, sync-client folder conventions, or user confirmation.
- Unknown/local: no cloud provider evidence, local filesystem path, or conflicting signals.

Decision rules:

- If the path is iCloud, use iCloud download/materialization. Do not use OneDrive-specific helpers.
- If the path is OneDrive, use provider-supported materialization or approved provider UI/helper hydration first.
- If the path is another known provider, use that provider's supported local-availability or download action.
- If the provider is unknown or signals conflict, leave the file in source, log the uncertainty, and gather more evidence before applying provider-specific nudges.

## macOS File Provider Hydration

On macOS File Provider-backed folders, separate three questions:

- Can the automation enumerate or receive the file path?
- Does provider metadata claim the file is downloaded/current or pinned?
- Can a normal process actually read stable bytes?

`fileproviderctl evaluate <path>` can inspect states such as `isDownloaded`, `isDownloading`, `isKeepDownloaded`, and `isMostRecentVersionDownloaded`. Treat this as diagnostic information, not final proof. The strongest proof is a successful POSIX read followed by validation.

Useful diagnostics include:

- Direct read errors such as `Resource deadlock avoided`, permission errors, zero-byte reads, invalid signatures, incomplete archives, or short reads.
- File Provider state claims the item is downloaded/current, but `cat`, `dd`, checksum, parser, or archive validation fails.
- A user-facing Finder/provider interaction makes the same script read successfully afterward.
- A visible normal-size file is marked `dataless` while reads fail.

For unattended intake, keep defensive staging. A previously available-offline folder can later be evicted, partially synced, paused, or stuck in a provider cache state.

## Hydration Wrapper Pattern

For macOS/File Provider sources, add a lightweight wrapper before or inside the intake script when hydration failures are observed:

- Receive explicit file paths or scan in the narrowest permission context available.
- Classify the provider per path before selecting a nudge routine.
- Try a cheap bounded read probe first.
- Trigger provider-appropriate hydration only after a read failure and only from an approved, narrow execution context.
- Wait for a bounded read probe to succeed or time out.
- Pass only readable files to the downstream intake path.
- Log retryable waiting states instead of treating placeholders as corruption.

The generic intake script remains responsible for correctness: stream/read into staging, validate nonzero and complete bytes, deduplicate, and atomically move into consume.

Avoid scheduled visible Finder windows. If provider UI automation is required, keep it in a trusted helper application or another narrow user-approved host. Do not grant broad Node, shell, scheduler, or generic automation processes Accessibility, Screen Recording, Full Disk Access, or equivalent privacy powers just to hydrate files.

## Two-Phase Enqueue And Deliver

Folder watchers, Automator Folder Actions, Shortcuts, or FSEvents may acknowledge that a file exists before it is hydrated. That acknowledgement is not a Paperless delivery signal.

Use two phases:

1. **Enqueue:** record an explicit path when a folder action, watcher, or scan sees it.
2. **Deliver:** copy/import only after bounded read proves the file is hydrated.

Observed Automator result: a temporary Folder Action fired for a newly added file in a OneDrive folder, but did not fire its `adding folder items` handler when an existing file was offloaded or hydrated. Do not rely on Folder Actions to notice hydration state changes for existing placeholders.

Dataless files should remain pending/retry candidates. A retry loop should prioritize pending files instead of repeatedly full-scanning large folders forever. Keep a rare/manual reconciliation scan for missed events.

## iCloud Drive Hydration

For iCloud Drive files, prefer the native iCloud download request plus a bounded read wait.

Generic shape:

1. Confirm provider classification says the source path is iCloud.
2. Check whether the item is an iCloud ubiquitous item.
3. Call the platform API equivalent of `startDownloadingUbiquitousItem`.
4. Poll a bounded read such as `dd if=<file> of=/dev/null bs=64k count=1` until it succeeds or times out.
5. Only then invoke the intake path.

In causal testing, an evicted iCloud file appeared as a normal-size `dataless` file and failed reads with `Resource deadlock avoided`. Finder folder update alone did not hydrate it. The native iCloud download request plus bounded read polling did.

Keep provider-specific helpers outside the generic intake core. Other providers need different materialization actions.

Do not use Quick Look for iCloud hydration automation. If native iCloud download fails or times out, explain the failure and ask the user how they want to proceed.

## OneDrive Hydration

For OneDrive File Provider folders on macOS, folder-level Finder update/open, `/pin`, and available-offline policy are not proof that a dataless child file is hydrated.

Observed OneDrive placeholder signals may include:

```text
filesystem flags: compressed,dataless
isDownloaded = 0
isDownloadRequested = 0
isMostRecentVersionDownloaded = 0
bounded read: Resource deadlock avoided
```

Preferred pattern:

1. Confirm provider classification says the source path is OneDrive.
2. Confirm the file is visible but not readable with a bounded read.
3. Confirm provider/local state where possible, such as `dataless`, `isDownloaded = 0`, or `isMostRecentVersionDownloaded = 0`.
4. Check whether sync is paused, offline, quit, or otherwise unavailable. If so, report it and ask before changing provider state.
5. Prefer a supported provider download/materialization action if one exists in the environment.
6. If a trusted helper application or approved narrow user-context automation host is available, use the Finder/provider cloud-status download button for the target file or folder.
7. Poll provider state and the same bounded read until every target file is readable.
8. Retry staging only after the read succeeds.
9. If no trusted helper application or approved user-context host exists, leave the file pending and tell the user provider/manual hydration is needed.

Observed behavior: in Finder list view, OneDrive may expose the cloud glyph as an Accessibility `AXButton` with description `Not downloaded`. Pressing that button materialized file bytes in the observed macOS File Provider test environment without Quick Look. This requires a narrow approved automation host; do not grant broad Node permissions for production.

For folder-level cloud-button hydration, poll every intended child file. Do not trust folder state alone.

Do not treat these as proof of hydration unless bounded read succeeds afterward:

- Opening or updating the OneDrive folder in Finder.
- `fileproviderctl evaluate com.microsoft.OneDrive.FileProviderActions.MarkPinned <file>`.
- `/Applications/OneDrive.app/Contents/MacOS/OneDrive /pin <file>`.
- Finder `Always Keep on This Device`.
- Provider badges or pinned/shared decorations.

Observed retest: `/unpin <file>` may print a failure while still offloading the file to `compressed,dataless`; `/pin <file>` may fail or may set policy without hydrating. Verification matters more than command output.

## Quick Look Deprecation

Quick Look is deprecated for automated Paperless/cloud hydration. It should not be built into intake scripts, scheduled retry loops, provider nudges, or parser workflows as an automated fallback.

Reason: Quick Look opens UI and invokes preview parsers. That makes it broader and riskier than provider-native or provider-UI hydration controls.

If all provider-native, provider-UI, and approved trusted-helper approaches fail, tell the user plainly that a manual Quick Look attempt may hydrate the file. Present it as a user-operated recovery option, not as an automated step:

```text
The safer provider hydration methods did not materialize this file. Quick Look is deprecated for automated hydration because it opens a preview parser, but you can manually try Quick Look in Finder if you accept that risk. Afterward, I will re-check with the same bounded read before continuing.
```

After any manual Quick Look attempt, repeat provider-state checks and the same bounded read. Do not continue downstream based only on the user seeing a preview.

## Trigger And Permission Pattern

Separate user-facing enumeration from generic staging when macOS privacy or File Provider behavior requires it:

- Use Automator, Shortcuts, Hazel, Finder AppleScript, or another user-facing automation layer when it can enumerate File Provider folders more safely than a broad shell runtime.
- Pass explicit file paths to the generic intake script when useful.
- Keep periodic retry where the scheduler can enumerate reliably.
- Avoid granting Full Disk Access, Accessibility, or Screen Recording to broad runtimes such as `/bin/bash`, generic `node`, or schedulers unless the user explicitly accepts that wider security surface.
- Prefer a trusted helper application or narrow approved host for privacy-gated macOS actions.

If a scheduler cannot enumerate the source folder, prefer explicit-path mode fed by a user-facing automation wrapper. If a scheduler can enumerate but reads fail, treat it as hydration/materialization and retry rather than moving anything into Paperless.

## Paperless Consumer Reliability

Do not assume that an atomic move into consume creates a Paperless document.

On Docker Desktop, macOS bind mounts, network mounts, and cloud-adjacent deployments, Paperless may miss filesystem notifications even when the file is visible in `consume`.

Recommended baseline:

- Enable native Paperless consumer polling where appropriate, such as `PAPERLESS_CONSUMER_POLLING=60`.
- Add an optional post-delivery one-shot consumer hook for automation-delivered files when prompt ingestion matters or polling is unavailable.
- Keep the post-delivery hook per deployment; do not assume every deployment needs it.

## Logging

When listing succeeds but content reads fail, log a retryable diagnostic, for example:

```text
waiting: cloud placeholder or File Provider hydration issue suspected; file metadata is visible but content is not locally readable; materialize the source folder/file and retry
```

Distinguish these states:

- `provider classified`: source path was classified, or classification was unknown/conflicting.
- `waiting`: source is not readable, zero-byte, incomplete, or timed out; leave it in source for retry.
- `pending hydration`: file is waiting for provider, trusted-helper, or manual hydration.
- `hydrating`: a provider-specific nudge is being attempted after a read failure.
- `quicklook deprecated`: Quick Look automation is not used; manual Quick Look may be mentioned only as a user-operated recovery option after safer methods fail.
- `delivered`: staged copy passed validation and was atomically moved into Paperless consume.
- `skipped duplicate`: checksum already processed.
- `error`: destination move or local state failure needs attention.

Avoid logging secrets, private paths, private filenames, client names, URLs, database credentials, tokens, or real document examples in public examples or reusable skill text.

## Definition Of Success

A file is successfully ingested only when:

- it was proven readable;
- staged successfully outside Paperless consume;
- validated as nonzero and complete enough for the document type;
- deduplicated against prior deliveries;
- atomically delivered into Paperless consume;
- Paperless recorded successful ingestion through a task, API record, database record, log, or another native signal;
- duplicate protection/state was updated so retries do not redeliver the same file.

Until all of those are true, treat the item as pending, retryable, duplicate-skipped, or failed with evidence.
## Verification Checklist

Verify all of the following before calling an intake path healthy:

1. Scheduler can enumerate or receive source paths.
2. Each source path's provider is classified before hydration.
3. Representative source files can be read, not only listed.
4. Every file is bounded-readable before delivery to Paperless.
5. If File Provider claims files are downloaded but reads fail, test the classified provider's API, provider action, Finder action, or approved trusted helper application and retry the same read.
6. Quick Look is disabled by default and deprecated for automation.
7. Broad Node/shell/scheduler processes have not been granted unnecessary privacy permissions.
8. No new zero-byte or partial files appear in Paperless consume.
9. Delivered files become visible inside the Paperless runtime/container.
10. Paperless creates document records, task successes, API records, database records, or another native ingestion signal.
11. Consume returns to a clean state after Paperless ingestion unless the deployment intentionally leaves originals.
12. Duplicate handling prevents repeated delivery after successful ingestion.

## Causal Test Pattern

Do not claim a nudge works just because a freshly local file succeeds.

A stronger test is:

1. Create or obtain a file that is visible but not locally readable.
2. Classify the provider from the path and provider metadata.
3. Prove pre-nudge read failure with a bounded read.
4. Capture provider/local state such as dataless, placeholder, or materialization error where available.
5. Run only the classified provider's hydration nudge or wrapper.
6. Prove the same bounded read now succeeds.
7. Run the downstream workflow.
8. Verify the downstream result independently.
9. Clean up test records and artifacts when they were created only for the test.

## Cleanup

Old failed placeholders or leftovers in consume should stay untouched until accounted for. Before cleanup, match leftovers against Paperless records, successful task logs, checksums, original filenames, or user confirmation. Move/delete only after the user explicitly approves cleanup.
