---
name: IMAP
slug: imap
version: 1.0.0
homepage: https://clawic.com/skills/imap
description: "Read, search, and sync IMAP mailboxes with UID-safe fetches, precise filters, and attachment-aware workflows."
changelog: "Built a deeper IMAP workflow for reliable mailbox review, incremental sync, safer flag handling, and attachment triage."
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

Use this skill when the user needs to inspect or operate an IMAP mailbox across Gmail, Fastmail, ProtonMail Bridge, Exchange-compatible gateways, or self-hosted mail servers.

Activate it for inbox search, unread triage, header and body fetches, attachment handling, folder mapping, or incremental mailbox sync when correctness matters more than quick ad hoc scraping.

## Architecture

Memory lives in `~/imap/`. If `~/imap/` does not exist, run `setup.md`. See `memory-template.md` for the default structure and file templates.

```
~/imap/
├── memory.md       # activation defaults, mutation policy, preferred reporting style
├── accounts.md     # mailbox-specific endpoints, auth notes, and server capabilities
├── folder-map.md   # canonical folder mapping and provider quirks
├── sync-state.md   # UIDVALIDITY, last UID, MODSEQ, and sync checkpoints
└── playbooks.md    # saved mailbox workflows and reusable search recipes
```

## Quick Reference

Use these files when the current mailbox task needs more detail than the core rules provide.

| Topic | File |
|-------|------|
| Setup and activation defaults | `setup.md` |
| Memory and file templates | `memory-template.md` |
| Session planning and discovery | `session-strategy.md` |
| Search and fetch patterns | `search-and-fetch.md` |
| State, flags, and sync rules | `state-and-flags.md` |
| Attachment and MIME handling | `attachments.md` |
| Failure diagnosis and provider quirks | `troubleshooting.md` |

## Core Rules

### 1. Discover mailbox capabilities before making assumptions
- Identify server capabilities, namespace layout, delimiter behavior, and special-use folders before building commands or interpreting results.
- Check whether the server supports features such as `UIDPLUS`, `CONDSTORE`, `QRESYNC`, `MOVE`, or `XLIST` replacements.
- Folder names, archives, and flag behavior vary by provider, so do not hard-code Gmail semantics onto every mailbox.

### 2. Default to read-safe operations unless the user clearly wants mutation
- Start with safe inspection patterns such as capability discovery, folder listing, `EXAMINE`, header fetches, and targeted body retrieval.
- Treat delete, move, copy, expunge, and bulk flag updates as mutating actions that require either explicit user approval or a previously confirmed standing policy.
- If the user only asked to inspect or summarize mail, do not silently mark messages seen or alter mailbox state.

### 3. Use UIDs and durable sync markers, not volatile sequence numbers
- Sequence numbers shift as mail arrives or is removed, so they are unsafe for persistent tracking.
- For repeatable workflows, store `UIDVALIDITY`, last processed UID, and when available `HIGHESTMODSEQ` or related sync checkpoints in `~/imap/sync-state.md`.
- If `UIDVALIDITY` changes, treat prior cursors as invalid and rescan instead of trusting stale state.

### 4. Fetch the minimum data that answers the question
- Start with folder listing, counts, flags, and envelope or header data before downloading full bodies or attachments.
- Escalate to body sections, MIME structure, or attachments only when the user actually needs that detail.
- Smaller fetches reduce latency, bandwidth, and the chance of dragging sensitive content into unnecessary downstream processing.

### 5. Search with explicit server-side filters and report what they mean
- Prefer precise IMAP search constraints such as date ranges, sender, subject fragments, flags, size limits, or UID windows over broad mailbox scans.
- Be clear about whether the server search is header-only, text-oriented, charset-sensitive, or provider-specific in its matching behavior.
- When search semantics are ambiguous, explain the limitation and offer a narrower or confirmatory pass.

### 6. Treat MIME and attachments as structured data, not opaque blobs
- Read `BODYSTRUCTURE` or equivalent metadata before assuming where text lives or which parts are attachments.
- Distinguish inline parts from downloadable attachments, decode filenames safely, and preserve charset and transfer-encoding details.
- Avoid downloading large attachments unless needed, and report part identifiers, sizes, and media types first when triaging.

### 7. Keep credentials out of skill memory and scope network use tightly
- Store only non-secret connection notes, capabilities, and workflow preferences under `~/imap/`.
- Never ask the user to paste account passwords into memory files; use existing local auth flows, app passwords, OAuth-backed bridges, or other secure runtime mechanisms the environment already supports.
- Restrict network activity to the user-configured IMAP endpoint needed for the mailbox task at hand.

## IMAP Traps

- Treating message sequence numbers as stable identifiers -> follow-up fetches hit the wrong message after mailbox changes.
- Marking mail seen during a read-only review -> the user loses unread state without asking for it.
- Downloading entire folders to answer a narrow question -> latency, bandwidth, and privacy costs rise for no gain.
- Ignoring `UIDVALIDITY` resets -> incremental sync silently skips or duplicates messages.
- Assuming every server supports `MOVE`, `IDLE`, or Gmail-style special folders -> commands fail or behave differently across providers.
- Parsing attachments without checking MIME structure first -> inline parts, filenames, or charsets get misread.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| User-configured IMAP or IMAPS server | authentication material handled by the runtime, mailbox commands, requested headers, bodies, flags, and attachments | list folders, search messages, fetch content, and update mailbox state when approved |

No other data is sent externally.

## Security & Privacy

Data that stays local:
- Activation defaults, provider quirks, sync checkpoints, and reusable playbooks stored under `~/imap/`
- Mailbox notes the user explicitly wants remembered for future sessions

Data that leaves your machine:
- Only the IMAP requests needed to talk to the configured mailbox server
- Message metadata, bodies, or attachments fetched from that mailbox when the current task requires them

This skill does NOT:
- store mailbox passwords or OAuth tokens in `~/imap/`
- assume mutating mailbox access is allowed by default
- send mailbox content to undeclared third parties
- treat sequence numbers as durable sync state

## Trust

By using this skill, data is exchanged with the user-configured mail provider or IMAP bridge.
Only use it with mailbox systems and local credential flows the user already trusts.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `api` - use when the mailbox task is really an API integration or authenticated service wrapper problem.
- `http` - use when the work is request shaping, header debugging, or protocol inspection outside an IMAP session.
- `json` - use when mailbox results need structured transformation, normalization, or downstream machine-readable output.
- `code` - use when the user needs a full implementation, parser, or sync worker built and verified end to end.
- `bash` - use for shell-first mailbox tooling, local automation, and repeatable command wrappers.

## Feedback

- If useful: `clawhub star imap`
- Stay updated: `clawhub sync`
