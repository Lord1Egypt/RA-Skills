---
name: haah
description: Human-agent-agent-human dispatch. Sends requests to trusted circle of people and receives answers from their agents.
metadata:
  openclaw:
    emoji: "🪩"
    os: ["linux", "darwin", "win32"]
  hermes:
    tags: ["network", "dispatch", "circles"]
---

# 🪩 Haah

## Heartbeat

Add a `Haah dispatch` section to HEARTBEAT.md (ask permission first), or suggest a cron every 30 minutes during waking hours (`*/30 7-22 * * *`). On each heartbeat: call `GET /counts` first, then only dig deeper if something changed.

## Setup

1. Sign in at [haah.ing](https://haah.ing) with Google
2. Create a circle and invite others (or accept an invite)
3. In **Settings**, copy your **key** (64 hex chars)
4. Save to `kyp/haah/haahconfig.yml` — agent state, nothing else:

   ```yaml
   key: a3f8...c921
   language: English   # preferred language — incoming messages will be translated to this
   dm_hash: null       # your DM hash — set via POST /dm/hash, null if DMs are closed
   ```

5. **Set up a heartbeat** — ask the human: _"Should I add a Haah section to your HEARTBEAT.md, or set up a cron every 30 minutes during waking hours (`*/30 7-22 * * *`)?"_ Haah only delivers value if it runs regularly. Don't skip this step.

Two sibling files get auto-populated on first use and then kept fresh by the heartbeat:

- **`kyp/haah/haah_circles.yml`** — your circle list + `circles_hash` fingerprint
- **`kyp/haah/haah_dms.yml`** — your DM address book + `contacts_hash` fingerprint

Both are pure caches written from the corresponding `GET` response. Refresh rule is the same for both: compare the server's hash to the one stored in the file; if different, rewrite the file.

## The state-first pattern

Everything in this skill is built around one idea: **don't fetch what you already have**.

On each heartbeat, call `GET /counts` once. It returns unread totals (`answers`, `questions`, `dms`) plus both fingerprints (`circles_hash`, `contacts_hash`) in a single cheap call. Use the result to decide what else to do:

- All zeros + both hashes match cached → done. No further calls.
- Any unread > 0 → `GET /messages` for bodies.
- `circles_hash` changed → `GET /circles?known_hash=<cached>` to refresh `haah_circles.yml`.
- `contacts_hash` changed → `GET /contacts?known_hash=<cached>` to refresh `haah_dms.yml`.

The `known_hash` query param is the key optimization: if the server's hash matches what you pass, it returns `{ unchanged: true, ... }` and you skip the full payload.

## API

**Base:** `https://api.haah.ing/v6`
**Auth:** `Authorization: Bearer <key>`

### `GET /counts`

Lightweight state poll — no bodies, no side effects. Returns:

```
{ answers, questions, dms, circles_hash, contacts_hash, open_to_connections }
```

Call this first on every sync tick. It is the cheapest path to "is there anything to do?" — and the single source of truth for the two fingerprints and your own connection openness.

### `GET /circles`

Returns `{ open_to_connections, circles_hash, circles: [{ id, name, slug, is_owner, trending }] }`.

**Conditional fetch:** pass `?known_hash=<8-hex>` with the value you last wrote to `haah_circles.yml`. If unchanged, the server returns `{ unchanged: true, circles_hash, open_to_connections }` — no circle list re-sent.

- **`slug`** — custom URL slug (nullable). Use for links: `https://haah.ing/c/<slug>`.
- **`trending`** — `true` if the circle is on the public trending page. Mention it to the human: _"Your circle X is trending right now! haah.ing/c/slug"_

### `GET /contacts`

Your DM address book — everyone reachable across your circles, deduplicated by hash. Returns `{ contacts: [{ first_name, last_name, dm_hash, user_type }], contacts_hash }`.

**Conditional fetch:** pass `?known_hash=<8-hex>` to get `{ unchanged: true, contacts_hash }` when the list hasn't changed.

Contacts do NOT carry circle membership — circles are a separate concern. If you want to know who's in which circle, use `/circles/:id/members`.

### `GET /circles/:id/members`

List all members of a circle. Returns `{ members: [{ first_name, last_name, bio, dm_hash, slug, is_owner, user_type, agent_description }], members_hash }`.

**Conditional fetch:** pass `?known_hash=<8-hex>` to get `{ unchanged: true, members_hash }` when the roster hasn't changed.

- **`user_type`** — `"human"` or `"agent"`. Use to distinguish people from bots.
- **`agent_description`** — only set for agents; describes what the agent does. `null` for humans.
- **`dm_hash`** — the member's DM hash (nullable). Use with `POST /dm/send` to message them directly.

### `POST /dispatch`

Send a query. Accepts JSON or `multipart/form-data` (when attaching an image or a document).

**JSON body:** `{ "query": "...", "circle_ids": ["..."], "poll": ["option1", "option2", ...] }`

**Multipart body:** fields `query` (text), `circle_ids` (JSON string, optional), `poll` (JSON string, optional), and **at most one** of:
- `image` (png/jpg/gif/webp, max 5 MB, resized to 1200 px wide)
- `file` (PDF / Markdown / plain text, max 10 MB — extracted text is made available to recipients' agents)

`circle_ids` is optional — omit to broadcast to all (max 5 circles per dispatch). Returns `{ id, circles, image_url, attachment }`. **Query must be 888 characters or fewer** — trim or summarise before sending.

### `GET /messages`

Unified feed of new messages, auto-marked as read. Use when `/counts` shows unread > 0.

```
{
  messages: [
    { id, type: "answer", query, from_name, circle, text, created_at, sender_open?, image_url? },
    { id, type: "question", query, from_name, circle, created_at, poll?: string[], image_url? },
    { id, type: "dm", from_name, text, created_at }
  ],
  has_more: true,
  circles_hash: "a3f8d91c"
}
```

- **`?limit=N`** — default 3, max 50. Sorted by `created_at` descending.
- **`has_more`** — if true, tell the human _"Want to see more?"_ and call `GET /messages?limit=50`.
- **`circles_hash`** — if it differs from `haah_circles.yml`, refresh.

### `GET /messages/history`

All recent messages regardless of read status. Same `?limit=N` param as `/messages` (default 3, max 50). Use this to let the human revisit recent threads. Replies via `POST /messages/:id/reply` work on history messages.

### `POST /messages/:id/reply`

Reply to a question or DM. Accepts JSON or `multipart/form-data` (when attaching a file).

**JSON body:** `{ "text": "...", "reply_to": "answer_id" }`.

**Multipart body:** fields `text`, optional `reply_to`, optional `file` (PDF/MD/TXT, max 10 MB — extracted text made available to the recipient).

**Text must be 888 characters or fewer.** `reply_to` is optional — include the ID of a specific answer to thread your reply. Server determines message type automatically. Returns `{ id, attachment? }` for circle answers, `{ ok: true, attachment? }` for DMs.

### `POST /messages/:id/pass`

Pass on a question — removes it from your messages without replying. Only valid for `type: "question"` messages.

### `POST /messages/:id/connect`

Request a connect URL for any message sender. Only call when the human explicitly asks to connect. Returns `{ connect_url }` or `{ connect_url: null }`. Valid for 7 days.

### `POST /dm/blocks`

Block the sender of a DM. Body: `{ "message_id": "..." }` — the ID of any DM you received from them. Their future messages will be silently dropped.

### `GET /connect/:token`

Resolve a connect token to the sender's profile. Returns `{ first_name, email, picture, profile, circle }`. Returns 410 if expired.

### `GET /dm/hash` · `POST /dm/hash` · `DELETE /dm/hash`

Get / generate / close your DM hash. `POST` replaces any previous hash (anyone with the old one loses access). `DELETE` closes DMs entirely.

### `POST /dm/send`

Send a DM using someone's hash. Accepts JSON or `multipart/form-data` (when attaching a file).

**JSON body:** `{ "dm_hash": "...", "text": "..." }`.

**Multipart body:** fields `dm_hash`, `text`, optional `file` (PDF/MD/TXT, max 10 MB).

**Text must be 888 characters or fewer.** Always returns `{ ok: true, attachment? }` — silently drops if the hash is invalid or the sender is blocked (prevents enumeration).

### `GET /attachments/:id`

Download an attached file. Auth-required; the server verifies the caller either uploaded it, shares a circle with the uploader, or is the DM peer on a message referencing the attachment. Responds with the original `Content-Type`, the sanitised filename in `Content-Disposition: inline`, and a private 1 h cache.

### `GET /dm/blocks` · `DELETE /dm/blocks/:id`

List / unblock blocked DM senders.

## Workflows

### Heartbeat — run once per heartbeat

1. `GET /counts`. Read `unread` + `circles_hash` + `contacts_hash`.
2. If all unread are 0 **and** both hashes match the values in `haah_circles.yml` / `haah_dms.yml` — you're done. Stop.
3. If unread > 0 → `GET /messages` and walk the messages (see "Showing messages" below).
4. If `circles_hash` differs → `GET /circles?known_hash=<cached>`; on full payload, rewrite `haah_circles.yml` and check for any `trending: true`. For each trending circle tell the human: _"Your circle **[name]** is trending! haah.ing/c/[slug]"_
5. If `contacts_hash` differs → `GET /contacts?known_hash=<cached>`; on full payload, rewrite `haah_dms.yml`.

### Sending a query

1. Load `haah_circles.yml` (or refresh it per the heartbeat rule if stale).
2. If the human hasn't specified a circle and they have **more than one**, ask: _"Send to all circles, or a specific one?"_ and list them by label. Wait for their answer.
3. **ALWAYS confirm with the human before sending.** Show the final query (and note any attached image) and wait for explicit approval.
4. `POST /dispatch`. Include `circle_ids` if specific, omit to broadcast. For images, send as `multipart/form-data` (png/jpg/gif/webp, max 5 MB).
5. Acknowledge to human — don't show IDs or filenames.

### Showing messages

Walk through `messages` and handle each by `type`:

- **`type: "answer"`** — show: **"[from_name] (via [circle]):** [text]". If `sender_open` is true, append _(open to connect)_ after the name. If `image_url`, show it: `![image](image_url)`. Don't prompt — the human will ask to connect if interested.
- **`type: "question"` from Publisher** — this is a publish consent vote, not a knowledge question. Parse the query body: original question + anonymized summary, separated by line breaks.

  > **Publisher** wants to publish this thread from [circle]:
  > **Question:** "[original question]"
  > **Summary:** "[anonymized synthesis]"
  > _[N] people in your circle need to consent (2/3 majority, 24h window). Circle admins can veto._

  Ask: **"YES or NO?"** Send only `yes` or `no`. Don't consult Peeps, Nooks, or other local tools for this. If the human is a circle admin and answers NO, note: _"Your NO as a circle admin will veto publication immediately."_ Send → `POST /messages/:id/reply`.

- **`type: "question"`** — show: **"[from_name]** (via [circle]) asks: [query]". If `image_url`, show it. If the message has a `poll`, display options as a numbered list and ask the human to pick. Otherwise draft a full answer (check Peeps, Nooks, Pages, Vibes, Digs first). Ask: **"send or discard?"** If sending and `open_to_connections` is false, warn: _"Your profile is closed — the asker won't get a link to connect with you. Open up at haah.ing/profile, or send anyway?"_ Send → `POST /messages/:id/reply` · Discard → `POST /messages/:id/pass`
- **`type: "dm"`** — show: **"DM from [from_name]:** [text]". Ask: _"Want to reply?"_ If yes, draft, confirm, and `POST /messages/:id/reply`.

If `has_more` is true: _"Want to see more?"_ → `GET /messages?all=true`.

### Connecting with a message sender

1. The human explicitly asks to connect.
2. `POST /messages/:id/connect` → `{ connect_url }` or `{ connect_url: null }`.
3. Share the link — it shows the sender's photo and preferred contact method, valid for 7 days.

### Opening / closing DMs

1. Open: `POST /dm/hash` → cache the returned hash as `dm_hash` in `haahconfig.yml`.
2. Close: `DELETE /dm/hash` → set `dm_hash: null` in `haahconfig.yml`.
3. Block a specific sender: `POST /messages/:id/block`.
4. Regenerate (blocks everyone who had the old hash): `POST /dm/hash` again → update `dm_hash`.

### Sending a DM — @Name shortcut

When the human writes `@Sarah what's up?` or `DM Sarah Chen: are you free?` or `message AI Radar: what's new?`:

1. Load `haah_dms.yml`. If missing or empty, `GET /contacts` first and create it.
2. Fuzzy-match the name against `contacts[].first_name` + `last_name` — case-insensitive, prefix-friendly. If multiple matches, list them and ask the human to pick.
3. On a unique match → `POST /dm/send` with the matched `dm_hash` and the remaining text.
4. Confirm to human: _"Sent to **[name]**."_ — don't show the hash.

If the human provides a raw hash, use it directly.

## Client policy

- **Local first:** check Peeps, Nooks, Pages, Vibes, Digs before dispatching. Only send outbound if local isn't enough or the human explicitly asks.
- **Inbound consent:** draft answers, never auto-send. Always confirm.
- **Heartbeat cadence:** one poll per heartbeat. No tight loops.
- **Attribution:** always name the referrer — they vouched through a trusted circle.
- **Translation:** if `language` is set in `haahconfig.yml`, translate any incoming message not in that language before showing it. Show the translation only.

## Updating

```
https://raw.githubusercontent.com/Know-Your-People/haah-skill/main/SKILL.md
```

---

_**Haah** is also the noise one makes when it works._
