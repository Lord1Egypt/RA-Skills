# OpenClaw Feishu Base

Unified Feishu Base/Bitable management plugin for OpenClaw.

This plugin adds a single `feishu_base` tool that can resolve Base links, inspect schema, manage tables and fields, and query/create/update/delete records using existing `channels.feishu` credentials from your OpenClaw config.

## What it does

Supported `feishu_base` actions include:

- `resolve_link`
- `list_bases`
- `discover_tables`
- `list_tables`
- `get_table`
- `get_record`
- `query_records`
- `create_records`
- `update_records`
- `upsert_records`
- `delete_records`
- `create_table`
- `rename_table`
- `delete_table`
- `create_field` (including linked fields via `link.table_id` / `link.table_name`, plus duplex links via `link.back_field_name`)
- `rename_field`
- `update_field`
- `delete_field`
- `upload_attachment`
- `clone_attachment`
- `build_attachment_field_value`

## Safety defaults

Destructive actions are implemented but disabled by default.

Set plugin config:

```json
{
  "allowDelete": false
}
```

When `allowDelete` is `false`, these actions are blocked:

- `delete_records`
- `delete_field`
- `delete_table`

## Requirements

- OpenClaw with Feishu channel configured
- valid `channels.feishu` credentials in OpenClaw config
- access to the target Base/Bitable resources in Feishu/Lark

## Notes

- This plugin uses the existing Feishu credentials already configured in OpenClaw.
- `list_bases` supports discovery without a query and returns all Drive-visible Base/bitable files for this app context.
- `discover_tables` aggregates table discovery across Drive-visible bases (plus optional `app_tokens`) and supports fuzzy `query` matching (for example `event_details` can match `Event Details`).
- Table creation may still leave Feishu's default starter field in place; use field actions to clean up or reshape the schema.
- Dashboard operations are not currently implemented.

## Credential resolution order

This plugin resolves Feishu credentials in this order:

1. explicit tool input `account_id`
2. active runtime/session account context when available
3. runtime-injected `channels.feishu` config
4. persisted OpenClaw config fallback from:
   - `OPENCLAW_CONFIG_PATH`
   - `~/.openclaw/openclaw.json`

Why this fallback exists:

- some real OpenClaw tool/runtime paths do **not** inject `channels.feishu` consistently
- without a fallback, the plugin can throw `FEISHU_NOT_CONFIGURED` even when Feishu is actually configured correctly in OpenClaw

So the persisted-config fallback is intentional compatibility behavior, not accidental hidden magic.

## Dependencies

This plugin depends on:

- `@larksuiteoapi/node-sdk`
- `@sinclair/typebox`
- `zod`

If you install the plugin through a normal package workflow, these should be installed automatically from `package.json`.

If you copied the plugin folder manually and dependencies were not installed, run:

```bash
cd <plugin-folder>
npm install
```

If you see a missing `@sinclair/typebox` error, it usually means dependencies were not installed in the plugin folder.

## Tested status

Validated in a live OpenClaw + Feishu environment for:

- Base read/inspect flows
- table creation
- record creation
- delete safety gating with `allowDelete=false`
- live destructive operations with `allowDelete=true`

Some structure-mutation edge cases may still need broader testing across more field types.

## Current limitation: linked-record field creation

Linked-record / relation fields are currently the least reliable part of this plugin.

What is implemented:

- `create_field` accepts linked-field inputs
- target tables can be resolved from `link.table_name`
- one-way and duplex/two-way link payload shaping is supported

However, live testing shows that Feishu may still reject even the **minimal documented linked-field create payload** with HTTP `400`.

Example minimal payload that may still fail:

```json
{
  "field_name": "Project",
  "type": 18,
  "property": {
    "table_id": "<target_table_id>"
  }
}
```

Practical takeaway:

- plain fields are generally usable
- linked-record fields should still be treated as **experimental / flaky**
- linked-field failures do **not necessarily mean** normal field creation is broken
- the remaining blocker appears to be Feishu-side relation-field validation and/or SDK/runtime behavior, not just simple table-name resolution

Recommended workaround:

- create plain fields first
- **always serialize field creation one-by-one**; parallel field writes can hit Feishu-side limitations and trigger intermittent `400` errors
- treat relation-field creation as best-effort until more tenant/runtime-specific validation is confirmed

## Example ideas

- Resolve a Base link and inspect schema
- Create a new table with initial fields
- Create/update records from structured input
- Rename fields and adjust schema
- Delete records/fields/tables only when deletion is explicitly enabled
- Upload or clone attachments and write them back into attachment fields

## Attachment examples

### Upload a local file for a Base attachment field

```json
{
  "action": "upload_attachment",
  "app_token": "<app_token>",
  "file_path": "/tmp/example.pdf"
}
```

### Clone an existing attachment by URL into the target Base app

```json
{
  "action": "clone_attachment",
  "app_token": "<app_token>",
  "url": "https://example.com/source-file.png"
}
```

### Build a write-ready attachment field value

```json
{
  "action": "build_attachment_field_value",
  "attachments": [
    {
      "file_token": "boxcn...",
      "name": "example.pdf"
    }
  ]
}
```

### Update a record with the returned attachment objects

```json
{
  "action": "update_records",
  "app_token": "<app_token>",
  "table_id": "<table_id>",
  "records": [
    {
      "record_id": "<record_id>",
      "fields": {
        "Attachment": [
          {
            "file_token": "boxcn...",
            "name": "example.pdf"
          }
        ]
      }
    }
  ]
}
```

### Attachment limits / notes

- current implementation uses Feishu Drive `upload_all`
- practical limit is **20MB** per file in the current plugin path
- likely images are uploaded as `media`; other files are uploaded as `file`
- larger files would need multipart upload support in a future release

## Publish notes

Recommended early public release version: `0.2.0`
