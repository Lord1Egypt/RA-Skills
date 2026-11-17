---
name: informat
description: "Use when operating the 织信/Informat platform, including apps, tables, workflows, automations, scripts, APIs, dashboards, records, listeners, schedules, or platform-generated files."
when_to_use: "When the user mentions Informat (织信), this skill must be loaded. When the user wants to operate Informat platform features such as data tables, applications, APIs, automations, scripts, etc. This includes creating tables, querying data, configuring automation workflows, developing scripts, and all other Informat platform related operations."
---

# Informat Platform System Methods

## Current Session Path Rules (Highest Priority)

The current session message prefix provides:
- `informatclawThreadId`
- the absolute path to `call_informat.js`
- the absolute Informat skill directory

You must use these absolute paths:
- API calls: `node "<absolute call_informat.js path from the runtime instruction>" <method> --threadId <informatclawThreadId> ...`
- Reference docs: `cat "<absolute Informat skill directory from the runtime instruction>/references/..."`

Do not use `Read` on `/root/.informatclaw/config/skills/informat`; do not use `$INFORMAT_CONFIG_DIR`, `{baseDir}`, `/data/workspace/informat`, or guessed paths; do not write or rely on `scripts/.env`.

Total 215 methods. The parameter definition file for each method is under `{baseDir}/references/`.
> 📚 **Reference Documentation Directory**: `{baseDir}/references/doc/` contains complete platform development documentation:
> - `references/doc/markdown/` directory: Official platform core feature documentation (AI Assistant, API, Automation, Dashboard, Expression, Scheduled Tasks, Scripts, Data Tables, Tasks, Websites, etc.)
> - `references/doc/markdown/script/` directory: Script API reference documentation, categorized by module (bpmn.md, table.md, http.md, etc.). Consult these first when developing scripts


## Invocation Rules

Based on method name prefix, the system automatically selects the corresponding agent interface:

| Prefix | Interface Type | Required Parameters |
|--------|---------------|-------------------|
| `_wb_` | Workbench Agent | No extra parameters |
| `_company_` | Team Agent | No extra parameters |
| Common methods | Common Agent | No extra parameters |
| Other | Application Agent | `--appId` |

### Invocation Protocol (combined gate: doc + schema in one shot)

⚠️ The script has a built-in gate: **before the first operation of a kind, read its domain design doc + parameter schema**, otherwise the script refuses to run and returns a hint. The two proofs (`_doc_ack` = doc read, `_ack` = schema read) are **merged into one** — bring whichever the hint asks for, and one retry clears it:

```bash
# Step 1: Read the parameter schema (understand required/enum/type/nested structure)
cat {baseDir}/references/system_create_table_module.json
# Step 2: Read the domain design doc (the matching .md under references/doc/markdown/; take its header DOCKEY: <token>)
cat {baseDir}/references/doc/markdown/informat.table.md

# Step 3: Write the parameter file; per the hint add _doc_ack (=DOCKEY token) and/or _ack (=this method's REQUIRED param names, comma-separated)
#         Both are "already read" proofs, stripped before sending to the backend. _ack only needs the REQUIRED names (not all).
echo '{"id":"t1","name":"Table","fields":[],"_doc_ack":"tbl-2e7a9","_ack":"id,name,fields"}' > params.json

# Step 4: Execute (the script still validates required/enum/type locally — the real safety net against fabricated args)
node {baseDir}/scripts/call_informat.js _create_table_module --appId <appId> --threadId <threadId> --file params.json

# Common/team/workbench methods (no --appId); read-only (query/list/read) and zero-arg methods skip the gate, need no _ack
node {baseDir}/scripts/call_informat.js _get_current_time --threadId <threadId>
```

**The gate fires once per domain**: `_doc_ack`/`_ack` proofs are tracked per **domain** (table/automatic/workflow/dashboard…) — after the first build method in a domain clears the gate, **the rest of that domain's methods are no longer gated** (e.g. after the 1st table, the next 11 tables pass straight through), backed by the step-4 local validation.

**Handling gate feedback**:
- `[First operation of this kind: please read the documentation and parameter definitions before calling]` (exit 3) → first build in this domain. Per the hint, **take the `DOCKEY` from the .md as `_doc_ack`, and the REQUIRED param names from the schema as `_ack`**, then re-call with the business args (bring whatever the hint lists; one retry clears it). **Never guess tokens/param names without reading.**
- `[Parameter validation failed: xxx]` (exit 4) → missing required / illegal enum / wrong type. Fix per the schema and retry. **This is the main defense against fabricated args after relaxing the gate — fix it carefully.**
- `[Before saving this script: read the SDK reference for each informat.* module it uses]` (exit 5) → only `_save_informat_script`: the `script/<module>.md` for an `informat.<module>.*` used in the script (e.g. `informat.table.*`) has not been read this session. **Read each `script/<module>.md` listed to verify exact signatures** (argument count/order/position; common errors: tableId placed inside query, update written with three args), then re-call with `_sdk_read=<comma-separated module names>`. Each module is gated only once per session.
- `[Before this operation: read the expression reference, as the payload contains a platform expression ${...}]` (exit 6) → any write method whose arguments contain a platform expression `${...}` (automation step values, formula fields, flow conditions, etc.) while `informat.expression.md` has not been read this session. Informat expressions are a platform DSL (UEL), **not JavaScript**; their syntax and available functions are defined by that document. **Read `informat.expression.md`**, then re-call with `_expr_ack=<the DOCKEY token in the document header>`. Gated only once per session (the `${}` in `_save_informat_script` and `_codestudio_*` are native JS template literals and do not trigger this gate).
- `[Blueprint not yet complete: finishing is not permitted]` (exit 7) → only during full-app orchestration: you called `_app_check_setting` but some component category is below its built count. **Continue creating the missing components listed** (linked to the blueprint, not added as filler) then finish. Built counts are tallied automatically by `name` (covering table/automatic/script/api/workflow/dashboard/**listener/schedule** — once listeners or scheduled tasks are confirmed by the user during §2 alignment they must be declared in plan.targets and actually built, **not silently dropped as "optional extensions" at build time**); a verbal "done" cannot bypass it. To genuinely drop an item, re-register targets via `_plan_set` and explain.
- `[Build artifact rejected: it violates the <domain> design rules]` (exit 10) → build-artifact validation (anti context-decay): at the moment of building, deterministic per-domain rules are checked, independent of whether the document is still remembered. Covers dashboard (enableCardStyle must be true / Number card xPosition·yPosition both center / subTitle ≠ name / orderByList sort entries must be {field,type:asc\|desc} objects, not a "count#desc" string / a card's width must fit the current row's remaining columns: the 24-column grid flows by order+width, so a width that overflows the row wraps and leaves a gap — fill each row to 24 and build cards in visual order / **a ProChart must have a data source: proChartSetting.dataset non-empty with each entry binding a real tableId or expression, and series non-empty**, else the chart is blank), automatic (each step's required references validated against the schema: OutputBpmnProcess needs bpmnModuleId+bpmnProcessDefineId+bpmnProcessStartFormTableId+bpmnProcessStartFormFieldList, OutputRecordCreate needs recordCreateTableId, CallScript needs scriptId+func, SetReturnValue needs valueVar, If needs expression+If.true/If.false branches; **interaction-output steps need display content: OutputToast needs toastValueVar, OutputConfirm needs confirmTitleVar or confirmDialogTitleVar, OutputNotification needs messageVar or message**, else a blank box pops on the client; funcSettingList must be non-empty), bpmn (a UserTask needs assignee+formSetting.tableId+at least one button / a return edge must not form a cycle from all-unconditional flows — carry a conditionExpression or use a TaskMoveToActivity button), listeners (eventList elements must be event-ID strings not objects / no top-level tableId / invokeType must have its executor), table (business fields must not be named id·seq / relation fields need a real target tableId), schedule (invokeType must have its executor / cron type needs a cron). The message includes a compact checklist; **fix the payload per the checklist and re-call** — no re-reading required. Fires only on an actual violation and never on legitimate variation.
- **Relation-modeling finish gate (part of exit 7)**: in full-app orchestration, if the planned table count is ≥2 but no Relation (M:N) or LookupList (1:N) field exists anywhere in the app, the finish self-check judges the model too flat (all relations are N:1) and blocks, asking you to add master→detail LookupLists / many-to-many Relations by semantics instead of making every link a single RelationRecord.
- **Transient network errors auto-retry**: a 5xx (including intermittent HTTP 550) / timeout / connection-reset is retried with backoff up to 4 times; 4xx and JSON-RPC application errors are not retried. On an intermittent network error just re-issue the same call — do not change parameters that were already correct.
- **Domain soft reminder (emitted once per domain per session, on the first build of that domain)**: after the first object of a domain is built successfully, a ≤8-line checklist for that domain is appended to the response (rules that cannot be machine-checked — theme consistency / chart-type choice / workflows must be multi-node with branches, etc.), throttled by a marker so later calls have zero overhead. Self-check against it; do not ignore it.
- Register the blueprint contract with the **`_plan_set` command** (`call_informat.js _plan_set --appId <id> --threadId <threadId> '{"targets":{...}}'`), **do not write the file yourself** — the process often changes into a read-only directory, so a self-written file cannot be located and the gates fail.

### Getting Application ID

```bash
# 1. Query all application list
node {baseDir}/scripts/call_informat.js _company_app_list --threadId <threadId>

# 2. Find the target application ID from the returned results, use for subsequent calls
node {baseDir}/scripts/call_informat.js _query_app_define_designer --appId <appId> --threadId <threadId>
```

## Configuration

The server injects `INFORMAT_HOST`, `INFORMAT_AGENT_TOKEN`, and `INFORMAT_AGENT_THREAD_ID` at runtime. Calls only need to explicitly pass `--threadId` as described above. Never write or rely on `scripts/.env`.

> INFORMAT_AGENT_TOKEN can be obtained at: <informat host>/workbench/account/aiAgentApiKey

## File Upload Required -- Important Rule

When you generate any file (Excel, PPT, PDF, Word, CSV, images, etc.) that users need to download:
1. You **MUST** call `_wb_upload_file` to upload the file to platform storage
2. You **MUST** provide the returned `downloadUrl` to the user as the download link
3. **NEVER** return local server file paths to the user (users cannot access the server filesystem)

```bash
# Example: Upload Excel after generation (base64 encoding, recommended for Docker compatibility)
# 1. Base64 encode the file and write params
node -e "const fs=require('fs');const b64=fs.readFileSync('/path/to/report.xlsx').toString('base64');fs.writeFileSync('params.json',JSON.stringify({fileName:'report.xlsx',fileContent:b64}))"
# 2. Call upload
node {baseDir}/scripts/call_informat.js _wb_upload_file --threadId <threadId> --file params.json
# Returns { "downloadUrl": "https://...", "fileName": "report.xlsx" }
# 3. Provide downloadUrl to the user
```

## Complete Application Orchestration -- Intent Recognition + Requirement Alignment + Blueprint

On receiving a request, do **intent analysis** first and split into two kinds — do NOT treat every request as a complete application:

- **Single operation** (one explicit action: add a table / query data / edit a field / create one automation) → go directly to the matching section under "Query Before Operation" below. Do **NOT** trigger this flow.
- **Website / frontend application** (the user asks for a website / official site / portal / frontend page / Vue application / H5, where the page experience is the main goal) → **prefer `_codestudio_*` (AICodeStudio, a complete Vue 3 project)**. Follow the AICodeStudio guidance under "Website Resource - Website (Designer)": query or create the module, read `informat.codestudio.md`, write the Vue project, compile it, and preview it. Consider `_website_*` only for purely static display pages. Do not apply the default "data tables + dashboards + workflow" bundle to these requests unless the user explicitly also wants a backend business application.
- **Complete application / system** (the user says "build an XX system / management platform / app", regardless of whether some modules are already listed) → enter the complete-application flow. User-listed modules are only initial requirements; still align the blueprint first and **do not build directly**:

Iron rules:
1. **Align first, act second**: clarify business domain/core objects/roles/key process/reporting needs → a complete app defaults to only three required component types: **data tables, dashboards, and 1 core workflow**; automations/scripts/APIs/listeners/scheduled tasks are optional extensions and are included only when the user explicitly confirms they are needed → **read the module design docs the blueprint will touch BEFORE producing it** (required: tables→informat.table.md, dashboard→informat.dashboard.uipreset.md, workflow→informat.bpmn.md; optional components read their matching docs only if confirmed). Table structures / card types / flow nodes / field choices in the blueprint MUST be based on these docs' real presets, **never invent from training memory** (typical anti-pattern: dashboard described as "number card + progress bar" / "pie + number" — the only real card types are Number/ProChart/Record/Pivot/Table) → produce a structured blueprint (each card noting type + size + row + theme) → **wait for explicit user confirmation**; build nothing before confirmation.
2. **Linkage iron rule + binding plan**: dashboards/workflows and any confirmed optional automations/scripts/APIs/listeners/scheduled tasks must each state "which table or process it serves, why it exists, how it links"; cut whatever you cannot articulate. **The blueprint must contain a "binding plan table"**: list line by line which workflow or optional automation binds to which table's which button (toolbar/form/**lookup-list·relation-list inline button** `_subtable_create_tool_bar_btn`) or which listener/scheduled task — an action component that is created but not bound to an entry is unreachable by the user and equivalent to invalid configuration. **Listeners/scheduled tasks** are optional extensions; ask once during alignment when relevant, and build them only when meaningful and user-confirmed.
3. **Solidify in 3 fixed-order steps**: after the user confirms the blueprint, in order — ① **first register the blueprint contract via `_plan_set`** (by default only the required three: `call_informat.js _plan_set --appId <id> --threadId <threadId> '{"targets":{"table":N,"dashboard":N,"workflow":1}}'`; if the user confirmed optional components, append `automatic/script/api/listener/schedule` counts; dashboard counts cards; **do not write the file yourself** — the script saves it to a session-stable location); ② **read all module design docs the targets touch** (table→informat.table.md, dashboard→informat.dashboard.uipreset.md, workflow→informat.bpmn.md; optional components: automatic→informat.automatic.md, script→informat.script.md, api→informat.api.md, listener→informat.listeners.md, schedule→informat.schedule.md) so modeling is grounded in documents; ③ execute components one by one in the order below and pass `_app_check_setting`.
4. **Execution order**: app→master-data tables (people/departments/customers — real entities, not dictionaries)→complex tables (reference real fieldIds)→workflow (multi-node + branches; a complete app must build 1 core workflow, and its start button is created here)→dashboards→confirmed optional extensions→`_app_check_setting` self-check→prompt the user to publish.
5. **Finish gate**: `_app_check_setting` checks built counts against plan.json (auto-counted by the script); below target it exits 7 and blocks, so the gaps must be filled before finishing — do not finish after only the major parts are done.
6. **Maintain a progress file**: on start `cat informat_progress/<appId>.md` to resume; after each step **rewrite** it (keep only Done-summary/Next/Key-IDs, bounded, no unbounded appending). It lets you resume quickly across conversations.
7. **Finishing requires a passing publish-health check**: if `_app_check_setting` returns any issue item (e.g. "module Ref not found …"), the script exits 9 and blocks. **Those issues mean tables/modules are not actually attached to the app and publishing will fail** — fix each one (recreate the missing module, rename conflicts), re-run the self-check until it returns an empty list, and only then report completion. **Do not finish while unresolved issues remain, and do not falsely claim "build complete".**

## Build Calls Must Be Sequential — No Parallelism (Critical)

**Create/save/edit/delete calls that write app structure (create table `_create_table_module`, create fields, create dashboard cards `_save_dashboard_*`, create workflow nodes/flows `_bpmn_*`, `_automatic_save_define`, `_api_create_define`, `_save_informat_script`, etc.) must be executed one at a time, strictly sequentially. Never issue several at once with `&` / background / parallel batches.**

Reason: each such call, on the backend, is "load the whole app module tree → add itself → save the whole tree back". Running several in parallel makes them **overwrite each other**, so tables/modules are created but not attached to the app module tree (invisible in the left panel, publish reports `refNotFound`). Actual incident: a `for f in …; do node … & done; wait` that created 8 tables in parallel ended up with only 2 surviving.

Iron rule: **issue one write call, wait for its response, then issue the next**. When many tables/cards are needed, loop sequentially — no `&`. (The script has a serialization lock as a backstop, but do not parallelize intentionally — it only queues and adds latency.)

## Query Before Operation -- The Most Important Rule

Before performing any create or modify operation, you must first query the system's existing structure and obtain real IDs. Never fabricate any ID or field name.

Querying the list alone is not enough - you must further query the complete field structure of each related table. Because creating relational fields requires the target table's field IDs, knowing only the table ID is insufficient.

### Before Creating an Application

```
1. _company_app_list          -> Get all existing applications including unique app identifiers
```

### Before Creating a Data Table

```
1. _query_table_list_designer          -> Get all existing tables and their IDs
2. For each table that might be referenced, call
   _query_table_define_designer        -> Get the complete field list (field IDs, field types, option values, etc.)
   This step cannot be skipped because relational fields require the target table's field IDs
3. cat {baseDir}/references/system_create_table_module.json  -> Read parameter documentation
4. Use the queried real table IDs and field IDs to construct parameters and create the new table
```

Why you must query each table's field structure:
- RelationRecord fields require tableId (target table ID) and nameFieldId (field ID in target table used for display)
- RelationRecordField fields require fieldId (foreign key field ID in current table), targetTableId, targetFieldId
- LookupList fields require sub-table ID and the foreign key field ID in the sub-table
- LookupRollup fields require sub-table ID and the aggregation field ID in the sub-table
- These IDs can only be obtained through _query_table_define_designer queries

Default table-modeling rules (see top of informat.table.md; the build doc gate will require reading it):
- Fixed-choice fields (status/type/priority) **use ListSelect single/multi**, **do not** create "dictionary table + text field".
- Relations pick one of three by semantics: RelationRecord (N:1) / Relation (M:N) / LookupList (1:N) — **do not use RelationRecord exclusively throughout**.
- RelationRecord/Relation/LookupList **must set display fields** (not only the primary display column).
- Business tables need sufficient fields (code+name+basic info+status+key dates+people+relations+amount/qty+remarks+attachments), not only three to five.

### Before Creating Dashboard Cards

```
1. _query_table_list_designer          -> Get all table IDs
2. For the target data source table, call
   _query_table_define_designer        -> Get all field IDs and field types for the table
   Without querying field structure, you cannot correctly configure aggregation fields, group fields, and filter conditions
3. _read_informat_dashboard_document   -> Get dashboard documentation
4. _read_informat_dashboard_ui_preset  -> Get UI presets (when the user does not explicitly specify styles, you must fill cardStyle per the presets;
   all cards in the same dashboard must use the same theme palette; before creating multiple cards, pick one of the 6 layout templates first)
5. Read the parameter documentation for the card type:
   cat {baseDir}/references/system_save_dashboard_prochart_card.json  (chart)
   or system_save_dashboard_number_card.json  (number)
   or system_save_dashboard_record_card.json  (record)
   or system_save_dashboard_pivot_card.json   (pivot)
   or system_save_dashboard_table_card.json   (table)
6. Use the queried real field IDs to construct card parameters
7. Dashboard cards must be tested after publishing to confirm the user-side view is not blank, misaligned, or stuck on a no-data placeholder
```

### Before Creating Automation

```
1. _query_app_define_designer          -> Get module list and existing automation groups
2. _query_table_list_designer          -> Get all table IDs
3. For each table involved in the automation, call
   _query_table_define_designer        -> Get field IDs (field mapping and filter conditions in automation steps require real field IDs)
4. _automatic_doc                      -> Get automation documentation
5. cat {baseDir}/references/system_automatic_save_define.json  -> Read parameter documentation
6. Use the queried real IDs to construct automation steps
```

### Before Creating Workflow

```
1. cat references/doc/markdown/informat.bpmn.md -> workflow design doc (required; calling _bpmn_* is gated by the doc-read gate)
2. _query_app_define_designer -> Get module list
3. _query_table_list_designer + _query_table_define_designer -> Get tables and fields
4. _read_informat_expression_doc -> Get expression documentation (assignee/flow conditions are expressions)
5. Read the corresponding parameter documentation
6. Create in order: module -> process definition -> start configuration -> _bpmn_query_process_define to get StartEvent id -> multiple approval nodes (full form fields + approve/reject buttons + x/y) -> sequence flows (branch via multiple conditional flows from one source + one default) -> bind start button on the main table
   The workflow must be multi-node, branched, fully wired, and table-bound — not a single node
```

### Before Creating Scripts

```
1. _query_informat_script_list -> Get existing scripts and directories
2. _read_informat_script_sdk -> Get script SDK documentation
3. [Mandatory] Before calling any informat.<module>.*, you must Read {baseDir}/references/doc/markdown/script/<module>.md (e.g. table.md, bpmn.md, http.md) to verify exact signatures (argument count/order/position) — do not write from memory; on save, call_informat.js validates this and blocks with exit 5 if unread. Common errors: informat.table.queryList is (tableId, query), not tableId placed inside query; update is (tableId, data) with two args and the id inside data
4. First use _create_informat_script_directory to create directories by function (api/service/utils/mapper, etc.), and split scripts by responsibility into the right directory — never place all functions in a single js file
5. Read cat {baseDir}/references/system_save_informat_script.json
6. Create or edit script (when editing, must pass the existing script ID, do not create duplicates)
```

### Before Editing Fields

```
1. _query_table_list_designer -> Find the target table
2. _query_table_define_designer -> Get the complete field list of the table
3. _read_informat_expression_doc -> If expression configuration is needed
4. Read cat {baseDir}/references/system_edit_table_field.json
5. Use real tableId and fieldId to operate
```

### Before Operating Data Records

```
1. _query_all_table_list -> Get published table IDs
2. _query_table_define -> Get published field structure
3. Read the corresponding parameter documentation
4. Use real field IDs to construct record data
```

## Workbench Agent Method List

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [User] | `_wb_set_curr_appid` | Set current session context application ID | `references/system_wb_set_curr_appid.json` MUST READ |
| [User] | `_wb_process_define_list` | Get workflow list available to current user | none |
| [User] | `_wb_get_process_define` | Get specified workflow process definition configuration | `references/system_wb_get_process_define.json` MUST READ |
| [User] | `_wb_get_table_info` | Get specified data table structure information | `references/system_wb_get_table_info.json` MUST READ |
| [User] | `_wb_get_login_info` | Get my login info including user info and system configuration | none |
| [User] | `_wb_create_instance` | Create and start workflow process instance | `references/system_wb_create_instance.json` MUST READ |
| [User] | `_wb_query_instance_list` | Query all process instances initiated by current user (cross-app) | `references/system_wb_query_instance_list.json` MUST READ |
| [User] | `_wb_query_instance_info` | Query workbench process instance details | `references/system_wb_query_instance_info.json` MUST READ |
| [User] | `_wb_query_task_list` | Query workbench workflow task list (cross-app) | `references/system_wb_query_task_list.json` MUST READ |
| [User] | `_wb_query_task_info` | Query workbench workflow task details | `references/system_wb_query_task_info.json` MUST READ |
| [User] | `_wb_complete_task` | Complete (approve) workbench workflow task | `references/system_wb_complete_task.json` MUST READ |
| [User] | `_wb_ask_ai` | Ask AI assistant | `references/system_wb_ask_ai.json` MUST READ |
| [User] | `_wb_upload_file` | Upload file to platform storage and return download URL | `references/system_wb_upload_file.json` MUST READ |


## Team Agent Method List

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Team] | `_company_app_list` | Query application list | none |
| [Team] | `_company_app_create` | Create application | `references/system_company_app_create.json` MUST READ |
| [Team] | `_company_app_update` | Update team application info (name, group, etc.) | `references/system_company_app_update.json` MUST READ |
| [Team] | `_company_app_group_list` | Get application group list | none |
| [Team] | `_company_app_group_create` | Create application group | `references/system_company_app_group_create.json` MUST READ |
| [Team] | `_company_app_group_update` | Update application group | `references/system_company_app_group_update.json` MUST READ |
| [Team] | `_company_app_group_delete` | Delete application group (dangerous operation) | `references/system_company_app_group_delete.json` MUST READ |
| [Team] | `_company_department_list` | Get team department list | none |
| [Team] | `_company_department_create` | Create a new department in the company | `references/system_company_department_create.json` MUST READ |
| [Team] | `_company_department_update` | Update an existing department in the company | `references/system_company_department_update.json` MUST READ |
| [Team] | `_company_department_delete` | Delete an existing department in the company (dangerous operation) | `references/system_company_department_delete.json` MUST READ |
| [Team] | `_company_role_list` | Query role list | none |
| [Team] | `_company_role_create` | Create a new role in the company | `references/system_company_role_create.json` MUST READ |
| [Team] | `_company_role_update` | Update an existing role in the company | `references/system_company_role_update.json` MUST READ |
| [Team] | `_company_role_delete` | Delete an existing role in the company (dangerous operation) | `references/system_company_role_delete.json` MUST READ |
| [Team] | `_company_role_permission_list` | Query available role permissions | none |
| [Team] | `_company_member_list` | Query team member list | `references/system_company_member_list.json` MUST READ |
| [Team] | `_company_member_list_count` | Get the total count of company members | none |
| [Team] | `_company_member_create` | Add existing account as team member | `references/system_company_member_create.json` MUST READ |
| [Team] | `_company_member_create_new` | Create new account and add as team member | `references/system_company_member_create_new.json` MUST READ |
| [Team] | `_company_member_update` | Update team member | `references/system_company_member_update.json` MUST READ |
| [Team] | `_company_member_delete` | Delete team member (dangerous operation) | `references/system_company_member_delete.json` MUST READ |
| [Team] | `_company_member_info` | Query team member details | `references/system_company_member_info.json` MUST READ |
| [Team] | `_company_get_ai_model_list` | Get team AI model list | none |
| [Team] | `_company_knowledgebase_search` | Search team knowledge base by keyword | `references/system_company_knowledgebase_search.json` MUST READ |
| [Team] | `_company_knowledgebase_list` | List team knowledge-base folders available to the current account | `references/system_company_knowledgebase_list.json` MUST READ |
| [Team] | `_company_expert_list` | Query team expert list | `references/system_company_expert_list.json` MUST READ |
| [Team] | `_company_expert_get` | Get complete team expert configuration | `references/system_company_expert_get.json` MUST READ |
| [Team] | `_company_expert_save` | Create or update a team expert | `references/system_company_expert_save.json` MUST READ |
| [Team] | `_company_expert_team_get` | Get complete team expert team configuration | `references/system_company_expert_team_get.json` MUST READ |
| [Team] | `_company_expert_team_save` | Create or update a team expert team | `references/system_company_expert_team_save.json` MUST READ |


## Application Agent Method List

> [Designer] = Draft environment. [User] = Published environment.

### API (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_api_create_define` | Create API definition (optional parentId to group it) | `references/system_api_create_define.json` MUST READ |
| [Designer] | `_api_create_directory` | Create API group directory (deduped by name, returns dir id for parentId) | `references/system_api_create_directory.json` MUST READ |
| [Designer] | `_api_delete_define` | Delete API definition (dangerous operation) | `references/system_api_delete_define.json` MUST READ |
| [Designer] | `_api_doc` | Query Informat API documentation | none |
| [Designer] | `_api_query_define_designer` | Query single API detailed definition | `references/system_api_query_define_designer.json` MUST READ |
| [Designer] | `_api_query_define_list` | Query API definition list under application | none |
| [Designer] | `_api_update_define` | Update API definition, updateFieldList declares fields to modify | `references/system_api_update_define.json` MUST READ |

### App (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_app_check_setting` | Validate draft configuration legality before publishing | none |
| [Designer] | `_app_create_role` | Create application role | `references/system_app_create_role.json` MUST READ |
| [Designer] | `_app_query_role_by_id` | Query application role details by role key (permissionList returns module key format) | `references/system_app_query_role_by_id.json` MUST READ |
| [Designer] | `_app_update_role` | Update application role name and remark, updateFieldList declares fields to modify | `references/system_app_update_role.json` MUST READ |
| [Designer] | `_app_permission_list` | Query custom app permissions (table moduleId returns table key) | none |
| [Designer] | `_app_permission_create` | Create custom app permission (pass table key as moduleId for table modules) | `references/system_app_permission_create.json` MUST READ |
| [Designer] | `_app_permission_update` | Update custom app permission, updateFieldList declares fields to modify | `references/system_app_permission_update.json` MUST READ |
| [Designer] | `_app_permission_delete` | Delete custom app permission and remove it from roles | `references/system_app_permission_delete.json` MUST READ |
| [Designer] | `_app_delete_draft_define` | Delete draft version Define (irreversible) | `references/system_app_delete_draft_define.json` MUST READ |
| [Designer] | `_app_get_define_list` | Get application definition object list | `references/system_app_get_define_list.json` MUST READ |
| [Designer] | `_app_get_define_object` | Get single definition object details | `references/system_app_get_define_object.json` MUST READ |
| [Designer] | `_app_get_define_type` | Get supported definition object types | none |
| [Designer] | `_app_define_object_log_count` | Query design change log count | `references/system_app_define_object_log_count.json` MUST READ |
| [Designer] | `_app_get_draft_define_count` | Draft change count statistics | none |
| [Designer] | `_app_get_draft_define_list` | Draft object list | none |
| [Designer] | `_app_publish` | Publish application to production  | `references/system_app_publish.json` MUST READ |
| [Designer] | `_app_set_themestyle` | Set application theme style (query _app_themestyle_doc first) | `references/system_app_set_themestyle.json` MUST READ |
| [Designer] | `_app_update_basic_info` | Update application basic information (theme color, menu colors, navigation bar style, etc.) | `references/system_app_update_basic_info.json` MUST READ |
| [Designer] | `_app_themestyle_doc` | Query application theme style documentation | none |
| [Designer] | `_query_app_define_designer` | Query designer application configuration (module list, roles, APIs, automation groups, etc.) | none |
| [Designer] | `_create_module_group` | Create module group | `references/system_create_module_group.json` MUST READ |
| [Designer] | `_update_module_and_group_order` | Update module sorting | `references/system_update_module_and_group_order.json` MUST READ |

### Data Table - Table (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_create_table_module` | Create data table (must query existing tables and field structures first) | `references/system_create_table_module.json` MUST READ |
| [Designer] | `_create_table_field_group` | Create data table field group | `references/system_create_table_field_group.json` MUST READ |
| [Designer] | `_update_table_field_group` | Update data table field group | `references/system_update_table_field_group.json` MUST READ |
| [Designer] | `_table_save_filter_condition` | Set data table view filter condition | `references/system_table_save_filter_condition.json` MUST READ |
| [Designer] | `_table_save_datasource_dbview` | Save database view table SQL configuration | `references/system_table_save_datasource_dbview.json` MUST READ |
| [Designer] | `_table_create_tool_bar_button` | Create data table toolbar button (supports calling script or automation) | `references/system_table_create_tool_bar_button.json` MUST READ |
| [Designer] | `_table_list_tool_bar_button` | Query data table toolbar button list | `references/system_table_list_tool_bar_button.json` MUST READ |
| [Designer] | `_table_update_tool_bar_button` | Update data table toolbar button | `references/system_table_update_tool_bar_button.json` MUST READ |
| [Designer] | `_table_delete_tool_bar_button` | Delete data table toolbar button | `references/system_table_delete_tool_bar_button.json` MUST READ |
| [Designer] | `_table_create_form_tool_bar_btn` | Create data table form toolbar button (supports calling script or automation) | `references/system_table_create_form_tool_bar_btn.json` MUST READ |
| [Designer] | `_table_list_form_tool_bar_btn` | Query data table form toolbar button list | `references/system_table_list_form_tool_bar_btn.json` MUST READ |
| [Designer] | `_table_update_form_tool_bar_btn` | Update data table form toolbar button | `references/system_table_update_form_tool_bar_btn.json` MUST READ |
| [Designer] | `_table_del_form_tool_bar_btn` | Delete data table form toolbar button | `references/system_table_del_form_tool_bar_btn.json` MUST READ |
| [Designer] | `_subtable_create_tool_bar_btn` | Create subtable toolbar button (Relation/LookupList fields only, supports add row, delete, call script or automation) | `references/system_subtable_create_tool_bar_btn.json` MUST READ |
| [Designer] | `_subtable_list_tool_bar_btn` | Query subtable toolbar button list | `references/system_subtable_list_tool_bar_btn.json` MUST READ |
| [Designer] | `_subtable_update_tool_bar_btn` | Update subtable toolbar button | `references/system_subtable_update_tool_bar_btn.json` MUST READ |
| [Designer] | `_subtable_delete_tool_bar_btn` | Delete subtable toolbar button | `references/system_subtable_delete_tool_bar_btn.json` MUST READ |
| [Designer] | `_query_table_list_designer` | Query all tables in designer (including unpublished, does not return field structure) | none |
| [Designer] | `_query_table_define_designer` | Query designer data table field structure | `references/system_query_table_define_designer.json` MUST READ |
| [Designer] | `_query_table_field_designer` | Query single field detailed configuration | `references/system_query_table_field_designer.json` MUST READ |
| [Designer] | `_edit_table_field` | Edit field (must query table structure to get real IDs first) | `references/system_edit_table_field.json` MUST READ |
| [Designer] | `_edit_table_module` | Modify data table module information | `references/system_edit_table_module.json` MUST READ |

### Workflow - Bpmn (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_bpmn_create_module` | Create workflow module | `references/system_bpmn_create_module.json` MUST READ |
| [Designer] | `_bpmn_create_process_define` | Create process definition | `references/system_bpmn_create_process_define.json` MUST READ |
| [Designer] | `_bpmn_update_start_setting` | Update process start configuration | `references/system_bpmn_update_start_setting.json` MUST READ |
| [Designer] | `_bpmn_create_or_update_node` | Create/update process node | `references/system_bpmn_create_or_update_node.json` MUST READ |
| [Designer] | `_bpmn_create_or_update_flow` | Create/update sequence flow | `references/system_bpmn_create_or_update_flow.json` MUST READ |
| [Designer] | `_bpmn_delete_node` | Delete process node | `references/system_bpmn_delete_node.json` MUST READ |
| [Designer] | `_bpmn_delete_flow` | Delete sequence flow | `references/system_bpmn_delete_flow.json` MUST READ |
| [Designer] | `_bpmn_query_process_define` | Query process definition details | `references/system_bpmn_query_process_define.json` MUST READ |
| [Designer] | `_bpmn_query_process_define_list` | Query process definition list under module | `references/system_bpmn_query_process_define_list.json` MUST READ |

### Automation - Automatic (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_automatic_create_group` | Create automation group (query _query_app_define_designer first to avoid duplication) | `references/system_automatic_create_group.json` MUST READ |
| [Designer] | `_automatic_delete_group` | Delete automation group | `references/system_automatic_delete_group.json` MUST READ |
| [Designer] | `_automatic_update_group` | Edit automation group | `references/system_automatic_update_group.json` MUST READ |
| [Designer] | `_automatic_save_define` | Save automation configuration (must query table structure to get field IDs before creation) | `references/system_automatic_save_define.json` MUST READ |
| [Designer] | `_automatic_query_define` | Query automation configuration | `references/system_automatic_query_define.json` MUST READ |
| [Designer] | `_automatic_run_once` | Execute automation immediately (high risk, confirm first) | `references/system_automatic_run_once.json` MUST READ |
| [Designer] | `_automatic_doc` | Read automation documentation | none |

### Dashboard (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_create_dashboard_module` | Create dashboard module | `references/system_create_dashboard_module.json` MUST READ |
| [Designer] | `_query_dashboard_list_designer` | Query all dashboards | none |
| [Designer] | `_query_dashboard_card_list` | Query dashboard card list | `references/system_query_dashboard_card_list.json` MUST READ |
| [Designer] | `_query_dashboard_card_detail` | Query card details | `references/system_query_dashboard_card_detail.json` MUST READ |
| [Designer] | `_delete_dashboard_card` | Delete dashboard card | `references/system_delete_dashboard_card.json` MUST READ |
| [Designer] | `_save_dashboard_number_card` | Create/edit number card (query table structure to get field IDs first) | `references/system_save_dashboard_number_card.json` MUST READ |
| [Designer] | `_save_dashboard_prochart_card` | Create/edit chart card (query table structure to get field IDs first) | `references/system_save_dashboard_prochart_card.json` MUST READ |
| [Designer] | `_save_dashboard_record_card` | Create/edit record card (Record type, displays data source table records with filter/sort/column config/pagination, columnList required) | `references/system_save_dashboard_record_card.json` MUST READ |
| [Designer] | `_save_dashboard_pivot_card` | Create/edit pivot card (Pivot type, cross-grouping by row/column dimensions with value field aggregation, colFieldId required) | `references/system_save_dashboard_pivot_card.json` MUST READ |
| [Designer] | `_save_dashboard_table_card` | Create/edit table card (Table type, data source is automation or expression, does not read data tables directly) | `references/system_save_dashboard_table_card.json` MUST READ |
| [Designer] | `_read_informat_dashboard_document` | Informat dashboard chart documentation | none |
| [Designer] | `_read_informat_dashboard_ui_preset` | Read dashboard UI preset documentation (7 theme palettes, 6 layout templates, card style presets, beautified defaults per chart type; must call before every card create/edit) | none |

### Script (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_create_informat_script_directory` | Create script directory | `references/system_create_informat_script_directory.json` MUST READ |
| [Designer] | `_save_informat_script` | Save script (must pass existing ID when editing) | `references/system_save_informat_script.json` MUST READ |
| [Designer] | `_query_informat_script_list` | Query script list | none |
| [Designer] | `_query_informat_script_content` | Query script content | `references/system_query_informat_script_content.json` MUST READ |
| [Designer] | `_execute_informat_script_designer` | Execute script in designer | `references/system_execute_informat_script_designer.json` MUST READ |
| [Designer] | `_script_save_git_config` | Save script Git repository configuration | `references/system_script_save_git_config.json` MUST READ |
| [Designer] | `_script_pull_from_git` | Pull scripts from Git repository to application | none |
| [Designer] | `_script_push_to_git` | Push application scripts to Git repository | `references/system_script_push_to_git.json` MUST READ |

### Scheduled Task - Schedule (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_schedule_create_define` | Create scheduled task | `references/system_schedule_create_define.json` MUST READ |
| [Designer] | `_schedule_update_define` | Update scheduled task | `references/system_schedule_update_define.json` MUST READ |
| [Designer] | `_schedule_delete_define` | Delete scheduled task | `references/system_schedule_delete_define.json` MUST READ |
| [Designer] | `_schedule_query_define_designer` | Query scheduled task details | `references/system_schedule_query_define_designer.json` MUST READ |
| [Designer] | `_schedule_query_define_list` | Query scheduled task list | none |
| [Designer] | `_schedule_run_once` | Trigger once immediately | `references/system_schedule_run_once.json` MUST READ |
| [Designer] | `_schedule_doc` | Query scheduled task documentation | none |

### Internationalization - I18n (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_i18n_query_define_designer` | Query internationalization configuration | none |
| [Designer] | `_i18n_save_define_designer` | Save translation definition | `references/system_i18n_save_define_designer.json` MUST READ |
| [Designer] | `_i18n_save_locale_designer` | Save language list | `references/system_i18n_save_locale_designer.json` MUST READ |
| [Designer] | `_i18n_set_app_name` | Set application internationalized name | `references/system_i18n_set_app_name.json` MUST READ |
| [Designer] | `_i18n_set_module_name` | Set module internationalized name | `references/system_i18n_set_module_name.json` MUST READ |
| [Designer] | `_i18n_set_table_field_name` | Set field internationalized name | `references/system_i18n_set_table_field_name.json` MUST READ |
| [Designer] | `_i18n_set_field_option_name` | Set option value internationalized name | `references/system_i18n_set_field_option_name.json` MUST READ |

### Website Resource - Website (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_website_create_module` | Create website module (query first to avoid duplication) | `references/system_website_create_module.json` MUST READ |
| [Designer] | `_website_create_directory` | Create resource directory | `references/system_website_create_directory.json` MUST READ |
| [Designer] | `_website_save_resource` | Create/edit resource (query ID first when editing) | `references/system_website_save_resource.json` MUST READ |
| [Designer] | `_website_delete_resource` | Delete resource | `references/system_website_delete_resource.json` MUST READ |
| [Designer] | `_website_query_define_designer` | Query website module details | `references/system_website_query_define_designer.json` MUST READ |
| [Designer] | `_website_query_list_designer` | Query all website modules | none |
| [Designer] | `_website_query_resource` | Query resource details | `references/system_website_query_resource.json` MUST READ |
| [Designer] | `_website_preview` | Preview website | `references/system_website_preview.json` MUST READ |
| [Designer] | `_website_read_informat_doc` | Read website designer documentation | none |
| [Designer] | `_codestudio_list_modules` | List existing AICodeStudio modules of the current app (query before creating; reuse when possible) | none |
| [Designer] | `_codestudio_create_module` | Create AICodeStudio module (full Vue3 project, returns moduleId) | `references/system_codestudio_create_module.json` MUST READ |
| [Designer] | `_codestudio_list_files` | List all source files of the module | `references/system_codestudio_list_files.json` MUST READ |
| [Designer] | `_codestudio_read_file` | Read a single source file | `references/system_codestudio_read_file.json` MUST READ |
| [Designer] | `_codestudio_write_file` | Create/overwrite a single source file | `references/system_codestudio_write_file.json` MUST READ |
| [Designer] | `_codestudio_create_script` | Create/update a script for the module (auto ai_{moduleId}_ prefix + comment + group) | `references/system_codestudio_create_script.json` MUST READ |
| [Designer] | `_codestudio_create_api` | Create/update an API for the module (auto ai/{moduleId}/ prefix + group) | `references/system_codestudio_create_api.json` MUST READ |
| [Designer] | `_codestudio_compile` | Compile and return structured build errors (always call after writing; self-fix from errors) | `references/system_codestudio_compile.json` MUST READ |
| [Designer] | `_codestudio_preview` | Get the preview URL | `references/system_codestudio_preview.json` MUST READ |

> **Frontend/website choice guidance:** For interactive, component-based frontends with routing/state/charts → **prefer `_codestudio_*` (AICodeStudio, full Vue3 project)**; use `_website_*` only for purely static display pages. Pick one per requirement; do not mix.
> **★ Query before creating:** Before calling `_codestudio_create_module`, you **MUST** first call `_codestudio_list_modules` to check whether the current app already has a suitable AICodeStudio module — reuse its moduleId if so. **Do not create duplicate modules in the same app.**
> **★★ Before building a codestudio app, you MUST read `references/doc/markdown/informat.codestudio.md` in full** (the end-to-end guide: create module → query tables → create scripts → create APIs → write Vue → compile → preview, covering script signature / error envelope / callApi unwrap / file-write boundary / npm whitelist and every known pitfall). Calling `_codestudio_*` without reading it almost always fails.
> **★ codestudio data-binding rule:** When a codestudio module needs to read/write platform table data, scripts/APIs **MUST** be created via `_codestudio_create_script` / `_codestudio_create_api` (backend auto-applies the `ai_{moduleId}_` / `ai/{moduleId}/` prefix + grouping, and same-name scripts / same-path APIs update the original resource). Do **NOT** use raw `_save_informat_script` / `_api_create_define`, and do **NOT** create `xxx2/list2` to bypass duplicates — otherwise resources won't be attributed to the module or will pollute the app with duplicates. In Vue, `callApi(path)` uses the full path returned by `_codestudio_create_api`.

### AI Assistant (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_aiassistant_create` | Create AI assistant module | `references/system_aiassistant_create.json` MUST READ |
| [Designer] | `_aiassistant_update` | Update AI assistant module | `references/system_aiassistant_update.json` MUST READ |
| [Designer] | `_aiassistant_delete` | Delete AI assistant module | `references/system_aiassistant_delete.json` MUST READ |
| [Designer] | `_aiassistant_doc` | Query AI assistant documentation | none |

### App Listener (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_app_listener_create` | Create a new listener definition | `references/system_app_listener_create.json` MUST READ |
| [Designer] | `_app_listener_update` | Update listener definition, updateFieldList declares fields to modify | `references/system_app_listener_update.json` MUST READ |
| [Designer] | `_app_listener_delete` | Delete listener definition (if it's a directory, all listeners under it will also be deleted) | `references/system_app_listener_delete.json` MUST READ |
| [Designer] | `_app_listener_list` | Query listener definition list under current application (tree structure, includes directories and sub-listeners) | none |

### Survey (Designer)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_survey_create_module` | Create survey module | `references/system_survey_create_module.json` MUST READ |
| [Designer] | `_survey_create_item` | Create survey question | `references/system_survey_create_item.json` MUST READ |
| [Designer] | `_survey_update_item` | Update survey question | `references/system_survey_update_item.json` MUST READ |
| [Designer] | `_survey_delete_item` | Delete survey question | `references/system_survey_delete_item.json` MUST READ |
| [Designer] | `_survey_query_define_designer` | Query survey configuration | `references/system_survey_query_define_designer.json` MUST READ |

### App (User)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [User] | `_query_app_define` | Query published application configuration (module list, roles, APIs, etc.) | none |
| [User] | `_query_app_user` | Query current user's roles and permissions in this application (admin has all permissions without permissionList; non-admin returns moduleKey_PermissionName format) | none |
| [User] | `_query_app_user_list` | Query account information (ID, email, supervisor, department) | `references/system_query_app_user_list.json` MUST READ |
| [Team] | `_wb_create_user_schedule` | Create a team scheduled task (UserSchedule/t_user_schedule), not an application designer scheduled task | `references/system_wb_create_user_schedule.json` MUST READ |
| [User] | `_app_member_create` | Add existing team members to the current application | `references/system_app_member_create.json` MUST READ |
| [User] | `_app_member_update` | Update application member role information | `references/system_app_member_update.json` MUST READ |
| [User] | `_app_member_delete` | Remove a member from the current application (dangerous operation) | `references/system_app_member_delete.json` MUST READ |

### Data Table - Table (User)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [User] | `_query_all_table_list` | Query all published data tables (does not return field structure) | none |
| [User] | `_query_table_define` | Query published table field structure (for record operations) | `references/system_query_table_define.json` MUST READ |
| [User] | `_query_table_record_list` | Query data table records by condition | `references/system_query_table_record_list.json` MUST READ |
| [User] | `_query_table_record_list_count` | Count records matching conditions | `references/system_query_table_record_list_count.json` MUST READ |
| [User] | `_table_record_batch_insert` | Batch insert records (query table structure to get field IDs first) | `references/system_table_record_batch_insert.json` MUST READ |
| [User] | `_table_record_batch_update` | Batch update records | `references/system_table_record_batch_update.json` MUST READ |
| [User] | `_table_record_batch_delete` | Batch delete records (dangerous operation) | `references/system_table_record_batch_delete.json` MUST READ |

### Workflow - Bpmn (User)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [User] | `_bpmn_create_instance` | Create and start workflow process instance (query process definition first) | `references/system_bpmn_create_instance.json` MUST READ |
| [User] | `_bpmn_query_instance_list` | Query process instances initiated by current user | `references/system_bpmn_query_instance_list.json` MUST READ |
| [User] | `_bpmn_query_instance_info` | Query process instance details | `references/system_bpmn_query_instance_info.json` MUST READ |
| [User] | `_bpmn_query_task_list` | Query workflow tasks assigned to current user | `references/system_bpmn_query_task_list.json` MUST READ |
| [User] | `_bpmn_query_task_info` | Query workflow task details | `references/system_bpmn_query_task_info.json` MUST READ |
| [User] | `_bpmn_complete_task` | Complete (approve) workflow task | `references/system_bpmn_complete_task.json` MUST READ |
| [User] | `_bpmn_process_define_list` | Get process definition list | none |
| [User] | `_bpmn_get_process_define` | Get process definition details | `references/system_bpmn_get_process_define.json` MUST READ |

### Search Engine - Textindex (User)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [User] | `_query_all_textindex_list` | Query search engine module list | none |
| [User] | `_textindex_search` | Search engine keyword search | `references/system_textindex_search.json` MUST READ |

### Knowledge Base - Knowledgebase (User)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [User] | `_knowledgebase_search` | Knowledge base keyword search | `references/system_knowledgebase_search.json` MUST READ |

### Notification (User)

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [User] | `_send_notification` | Send in-app notification | `references/system_send_notification.json` MUST READ |


## Common Agent Method List

> The following methods do not require `--appId`, call them directly.

| Side | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Common] | `_app_get_web_url` | Get application Web root URL | none |
| [Common] | `_app_doc` | Query application documentation | none |
| [Common] | `_javascript_eval` | Execute JavaScript code | `references/system_javascript_eval.json` MUST READ |
| [Common] | `_render_html` | Render HTML content | `references/system_render_html.json` MUST READ |
| [Common] | `_web_content` | Get web URL content | `references/system_web_content.json` MUST READ |
| [Common] | `_get_current_time` | Get current time | none |
| [Common] | `_get_current_user` | Get current user | none |
| [Common] | `_read_informat_expression_doc` | Informat expression documentation | none |
| [Common] | `_read_informat_script_sdk` | Informat script SDK documentation | none |
| [Common] | `_list_informat_markdown` | List all available Markdown documents | none |
| [Common] | `_read_informat_markdown` | Read specified Markdown document content (supports subdirectories like script/) | `references/system_read_informat_markdown.json` MUST READ |
| [Common] | `_read_office_file` | Read Office document content | `references/system_read_office_file.json` MUST READ |
| [Common] | `_send_system_email` | Send email | `references/system_send_system_email.json` MUST READ |

> Note: `_send_notification` (send notification) and `_read_informat_dashboard_document` (dashboard documentation) are Application Agent methods and must be called with `--appId`.

## Local Reference Documentation

Consult directly without API calls, under `{baseDir}/references/doc/` directory:

**Core Feature Documentation (`doc/markdown/` directory)**:

| Document Filename | Description |
|-----------|------|
| `informat.aiassistant.md` | AI Assistant Development Documentation |
| `informat.api.md` | Open API Documentation |
| `informat.app.md` | Application Documentation |
| `informat.bpmn.md` | Workflow design doc (six-step creation order + approval-node depth config + branching gateways + countersign/or-sign + x/y layout + table start button; must-read before building a workflow; calling `_bpmn_*` is gated by the doc-read gate) |
| `informat.app.role.md` | Application Role Permission Documentation |
| `informat.app.themestyle.md` | Application Theme Style Documentation |
| `informat.automatic.md` | Automation Process Documentation |
| `informat.company.md` | Team Documentation (members, roles, organization structure) |
| `informat.dashboard.md` | Dashboard Development Documentation |
| `informat.dashboard.uipreset.md` | Dashboard UI Preset Documentation (theme palettes, layout templates, card style presets) |
| `informat.expression.md` | Expression Syntax Documentation |
| `informat.listeners.md` | App Listener Documentation |
| `informat.schedule.md` | Scheduled Task Documentation |
| `informat.script.md` | Script Development Overview |
| `informat.table.md` | Data Table Design Documentation |
| `informat.website.md` | Website Designer Documentation |
| `informat.codestudio.md` | AI Code Studio end-to-end guide (build a full Vue app via `_codestudio_*`: module→script→API→Vue→compile→preview) |

**Script API Documentation (`doc/markdown/script/` directory)**: Categorized by module (bpmn.md, table.md, http.md, etc.), with method descriptions, parameter definitions, and sample code.

## FAQ

**Q: Application module identifier already exists?** The module ID is already in use, you need to use a different one.

**Q: How to get the module list of an application?** Use `_query_app_define_designer`.

**Q: Application access URL?** `{host}/app/{appId}`
