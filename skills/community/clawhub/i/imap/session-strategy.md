# Session Strategy

Use this flow when starting or resuming mailbox work.

## 1. Clarify the task shape

Identify which of these the user actually wants:
- inspect mailbox state
- search for messages
- fetch headers or full content
- review or download attachments
- update flags or move mail
- debug sync behavior

If they only want information, stay read-safe.

## 2. Discover before acting

For a new mailbox or provider:
- record endpoint and auth style
- list capabilities and special folders
- confirm delimiter and namespace layout
- note whether `IDLE`, `MOVE`, `UIDPLUS`, `CONDSTORE`, or `QRESYNC` exist

Do not assume Gmail-specific folder behavior unless it is actually Gmail or a Gmail-compatible bridge.

## 3. Choose the minimum safe fetch plan

Use the smallest scope that answers the question:
- counts or folder listing
- UID or flag windows
- envelope or selected headers
- targeted body sections
- attachment metadata
- attachment download only if needed

## 4. Declare mutation gates clearly

Before move, copy, delete, expunge, or bulk flag updates, check:
- does the user want mailbox state changed now
- is there already a standing policy in memory
- can the action be previewed first

If not, stop at a dry-run summary.

## 5. Persist only durable state

Update memory files only with:
- discovered account capabilities
- stable folder mapping
- durable sync checkpoints
- reusable search or triage playbooks

Do not store credentials or large chunks of mailbox content.

## 6. Report in a way the user can act on

For each session, make it obvious:
- what was searched or fetched
- what was not searched or fetched
- whether mailbox state changed
- what the next safe action would be
