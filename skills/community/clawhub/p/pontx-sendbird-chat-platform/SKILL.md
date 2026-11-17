---
name: pontx-sendbird-chat-platform
description: Use for Sendbird Chat Platform API v3 server-side integration — users, group channels, open channels, messages, metadata, moderation, bots, announcements, and statistics — with caller-owned application credentials and preview-first mutation confirmation.
---

# Sendbird Chat Platform API v3

Start with live Pontx discovery rather than copying API fields into an
application. Use the universal CLI to resolve the current product, Endpoint,
Schema, and package guidance:

```bash
pontx-hub search "list group channels" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk sendbird-chat-platform
```

Use `@pontx/sendbird-chat-platform` in application code and
`pontx-sendbird-chat-platform` for an optional local script. The product is
the server-side Chat Platform API v3: users, group channels, open channels,
messages, metadata, moderation, bots, announcements, and statistics. It is a
caller-directed service — Pontx Hub does not proxy, cache, or aggregate
Sendbird application data.

## Caller-direct boundary and credentials

- The client connects directly to `https://api-{app_id}.sendbird.com`, where
  `app_id` is the caller's Sendbird application ID (set in the local
  environment as `SENDBIRD_APP_ID`).
- The generated SDK attaches the Application API Token as the `api-token`
  request header. Provide it via the `SENDBIRD_API_TOKEN` environment
  variable; never log, print, or commit it, and never put it in a request
  example.
- Credentials stay in the caller's local environment or browser session. Hub
  documentation pages do not store or forward them.

## Mutations are preview-first and explicitly confirmed

The Platform API is a management surface: creating users, sending messages,
inviting members, deleting channels, blocking users, and scheduling
announcements all change application state. Before executing:

1. Resolve the endpoint and its required path/body inputs.
2. Preview the exact request locally:

```bash
pnpm exec pontx-sendbird-chat-platform list apis
pnpm exec pontx-sendbird-chat-platform call <controller> <method> --dry-run
```

3. Review the rendered path, body, and side effects, and require the
   caller's explicit confirmation before sending.

## Read-only workflows

For reads (view a user, list channels, get a message, DAU/MAU statistics),
resolve the endpoint and pagination inputs first, then preview the exact
caller-directed request. Respect documented limits — a single user can join
up to 2,000 group channels, DAU/MAU metrics update on a fixed 30-minute
cadence, and the message migration feature is turned on through Sendbird
support. Treat an empty successful response as its own documented outcome.

## Contract provenance

Sendbird publishes no OpenAPI document; the contract is deterministically
reconstructed from the pinned official generated SDK. The official generated
SDK TypeScript package.json declares the Unlicense license. The Sendbird name
is used descriptively; this project is not affiliated with or endorsed by
Sendbird. Callers remain responsible for Sendbird terms and their own
data-compliance posture.

## Few-shot workflows

### Scenario 1: Read a user profile

**User:** "Look up a user in our Sendbird app."

**Approach:** confirm the app ID and token are set locally, discover the
current `users/viewAUser` endpoint, preview the request with a real
`user_id`, then execute and return the rendered user fields without
persisting upstream data in Hub.

### Scenario 2: Send a message to a group channel

**User:** "Send a message to our support group channel."

**Approach:** resolve `messages/sendAMessage` and its
`channel_type`/`channel_url`/body inputs, show a complete request preview
(path, body, `message_type`), and require the caller's explicit confirmation
before executing the mutation with their own credentials.

### Scenario 3: Clean up a test channel

**User:** "Delete one of our group channels to clean up a test app."

**Approach:** resolve `deleteAGroupChannel` with the `channel_url`, preview
the exact destructive request, and refuse to execute until the caller
explicitly confirms the removal.
