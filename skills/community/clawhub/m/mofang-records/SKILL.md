---
name: mofang-records
description: Magicflu/Mofang web-table records and BPM workflow CLI skill. Use when users ask about 魔方网表, Magicflu/Mofang spaces, forms, fields, records, data query/search/list, create/update/delete/import records, field definitions, CRUD, json records, BPM/workflow tasks, 待办, 审批, 提交, 转办, 认领, 驳回, 终止, 取回, 加签, or process transactions. Supports OpenClaw, Claude Code, Codex, Trae, and Trae CN.
metadata:
  version: 3.1.0
  author: magicscape
  platforms:
    - OpenClaw
    - Claude Code
    - Codex
    - Trae
    - Trae CN
  compatibility:
    node: ">=18"
---

# 魔方网表记录与流程 CLI

Use this skill to operate Magicflu/Mofang web-table records and BPM tasks through the bundled CLI. Do not hand-write HTTP requests for supported operations; the CLI handles token refresh, field mapping, space/form resolution, filters, and BPM cookies.

## Install Locations

Copy the whole `mofang-records/` folder, not only `SKILL.md`.

| Client | Project install | Global install |
| --- | --- | --- |
| OpenClaw | `.openclaw/skills/mofang-records/` | `~/.openclaw/skills/mofang-records/` |
| Claude Code | `.claude/skills/mofang-records/` | `~/.claude/skills/mofang-records/` |
| Codex | `.codex/skills/mofang-records/` | `~/.codex/skills/mofang-records/` |
| Trae | `.trae/skills/mofang-records/` | `~/.trae/skills/mofang-records/` |
| Trae CN | `.trae/skills/mofang-records/` | `~/.trae-cn/skills/mofang-records/` |

Required runtime: Node.js 18+.

## Configuration

The CLI reads these environment variables, with `MOFANG_*` taking priority:

- `MOFANG_BASE_URL` or `BASE_URL`
- `MOFANG_USERNAME` or `USERNAME`
- `MOFANG_PASSWORD` or `PASSWORD`
- Optional: `FETCH_TIMEOUT_MS` in milliseconds, default `120000`

If a `.env` file exists beside `cli.mjs`, values are loaded only when the variable is not already set in the environment.

## CLI Contract

Run commands from the skill directory:

```bash
node cli.mjs <command> '<json-params>'
```

Every command prints JSON:

```json
{"success":true,"message":"...","data":{}}
```

If a command fails, keep the JSON output and report `message` to the user. Do not expose tokens or passwords.

### Bash Examples

```bash
export MOFANG_BASE_URL="http://appdev.com.magicflu.com:9999"
export MOFANG_USERNAME="admin"
export MOFANG_PASSWORD="***"
node cli.mjs mofang_list_spaces '{}'
node cli.mjs mofang_list_spaces '{"q":"前端编程"}'
node cli.mjs mofang_list_forms '{"spaceHint":"AI前端编程演示"}'
node cli.mjs mofang_query_records '{"spaceHint":"AI前端编程演示","formHint":"采购申请主表","pageSize":10}'
```

### PowerShell Examples

```powershell
$env:MOFANG_BASE_URL='http://appdev.com.magicflu.com:9999'
$env:MOFANG_USERNAME='admin'
$env:MOFANG_PASSWORD='***'
node cli.mjs mofang_list_spaces '{}'
node cli.mjs mofang_list_spaces '{\"q\":\"前端编程\"}'
node cli.mjs mofang_list_forms '{\"spaceHint\":\"AI前端编程演示\"}'
node cli.mjs mofang_query_records '{\"spaceHint\":\"AI前端编程演示\",\"formHint\":\"采购申请主表\",\"pageSize\":10}'
```

## Required Workflow

1. Prefer read-only commands first: list spaces, list forms, get field definitions, query records.
2. Always pass `spaceHint` when the user provides or implies a target space. This prevents cross-space ambiguity.
3. Before `create` or `update`, run `mofang_get_field_definitions` for the target form and use real field `name` or `label` values.
4. Show a concise preview before write operations and get user confirmation, unless the user already explicitly confirmed the exact write.
5. Treat delete and BPM actions as high risk. Confirm the target record/task and explain the consequence before running them.
6. Use the CLI for supported operations. Do not import handler modules directly or build custom fetch/requests calls for records/BPM.

## Commands

### Records and Forms

| Command | Purpose | Key params |
| --- | --- | --- |
| `mofang_test_connection` | Test base URL and credentials | `{}` |
| `mofang_list_spaces` | List or search accessible spaces | `q?`, `spaceHint?`, `page?`, `pageSize?`, `all?` |
| `mofang_list_forms` | List forms in a space | `spaceHint?` |
| `mofang_get_field_definitions` | Get fields, names, types, options | `formHint`, `spaceHint?` |
| `mofang_query_records` | Query records with pagination/filter/order | `formHint`, `spaceHint?`, `filters?`, `page?`, `pageSize?`, `all?` |
| `mofang_create_record` | Create one record | `formHint`, `spaceHint?`, `data` |
| `mofang_update_record` | Update one record | `formHint`, `spaceHint?`, `recordId`, `data` |
| `mofang_delete_record` | Delete one record | `formHint`, `spaceHint?`, `recordId` |

### BPM

| Command | Purpose | Key params |
| --- | --- | --- |
| `mofang_bpm_list_tasks` | List assignee/candidate/delegated tasks | `mode?`, `page?`, `pageSize?` |
| `mofang_bpm_query_tasks` | Locate BPM tasks by form/record/process | `formHint?`, `spaceHint?`, `recordId?`, `taskName?` |
| `mofang_bpm_get_task` | Get one task and variables | `taskId` |
| `mofang_bpm_complete_task` | Complete/submit a task | `taskId`, `simple?`, `variables?` |
| `mofang_bpm_delegate_task` | Delegate a task | `taskId`, `assignee` |
| `mofang_bpm_claim_task` | Claim a group task | `taskId`, `assignee?` |
| `mofang_bpm_resolve_task` | Resolve delegated task | `taskId` |
| `mofang_bpm_jump_task` | Abort, rollback, or recover | `taskId`, `kind`, `jumpTargetId?`, `targetTaskName?` |
| `mofang_bpm_open_transaction` | Open transaction such as COSIGN | `taskAction`, `processName?`, `taskName?` |
| `mofang_bpm_close_transaction` | Close transaction | `transactionId` |

## Field Value Rules

- Text, multiline text, URL: string
- Number: number, never `""`
- Date: `YYYY-MM-DD`
- Datetime: `YYYY-MM-DD HH:mm:ss`
- Dropdown/tree: option value shown by `mofang_get_field_definitions`
- Checkbox: comma-separated option values, such as `"1,2"`
- Main reference: `{"id":"recordId"}`
- Embed field: do not create child records inside the main create call. Create child records first, then update the main embed field with `{"entry":[{"id":"childId"}]}`

The CLI accepts either Chinese `label` or English `name` for `data` keys and `filters[].fieldName`, but using field `name` is safest for generated code.

## Filters

Use `filters` as an array. Do not use frontend-only `filterType`, `value2`, or `filterGroup` unless you are relying on the CLI's best-effort legacy conversion.

```json
{
  "formHint": "采购申请主表",
  "spaceHint": "AI前端编程演示",
  "filters": [
    {"fieldName": "申请日期", "operator": "between", "value": "2026-03-01,2026-04-01"}
  ],
  "pageSize": 50
}
```

Supported operators include `eq`, `noteq`, `like`, `like_and`, `like_or`, `lt`, `gt`, `lte`, `gte`, `between`, `isnull`, `isnotnull`, `in`, `notin`, `checkbox_in`, `checkbox_eq`, `tree`, and `rddl`.

## Troubleshooting

- If a form name resolves incorrectly, rerun with explicit `spaceHint`.
- `mofang_list_spaces {}` lists spaces by created time descending. To locate a specific space faster, search directly with `{"q":"关键词"}` or `{"spaceHint":"空间名"}`.
- If a request hangs or times out, check `MOFANG_BASE_URL`, network/VPN, and optionally set `FETCH_TIMEOUT_MS`.
- If numeric fields fail with `NumberFormatException`, remove empty string values and check field definitions.
- If dropdown values become empty, inspect `mofang_get_field_definitions` options and submit the shown option value, not the display label unless they are the same.
- If PowerShell JSON parsing fails, escape inner quotes as `\"` or run from bash with normal single-quoted JSON.
