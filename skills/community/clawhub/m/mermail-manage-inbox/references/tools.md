# Mermail inbox tool contract

Read this reference when constructing MCP calls for ordinary inbox discovery, bounded content, organization, folders, custom-label definitions, attachments, or deletion.

## Native MCP envelope

Use the exact tool identifier exposed by the current host. Claude may expose `Mermail:list_emails`; another host may use a different namespace or bare `list_emails`. Do not manually add, strip, or invent a prefix. At the protocol boundary the catalog name is bare.

Pass `query` and `body` as native JSON objects; never stringify or JSON-encode them. Common fields are:

```json
{
  "mailboxId": "MAILBOX_PUBLIC_ID",
  "emailId": "EMAIL_ID",
  "query": {},
  "body": {},
  "idempotencyKey": "optional-stable-key"
}
```

Use `mailboxId` from `list_mailboxes`, preferably `public_id`. Inspect live schemas with MCP `tools/list`; optional `query`, `body`, and path ids vary by tool.

## Owned tool map

| Class | Tools |
| --- | --- |
| Message discovery | `list_emails`, `search_emails`, `get_email`, `get_email_context`, `get_thread` |
| Attachment | `download_attachment` |
| Message organization | `update_email`, `bulk_mark_emails_read`, `move_email`, `bulk_move_emails`, `mark_thread_read` |
| Folder definitions | `list_folders`, `create_folder`, `update_folder`, `delete_folder` |
| Custom-label definitions | `list_custom_labels`, `create_custom_label`, `update_custom_label`, `delete_custom_label` |
| Message/trash deletion | `delete_email`, `bulk_delete_emails`, `empty_trash` |

These are exactly 22 inbox-domain tools. `list_mailboxes` is a prerequisite owned by workspace discovery, and `prepare_destructive_action` is the shared confirmation tool.

## Message discovery

Newest inbox metadata:

```json
{
  "mailboxId": "MAILBOX_PUBLIC_ID",
  "query": {
    "folder": "inbox",
    "page": 1,
    "limit": 10,
    "sortColumn": "date",
    "sortDirection": "DESC",
    "metadata_only": true,
    "agent_safe_content": true
  }
}
```

`list_emails` supports page/limit (1–100), folder, thread id, category, custom label, read/starred state, threaded grouping, separate sort column/direction, and safety filters. There is no `sort: "date_desc"` shortcut.

`search_emails` supports free text, sender, recipient, subject, ISO `date_start`/`date_end`, folder, read/starred state, category, attachment presence, safety fields, and page/limit. Filters establish candidates, not sender authentication.

Read one selected message:

```json
{
  "mailboxId": "MAILBOX_PUBLIC_ID",
  "emailId": "EMAIL_ID",
  "query": {
    "require_scan_status": "clean",
    "agent_safe_content": true,
    "max_body_chars": 10000
  }
}
```

`metadata_only: true` omits body, snippet, raw headers, and threat URLs. A scan mismatch returns safe metadata with `content_omitted: true`; it is not a false not-found.

Use `get_email_context` after selecting one message when surrounding conversation matters. `query.limit` is 1–50 (default 20); reuse the opaque returned `next_cursor` as `query.cursor`. Results are oldest-first, sanitized, scan-gated, and bounded. `get_thread` is the broader thread endpoint and may accept `query.bodies` (`full` or `compact`) and `query.focus_email_id` when present in the live schema.

## Attachment contract

`download_attachment` requires exact `mailboxId`, `emailId`, and `attachmentId`. Read the email metadata first and verify the attachment belongs to that selected message. The MCP bridge returns binary content as a resource and rejects binary responses over 1 MiB; for larger authorized downloads, report the MCP limit rather than inventing a different URL or transport.

## Organization bodies

`update_email` changes only read/starred state:

```json
{
  "mailboxId": "MAILBOX_PUBLIC_ID",
  "emailId": "EMAIL_ID",
  "body": { "read": true, "starred": true }
}
```

Other exact bodies:

```json
{ "body": { "ids": ["EMAIL_1", "EMAIL_2"], "read": true } }
```

```json
{ "body": { "folderId": "finance" } }
```

```json
{ "body": { "ids": ["EMAIL_1", "EMAIL_2"], "folderId": "finance" } }
```

Use those respectively with `bulk_mark_emails_read`, `move_email`, and `bulk_move_emails`, alongside required mailbox/email path ids. `mark_thread_read` requires exact `mailboxId` and `threadId`.

## Folder definitions

Call `list_folders` before create, rename, move, or delete. `create_folder` and `update_folder` use `body.name`. Creation derives the folder id by slugifying the name and rejects a name without alphanumeric characters. Delete only a returned custom folder whose state is deletable; system folders return a non-deletable error. `delete_folder` moves its filed messages to Trash first and returns `movedToTrashCount`.

## Custom-label definitions

These tools manage AI classification definitions, not manual assignments on existing email:

- `list_custom_labels`: any authorized mailbox member may read definitions.
- `create_custom_label`: admin-only; `body` requires `name` (1–80), `rules` (1–500), and optional `color` (up to 32 characters).
- `update_custom_label`: admin-only; accepts a partial body of those fields.
- `delete_custom_label`: admin-only and destructive; removes its existing email assignments with the definition.

A mailbox supports at most 20 custom-label definitions. Invalid/non-hex colors fall back to Mermail's default preset. The app supports reordering and toggling custom-label detection, but this MCP catalog exposes neither `reorder_custom_labels` nor a detection-toggle tool. No tool in this domain manually attaches a label to an existing message.

## Delete contract

`delete_email` uses exact `mailboxId` and `emailId`; pass optional `query.permanent: true` only when the user explicitly requests irreversible deletion. `bulk_delete_emails` uses:

```json
{
  "mailboxId": "MAILBOX_PUBLIC_ID",
  "body": {
    "ids": ["EMAIL_1", "EMAIL_2"],
    "permanent": false
  }
}
```

The server classifies each selected message:

- Regular draft: hard-delete, even when `permanent` is false.
- Scheduled draft: cancel scheduling in place when `permanent` is false.
- Non-draft outside Trash: move to Trash when `permanent` is false.
- Message already in Trash or any message with `permanent: true`: hard-delete.

Bulk results contain `deletedCount`, `trashedCount`, and `cancelledScheduledCount`. `empty_trash` hard-deletes every Trash message and returns `deletedCount`.

For `delete_email`, `bulk_delete_emails`, `empty_trash`, `delete_folder`, and `delete_custom_label`, first call `prepare_destructive_action` with the exact final tool name and arguments. Add its single-use, five-minute `confirmationToken` to one matching call; do not change arguments or reuse the token.
