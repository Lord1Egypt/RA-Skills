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

Targets can be either:

- A raw document id such as `<YOUR_SHEET_ID>`
- A Maybe Sheet URL such as `https://www.maybe.ai/docs/spreadsheets/d/<YOUR_SHEET_ID>`

Use `--doc-id` for raw document ids, or `--sheet-id` when you want to pass a raw
document id or full Maybe Sheet URL directly.

## CLI Commands

Use these commands for sharing tasks:

```bash
# Query current authenticated user's effective permission
mbs share permission --doc-id <YOUR_SHEET_ID>
mbs share permission --sheet-id "<YOUR_SHEET_ID_OR_SHEET_URL>"

# Public/private visibility
mbs share visibility --doc-id <YOUR_SHEET_ID> --visibility public --public-permission viewer
mbs share visibility --doc-id <YOUR_SHEET_ID> --visibility public --public-permission editor
mbs share visibility --doc-id <YOUR_SHEET_ID> --visibility private

# Grant read-only access for a MaybeAI user email
mbs share grant --doc-id <YOUR_SHEET_ID> --email "<USER_EMAIL>" --permission viewer

# Grant write/edit access for a MaybeAI user email
mbs share grant --doc-id <YOUR_SHEET_ID> --email "<USER_EMAIL>" --permission editor

# Remove email-specific access
mbs share remove --doc-id <YOUR_SHEET_ID> --email "<USER_EMAIL>"
mbs share list --doc-id <YOUR_SHEET_ID>
```

Use `--gid <GID>` only when a backend workflow explicitly needs a narrower permission scope.

## Usage Rules

Use `share visibility` when the user asks to:

- make a sheet public
- make a sheet private
- allow anyone with the link to view
- allow anyone with the link to edit

Payload rules:

- `visibility` must be `public` or `private`
- `public_permission` is required only when `visibility` is `public`
- `public_permission` must be `viewer` or `editor`

Use `share grant` when the user asks to share a sheet with a named person or email.

Payload rules:

- `permission` must be `viewer` or `editor`
- `email` must belong to an existing MaybeAI user
- `gid` may be `null`

Use `share permission` when the task is to confirm whether the current authenticated user can view or edit a given sheet.

Possible `access` values:

```text
none
viewer
editor
owner
```

Use `share remove` when the user asks to unshare a sheet from a specific email.
Use `share list` when the user asks who currently has access to a sheet.

## Decision Rules

- Use sharing commands only for access control. Do not mix them up with worksheet edits, filters, formulas, or dashboard work.
- Prefer passing the full Maybe Sheet URL when you already have it. Passing the raw document id is also valid.
- Treat `gid` as `null` unless a narrower permission scope is explicitly required by the backend workflow.
- If the user asks to "make it public", clarify whether they want public `viewer` or public `editor` access if that is not obvious from context.
- If the caller is not the owner, visibility changes and permission mutations can fail even if the user can edit cells.

## Recommended Workflow

1. Resolve the target sheet URL or document id.
2. If needed, run `mbs share permission` first to confirm the current user's access.
3. Apply `mbs share visibility`, `mbs share grant`, or `mbs share remove`.
4. If the user wants verification, run `mbs share permission` or `mbs share list`.
