---
name: mdshare-agent
description: Create, read, unlock, update, and delete temporary Markdown shares through the MDShare service. Use when an agent needs to publish Markdown as a short-lived share link, fetch shared Markdown, access password-protected or burn-after-read content, continue editing with a manage or edit token, or hand back public/edit/manage links for collaboration. Triggers include “share this markdown”, “generate a temporary link”, “publish notes”, “read an MDShare link”, “update an existing share”, and “delete a temporary share”.
---

# MDShare Agent

Use MDShare as a lightweight anonymous Markdown publishing backend.

## Service

- Default base URL: `https://share.yekyos.com`
- If the caller provides another deployment, use that instead.
- Keep public links and token-bearing links separate:
  - Public link: `/s/{slug}`
  - Edit/manage page: `/e/{slug}#edit={token}` or `/e/{slug}#manage={token}`
- Never expose `ownerToken` or `editorToken` unless the user explicitly wants those links.

## Core Workflows

### Create a share

Send `POST /api/shares` with JSON:

```json
{
  "markdownContent": "# Title\n\nBody",
  "expiresInHours": 24,
  "password": "",
  "burnMode": "OFF",
  "editableMode": "READ_ONLY"
}
```

Rules:

- `expiresInHours` should normally be one of `1`, `24`, `168`, `720`.
- `burnMode` values:
  - `OFF`
  - `AFTER_FIRST_VIEW_GRACE`
  - `AFTER_FIRST_VIEW_INSTANT`
- `editableMode` values:
  - `READ_ONLY`
  - `EDIT_LINK`

Return these links to the user:

- Public: `{baseUrl}/s/{slug}`
- Manage: `{baseUrl}/e/{slug}#manage={ownerToken}`
- Edit: only if `editorToken` exists, `{baseUrl}/e/{slug}#edit={editorToken}`

Example using the default deployment:

- Public: `https://share.yekyos.com/s/abc123xy`
- Manage: `https://share.yekyos.com/e/abc123xy#manage=<ownerToken>`
- Edit: `https://share.yekyos.com/e/abc123xy#edit=<editorToken>`

### Read a public share

Call `GET /api/shares/{slug}/public`.

Possible states:

- `available`: content is returned
- `gated`: password and/or confirm-view is required
- `expired`
- `burned`
- `deleted`
- `not_found`

If the state is `gated`, ask for the password only when needed and explain burn-after-read before confirming access.

### Unlock a gated share

Send `POST /api/shares/{slug}/public` with JSON:

```json
{
  "password": "optional-password",
  "confirmView": true
}
```

Use `confirmView: true` when the service says burn confirmation is required.

### Read or edit through a token

Use header:

```text
x-share-token: <token>
```

Call `GET /api/shares/{slug}/manage` to inspect the current share and role.

### Save content

Send `PATCH /api/shares/{slug}/manage` with header `x-share-token` and JSON:

```json
{
  "markdownContent": "# Updated\n\nContent",
  "lastKnownUpdatedAt": "2026-03-12T00:00:00.000Z",
  "force": false
}
```

If the API returns `409` with `conflict: true`, do not overwrite silently. Summarize the conflict and ask whether to force-save.

### Update settings

Owner token only. Send `PATCH /api/shares/{slug}/settings` with JSON:

```json
{
  "expiresInHours": 168,
  "password": "",
  "burnMode": "OFF",
  "editableMode": "READ_ONLY"
}
```

If the response includes a new `editorToken`, regenerate the edit link.

### Delete a share

Owner token only. Call `DELETE /api/shares/{slug}/manage` with `x-share-token`.

## Behavior Guidance

- Prefer simple defaults:
  - `expiresInHours: 168`
  - `burnMode: OFF`
  - `editableMode: READ_ONLY`
- Treat password as optional. Empty string means no password.
- Preserve user Markdown exactly unless they explicitly ask for formatting or cleanup.
- When the user only wants a formatting preview, do not create a share link unless they ask.
- For sensitive content, remind the user that anyone with a manage link can modify or delete the share.

## Reference

- For endpoint details and payload shapes, read [references/api.md](references/api.md).
- For end-to-end agent flows, read [references/workflows.md](references/workflows.md).
- For install and invocation examples, read [references/install-examples.md](references/install-examples.md).
