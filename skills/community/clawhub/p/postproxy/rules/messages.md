# Direct Messages

> 🔒 **Privacy.** DMs are private conversations with real people. Only read or send them when the user explicitly asks. Do not quote, forward, or summarize DM contents into public posts, other tools, or external services without the user's consent. Confirm recipient and message text before sending.

The Direct Messages API reads and sends 1:1 DMs. A **Chat** is a conversation between a profile and a participant; each chat holds inbound/outbound **Messages**. Outbound sends are processed **asynchronously** — `POST` returns `202 Accepted` with `status: "pending"`, then the message transitions to `published` (or `failed_waiting_for_retry` / `failed`).

## Platform Support

| Platform | Network ID |
|----------|------------|
| Facebook (Messenger) | `facebook` |
| Instagram (DMs) | `instagram` |
| Telegram (Bot DMs) | `telegram` |
| Bluesky | `bluesky` |

Using the DM API on any other platform returns `422 Unprocessable Entity`. Two important platform quirks:
- **Telegram**: no 24h window, but a bot can only DM a user **after that user has DM'd the bot at least once** (Telegram-enforced — sends to users who haven't initiated are rejected by the platform). No reactions, no private-reply, and `tag` is ignored. Telegram *does* support message editing and inline keyboards (`reply_markup`).
- **Bluesky**: text-only — no attachments, reactions, edits, or delivery/read receipts. Inbound messages arrive via a per-profile poller (every ~5 minutes), not a webhook. Supports archive/unarchive (maps to mute/unmute).

## Messaging Window
Meta (Facebook/Instagram) only permits free-form sends within **24 hours** of the participant's last inbound message. Outside that window, pass `tag: "HUMAN_AGENT"` (the only allowed tag). Telegram and Bluesky have no window and ignore `tag`.

## List Chats
Returns paginated chats for a profile, ordered by `last_message_at` descending.
```bash
curl -X GET "https://api.postproxy.dev/api/profiles/{profile_id}/chats?page=0&per_page=20" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Query parameters:
- `page` (optional): Page number, zero-indexed (default: `0`)
- `per_page` (optional): Items per page (default: `20`)
- `before` (optional): ISO 8601 — only chats with `last_message_at` before this
- `after` (optional): ISO 8601 — only chats with `last_message_at` after this

Response is `{ "total", "page", "per_page", "data": [...] }`.

## Create or Find Chat
Idempotently creates a chat for a `(profile, participant)` pair — returns the existing chat if one already exists (and updates any provided participant fields). Use this before sending to a participant the profile has not yet messaged. Returns `201` (created) or `200` (already existed).
```bash
curl -X POST "https://api.postproxy.dev/api/profiles/{profile_id}/chats" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "participant_external_id": "igsid_8675309",
    "participant_username": "jane_doe"
  }'
```

Parameters:
- `participant_external_id` (required): Platform participant ID (IG-scoped user ID for Instagram, PSID for Facebook Messenger)
- `participant_username` (optional): Display username
- `participant_name` (optional): Display name

## Get Chat
```bash
curl -X GET "https://api.postproxy.dev/api/chats/{chat_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

The `chat_id` can be a Postproxy hashid or the platform's `external_conversation_id`.

## List Messages
Returns paginated messages in a chat, ordered by `external_posted_at` descending (pending outbound messages are ordered by `created_at`).
```bash
curl -X GET "https://api.postproxy.dev/api/chats/{chat_id}/messages?page=0&per_page=20" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Query parameters:
- `page` (optional): Page number, zero-indexed (default: `0`)
- `per_page` (optional): Items per page (default: `20`)
- `direction` (optional): `inbound` or `outbound`
- `status` (optional): Filter by message status

## Send Message
Creates an outbound message and queues it for delivery. Returns `202 Accepted` with `status: "pending"`. Pass **either** `body` **or** a single `media` attachment, never both.
```bash
# Text reply (within the 24h window)
curl -X POST "https://api.postproxy.dev/api/chats/{chat_id}/messages" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "body": "Yes, we ship worldwide!" }'
```
```bash
# Send outside the 24h window (Meta) — requires a tag
curl -X POST "https://api.postproxy.dev/api/chats/{chat_id}/messages" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "body": "Following up on your order.", "tag": "HUMAN_AGENT" }'
```
```bash
# Send an image (multipart upload)
curl -X POST "https://api.postproxy.dev/api/chats/{chat_id}/messages" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -F "media[]=@./photo.png"
```

Parameters:
- `body` (conditional): Message text. Required when `media` is empty.
- `media` (conditional): Up to **one** attachment. Same shapes as the Posts API — multipart upload, public URL, base64 data URI, or base64 hash. More than one returns `422`.
- `tag` (optional): `HUMAN_AGENT` to send outside the Meta 24h window. Facebook/Instagram only — ignored on Telegram.
- `reply_to_external_id` (optional, **Telegram only**): Platform `message_id` to thread the reply under.
- `reply_markup` (optional, **Telegram only**): Telegram `reply_markup` payload (inline keyboard, custom reply keyboard, force-reply, or remove-keyboard).

## Get Message
```bash
curl -X GET "https://api.postproxy.dev/api/messages/{message_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

The `message_id` can be a Postproxy hashid or the platform's `external_id`.

## Edit Message
Edits a previously-sent outbound message on the platform. **Telegram only** (Meta does not expose outbound edits to bots — calling on a non-Telegram message returns `422`). At least one of `body` / `reply_markup` is required.
```bash
curl -X PATCH "https://api.postproxy.dev/api/messages/{message_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "body": "Updated answer: we ship to 90+ countries." }'
```

Parameters:
- `body` (conditional): New text. For media messages this becomes the new caption.
- `reply_markup` (conditional): New inline keyboard. Pass an empty `{}` to remove the existing keyboard.

## React to Message
Adds a reaction from your business account to a message. **Facebook Messenger and Instagram only.**
```bash
# Instagram — react with ❤️
curl -X POST "https://api.postproxy.dev/api/messages/{message_id}/react" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -d 'reaction=love' \
  -d 'emoji=❤️'

# Facebook Messenger — react by name (auto-translated to the emoji)
curl -X POST "https://api.postproxy.dev/api/messages/{message_id}/react" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -d 'reaction=smile'
```

Parameters:
- `reaction` (optional): Named reaction, defaults to `love`. Instagram accepts only `love`. On Facebook Messenger, named reactions are auto-translated to a unicode emoji before being sent to Meta.
- `emoji` (optional): Unicode emoji. On Messenger it overrides `reaction` as the literal value sent to Meta.

Messenger name → emoji translation: `love`→❤, `like`→👍, `dislike`→👎, `smile`→😆, `wow`→😮, `sad`→😢, `angry`→😡.

A second react from the same account **replaces** the previous reaction (Meta does not stack). Reactions not supported by the network return `422`.

## Remove Reaction
Removes the business account's reaction from a message.
```bash
curl -X DELETE "https://api.postproxy.dev/api/messages/{message_id}/unreact" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## Archive / Unarchive Chat
**Bluesky only** — maps to mute/unmute. Reflected in the chat's `metadata`.
```bash
curl -X POST "https://api.postproxy.dev/api/chats/{chat_id}/archive" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"

curl -X DELETE "https://api.postproxy.dev/api/chats/{chat_id}/archive" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## Private Reply to Comment
Sends a DM in reply to a comment (Instagram & Facebook). See [comments.md](comments.md) — `POST /api/posts/:post_id/comments/:id/private_reply`. It bypasses the 24h window, needs no existing chat, and is limited to one reply per comment.

## Message Statuses
- `pending` — outbound, queued, not yet delivered to the platform
- `published` — outbound, successfully delivered to the platform
- `failed_waiting_for_retry` — outbound send failed; will be retried with backoff
- `failed` — outbound send failed permanently (retries exhausted)
- `received` — inbound, received from the platform

## Chat Object Fields
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Chat hashid |
| `profile_id` | string | Profile hashid this chat belongs to |
| `platform` | string | Network ID (`facebook`, `instagram`, `telegram`, `bluesky`) |
| `participant_external_id` | string | Platform-native participant ID |
| `participant_username` / `participant_name` | string\|null | Participant identity (when known) |
| `participant_avatar_url` | string\|null | Stable storage URL of the participant's avatar (null until fetched) |
| `external_conversation_id` | string\|null | Platform's native conversation ID |
| `last_inbound_at` / `last_outbound_at` / `last_message_at` | string\|null | ISO 8601 timestamps |
| `metadata` | object\|null | Platform-specific metadata (e.g. follower signals; `muted`/`archived` state on Bluesky) |
| `created_at` | string | ISO 8601 |

## Message Object Fields
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Message hashid |
| `chat_id` | string | Parent chat hashid |
| `external_id` | string\|null | Platform-native message ID (null while pending) |
| `direction` | string | `inbound` or `outbound` |
| `body` | string | Message text |
| `status` | string | See Message Statuses |
| `tag` | string\|null | Tag used for sending outside the 24h window |
| `external_comment_id` | string\|null | Set when sent as a private reply to a comment |
| `error_message` | string\|null | Last platform error (when failed) |
| `platform_data` | object\|null | Platform-specific payload |
| `external_posted_at` | string\|null | Platform timestamp |
| `external_delivered_at` / `external_read_at` | string\|null | Delivery / read receipts (outbound; **Facebook & Instagram only**) |
| `external_edited_at` | string\|null | Timestamp of the latest platform-side edit |
| `external_deleted_at` | string\|null | Set when the message was deleted/unsent on the platform (treat as redacted) |
| `reply_to_external_id` | string\|null | Platform message ID this message replies to |
| `reply_markup` | object\|null | **Telegram only** — the attached keyboard payload |
| `reactions` | array | Live reactions; each entry has `sender_external_id`, `emoji`, `reaction`, `at` |
| `attachments` | array | Media on the message (see below) |
| `is_unsupported` | boolean | `true` when the platform flagged the message type as unsupported |
| `created_at` | string | ISO 8601 |

## Message Attachments
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Attachment hashid |
| `type` | string | `image`, `video`, `audio`, `sticker`, `file` |
| `url` | string\|null | Stable storage URL (may fall back to the source URL while `pending`) |
| `status` | string | `pending`, `processed`, `failed` |
| `external_id` | string\|null | Platform-side attachment ID (e.g. Messenger sticker ID) |

Inbound messages may carry both `body` and `attachments`; on outbound they are **mutually exclusive** (one attachment per send — Meta limitation). Bluesky carries no attachments.

## Webhook Events
Subscribe to message events via the [Webhooks API](webhooks.md). Event types:
- `message.received` — inbound message arrived
- `message.sent` — outbound message accepted by the platform
- `message.delivered` — delivery confirmed (sets `external_delivered_at`; **Facebook & Instagram only**)
- `message.read` — recipient read the message (sets `external_read_at`; **Facebook & Instagram only**)
- `message.edited` — message edited on the platform (Facebook, Instagram, Telegram)
- `message.deleted` — message deleted on the platform (sets `external_deleted_at`; **Instagram only**)
- `message.failed_waiting_for_retry` / `message.failed` — send failure events
- `reaction.received` — a reaction was added or removed; payload includes `action` (`react` | `unreact`), `emoji`, `reaction`, `sender_external_id`, and the post-mutation `message`
