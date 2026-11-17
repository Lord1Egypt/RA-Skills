# Channels, DMs, threads, activity

The chat surface. All chat lives under `chunter:space:Chunter`. Three flavors:

- **Channels** — group conversations, listed in the sidebar.
- **DMs** — direct or group, hidden from sidebar.
- **Threads** — replies to a message (channel or DM).

Plus the cross-cutting **Activity** surface: reactions, pins, saved messages, mentions, replies to activity items.

---

## Decision: Channel vs DM vs Thread vs Comment

| Use                              | When                                                                       |
| -------------------------------- | -------------------------------------------------------------------------- |
| `huly channel message send`      | Public/semi-public team discussion; channel visible in sidebar             |
| `huly dm send --person <email>`  | 1:1 or small group conversation; should NOT appear in the channel sidebar  |
| `huly thread add`                | Reply to an existing message (channel or DM)                               |
| `huly comment add --issue <ref>` | Top-level comment on a tracker issue (these are ChatMessages on the issue) |

Use DMs for hidden conversations. Private channels still appear in the sidebar (users must request access); only DMs/close-conversation hide from it.

---

## People: resolving `--person`, `--members`, `--assignee`

The resolver is strict — substring fallback is NOT used here (unlike `--assignee`):

```bash
# Exact email match
huly dm create --person alice@example.com
huly channel create --name "engineering" --members alice@example.com bob@example.com

# Exact UUID match
huly dm create --member <uuid>

# "me" or "" → current user
huly channel join <ref>               # defaults to current user
huly channel leave <ref> --member alice@example.com   # override to someone else
```

Resolution order (`resolvePersonId` in `resources/channel.ts:61-130`):

1. **Workspace-local Person scan** — `findAll('contact:class:Person', {}, { limit: 200 })`. Exact case-insensitive match on email OR name.
2. **Account service fallback** — `accountClient.findPersonBySocialKey(email)` for cross-workspace; `findPersonBySocialId(socialId, true)` creates the Person if missing.
3. Otherwise throw `NotFound` with a hint.

**No fuzzy matching.** If the user passes `bob` and there is no person whose name or email is exactly `bob` (case-insensitive), the CLI throws `NotFound`. If multiple persons match exactly (e.g. two people both literally named "Bob"), the **first** one in the `findAll()` result order wins — the CLI does NOT throw and does NOT sort. Pass a full email to disambiguate.

---

## Channel commands

### Discover

```bash
huly channel list --json
huly channel list --archived --json               # only archived
huly channel list --archived false --json         # only non-archived (anything not "false"/"0" counts as true)
huly channel get "engineering" --json
huly channel get <ref> --json                     # by ref
huly channel members engineering --json | jq -r '.[] | .uuid'
huly channel message list engineering --json | jq -r '.[].message'
```

### Create / configure

```bash
huly channel create \
  --name "engineering" \
  --description "…" \
  --topic "Engineering topics" \
  --private false \
  --auto-join false \
  --members alice@example.com bob@example.com
```

**Auto-applied:**

- The current user is ALWAYS added to `members` first (prepended) and to `owners`. Cannot skip.
- `autoJoin: false` and `autoJoinForRoles: []` by default.
- `archived: false`.

**`--private` channels** still appear in the sidebar — users must request access. They're not "hidden". Use DMs for hidden.

**`--auto-join`** only affects FUTURE workspace members; existing members are not retroactively added.

### Archive / unarchive

```bash
huly channel archive "engineering"
huly channel archive "engineering" --value false  # unarchive
huly channel unarchive "engineering"              # alias for archive --value false
```

**`#general` and `#random`** require **Spaces Admin** or **Workspace Owner** to archive. The CLI does NOT pre-check this — the server rejects. If you get a 403, switch workspaces or ask for an admin role.

### Membership

```bash
huly channel join engineering                       # joins current user
huly channel join engineering --member alice@example.com
huly channel leave engineering
huly channel leave engineering --member alice@example.com
huly channel add-member engineering --members alice@example.com bob@example.com
huly channel remove-member engineering --members alice@example.com
```

`--member <email>` defaults to current user. `add-member` and `remove-member` both require `--members <email...>` (variadic; `--member` singular is for `join`/`leave`).

### Delete

```bash
huly channel delete engineering                  # no --yes
huly channel delete engineering random --yes     # multiple, REQUIRED --yes
```

Cascade: server removes chat message collections.

---

## Channel messages

```bash
huly channel message list engineering --json
huly channel message send engineering --body "Standup at 10"
huly channel message send engineering --body-file ./announcement.md
huly channel message send engineering --body "Hi @alice"               # @mention parsed
huly channel message update engineering <msg-id> --body "edited"
huly channel message delete engineering <msg-id>                      # no --yes
huly channel message delete engineering <m1> <m2> --yes               # REQUIRED --yes
```

### The "no channel message get" gotcha

There is intentionally **NO** `huly channel message get <id>`. The CLI exposed `list` only. To fetch a single message:

```bash
huly channel message list engineering --json \
  | jq '.[] | select(._id == "chunter:class:ChatMessage:<id>")'
```

### Side effects on `message send` (server-side)

The CLI just calls `addCollection`. Server-side behavior (NOT done by the CLI):

- **Auto-adds sender to `channel.members`** if not already a member. The CLI itself does NOT `$push` the sender; if the platform doesn't add them either, the send will fail for non-members.
- **Every `@name` in body** is parsed via `extractReferences`. Each mentioned Person is:
  - Added as `core:class:Collaborator` on the channel
  - Sent an inbox notification (subject to their `notification:class:NotificationTypeSetting`)
- Each collaborator receives an inbox notification for the message.

### `@mention` resolution

- `@alice` looks up by display name in the workspace. Multiple matches → server behavior.
- `@alice@example.com` matches by exact email.
- The CLI does not pre-process mentions — the server does. So `huly channel message send --body "hi @alice"` is sufficient; you don't escape or annotate.

---

## DMs

```bash
huly dm list --json
huly dm create --person alice@example.com
huly dm create --members alice@example.com bob@example.com   # group DM
huly dm message list <dm-ref> --json
huly dm messages <dm-ref> --json                  # deprecated alias of message list
huly dm send <dm-ref> --body "Hi"                 # deprecated alias of message send
huly dm message send <dm-ref> --body "Hi"
huly dm message send --person alice@example.com --body "Hi"   # AUTO-CREATES the DM
```

**Aliases:** `huly dm messages <dm>` is the deprecated alias for `huly dm message list <dm>`; `huly dm send <dm>` is the alias for `huly dm message send <dm>`. They invoke the same handlers. Use the canonical form.

**Auto-creation:** passing `--person` to `dm send` _creates a new_ `DirectMessage` doc. The CLI does NOT check whether a DM with that person already exists — it calls `createDoc(DM_CLASS, …)` unconditionally. Repeated calls produce duplicate DMs (one per call). To avoid duplicates, run `huly dm list --json` first. **No `--yes` required for DM creation.**

### "Close conversation" mechanism

There is no `huly dm close` command. The mechanism is the **notification context**: each DM has a per-user `notification:class:DocNotifyContext` that can be hidden:

```bash
huly notification contexts hide <dm-ref>          # hides from YOUR sidebar
huly notification contexts hide <dm-ref> --unhide  # shows again
huly notification contexts pin <dm-ref>           # pin
huly notification contexts pin <dm-ref> --unpin
```

Hidden = hides from sidebar. Message history preserved. To unhide, the inverse flag (`--unhide`).

---

## Threads (replies to a chat message)

```bash
huly thread list <parent-msg-id> --json
huly thread list <parent-msg-id> --limit 50 --offset 0 --json
huly thread add <parent-msg-id> --body "thoughts?"
huly thread update <reply-id> --body "edited"
huly thread delete <reply-id>
huly thread delete <r1> <r2> --yes
```

A thread reply is a `chunter:class:ThreadMessage` with `attachedTo = <parent-msg-id>`, `attachedToClass = chunter:class:ChatMessage`, `collection = 'replies'`.

**Server-side cascade:**

- Author pushed into parent's `repliedPersons[]`.
- Parent's `lastReply` updated.
- Inbox notifications sent to all collaborators + every `@mention` in the reply body.
- **Telegram replies to a Huly notification** appear here as ThreadMessage rows.

---

## Comments on issues

```bash
huly comment list --issue TSK-1 --json
huly comment add --issue TSK-1 --body "Looking into this"
huly comment add --issue TSK-1 --body-file ./note.md
huly comment update <comment-ref> --body "Updated text"
huly comment delete <comment-ref>             # no --yes
huly comment delete <c1> <c2> --yes          # REQUIRED --yes
```

Issue comments are `ChatMessage` rows in the issue's `comments` collection. Same mention/notification rules as channel messages. Delete cascades `notification:class:InboxNotification` rows.

---

## Activity (cross-cutting)

ActivityMessages are the universal "what happened on this doc" feed. They are emitted automatically on many operations (issue status change, comment add, etc.). The activity namespace gives you low-level access to them.

```bash
huly activity list --json
huly activity list --target <doc-ref> --json
huly activity list --target <doc-ref> --target-class tracker:class:Issue --json
huly activity list --pinned --json

huly activity get <activity-id> --json
huly activity pin <activity-id>                          # pins
huly activity pin <activity-id> --unpin                 # unpins

huly activity react --target <msg-id> --emoji 🎉                # adds reaction
huly activity react --target <msg-id> --emoji 🎉 --remove       # removes yours
huly activity react --target <msg-id> --emoji 🎉 --list         # list reactions

huly activity reply list <activity-id> --json
huly activity reply add <activity-id> --body "reply"
huly activity reply update <reply-id> --body "edited"
huly activity reply delete <reply-id>                      # no --yes
huly activity reply delete <r1> <r2> --yes                 # REQUIRED --yes

huly activity saved list --json
huly activity saved save --target <activity-id>
huly activity saved unsave --target <activity-id>

huly activity mentions --json
```

### Reactions, saved, mentions quirks

- **`react --remove`** filters by `createBy = account.primarySocialId` so it only removes YOUR reactions. You cannot remove someone else's reaction via CLI.
- **`saved save`** does NOT dedupe — calling twice creates two SavedMessage rows pointing at the same target.
- **`saved list`** is filtered by `modifiedBy = <current-user-uuid>` to avoid leaking other users' bookmarks (the SavedMessage class extends Preference, which has no per-user security filter built in).
- **`mentions`** has a fallback when `account.person === undefined` (right after signup) — it scans by UUID instead of by Person ref. Without this guard, undefined keys would be silently stripped and the query would match every Person's mentions.

---

## Per-thread unsubscribe (NOT exposed)

The web UI offers a per-thread unsubscribe (three-dot → unsubscribe). **The CLI does NOT expose this.** If the user wants to unsubscribe from a noisy thread, fall back to web UI or update the `DocNotifyContext.hidden` flag via raw RPC.

---

## Common task recipes

### Post a standup message with mentions

```bash
huly channel message send "standup" --body "Yesterday:
$(huly issue list --status Done --json | jq -r '.[].identifier')

Today: $PLAN

cc: @alice @bob"
# @ mentions auto-resolve server-side; recipients get inbox notifications.
```

### Send someone a DM (auto-creates a new DM)

```bash
# Creates a NEW DM doc with alice — does NOT detect or reuse an existing DM.
# To avoid duplicates, run `huly dm list --json` first.
huly dm send --person alice@example.com --body "ping"
# Subsequent sends should reuse the same dm-ref from the response:
huly dm send <dm-ref> --body "follow-up"
```

### List all unread notifications for the user (the inbox)

```bash
huly notification list --unread --json
```

### React to your own message (or anyone's)

```bash
huly activity react --target <msg-id> --emoji 👍
```

### Close a noisy DM without deleting history

```bash
huly notification contexts hide <dm-ref>
# To bring it back:
huly notification contexts hide <dm-ref> --unhide
```

### Migrate channel messages to a thread (or pull replies into a topic)

There is no CLI helper. If the user wants this:

- Use `huly channel message list ...` and `huly thread add ...` manually.
- Or use the web UI.

---

## Gotchas

- **`channel message get` doesn't exist.** Use `list --json | jq`.
- **Sending on a channel where you've been removed** still works (the server auto-adds the sender). But sending on a channel you've been `remove-member`-d from in a way that doesn't auto-rejoin depends on server config — if it fails, ask for explicit re-add.
- **Notifications cascade from messages, not from `huly channel …` get calls.** So a `channel get` doesn't mark anything as read.
- **`--archived` for channels** uses non-strict coercion: `--archived 0` and `--archived false` both mean "non-archived"; any other string is "archived". Use exact values.
- **`reaction --remove` removes only YOUR reactions.** If the user wants to remove someone else's reaction (e.g. moderation), this is not exposed.
- **`saved save` is not idempotent.** Don't double-call.
- **Telegram → Huly replies** appear in `huly thread list <parent-id> --json`. They look identical to user-written replies.
- **Per-thread unsubscribe** is web UI only.
- **`Comment add --issue X --body "@mention"`** fires the same cascade as channel messages — author auto-added as collaborator, mentions get notifications.
- **Inline comments on documents** (NOT issue comments) are NOT shown in any of these surfaces. They're document-scoped and isolated from notifications. See `references/documents.md`.
