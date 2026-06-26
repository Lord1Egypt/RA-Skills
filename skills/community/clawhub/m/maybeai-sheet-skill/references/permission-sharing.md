# Permission And Sharing Reference

Use this reference when the task is about spreadsheet visibility, public access, or user-specific sharing permissions rather than cell data editing.

## Scope

These APIs cover:

- Change a sheet between `private` and `public`
- Set public access as `viewer` or `editor`
- Grant `viewer` or `editor` access to a specific email
- Query the current user's effective permission on a sheet
- Remove a user's access
- List current share entries on a sheet

Only the sheet owner can change visibility, assign permissions, remove access, or list shares.

## Setup

Examples below assume:

```bash
HOST="${BASE_URL:-https://play-be.omnimcp.ai}"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
SHEET_ID="<YOUR_SHEET_ID_OR_SHEET_URL>"
EMAIL="<USER_EMAIL>"
```

`SHEET_ID` can be either:

- A raw document id such as `<YOUR_SHEET_ID>`
- A Maybe Sheet URL such as `https://www.maybe.ai/docs/spreadsheets/d/<YOUR_SHEET_ID>`

For sharing APIs, `sheet_id` accepts either form.

## Endpoints

### Update Sheet Visibility

```text
POST /api/v1/share/sheet/visibility
```

Use this when the user asks to:

- make a sheet public
- make a sheet private
- allow anyone with the link to view
- allow anyone with the link to edit

Payload rules:

- `visibility` must be `public` or `private`
- `public_permission` is required only when `visibility` is `public`
- `public_permission` must be `viewer` or `editor`

Example: public viewer

```json
{
  "sheet_id": "<YOUR_SHEET_ID_OR_SHEET_URL>",
  "visibility": "public",
  "public_permission": "viewer"
}
```

Example: public editor

```json
{
  "sheet_id": "<YOUR_SHEET_ID_OR_SHEET_URL>",
  "visibility": "public",
  "public_permission": "editor"
}
```

Example: private

```json
{
  "sheet_id": "<YOUR_SHEET_ID_OR_SHEET_URL>",
  "visibility": "private"
}
```

Typical response:

```json
{
  "sheet_id": "<YOUR_SHEET_ID>",
  "gid": null,
  "access": "owner",
  "can_view": true,
  "can_edit": true,
  "is_owner": true,
  "visibility": "public",
  "public_permission": "viewer"
}
```

### Assign Permission To Email

```text
POST /api/v1/share/sheet/update-permission
```

Use this when the user asks to share a sheet with a named person or email.

Payload rules:

- `permission` must be `viewer` or `editor`
- `email` must belong to an existing MaybeAI user
- `gid` may be `null`

Example: assign viewer

```json
{
  "sheet_id": "<YOUR_SHEET_ID_OR_SHEET_URL>",
  "email": "<USER_EMAIL>",
  "permission": "viewer",
  "gid": null
}
```

Example: assign editor

```json
{
  "sheet_id": "<YOUR_SHEET_ID_OR_SHEET_URL>",
  "email": "<USER_EMAIL>",
  "permission": "editor",
  "gid": null
}
```

Typical response:

```json
{
  "sheet_id": "<YOUR_SHEET_ID>",
  "email": "<USER_EMAIL>",
  "gid": null,
  "permission": "editor",
  "updated": true,
  "removed": false
}
```

### Query Current User Permission

```text
POST /api/v1/share/sheet/permission
```

Use this when the task is to confirm whether the current authenticated user can view or edit a given sheet.

Example payload:

```json
{
  "sheet_id": "<YOUR_SHEET_ID_OR_SHEET_URL>",
  "gid": null
}
```

Typical response:

```json
{
  "sheet_id": "<YOUR_SHEET_ID>",
  "gid": null,
  "access": "editor",
  "can_view": true,
  "can_edit": true,
  "is_owner": false,
  "visibility": "private",
  "public_permission": "viewer"
}
```

Possible `access` values:

```text
none
viewer
editor
owner
```

### Remove Email Permission

```text
POST /api/v1/share/sheet/remove-access
```

Use this when the user asks to unshare a sheet from a specific email.

Example payload:

```json
{
  "sheet_id": "<YOUR_SHEET_ID_OR_SHEET_URL>",
  "email": "<USER_EMAIL>",
  "gid": null
}
```

### List Current Sheet Shares

```text
POST /api/v1/share/sheet/list
```

Use this when the user asks who currently has access to a sheet.

Example payload:

```json
{
  "sheet_id": "<YOUR_SHEET_ID_OR_SHEET_URL>"
}
```

## Decision Rules

- Use sharing APIs only for access control. Do not mix them up with worksheet edits, filters, formulas, or dashboard APIs.
- Prefer passing the full Maybe Sheet URL when you already have it. Passing the raw document id is also valid.
- Treat `gid` as `null` unless a narrower permission scope is explicitly required by the backend workflow.
- If the user asks to "make it public", clarify whether they want public `viewer` or public `editor` access if that is not obvious from context.
- If the caller is not the owner, visibility changes and permission mutations can fail even if the user can edit cells.

## Recommended Workflow

1. Resolve the target sheet URL or document id.
2. If needed, call `/api/v1/share/sheet/permission` first to confirm the current user's access.
3. Apply one of:
   - `/api/v1/share/sheet/visibility`
   - `/api/v1/share/sheet/update-permission`
   - `/api/v1/share/sheet/remove-access`
4. If the user wants verification, call `/api/v1/share/sheet/permission` or `/api/v1/share/sheet/list`.
