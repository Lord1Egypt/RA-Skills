---
name: openclaw-feishu-base
description: Unified Feishu Base/Bitable management for OpenClaw. Use when you need to inspect Base schema, manage tables/fields, or query/create/update/delete records in Feishu Base/Bitable with existing Feishu credentials.
---

# OpenClaw Feishu Base

Use this plugin when working with **Feishu Base / Bitable** in OpenClaw.

## What it provides

A unified tool:

- `feishu_base`

Recommended actions include:

- `resolve_link`
- `list_bases`
- `discover_tables`
- `find_table`
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
- `list_folder`

## Best-use guidance

- Prefer **direct Base links** or explicit identifiers (`app_token`, `table_id`) when available.
- Discovery helpers are convenience features; direct link/token workflows are more reliable.
- Use `discover_tables` for broad, self-discoverable scans when you do not know the app token.
- Inspect schema before writing when field names are uncertain.
- Query/list before update when locating existing records.
- Avoid hardcoding a fixed app/table in workflow logic; derive the target from the current user request (link, base, table name, or explicit IDs).

## Workflow: add customer record (dynamic, non-hardcoded)

Use this when user asks to “add customer”.

1. Resolve target table first.
   - If user provides a Base link, run `resolve_link` and use returned `app_token` + `table_id`.
   - If no table is specified, run `list_tables` / `find_table` and choose best match (`Customers`, `Customer`, `客户`).
   - If multiple likely matches exist, ask one concise disambiguation question.

2. Inspect schema before write.
   - Run `get_table` and read writable fields.
   - Map by field names (for example: `Customer Name`, `Company Name`, `City`, `State`, `Country`, `Phone`, `Email`, `Status`).

3. Build minimal safe payload.
   - Fill only fields provided by user.
   - If user says location only (e.g., “Jiji at Penang”), map `Customer Name=Jiji`, `City/State=Penang` when present.
   - For select fields, only use valid options; otherwise ask or write to a text fallback field.

4. Create and verify.
   - Run `create_records` with one record first.
   - Confirm success by returned `record_id` (and optionally `get_record` / `query_records` if needed).
   - Report exact fields written.

5. Handle blockers explicitly.
   - If `FEISHU_NOT_CONFIGURED` or permission errors occur, stop and ask user to reconnect/authorize Feishu; do not loop retries.

## Safety

Destructive operations are supported but should be **disabled by default** unless explicitly needed.

Config flag:

- `allowDelete: false` (recommended default)

When deletion is disabled, destructive actions should be blocked:

- `delete_records`
- `delete_field`
- `delete_table`

## Requirements

- OpenClaw with Feishu channel configured
- valid Feishu credentials already present in OpenClaw config
- access to the target Base/Bitable resources

## Notes

- This plugin works best as a link-first / token-first Feishu Base tool.
- Some discovery flows depend on what Feishu APIs expose in the current tenant/account context.
- For field creation and schema mutation, prefer **serialized one-by-one writes**. Parallel field creation can hit Feishu-side limits and cause intermittent `400` failures.
- Credential resolution prefers explicit `account_id`, then active runtime/session account context when available, then runtime-injected `channels.feishu`, and finally persisted OpenClaw config from `OPENCLAW_CONFIG_PATH` or `~/.openclaw/openclaw.json` when some runtime paths do not inject Feishu config consistently.
