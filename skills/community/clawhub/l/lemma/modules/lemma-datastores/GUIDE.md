---
name: lemma-datastores
description: "Use for Lemma pod data work: design pod tables and files, manage records, and use pod-scoped table and file endpoints correctly."
---

# Lemma Datastores

Use this skill for durable pod data and knowledge storage: tables, records, folders, and files.

## When To Use This Skill

Use `lemma-datastores` when the work involves any of the following:

- designing or updating a pod table schema
- deciding whether data belongs in a table or a file
- creating, listing, updating, or deleting records
- designing ownership fields and RLS behavior
- creating folders, uploading files, or searching pod files
- inspecting live table or file state before other resource work

## Core Data Model

### Tables

Use tables for durable structured business facts.
Examples: expenses, tickets, opportunities, approvals.

### Records

Use record APIs for direct table CRUD.
Prefer record operations for simple single-table writes.

### Files and folders

Files and folders live directly in the pod file namespace.
Use them for attachments, policies, manuals, reports, transcripts, and other unstructured content.

## Critical Facts

- File indexing is asynchronous. Search may lag behind upload.
- `created_at` and `updated_at` are system-managed.
- If RLS is enabled, `user_id` is system-managed.
- Never send `user_id`, `created_at`, or `updated_at` in record create or update payloads.
- `table describe` shows the physical schema, including implicit system columns.
- `query.execute` is read-only SQL for the pod datastore and should only be used for non-RLS tables.

## Fast Decision Rules

### Collaborative table vs personal table

Use a collaborative table when multiple users need to see the same rows.
Examples: tickets, accounts, approvals, work queues.

Use a personal table with `enable_rls=true` only when each caller should see only their own rows.
Examples: personal notes, personal expense drafts, personal saved items.

### Table vs file

Use a table when you need typed fields, filtering, sorting, structured updates, or durable workflow state.

Use a file when the object is primarily a document or binary asset and the important interaction is retrieval, reading, or attachment handling.

### Record APIs vs query.execute

Use record APIs as the default path.
Use `query.execute` only when read-only SQL is truly helpful and the table is not RLS-protected.

## Guardrails

### Ownership guardrail

For collaborative tables, model ownership explicitly with business fields such as:

- `creator_user_id`
- `assignee_user_id`
- `owner_user_id`
- `reporter_user_id`

Populate these from `lemma pod member-list`.
Do not create mirror membership tables.

### RLS guardrail

Do not turn on RLS for collaborative shared tables.
Do not manually write `user_id` into RLS tables.

### File-to-LLM guardrail

Uploading a file does not inject its text into an agent, assistant, workflow, or function.
Store the file, pass a stable reference, grant folder access, and have the runtime fetch or search the file explicitly.

## Common Table Patterns

### Collaborative business table

Use `enable_rls=false` and explicit ownership columns.
Good fit for shared team workflows.

### Personal table

Use `enable_rls=true` and let the backend manage `user_id`.
Good fit for per-user data that should not be shared.

### Supporting domain table

Use extra tables only for real business concepts such as queues, territories, rotations, or approval groups.
Do not use them to duplicate member identity.

## Seed Data Pattern For Desk Testing

Use a standard idempotent seed-data workflow so desk and workflow testing always has realistic records.

Required pattern:

1. create a repeatable seed script in the project, for example `scripts/seed_data.py`
2. use stable natural keys such as `external_ref` or `slug` to identify existing rows
3. seed parent tables first, then child tables that reference parent ids
4. create missing rows and update changed rows so reruns are safe
5. include at least one realistic relational sample set per core desk flow

Minimal relational sample set:

- one parent record, for example `accounts`
- multiple child records, for example `opportunities` linked to that account
- one "edge" record in a non-default status to exercise desk state transitions

Do not rely on hand-created one-off rows for acceptance testing.

## Common File Patterns

Use stable folder structures and clear path ownership.
Examples:

- `/receipts`
- `/contracts`
- `/manuals`
- `/reports`
- `/transcripts`

When files support a business record, keep the record in a table and the document in pod files, then connect them with a stable path or file identifier.

## Recommended Workflow

1. inspect current state first
2. choose table vs file deliberately
3. decide collaborative vs personal access model
4. define ownership fields
5. provision the schema or folder structure
6. run the idempotent seed-data script for realistic records
7. verify read, list, and search behavior

## Snapshot Commands

```bash
lemma table list --pod-id <pod-id>
lemma table describe <table-name> --pod-id <pod-id>
lemma file list / --pod-id <pod-id>
lemma file ls / --pod-id <pod-id>
```

## Canonical CLI Patterns

Create a collaborative table:

```bash
lemma table create --pod-id <pod-id> --payload '{
  "name": "expenses",
  "enable_rls": false,
  "columns": [
    {"name": "merchant", "type": "TEXT", "required": true, "max_length": 255},
    {"name": "amount", "type": "FLOAT", "required": true},
    {"name": "status", "type": "TEXT", "required": true, "default": "SUBMITTED"},
    {"name": "owner_user_id", "type": "UUID"}
  ]
}'
```

Create a personal table with RLS:

```bash
lemma table create --pod-id <pod-id> --payload '{
  "name": "personal_expenses",
  "enable_rls": true,
  "columns": [
    {"name": "merchant", "type": "TEXT", "required": true},
    {"name": "amount", "type": "FLOAT", "required": true}
  ]
}'
```

Create and verify a record:

```bash
lemma record create expenses --pod-id <pod-id> --payload '{
  "data": {"merchant": "Uber", "amount": 19.75, "status": "SUBMITTED"}
}'
lemma record list expenses --pod-id <pod-id>
lemma record get expenses <record-id> --pod-id <pod-id>
```

Create folders and upload files:

```bash
lemma file folder-create /receipts --pod-id <pod-id> --description "Receipt uploads"
lemma file upload --pod-id <pod-id> --file ./receipt.pdf --directory-path /receipts
lemma file list /receipts --pod-id <pod-id>
lemma file search reimbursement --pod-id <pod-id> --scope-path /receipts --scope-mode SUBTREE
```

## Supported Column Types

- `TEXT`
- `INTEGER`
- `FLOAT`
- `BOOLEAN`
- `JSON`
- `DATE`
- `DATETIME`
- `UUID`
- `VECTOR`
- `SERIAL`
- `ENUM`

## Column Rules

- Use `auto` only for backend-generated columns such as `UUID` or `SERIAL`.
- Do not declare `created_at` or `updated_at`.
- Do not declare `user_id` when `enable_rls=true`.
- It is valid to omit `id` when the primary key is the default materialized UUID id.
- `max_length` is for `TEXT`.
- `options` is required for `ENUM`.
- Computed columns should not also be `required`, `unique`, `auto`, or `foreign_key`.

## Verification Rules

Always verify with realistic data.

- create at least one representative record
- list records and inspect returned shape
- confirm ownership fields look correct
- for files, verify upload, list, and search behavior
- if RLS is involved, verify behavior with the correct caller expectations

## Common Mistakes

- using RLS on collaborative shared tables
- manually writing `user_id` into RLS tables
- creating mirror membership tables
- using files where structured records are needed
- assuming uploaded files are immediately searchable
- relying on `query.execute` for RLS tables

## Inspect Payload Shapes First

```bash
lemma operation show table.create
lemma operation show record.create
lemma operation show record.update
lemma operation show file.upload
```

## Known CLI Behavior

Read shared CLI behavior notes in [`../lemma-main/references/known-cli-behavior.md`](../lemma-main/references/known-cli-behavior.md).

## Related Skills

Route to:

- `lemma-functions` when writes span multiple tables or need backend validation
- `lemma-agents` when an LLM worker must classify, extract, or summarize
- `lemma-workflows` when the table or file activity is part of a multi-step process
- `lemma-assistants` or `lemma-desks` when humans need a front end on top of the data model
