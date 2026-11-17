# Notifications & approvals

Two surfaces that overlap: notifications tell you what happened; approvals route decisions.

---

## Notification commands (inbox)

### Discover the inbox

```bash
huly notification list --json
huly notification list --read --json
huly notification list --unread --json
huly notification list --archived true --json
huly notification list --archived false --json                # non-archived
huly notification list --limit 50 --offset 0 --json

huly notification get <ref> --json
huly notification unread-count                                # plain text
huly notification unread-count --json                         # {"count": N}
```

`--archived` non-strict coercion: `--archived 0` → false; any other value → true.

### Act on the inbox

```bash
huly notification mark-read <ref>                # single
huly notification mark-read <r1> <r2> --yes       # multiple, REQUIRED --yes
huly notification mark-unread <ref>
huly notification mark-unread <r1> <r2> --yes

huly notification mark-all-read                   # bulk, all unread
huly notification archive <ref>
huly notification unarchive <ref>
huly notification archive-all --yes               # ALWAYS --yes (bulk)
huly notification delete <ref>                   # cascade-removes InboxNotification rows
```

Marking read/unread does NOT auto-archive. Deleting is destructive; archive is reversible.

### Per-target subscription

```bash
huly notification subscribe --target <doc-ref> --target-class tracker:class:Issue
huly notification unsubscribe --target <doc-ref> --target-class tracker:class:Issue
```

Default `--target-class` is `core:class:Doc`. Pass the right class so the DocNotifyContext attaches correctly.

### Notification context (per-user pin / hide on a doc)

```bash
huly notification contexts list --json
huly notification contexts list --pinned --json
huly notification contexts list --hidden --json

huly notification contexts get <ref> --json
huly notification contexts pin <ref>
huly notification contexts pin <ref> --unpin
huly notification contexts hide <ref>             # hide from sidebar
huly notification contexts hide <ref> --unhide
```

This is the mechanism that powers "Close conversation" on DMs/channels. Each user has a per-doc `notification:class:DocNotifyContext` that controls sidebar visibility.

### Notification providers, types, settings

```bash
huly notification providers --json                # list notification backends (email, web-push, …)
huly notification types --json                    # list NotificationType docs

huly notification settings list --json
huly notification settings list --provider <provider-ref> --json

huly notification settings update \
  --provider <provider-ref> \
  --type <type-ref> \
  --enabled true
```

`--enabled` is non-strict: anything except `'false'` / `'0'` → true. **Required after signup caveat:** if `account.person` isn't yet provisioned, the CLI throws "cannot update notification settings without an associated person profile" — re-login and retry.

---

## Approval commands

### Discover

```bash
huly approval list --json
huly approval list --status Active --json         # Active|Completed|Rejected|Cancelled
huly approval list --status Active --attached-to TSK-1 --json
huly approval get <ref> --json
```

Filter enums for `--status`: `Active | Completed | Rejected | Cancelled` (case-sensitive).

### Create a request

```bash
huly approval request \
  --attached-to TSK-1 \
  --attached-to-class tracker:class:Issue \
  --requested alice@example.com bob@example.com \
  --required-count 2 \
  --tx '{"_class":"core:class:TxUpdateDoc",…}'    # the tx to apply on approval
```

**Required:** `--attached-to`, `--requested` (variadic emails), `--tx` (the JSON of the tx to apply on approval).

**Defaults:** `--required-count` defaults to the number of `--requested` emails. `attached-to-class` defaults to `tracker:class:Issue`.

The `--tx` is mandatory: approvals are wrappers for an idempotent operation. The server validates the tx shape on create and applies it when the request is approved.

### Comment / approve / reject / cancel

```bash
# Plain comment (no decision)
huly approval comment <ref> --body "considering this"

# Comment with a decision (rare — usually approve/reject below)
huly approval comment <ref> --body "ready" --decision approve
# --decision accepts: approve | reject | comment. Omit for plain comment.

huly approval approve <ref> --comment "Looks good"
huly approval reject <ref> --comment "blocking on X" --rejected-tx '{"…":"…"}'
huly approval cancel <ref>              # only by the requester
```

**Critical semantics:**

- `comment` — `--decision` is OPTIONAL. Omit for a plain comment; pass `--decision comment` for symmetry (the CLI prefers omitting the flag).
- `approve` — requires `--comment` is recommended but optional. The request auto-completes server-side when `requiredCount` reached.
- `reject` — `--comment` is REQUIRED. `--rejected-tx` is optional; the tx to apply on rejection.
- `cancel` — only the requester can cancel. The CLI checks this locally (`resources/approvals.ts:301-303`) and throws `Auth: only requesters can cancel` if you're not one; the server would also reject.

### Delete

```bash
huly approval delete <ref>                  # single
huly approval delete <r1> <r2> --yes        # REQUIRED --yes for multiple
```

ApprovalRequest is an AttachedDoc (`request:class:Request`), so delete uses `removeCollection`, not `removeDoc`. Errors per-doc are caught and reported.

---

## Cross-surface: how notifications fire

The platform emits `InboxNotification` rows automatically on most mutations:

| Trigger                           | Notification?                                                                 |
| --------------------------------- | ----------------------------------------------------------------------------- |
| Channel/DM/thread message send    | Every collaborator + every `@mention` (the sender does NOT notify themselves) |
| `comment add --issue X`           | Every `@mention` + every collaborator (the author does NOT notify themselves) |
| Issue status/assignee change      | New assignee (and previous assignee on close)                                 |
| Action (todo) created on an issue | Issue collaborators (depends on cascade shape)                                |
| Card/Document update              | `@mentioned` users                                                            |
| Calendar event with attendee      | Attendees                                                                     |
| Approval status change            | Requester + approvers                                                         |
| Telegram reply to a notification  | Notification sender (creates a thread reply in Huly)                          |

**Class-level mixin to disable notifications:** `IgnoreActivity` (CLI doesn't expose this — server-side plugin config).

**Telegram → Huly:** replies from Telegram arrive as `ThreadMessage` rows; use `huly thread list <parent-id>`.

**Activity feed:** ActivityMessages are emitted for many operations; queryable via `huly activity list --target <doc-ref> --target-class <id>`.

---

## Web-push / Gmail / Google Calendar integrations (FYI)

- **Web-push** sends only if `serverNotification.metadata.WebPushUrl` is configured server-side.
- **Gmail back-fill:** on first connect, past emails with each contact back-fill onto the contact page.
- **Google Calendar pre-sync events** don't retroactively push to Google; you sync from Huly → Google for new events.
- **Disconnecting Google** does NOT delete already-synced events on either side.
- **TraceX / Recording / Live transcription** behaviors are out of CLI scope.

These are server-side plugin settings. The CLI doesn't expose them.

---

## Common task recipes

### "Triage my inbox"

```bash
# Count unread
huly notification unread-count

# See the unread items
huly notification list --unread --json \
  | jq -r '.[] | "[kind=\(.kind)] \(.object | tostring | .[0:40])…"'

# Mark all as read in one go
huly notification mark-all-read
```

### Hide a noisy DM

```bash
# List to get the DM ref
huly dm list --json

# Hide it from your sidebar (preserves history)
huly notification contexts hide <dm-ref>

# Bring back
huly notification contexts hide <dm-ref> --unhide
```

### Subscribe to receive notifications for a specific issue

```bash
huly notification subscribe --target TSK-1 --target-class tracker:class:Issue
```

Unsubscribe later:

```bash
huly notification unsubscribe --target TSK-1 --target-class tracker:class:Issue
```

### Set up an approval workflow for "merge PR after 2 reviews"

```bash
# 1. The PR is some kind of resource — for a tracker issue, attach the approval to it.
# 2. Build the tx that the approval will apply when approved
TX='{"_class":"core:class:TxUpdateDoc","objectId":"<issue-id>","objectClass":"tracker:class:Issue","space":"<issue-space>","operations":{"$set":{"status":"<closed-status-id>"}}}'

# 3. Create the request requiring 2 reviews
huly approval request \
  --attached-to TSK-42 \
  --attached-to-class tracker:class:Issue \
  --requested alice@example.com bob@example.com carol@example.com \
  --required-count 2 \
  --tx "$TX"

# Each reviewer approves:
huly approval approve <request-ref> --comment "+1"

# Auto-completes when count reached; server applies --tx.
```

### Reject an approval (with optional compensating tx)

```bash
huly approval reject <request-ref> \
  --comment "needs more info" \
  --rejected-tx '{"_class":"core:class:TxUpdateDoc",…}'
```

### Cancel a pending request (only requester)

```bash
# You can only cancel if you're in the requesterIds.
# The CLI checks this locally and refuses otherwise.
huly approval cancel <request-ref>
```

---

## Gotchas

- **Right-after-signup:** `notification settings update` may throw if `account.person` isn't provisioned yet. Re-login and retry.
- **`notification delete`** cascades — `notification:class:InboxNotification` rows pointing at the deleted ChatMessage / doc are removed. Reversible only by reactivating the source event.
- **`notification contexts pin / hide`** is per-user. Your setting doesn't affect anyone else.
- **Per-thread unsubscribe** is web UI only. Not exposed in CLI.
- **Approval `--tx`** is REQUIRED on create. The CLI does NOT validate the tx shape — that's the server's job. A malformed tx will surface as a `TxApplyIf` error at approval time.
- **CLI quirk:** if you forget `--tx`, the error message reads `missing --tx-json` (`resources/approvals.ts:178`). The real flag is `--tx`; `--tx-json` is a stale string in the error. Ignore the name and just add `--tx`.
- **Approval `cancel`** refused locally if you're not the requester. The server would refuse too, but the CLI fails fast.
- **Approval `--decision` on comment** is optional. Omit for plain comment; pass `--decision comment` for symmetry.
- **Approval `reject --comment` is REQUIRED.** A bare reject will throw Validation.
- **`mark-all-read` and `archive-all`** are non-destructive read actions in some sense, but `archive-all` requires `--yes` defensively.
- **Notification provider settings** are scoped per-user per-provider per-type. Disabling a type silences it for that provider; enabling re-enables.
- **`activity feed`** is the human-readable summary of `Tx` activity, with `IgnoreActivity`-mixin classes excluded. Useful for "what happened to this doc" queries.
- **Hover-peek in inbox** lets you preview without marking read. Web UI only.
