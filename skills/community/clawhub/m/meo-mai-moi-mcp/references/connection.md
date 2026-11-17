# Connection and scope selection

## Endpoint and OAuth

Configure the remote Streamable HTTP endpoint:

```text
https://mcp.meo-mai-moi.com/mcp
```

Use the client's native OAuth action. A normal flow is: choose scopes, configure
the server, authenticate, sign in to Meo Mai Moi, approve scopes, confirm the
client can reach the server, ensure tools are projected into the current session,
then make the smallest useful call. The public health endpoint is
`https://mcp.meo-mai-moi.com/health`.

Codex, Cursor, OpenClaw, and other OAuth-capable MCP clients share the same
endpoint. Do not invent a local token or work around native OAuth.

When the user explicitly asks to connect or authorize Meo, prefer the client's
own MCP configuration surface and initiate OAuth on their behalf. Fall back to
user-run commands only when the client cannot modify its MCP configuration or
execution policy blocks the required command.

## Named presets

### Everyday care (default for broad requests)

Use when the user says “connect Meo Mai Moi,” “authorize Meo,” or “manage my
pets” without naming a narrower task or selecting Full management:

```text
pets:read pets:write health:read health:write habits:read habits:write microchips:read microchips:write
```

Covers ordinary pet profiles, health records, care habits, and microchips. It
does **not** authorize sharing, placement, helpers, messages, groups, finance,
notifications, profile, or invitations.

### Full management (explicit selection only)

Offer only after the user asks for complete access or clearly chooses this
preset. Before authorizing, state plainly that it permits sensitive reads and
writes across finances, messages, sharing, placement, groups, profile, and
invitations. Never select Full management by inference.

```text
pets:read health:read habits:read microchips:read pets:write health:write habits:write microchips:write sharing:read sharing:write placement:read placement:write helpers:read helpers:write messages:read messages:write groups:read groups:write finance:read finance:write notifications:read notifications:write profile:read profile:write invitations:read invitations:write
```

## Request scopes by task

When the user names a narrower task, request only that task's scopes—not a
preset.

| Task family | Start with |
|---|---|
| Pet profile, types, categories, photos, lifecycle | `pets:read` or `pets:read,pets:write` |
| Weights, vaccinations, medical records | `health:read` or `health:read,health:write` |
| Care routines | `habits:read` or `habits:read,habits:write` |
| Microchip identity | `microchips:read` or `microchips:read,microchips:write` |
| Sharing a pet | `sharing:read` or `sharing:read,sharing:write` |
| Rehoming, fostering, sitting, helpers | the relevant `placement:*` and/or `helpers:*` pair |
| Chats and messages | `messages:read` or `messages:read,messages:write` |
| Groups | `groups:read` or `groups:read,groups:write` |
| Ledgers, expenses, receipts | `finance:read` or `finance:read,finance:write` |
| Notifications | `notifications:read` or `notifications:read,notifications:write` |
| Own profile, locale, owner-weight history | `profile:read` or `profile:read,profile:write` |
| Account invitations | `invitations:read` or `invitations:read,invitations:write` |

Write tools require their matching read scope. A tool may require multiple
domain scopes; discover its schema before requesting extra consent.

When a later tool reports `insufficient_scope`, merge only the missing domain
pair and reauthorize unless the user explicitly switches preset.

## Readiness states

Do not treat these as one state:

1. **Configured** — server entry saved.
2. **OAuth success** — tokens exchanged.
3. **MCP probe success** — live reachability/auth check passed.
4. **Native tool projection** — Meo tools are callable in this session.

A successful probe does not prove the current chat can call Meo tools. An empty
or unrelated `tool_search` result does not prove the Meo server lacks tools.

## First-call pattern

For “show my pets,” connect with `pets:read` (or Everyday care when the request
was broad), confirm projection, discover tools, then call `list_pets` with `{}`.
Summarize only what the user needs.

For a requested change, first call the matching list/detail tool. Use the
returned stable ID and version, choose one new idempotency key, then read again
to verify.
