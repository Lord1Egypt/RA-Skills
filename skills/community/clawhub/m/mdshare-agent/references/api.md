# MDShare API Reference

Base URL example: `https://share.yekyos.com`

## `POST /api/shares`

Create a share.

Request body:

```json
{
  "markdownContent": "string, required",
  "expiresInHours": "number, optional",
  "password": "string, optional",
  "burnMode": "OFF | AFTER_FIRST_VIEW_GRACE | AFTER_FIRST_VIEW_INSTANT",
  "editableMode": "READ_ONLY | EDIT_LINK"
}
```

Success response:

```json
{
  "share": {
    "slug": "string",
    "markdownContent": "string",
    "expiresAt": "ISO string",
    "createdAt": "ISO string",
    "updatedAt": "ISO string",
    "editableMode": "READ_ONLY | EDIT_LINK",
    "burnMode": "OFF | AFTER_FIRST_VIEW_GRACE | AFTER_FIRST_VIEW_INSTANT",
    "firstViewedAt": "ISO string | null",
    "burnDeadline": "ISO string | null",
    "deletedAt": "ISO string | null",
    "burnedAt": "ISO string | null",
    "statusLabel": "string",
    "expiresAtLabel": "string"
  },
  "ownerToken": "string",
  "editorToken": "string | null"
}
```

## `GET /api/shares/{slug}/public`

Read public state.

Response states:

- `available`
- `gated`
- `expired`
- `burned`
- `deleted`
- `not_found`

`available` response includes `share.markdownContent`.

`gated` response shape:

```json
{
  "state": "gated",
  "passwordRequired": true,
  "burnConfirmationRequired": false,
  "share": {
    "expiresAt": "ISO string",
    "burnMode": "string"
  }
}
```

## `POST /api/shares/{slug}/public`

Unlock gated content.

Request body:

```json
{
  "password": "string, optional",
  "confirmView": "boolean, optional"
}
```

Response:

- `200` for `available`
- `404` for `not_found`
- `410` for `expired`, `burned`, or `deleted`
- `400` for wrong password or invalid request

## `GET /api/shares/{slug}/manage`

Read manage/edit payload.

Required header:

```text
x-share-token: <token>
```

Success response:

```json
{
  "role": "owner | editor",
  "share": {
    "slug": "string",
    "markdownContent": "string",
    "expiresAt": "ISO string",
    "createdAt": "ISO string",
    "updatedAt": "ISO string",
    "editableMode": "READ_ONLY | EDIT_LINK",
    "burnMode": "OFF | AFTER_FIRST_VIEW_GRACE | AFTER_FIRST_VIEW_INSTANT",
    "firstViewedAt": "ISO string | null",
    "burnDeadline": "ISO string | null",
    "deletedAt": "ISO string | null",
    "burnedAt": "ISO string | null",
    "statusLabel": "string",
    "expiresAtLabel": "string"
  }
}
```

## `PATCH /api/shares/{slug}/manage`

Save Markdown content.

Required header:

```text
x-share-token: <token>
```

Request body:

```json
{
  "markdownContent": "string, required",
  "lastKnownUpdatedAt": "ISO string | null",
  "force": false
}
```

Conflict response:

```json
{
  "conflict": true,
  "role": "owner | editor",
  "share": {
    "...": "latest remote share payload"
  }
}
```

## `PATCH /api/shares/{slug}/settings`

Owner token only.

Required header:

```text
x-share-token: <token>
```

Request body:

```json
{
  "expiresInHours": 168,
  "password": "",
  "burnMode": "OFF",
  "editableMode": "READ_ONLY"
}
```

Response may include:

```json
{
  "role": "owner",
  "share": {
    "...": "updated share payload"
  },
  "editorToken": "string | null"
}
```

## `DELETE /api/shares/{slug}/manage`

Owner token only.

Required header:

```text
x-share-token: <token>
```

Success response:

```json
{
  "success": true
}
```
