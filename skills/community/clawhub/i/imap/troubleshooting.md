# Troubleshooting

Use this file when mailbox behavior is inconsistent, slow, or provider-specific.

## Auth succeeds elsewhere but IMAP fails

Check:
- whether the account actually allows IMAP
- whether an app password, bridge, or delegated auth flow is required
- whether the endpoint, port, and TLS mode match the provider

Do not keep retrying blind login attempts without confirming the provider requirements.

## Search misses messages that should exist

Possible causes:
- wrong folder or namespace
- server-side search semantics differ from expectations
- charset or MIME encoding mismatch
- provider indexing lag or virtual folder behavior

Narrow the question, test a simpler filter, and verify with lightweight header fetches.

## Incremental sync duplicates or skips mail

Suspect:
- saved sequence numbers instead of UIDs
- a changed `UIDVALIDITY`
- partial reconciliation after move or delete events
- stale `MODSEQ` handling

Rebuild the checkpoint for that folder instead of compounding drift.

## Read-only review changed mailbox state

Likely causes:
- used `SELECT` plus body fetches that marked messages seen
- omitted a read-only mode such as `EXAMINE`
- provider treats some operations differently than expected

Record the provider behavior and tighten the default mutation policy.

## Folders look duplicated or wrong

This often points to:
- namespace misunderstandings
- delimiter assumptions
- special-use mapping differences
- Gmail labels or virtual folders

List the raw folders first, then map canonical roles in `folder-map.md`.

## Large mailbox tasks are slow

Reduce scope before optimizing:
- search server-side
- fetch metadata first
- limit UID windows
- avoid full-body downloads
- avoid attachment downloads until needed

In mailbox work, smaller scope usually beats more code.
