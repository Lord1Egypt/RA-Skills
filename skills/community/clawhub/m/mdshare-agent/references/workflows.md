# MDShare Agent Workflows

Use these flows when the caller wants the agent to operate MDShare directly instead of just describing the API.

## Workflow 1: Create a temporary share and return links

Use when the user says things like:

- “帮我把这份 Markdown 发成临时链接”
- “share this note”
- “generate a temporary markdown link”

Steps:

1. Collect the Markdown exactly as provided.
2. Unless the user specifies otherwise, use:
   - `expiresInHours: 168`
   - `burnMode: OFF`
   - `editableMode: READ_ONLY`
   - empty password
3. Call `POST /api/shares`.
4. Return:
   - public link
   - manage link
   - edit link only if `editorToken` exists
5. Briefly explain the difference between public and manage links.

Suggested reply shape:

```text
分享已创建。
公开访问：https://share.yekyos.com/s/{slug}
管理链接：https://share.yekyos.com/e/{slug}#manage={ownerToken}
```

Only include the edit link when editing is enabled.

## Workflow 2: Read a protected share

Use when the user gives an MDShare public link and asks to read or summarize it.

Steps:

1. Extract `{slug}` from `/s/{slug}`.
2. Call `GET /api/shares/{slug}/public`.
3. If state is `available`, use the content directly.
4. If state is `gated`:
   - ask for a password only when `passwordRequired` is true
   - mention burn-after-read before using `confirmView: true`
5. Call `POST /api/shares/{slug}/public` with the required fields.
6. Continue only after the API returns `available`.

Guardrails:

- Do not assume a password.
- Do not auto-confirm burn-after-read unless the user clearly wants to proceed.
- If the API returns `expired`, `burned`, `deleted`, or `not_found`, report that state plainly.

## Workflow 3: Update an existing share through a token

Use when the user provides a manage link or edit link and wants to continue editing.

Steps:

1. Extract:
   - `slug` from `/e/{slug}`
   - token from `#manage=...` or `#edit=...`
2. Call `GET /api/shares/{slug}/manage` with `x-share-token`.
3. Present the current role:
   - `owner`
   - `editor`
4. When saving new Markdown, send `PATCH /api/shares/{slug}/manage` with:
   - `markdownContent`
   - `lastKnownUpdatedAt`
   - `force: false`
5. If the API returns `409` and `conflict: true`, summarize the remote update and ask whether to force overwrite.
6. Only use `force: true` after explicit confirmation.

Guardrails:

- `editor` can edit content but not settings.
- `owner` can edit content, change settings, and delete the share.

## Workflow 4: Change expiry, password, or editability

Use when the user provides a manage link and asks to:

- extend expiry
- add/remove password
- enable/disable edit link
- change burn-after-read behavior

Steps:

1. Extract `slug` and owner token.
2. Call `PATCH /api/shares/{slug}/settings`.
3. Preserve unspecified settings when possible by reading current state first.
4. If a new `editorToken` is returned, regenerate the edit link and return it.

## Workflow 5: Delete a share

Use when the user wants a share permanently disabled.

Steps:

1. Require the manage link or owner token.
2. Confirm intent when the user has not already been explicit.
3. Call `DELETE /api/shares/{slug}/manage`.
4. Report success only after `{ "success": true }`.

## Workflow 6: Use MDShare as a formatting helper

Use when the user wants formatted Markdown output but does not necessarily want a share link.

Steps:

1. Do not call the API by default.
2. Render or transform Markdown locally when the task is just formatting, preview, or conversion.
3. Only create a share if the user explicitly asks to publish or share it.

This keeps MDShare positioned as a lightweight sharing backend rather than forcing publication for every Markdown task.
