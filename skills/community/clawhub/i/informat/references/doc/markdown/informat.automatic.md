<!-- DOCKEY: auto-7b3e8 -->
This document is the automation documentation for the Informat low-code platform.

## Overview
An Informat automation is **a list of steps**. Each step is either an **interactive step** (`type` starts with `Output`, requires user interaction such as opening a form, confirmation dialog, upload, scan, or starting a workflow) or a **non-interactive step** (control flow, script invocation, etc.). A complete automation is typically composed of multiple step types interleaved together.
If the automation involves data table operations, you must consult the data table documentation.

## Finishing rules (creating the automation is not the end; an unbound automation is invalid configuration that never runs)

The following are two common half-finished defects; both must be avoided:

### 1. After creating an automation, a trigger entry must be bound

An automation created via `_automatic_save_define` with no trigger attached **will never execute**. After creating it, **bind** at least one of the following trigger entries (choose by need):

| Trigger scenario | How to bind |
|------------------|-------------|
| User clicks a button in the data table list | `_table_create_tool_bar_button`, `action="CallAutomatic"`, `actionSetting.automaticId` = this automation id (see "Calling an automation from a data table toolbar button" below) |
| User clicks a button inside a record form | `_table_create_form_tool_bar_btn`, also `action="CallAutomatic"` |
| Auto-trigger on data change (after create/update/delete) | Configure a listener (`AppEvent` event, e.g. `record.create.after`); server-side, `Output*` forbidden |
| Time-based trigger | A scheduled task (`_schedule_*`) calls this automation |
| Workflow event trigger | Workflow listener `BpmnListenerSetting` / user-task `completeAutomaticId` bound to this automation |

> **A client interactive automation (containing any `Output*` step) is bound to a toolbar or form button by default** — only a button trigger is client-side execution that can present UI. An automation with `Output*` steps but no button binding cannot run.

### 2. Prefer built-in steps; avoid defaulting everything to `CallScript`

"Start a workflow", "open a create-record form", "upload a file", "confirmation dialog", "Toast" — the platform has **dedicated built-in steps** for all of these (`OutputBpmnProcess` / `OutputRecordCreate` / `OutputUpload` / `OutputConfirm` / `OutputToast` …). **Prefer the built-in step**; do not write everything as `CallScript`. In particular:

- **"Let the user start a workflow" → use `OutputBpmnProcess`** (opens the start-form dialog), not CallScript.
- **"Silently start a workflow in the background" (server-side) → start the process via the `informat.bpmn.*` API inside a `CallScript` script**.
- Only "data CRUD / HTTP / SSH / AI calls / complex computation" — pure back-end logic with no ready-made built-in step — should use `CallScript`.

See "Key decisions" and the "step whitelist" below for the decision tree and the legal types.

### 3. Ordering: build dependencies first, then query real IDs to fill each step (no empty references)

Almost every automation step references the real ID of another component (workflow module, process define, data table, script function). Those IDs can only be queried after the corresponding component exists, therefore:

- **An automation must be orchestrated AFTER all the components it depends on (tables / workflows / scripts) are built**; it is among the last things built in the whole app.
- **Before writing each step, query the real ID of the referenced object** (e.g. query the workflow module define for `bpmnModuleId` / `bpmnProcessDefineId`, the script list for `scriptId`, the table for `tableId`) and put the exact value into the step setting. **Never leave it empty or use a placeholder.**
- On save, `call_informat.js` validates each step's required references against the schema and rejects empty ones (exit 10).

Common empty-reference anti-patterns (all rejected — avoid each):

| Step | Required references (must not be empty) |
|------|-----------------------------------------|
| `OutputBpmnProcess` (start a workflow) | `bpmnModuleId` + `bpmnProcessDefineId` + `bpmnProcessStartFormTableId` + `bpmnProcessStartFormFieldList` |
| `OutputRecordCreate` (create-record dialog) | `recordCreateTableId` (table ID) |
| `CallScript` (call a script) | `scriptId` + `func` |
| `SetReturnValue` (set return value) | `valueVar` (return-value expression) |
| `OutputToast` (show a toast) | `toastValueVar` (toast-content expression) — an empty content shows nothing |
| `OutputConfirm` (confirm dialog) | `confirmTitleVar` or `confirmDialogTitleVar` (at least one carries the prompt text) — an empty content pops a blank confirm dialog |
| `OutputNotification` (notification) | `messageVar` or `message` (at least one carries the body) |
| `If` (condition) | `expression`, and it must contain both an `If.true` and an `If.false` child branch (with real steps inside) |

> An automation that contains only empty steps, empty expressions, empty return values, or **empty display content** has no logic; when orchestrating, make every step's reference and display text resolve to real content — an interaction-output step (toast / confirm / notification) with empty content just pops a blank box on the client.

---

### 🖥️ Execution Environment · Client-side vs Server-side (Determines Whether `Output*` Steps Are Allowed)

Automations run in two environments, **and this determines which steps can be used**. Before designing the flow, identify which environment the current automation belongs to:

| Environment | Typical Trigger | Can Use `Output*` Interactive Steps |
|------|---------------|----------------------------|
| **Client-side** | Automation bound to a control button (triggered by button click) | ✅ Allowed |
| **Server-side** | Scheduled tasks, listeners (e.g. `record.insert.after`), workflow task completion callbacks, HTTP callbacks, and any **non-button-triggered** automation | ❌ **All `Output*` steps forbidden** — no UI exists on the server |

> **Decision rule**: Is the automation bound to a control button? Yes → client-side; No → server-side.

#### Server-side Execution Constraints (Critical)

Server-side automations may **only use non-interactive steps**: `If` / `If.true` / `If.false` / `ForEach` / `While` / `CallScript` / `SetReturnValue`. All `Output*` steps are forbidden because no user interface exists on the server.

If a server-side requirement appears to "need interaction" (e.g. "send a notification to the requester after creating a record"), it is actually not interaction — notifications, database writes, etc. must be done via `CallScript` invoking script-side server APIs (such as `notify`, `model.insert`).

> **Going further**: If a server-side automation consists entirely of `CallScript` calls with no control flow branches, you should consider writing it as a script module directly instead of as an automation.

---

### ⛔ Critical Decision · Three-Layer Judgment (Environment → Intent → Ask When Ambiguous)

#### Layer 1 · Check the Execution Environment

| Environment | Allowed Steps |
|------|------------|
| Client-side (button-triggered) | All interactive steps + all non-interactive steps |
| Server-side (scheduled / listener / workflow callback, etc.) | **Only** non-interactive steps (control flow + `CallScript` + `SetReturnValue`) |

**If server-side, skip "Path A" in Layer 2 and go directly to "Path B".**

#### Layer 2 · Choose Step by Intent (Only When Client-Side Execution)

When you receive a requirement, **do not associate types by noun matching** ("create record" ≠ `InsertRecord`, "workflow" ≠ `CreateBpmnProcess`). First answer:

> **Does this step require user interaction with the UI?** (clicking, filling out a form, confirming, selecting a file, scanning, etc.)

##### Path A · User Interaction Needed → Find the Best `Output*` Step in the Whitelist

Many requirements that look like "data writes / workflow operations" already have **dedicated interactive steps** that should be preferred:

| Requirement | Interactive Step (do not go through CallScript) |
|---------|-----------------------------------------|
| Let the user fill out a form to create a record | `OutputRecordCreate` (opens the create-record form dialog; the platform persists it for you) |
| Let the user fill a lightweight form (not necessarily backed by a data table) | `OutputDynamicForm` (custom-field form dialog) |
| Let the user upload a file / Excel | `OutputUpload` / `OutputUploadExcel` |
| Let the user pick a record from a list | `OutputRecordSelect` |
| Let the user start a workflow | `OutputBpmnProcess` (opens the workflow start-form dialog) |
| Let the user view a workflow task / instance detail | `OutputBpmnTaskInfo` / `OutputBpmnInstanceInfo` |
| Let the user confirm / see a Toast or notification | `OutputConfirm` / `OutputToast` / `OutputNotification` |

The full whitelist of interactive steps is in the "Automation Steps" section below.

##### Path B · No Interaction Needed (Pure Backend Logic) → `CallScript`

Data CRUD, HTTP, SSH, variable computation, AI invocation — anything that **does not involve user interaction** — uses `CallScript` to call functions in script modules.

> ⚠️ **The `scriptId` of `CallScript` is the ID of the .js file itself, NOT the directory/group ID**. After creating a new script, you must call `_query_informat_script_list` again to retrieve the corresponding .js file ID before filling in `scriptId` — the `parentId` you passed to `_save_informat_script` is the directory ID that contains the script, **not the `scriptId`**.

#### Layer 3 · Ambiguous Intent? Ask the User First, Don't Guess

In client-side automations, some verbs have both "frontend interaction" and "silent backend" implementations. **When intent is unclear, do not guess — ask the user first.**

##### Clear Requirements (Choose Directly, No Need to Ask)

When the requirement contains the following **frontend-interaction-specific verbs**, intent clearly points to interactive steps:

| Clear Verb | Choose Directly |
|---------|---------|
| "**Open** the create-record dialog" / "**Pop up** a create form" | `OutputRecordCreate` |
| "**Let the user fill** a form to create / edit a record" | `OutputRecordCreate` / `OutputRecordInfo` / `OutputDynamicForm` |
| "**Pop up** a confirmation dialog" | `OutputConfirm` |
| "**Let the user upload** a file" | `OutputUpload` |
| "**Show** a Toast / notification" | `OutputToast` / `OutputNotification` |
| "**Open** the workflow start form" / "**Let the user start** a workflow" | `OutputBpmnProcess` |

When the requirement contains the following **backend verbs**, intent clearly points to `CallScript`:

| Clear Verb | Choose Directly |
|---------|---------|
| "**Silently** create a record" / "**Directly** write a row of data" | `CallScript` |
| "**Automatically** update a field" / "**Background** sync" | `CallScript` |
| "**Call** an HTTP API" / "**Call** an AI" | `CallScript` |

##### Ambiguous Requirements (Must Ask First)

When the requirement only contains **neutral verbs** like "create / update / delete / query / start workflow" without explicitly indicating "whether a dialog / user form is needed", **stop and ask the user**, do not choose on your own.

| Ambiguous Requirement | Ask the User | Two Possible Implementations |
|---------|----------|--------------|
| "Create a record" | "Should a form dialog pop up for the user to fill in and save (A), or should it be silently created with preset fields (B)?" | A → `OutputRecordCreate`; B → `CallScript` |
| "Update this record" | "Should an edit form pop up (A), or should it be updated by rule in the background (B)?" | A → `OutputRecordInfo`; B → `CallScript` |
| "Start a workflow" | "Should the start form pop up for user input (A), or should it be started in the background with preset variables (B)?" | A → `OutputBpmnProcess`; B → `CallScript` |
| "Upload a file" | "Should the user pick a file to upload (A), or pull data from an existing source / URL and store it (B)?" | A → `OutputUpload`; B → `CallScript` |
| "Select a record" | "Should a dialog pop up for the user to pick (A), or should it be fetched in the background by filter (B)?" | A → `OutputRecordSelect`; B → `CallScript` |

> **Special case**: If the environment is server-side, ignore option A and go directly to B (`CallScript`), but it's still recommended to inform the user "Since this automation runs server-side (e.g. scheduled task), no dialog is possible — it will be created directly in the background."

> **Sample wording for asking the user**:
> "Your requirement mentions 'create a record' — would you like (A) a form dialog for the user to fill out and save, or (B) the automation to silently create with preset fields? The implementations differ — please confirm."

#### Decision Examples

| Requirement | Wrong Choice | Correct Choice | Reason |
|------|---------|---------|------|
| "**Open** the create-record dialog → Toast after creation" | `OutputDynamicForm` + `InsertRecord` | `OutputRecordCreate` + `OutputToast` | "Open" clearly indicates frontend interaction; `OutputRecordCreate` is a one-stop solution |
| "User clicks button → **Create a** project record → Toast" | Choose any single implementation | First ask the user: "Pop up a form for the user, or silently create with preset fields?" | No "open / pop up" mentioned, ambiguous, must confirm |
| "User fills form → **Start** a leave-of-absence workflow" | `OutputDynamicForm` + `CreateBpmnProcess` | Use `OutputBpmnProcess` directly | The platform already provides a dedicated interactive step for "user starts workflow" |
| "Daily sync external API data into records" | `Http` + `InsertRecord` step | Server-side → `CallScript` (script does request + DB write) | Scheduled tasks are server-side, `Output*` is forbidden; and `Http` / `InsertRecord` are not legal step types |
| "Pop up notifying the user '5 new tickets', requires querying DB first" | `QueryRecordList` + `OutputToast` | `CallScript` (script uses `model.query` to get count) + `OutputToast` | "Pop up" → client-side; `QueryRecordList` is not a legal step type, query logic goes inside `CallScript` |
| "Send a notification to the applicant after a workflow task completes" | `OutputNotification` | Server-side → use server-side `notify` API in the script invoked by `CallScript` | Workflow task callback is server-side, all `Output*` forbidden |

---

### 🚫 Severe Error List · These Types Cannot Be Automation Steps

The following types are **not legal automation steps** and cannot appear directly in `funcSettingList`:

| Category | Wrong type (cannot be a step) | Correct Replacement in Automation |
|------|------------------------|------------------|
| Data CRUD | `InsertRecord` `UpdateRecord` `DeleteRecord` `QueryRecord` `QueryRecordList` `QueryRecordRelList` `QueryRecordListCount` `QueryRecordRelListCount` `UpdateLookupRollup` | If user form input is needed: `OutputRecordCreate` / `OutputRecordInfo` / `OutputDynamicForm`; for silent backend: `CallScript` (script calls `model.insert/update/delete/query`) |
| Network/System | `Http` `SshRequest` | `CallScript` (script makes the request) |
| Variables and flow internals | `SetVar` `UpdateVar` `Abort` `Log` `Sleep` `Notification` `SetAppBadge` `PublishAppEvent` `PushEvent` `SetModuleAlert` | `CallScript`; variable passing within an automation goes through step `retValues` + `${name}` references |
| Workflow write operations | `CreateBpmnProcess` `SetBpmnVar` `GetBpmnVar` `BpmnQueryInstance` `BpmnQueryTask` `SetBpmnAssignee` `SetBpmnChangeActivity` `SetBpmnRevoke` `SetBpmnDelete` `BpmnDeleteTask` `SetBpmnTaskComplete` `BpmnSendSignal` `BpmnSendMessage` `BpmnTrigger` | If user start / view workflow: `OutputBpmnProcess` / `OutputBpmnTaskInfo` / `OutputBpmnInstanceInfo` / `OutputBpmnEvent`; for silent backend: `CallScript` |
| AI invocation | `CallAI` `OpenAIChatGpt` | `CallScript` (script invokes AI) |

> **Decision order**:
> ① **Is the current automation client-side or server-side?** Server-side → jump to ③, all `Output*` forbidden.
> ② **Does this step's intent require user interaction?** Ambiguous requirements (like "create a record") must ask the user first, do not guess.
> ③ **Final landing**: a whitelisted `Output*` (client-side only) or `CallScript`. **Never any type from the table above.**

---

### ✅ Wrong vs Right · Complete Comparison Examples

**Business requirement**: User fills a form → create a project record → show success message

#### ❌ Wrong (treating InsertRecord as a step)

```jsonc
{
  "funcSettingList": [
    { "type": "OutputDynamicForm",  "outputDynamicFormFuncSetting": { /* ... */ } },
    { "type": "InsertRecord",       "insertRecordFuncSetting": { /* ... */ } },  // ← Severe error: InsertRecord is not a legal step type
    { "type": "OutputToast",        "outputToastFuncSetting": { /* ... */ } }
  ]
}
```

What's wrong: `InsertRecord` is not in the legal step type whitelist. Whether the setting field is named `insertRecordSetting` or `insertRecordFuncSetting` doesn't matter — both invalid. **Moreover, this requirement doesn't need `CallScript` at all** — the platform already has a dedicated "open create-record form" interactive step.

#### ✅ Solution 0 · Best: Use `OutputRecordCreate` Directly (One-Stop Interaction)

`OutputRecordCreate` is itself the complete interaction "open create-record form dialog + user fills in + platform saves". It is the optimal solution for this kind of requirement:

```jsonc
{
  "funcSettingList": [
    {
      "type": "OutputRecordCreate",
      "retValues": [{ "id": "result", "name": "newProject" }],
      "outputRecordCreateFuncSetting": {
        "tableId": "project",
        "recordCreateSubmitType": "Create"
        /* The platform reads the project table's field definitions and auto-generates the form */
      }
    },
    {
      "type": "OutputToast",
      "outputToastFuncSetting": {
        "toastValueVar": "${String.concat('Project created - ', newProject.name)}"
      }
    }
  ]
}
```

#### ✅ Solution A · Fallback: Custom Form + `CallScript`

Only when `OutputRecordCreate` doesn't meet the requirement (e.g. form fields don't fully match data table fields, or complex preprocessing is required before the DB write) should you take this path.

Step 1: Write a function in a script module

```javascript
// createProject function in scriptId = "projectScript"
const createProject = (formData) => {
    return model.insert("project", {
        name: formData.projectName,
        budgetCode: formData.budgetCode,
        pm: formData.projectManager,
        status: formData.projectStatus
    });
};
```

Step 2: In the automation use `OutputDynamicForm` to collect data + `CallScript` to call the script and write to DB

```jsonc
{
  "funcSettingList": [
    {
      "type": "OutputDynamicForm",
      "retValues": [{ "id": "result", "name": "formData" }],
      "outputDynamicFormFuncSetting": { /* must follow "minimum viable skeleton": include UI fields like dynamicFormStyle/dynamicFormFieldStyle/dynamicFormStyleWidth/dynamicFormStyleWidthUnit, see "Dialog/Form Step Required Settings Reminder" below */ }
    },
    {
      "type": "CallScript",
      "retValues": [{ "id": "result", "name": "newProject" }],
      "callScriptFuncSetting": {
        "scriptId": "projectScript",
        "func": "createProject",
        "args": [{ "valueVar": "${formData}" }]
      }
    },
    {
      "type": "OutputToast",
      "outputToastFuncSetting": {
        "toastValueVar": "${String.concat('Project created - ', formData.projectName)}"
      }
    }
  ]
}
```

> **Solution selection summary**: First check the interactive step whitelist for an existing fit (Solution 0), use it if available; otherwise go through `CallScript` (Solution A).

---

An automation is similar to a function whose parameters are an array of objects. The caller passes parameters to the automation, which executes specific actions and returns results to the caller. **Regardless of how the automation is invoked (HTTP call, toolbar button, listener, automation step, etc.), the number of input parameters passed in must equal the length of the automation's `varList`, otherwise parameter mapping fails.**

## Input Parameters (varList)

Input parameters are passed by `varList` definition when calling an automation. Each parameter consists of `id` and `name`:

- **`id`** is the platform-preset **parameter type identifier** (such as `String`, `Integer`, `Array<Record>`, `HttpRequest`, etc.). Like `retValues`'s `id`, it **cannot be modified**. It determines what data the parameter can accept and what methods can be called on it in expressions.
- **`name`** is the **user-defined parameter name** used to reference it in expressions. Subsequent steps read parameter values via `${name}`.
- All `name` values within the same automation must be unique; duplicate `name` (even with different `id`) causes reference ambiguity and must be avoided.
- The same `id` may appear multiple times in `varList` (distinguished by different `name`s carrying different semantics) — for example, `Record` can serve both as "data table record" and "dashboard filter condition".
- Input parameters map by position to caller-passed parameters: the first passed parameter corresponds to `varList[0]`, and so on. **The number of passed parameters must equal `varList` length**, otherwise mapping fails.

### Reference Example

```jsonc
// varList definition
[
  { "id": "Record",         "name": "currentRecord",   "optional": false },
  { "id": "Array<Record>",  "name": "selectedRecords", "optional": false },
  { "id": "BpmnEvent",      "name": "workflowEvent",   "optional": false }
]
```

Subsequent steps can read these parameters via `${currentRecord.title}`, `${selectedRecords.size()}`, `${workflowEvent.id}`.

### Supported Type List

Grouped by use, all usable as `varList[].id`:

#### Basic Types

| id | Meaning | Expression Example |
|----|------|----------|
| `String` | String | `${name}`, `${String.concat('prefix-', name)}` |
| `Integer` | Integer | `${count + 1}`, `${count > 0}` |
| `Double` | Decimal | `${amount * 1.13}` |
| `Boolean` | Boolean | `${enabled ? 'on' : 'off'}` |
| `Object` | Generic object | `${object.fieldA}` |

#### Collection Types

| id | Meaning |
|----|------|
| `Array<String>` | String array |
| `Array<Object>` | Object array |
| `Array<Record>` | Data table record list |
| `Array<Task>` | Workflow task list |
| `Array<Instance>` | Workflow instance list |

#### Business Object Types

| id | Meaning |
|----|------|
| `Record` | Data table record (also used for "dashboard filter conditions" and other scenarios that carry structured records) |
| `UploadFile` | Uploaded file |
| `Task` | Workflow task |
| `Instance` | Workflow instance |

#### Request / Invocation Context Types

| id | Meaning |
|----|------|
| `HttpRequest` | HTTP request (input when automation is HTTP-triggered) |
| `DesignerRequest` | Print template HTTP request |
| `MqMessage` | Message queue message |
| `WebsiteDynamicInvokeContext` | Website page dynamic rendering context |
| `PageDesignerPageData` | URL parameters for accessing custom UI |
| `SurveyContext` | Survey context |

#### Event Types (Listener / Workflow / Dashboard etc. trigger scenarios)

| id | Meaning |
|----|------|
| `AppEvent` | Listener event (unified entry for data / workflow / general events) |
| `NotificationEvent` | Notification event |
| `FormEvent` | Form event |
| `RecordFormCloseEvent` | Data table form close event |
| `ViewEvent` | Data table view event |
| `BpmnEvent` | Workflow event |
| `BpmnTaskArgs` | Workflow task arguments |
| `ChartClickEvent` | Chart click event |
| `CardEvent` | Dashboard card event |
| `RichtextClickEvent` | Rich text card click event |
| `TextIndexEvent` | Search engine click event |
| `DeptClickEvent` | Department node click event |

#### Query Conditions / Interception Context Types

| id | Meaning |
|----|------|
| `QueryCondition` | Related query condition |
| `RelationQueryCondition` | Related-record automation return data condition |
| `ViewCondition` | Data table query condition |
| `TableRecordQueryBeforeContext` | Data detail pre-query context |
| `TableRecordQueryAfterContext` | Data detail post-query context |
| `TableQueryBeforeContext` | View data pre-query context |
| `TableQueryAfterContext` | View data post-query context |

> ⚠️ **`id` must be selected exactly from the list above**. Inventing your own type names (e.g. `int`, `string`, `List<String>`) is forbidden.

## Variables

Variables have a unique identifier and a type — that identifier is `varList[].name` (input parameter) or step `retValues[].name` (step return value). They share the same expression scope. In automation expressions, all variables can be referenced via `${name}`. Variables have a scope; they are invisible outside it, and undefined variables cannot be referenced in expressions.


## Flow Control

- **Conditional (If)**: controls automation flow branching with an expression. The condition expression must return a boolean.
- **List loop (ForEach)**: takes an expression as the loop collection and executes child steps sequentially for each item.
- **Loop (While)**: repeats child steps while the expression evaluates to true.
- **Call script (CallScript)**: calls a function in an existing script module of the application and returns the result.
- **Set automation return value (SetReturnValue)**: takes an expression as the automation's return value. Can be called multiple times; later calls override earlier ones.

## Expressions
Informat expressions use UEL syntax and are a platform-specific DSL, **not JavaScript** — `${}` is the evaluation boundary, and the signatures and syntax rules of the available functions (`String`/`Array`/`Date`/`Math`/`Misc`/`Encode`/`Record`/`User`/`Context`, etc.) are defined by `informat.expression.md`. **Before writing any step value, condition, loop collection, or return value containing `${...}`, you must Read `informat.expression.md` to verify the syntax and function signatures; do not write from memory.** When saving, `call_informat.js` validates this: if the arguments contain `${...}` and that document has not been read this session, it is blocked and the document must be read first (exit 6).

## Automation Steps

In automations you use automation steps to implement program functionality. Automation steps consist of **settings** (`<lowercase-first-letter-of-type>FuncSetting`) and **return values** (`retValues`).

### funcSetting Field Naming Rule (Strict)

Each step must carry exactly one `FuncSetting` field corresponding to its `type`, with naming rule fixed as:

> **`type` lowercased first letter + `FuncSetting`**

| type Example | Corresponding Field Name |
|----------|-----------|
| `OutputToast` | `outputToastFuncSetting` |
| `OutputDynamicForm` | `outputDynamicFormFuncSetting` |
| `CallScript` | `callScriptFuncSetting` |
| `If` | `ifFuncSetting` |
| `ForEach` | `forEachFuncSetting` |

> ⚠️ **Field names not declared by the schema are forbidden.** For example, naming `InsertRecord`'s setting `insertRecordSetting` or `insertRecordFuncSetting` will not be recognized — and more importantly, `InsertRecord` is not a legal automation type to begin with (it should be replaced by `CallScript` calling a script function).

### Step Whitelist (Only the Following Types Are Legal)

Only the following types may appear in `funcSettingList`. **When choosing a type, first follow "Critical Decision" above to analyze intent**: prefer existing `Output*` steps in the whitelist for interactive needs (many "create record" / "start workflow" / "upload file" requirements have dedicated interactive steps); pure backend logic uses `CallScript`. **Any type not in the whitelist is an error** — for example, treating `InsertRecord/UpdateRecord/Http/SetVar/CreateBpmnProcess/CallAI` as steps is a severe error.

| Category | Legal Types |
|------|----------|
| Control flow | `If` `If.true` `If.false` `ForEach` `While` `CallScript` `SetReturnValue` |
| Dialog | `OutputConfirm` `OutputUpload` `OutputUploadExcel` `OutputDynamicForm` `OutputDynamicTable` `OutputRecordInfo` `OutputRecordCreate` `OutputRecordSelect` `OutputFormDesigner` `OutputOpenFile` `OutputRichtext` `OutputString` `OutputPageDesigner` `OutputOpenSplitDrawer` `OutputOpenWebsite` |
| Notification | `OutputToast` `OutputNotification` |
| Form operations | `OutputSetFormValue` `OutputFormValidate` `OutputRecordFormRefresh` `OutputCloseRecordInfo` `OutputSetFormTableSelection` |
| Data table operations | `OutputTableRefresh` `OutputTableEvent` `OutputRefreshTableViewColumn` `OutputSetTableViewFilter` `OutputSetTableViewFilterCondition` `OutputSetTableViewOrderBy` `OutputSetTableViewExpand` `OutputSetTableViewSelection` `OutputSetTableViewActiveRecords` `OutputSetTableViewRootRecordId` `OutputSetTableViewData` |
| Dashboard | `OutputRefreshDashboardCard` `OutputSetDashboardFilter` |
| Page/Navigation | `OutputOpenUrl` `OutputExternal` `OutputSetExternalUrl` `OutputCloseModuleVisitHistory` |
| Print/Download | `OutputPrintRecord` `OutputPrintRecordList` `OutputPrintByPageDesigner` `OutputDownloadFile` `OutputDownloadExcel` |
| Script/Clipboard | `OutputInjectScript` `OutputExecuteScript` `OutputCopyClipboard` `OutputGetAppClipboard` `OutputSetAppClipboard` |
| Media/Scanner | `OutputPlayAudio` `OutputPlayImage` `OutputQRCodeScanner` |
| Search/Messaging | `OutputTextindexSearch` `OutputWebsitePageFireEvent` |
| Workflow | `OutputBpmnEvent` `OutputBpmnProcess` `OutputBpmnTaskInfo` `OutputBpmnInstanceInfo` |

### Return Values and Reference Rules

Each step may declare 0, 1, or multiple return values in its `retValues`. Each return value consists of `id` and `name`:

- **`id`** is the platform-preset, type-bound **fixed identifier**, **not modifiable**. It depends on the step's type — different types have different ids (e.g. `QueryRecordList`'s id is `list`; `UpdateRecord`'s ids include `count` and `recordIdList`; not all steps use `result`).
- **`name`** is the user-**customized** alias used as the reference name in expressions. Subsequent steps reference the value via `${name}`.
- All `name` values within the same automation must be unique; duplicate names cause reference ambiguity.

#### Reference Example

```jsonc
// Step A (OutputDynamicForm)
retValues = [{ "id": "result", "name": "formData" }]

// Step B (CallScript)
retValues = [{ "id": "result", "name": "newProject" }]
```

Subsequent steps can reference these via `${formData}` and `${newProject}`.

#### Quick Reference: Return Value Structures of Legal Automation Steps

| Step type | Return value structure (id → default name) |
|----------|---------------------------|
| `If` / `If.true` / `If.false` / `While` / `SetReturnValue` | No return value |
| `ForEach` | `object` → list item; `idx` → index |
| `CallScript` | **Three**: `result` → return value; `code` → exception code; `message` → exception message (all three must be declared in retValues, not only `result`; later steps read the script result via `${returnValueName}`) |
| `OutputConfirm` | `result` → confirmed (boolean) |
| `OutputDynamicForm` / `OutputFormDesigner` / `OutputRecordCreate` | `result` → form data |
| `OutputDynamicTable` | `result` → record list |
| `OutputRecordSelect` / `OutputUploadExcel` | `result` → data list |
| `OutputUpload` / `OutputOpenFile` | `result` → file list |
| `OutputOpenUrl` / `OutputOpenWebsite` | `result` → return value |
| `OutputQRCodeScanner` | `result` → scan result |
| `OutputBpmnProcess` | `result` → workflow instance ID |
| `OutputFormValidate` | `result` → validation passed |
| `OutputGetAppClipboard` | `result` → app clipboard data |
| `OutputExecuteScript` | `result` → script return data |

> The "default name" in the table is the platform-preset Chinese name, which can be changed when editing a step to any alias matching expression context naming conventions; references then use the new name. Other Output-type steps (such as various `Set*`, `Refresh*`, `Print*`, `Download*`) have no return value.

> **The step structure must be complete**: each step object in `funcSettingList` should carry `id` (a unique lowercase-English identifier) + `name` (step name) + `type` + the matching `<type-first-letter-lowercase>FuncSetting` + `retValues` (even steps with no return value, like `SetReturnValue`, should write `"retValues": []`). For `CallScript`, **all three** retValues `result`/`code`/`message` must be declared (declaring only `result` is incomplete). Do not provide only `type` + setting — an incomplete structure can make variables unreferenceable or cause the step to behave abnormally.

> ⚠️ **`OutputUploadExcel` return structure**: The outermost layer is a sheet **array** (even with only 1 sheet, it's still an array). The whole shape is `[{ id, name, isHidden, data: { header, headerName, list } }, ...]`. Before accessing data you must take an index (e.g. `excelData[0]` or find the right sheet by `id`/`name`); **do not treat `excelData` as a single sheet object**. `data.list` is the row array, `list[0]` is the header row (duplicates `data.header`), and the actual data starts from `list[1]`.

### Control Flow Steps

| type | Description |
|------|------|
| If | Conditional, controls flow branching by expression; must contain If.true and If.false child nodes |
| If.true | If's true branch, exists as If's child |
| If.false | If's false branch, exists as If's child |
| ForEach | List loop, executes child steps sequentially for each item in the collection |
| While | Conditional loop, repeats child steps while expression is true |
| CallScript | Calls a script function in the application and returns the result |
| SetReturnValue | Sets the automation return value, retrievable by the caller |

### Interactive Steps - Dialogs/Forms

| type | Description |
|------|------|
| OutputConfirm | Opens a confirmation dialog and waits for user confirm/cancel |
| OutputUpload | Upload file, supports Base64 or shared storage modes |
| OutputUploadExcel | Upload and parse an Excel file, returns parsed data |
| OutputDynamicForm | Open a custom form page, wait for the user to fill in and submit |
| OutputDynamicTable | Open a custom table dialog for the user to operate on data |
| OutputRecordInfo | Open record detail dialog displaying the form for the specified record |
| OutputRecordCreate | Open create-record form dialog and return the new record |
| OutputRecordSelect | Open record-selection dialog letting the user pick records |
| OutputFormDesigner | Open form-designer form dialog |
| OutputOpenFile | Preview shared-storage files (Excel, Word, Ppt, etc.) |
| OutputRichtext | Display rich text content in a dialog |
| OutputString | Display text/markdown/html content in a dialog |
| OutputOpenSplitDrawer | Open a side drawer or dialog showing modules / websites / print templates etc. |
| OutputOpenWebsite | Open an in-app website module page in a dialog |
| OutputPageDesigner | Open print-template dialog, supports printing and image export |

### Interactive Steps - Toast/Notification

| type | Description |
|------|------|
| OutputToast | Show a brief Toast message |
| OutputNotification | Show a notification box with a title |

### Interactive Steps - Form Operations

| type | Description |
|------|------|
| OutputSetFormValue | Set field values of the currently open form |
| OutputFormValidate | Validate the current form and return validation status |
| OutputRecordFormRefresh | Refresh the record form, reload form data |
| OutputCloseRecordInfo | Close the current record detail / create dialog |
| OutputSetFormTableSelection | Set selected rows in a sub-table within a form |

### Interactive Steps - Data Table Operations

| type | Description |
|------|------|
| OutputTableRefresh | Refresh data table view data |
| OutputTableEvent | Send data table change events to the frontend |
| OutputRefreshTableViewColumn | Refresh the data table view column configuration |
| OutputSetTableViewFilter | Set data table filter |
| OutputSetTableViewFilterCondition | Set data table filter (condition list mode) |
| OutputSetTableViewOrderBy | Set data table sort rules |
| OutputSetTableViewExpand | Set expand/collapse state (tree structure) |
| OutputSetTableViewSelection | Set selected rows in data table |
| OutputSetTableViewActiveRecords | Set active records (highlighted) |
| OutputSetTableViewRootRecordId | Set the root node of a tree-shaped data table |
| OutputSetTableViewData | Inject or update data into the frontend data table directly |

### Interactive Steps - Dashboard

| type | Description |
|------|------|
| OutputRefreshDashboardCard | Refresh dashboard card data |
| OutputSetDashboardFilter | Set dashboard filter |

### Interactive Steps - Page/Navigation

| type | Description |
|------|------|
| OutputOpenUrl | Open a URL (new window / current window / iframe) |
| OutputExternalUrl | Embed external URL in module area |
| OutputSetExternalUrl | Dynamically modify the URL of the displayed external page |
| OutputCloseModuleVisitHistory | Close module visit history |

### Interactive Steps - Print/Download

| type | Description |
|------|------|
| OutputPrintRecord | Print a single record in form layout |
| OutputPrintRecordList | Print multiple records in tabular layout |
| OutputPrintByPageDesigner | Print a record using a print template |
| OutputDownloadFile | Download a file locally |
| OutputDownloadExcel | Export data as Excel and download |

### Interactive Steps - Client Scripts/Clipboard

| type | Description |
|------|------|
| OutputInjectScript | Inject and execute JavaScript on the page |
| OutputExecuteScript | Execute JavaScript on the frontend, supports passing variables and getting return values |
| OutputCopyClipboard | Copy text to system clipboard |
| OutputGetAppClipboard | Read application internal clipboard data |
| OutputSetAppClipboard | Write data to application internal clipboard |

### Interactive Steps - Media/Scanner

| type | Description |
|------|------|
| OutputPlayAudio | Play audio file |
| OutputPlayImage | Open image preview window |
| OutputQRCodeScanner | Open QR code scanner (mobile) |

### Interactive Steps - Search/Messaging

| type | Description |
|------|------|
| OutputTextindexSearch | Open full-text search interface |
| OutputWebsitePageFireEvent | Send custom event to website page |

### Interactive Steps - Workflow (BPMN)

| type | Description |
|------|------|
| OutputBpmnEvent | Send workflow change event to the frontend |
| OutputBpmnProcess | Open workflow start-form dialog |
| OutputBpmnTaskInfo | Open workflow task detail dialog |
| OutputBpmnInstanceInfo | Open workflow instance detail dialog |

> When `OutputBpmnProcess` starts a workflow, **a new record is inserted into the start table** (it does not reuse the source record passed in by the caller). If subsequent steps need to operate on this start record (update status, read fields, etc.), you **must** retrieve the new record's ID via `informat.bpmn.getInstanceVar(moduleId, instanceId, 'form_recordId')`, not use the source record ID.

## Interactive Execution

Automations may include steps requiring user interaction; we call these interactive steps.

Interactive execution mechanism:
Automation flows can include steps that require user participation; these are called **interactive steps**.
When the automation reaches an interactive step, the system will:
- Automatically save the current execution context and variable state
- Pause the flow
- Notify the user to interact with the UI (fill out a form, confirm, etc.)
- Restore execution context after user submission
- Continue execution from that step

Interactive execution lets automations integrate naturally into business approval / input / confirmation scenarios.
Interactive automations make it easier for developers to write business processes. All UI-interaction automation steps in the execution are interactive.

Interactive step determination rule (important):
Among all automation steps, those whose `type` starts with `Output` are interactive.
i.e.:
`type.startsWith("Output")`

Examples (interactive steps):
- OutputDynamicForm
- OutputDynamicTable
- OutputConfirm
- OutputToast
- OutputPageDesigner
- OutputRecordSelect
- OutputUpload

> **Execution environment constraint**: Interactive steps **can only be used in client-side automations**. Automations bound to control buttons are client-side; scheduled tasks, listeners (except those triggered client-side), and workflow task callbacks are server-side, where **all `Output*` steps are forbidden**. See "Execution Environment" at the top.

## Listener-Triggered Automation

A listener is a triggering mechanism that automatically executes a corresponding automation when specific events occur in the system (data changes, user actions, etc.).

### Transaction Characteristics

All event listeners (except notifications and client-triggered ones) execute in the same transaction as the trigger. If the automation throws an exception, the original operation and the entire transaction will roll back.

**Important constraint**: Non-client-triggered listeners run in the **server-side** environment and must not contain interactive steps (steps whose `type` starts with `Output`). For "create record" / "send notification" needs in listeners, use `CallScript` to invoke a script. See "Execution Environment" at the top.

### Listener Parameter Structure

The automation receives a single parameter `AppEvent`:
```json
{
  "id": "eventTypeId",
  "content": { /* event content; format varies by event type */ }
}
```

### Event Type List

#### Data Table Record Events

| Event ID | Description | Trigger Timing |
|--------|------|----------|
| `record.create.before` | Before record creation | User creates record via form (automation/script creation does not trigger) |
| `record.create.after` | After record creation | Same as above |
| `record.update.before` | Before record update | User updates record via form |
| `record.update.after` | After record update | Same as above |
| `record.delete.before` | Before record deletion | User deletes record via form |
| `record.delete.after` | After record deletion | Same as above |

**record.create.before** content:
```json
{
  "record": {"name": "value", "age": 0},
  "source": "form",
  "tableId": "listenerData"
}
```

**record.create.after** content:
```json
{
  "afterRecord": {"id": "d6dhvhodo62nl", "name": "value", "age": 0, "seq": 2},
  "record": {"name": "value", "age": 0},
  "source": "form",
  "tableId": "listenerData"
}
```

**record.update.before** content:
```json
{
  "beforeRecord": {"id": "xg2d0hi83cwym", "name": "old", "age": 100, "seq": 1},
  "record": {"id": "xg2d0hi83cwym", "name": "new"},
  "source": "form",
  "tableId": "listenerData",
  "updateFieldList": ["name"]
}
```

**record.update.after** content:
```json
{
  "afterRecord": {"id": "xg2d0hi83cwym", "name": "new", "age": 100, "seq": 1},
  "beforeRecord": {"id": "xg2d0hi83cwym", "name": "old", "age": 100, "seq": 1},
  "record": {"id": "xg2d0hi83cwym", "name": "new"},
  "source": "form",
  "tableId": "listenerData",
  "updateFieldList": ["name"],
  "updateRowCount": 1
}
```

**record.delete.before / record.delete.after** content:
```json
{
  "record": {"id": "d6dhvhodo62nl", "name": "value", "age": 0, "seq": 2},
  "source": "form",
  "tableId": "listenerData"
}
```

> Event order: parent table create-before → child table create-before/after → parent table create-after. Removing items from a relation list only deletes the relation, it does not trigger child-table events.

#### Comment Events

| Event ID | Description |
|--------|------|
| `record.comment.create.after` | After user posts a comment |
| `record.comment.delete.after` | After user deletes a comment |

content:
```json
{
  "comment": {
    "id": 0,
    "parentId": 0,
    "content": "{richtext_json}",
    "recordId": "xg2d0hi83cwym",
    "tableId": "listenerData"
  }
}
```

#### Row Number Events

| Event ID | Description |
|--------|------|
| `record.rownumber.update.before` | Before row order change by drag |
| `record.rownumber.update.after` | After row order change by drag |

**record.rownumber.update.before** content:
```json
{
  "beforeRowNumber": 4,
  "recordId": "gf13shmq3njqf",
  "source": "form",
  "tableId": "listenerData"
}
```

**record.rownumber.update.after** content:
```json
{
  "afterRowNumber": 3,
  "beforeRowNumber": 4,
  "recordId": "gf13shmq3njqf",
  "source": "form",
  "tableId": "listenerData"
}
```

#### Automation Execution Events

| Event ID | Description |
|--------|------|
| `app.automatic.before` | Automation execution start |
| `app.automatic.success` | Automation execution success |

content:
```json
{
  "args": ["param1"],
  "id": "trang7ixclbtg",
  "uuid": "trang7ixclbtg:sesgv3tgz0el",
  "draft": false,
  "isDraft": false
}
```

#### Scheduled Task Events

| Event ID | Description |
|--------|------|
| `app.schedule.before` | Scheduled task starts |
| `app.schedule.success` | Scheduled task success |

content:
```json
{
  "id": "tlijinwmbtnet",
  "name": "Task name",
  "requestId": "arqwu3bsirbh8",
  "serverId": "informat-biz2-prd",
  "startTime": 1718157714369,
  "endTime": 1718092915132
}
```

#### Application-Level Events

| Event ID | Description | Trigger Side |
|--------|------|----------|
| `app.enter` | User enters the app | Client-side, may include interactive steps |
| `app.module.enter` | User enters a module | Client-side, may include interactive steps |
| `app.publish` | After app publish | Server-side |

**app.enter** content: full app info, user info, platform info, URL parameters, etc.

**app.module.enter** content: extends app.enter with `moduleId`, `moduleKey`, etc.

**app.publish** content:
```json
{
  "appId": "i1mwqy35y88hl",
  "appDefineId": "demoApp",
  "companyId": "icxt9rsd1f0ai",
  "build": 1906,
  "publishUser": "username"
}
```

#### Member Events

| Event ID | Description |
|--------|------|
| `app.member.add.after` | After member joins app |
| `app.member.remove.after` | After member is removed from app |
| `app.member.role.update.after` | After member role update |

**app.member.add.after** content:
```json
{
  "appId": "i1mwqy35y88hl",
  "appDefineId": "demoApp",
  "companyId": "icxt9rsd1f0ai",
  "userId": "bt4tdzx8vtjoe",
  "roleList": ["admin"]
}
```

**app.member.role.update.after** content:
```json
{
  "appId": "i1mwqy35y88hl",
  "appDefineId": "demoApp",
  "companyId": "icxt9rsd1f0ai",
  "userId": "yvkc2kwpy3xzr",
  "beforeRoleList": ["admin", "ceo"],
  "afterRoleList": ["admin", "ceo", "manager"]
}
```


## Data Table Toolbar Button Calling Automation

You can create a button on the data table top toolbar that calls an automation when clicked.

### Creation Steps

1. First create the automation (using `_automatic_save_define`)
2. Use `_table_create_tool_bar_button` to create the toolbar button with `action` set to `CallAutomatic`
3. In `actionSetting`, configure `automaticId` (automation ID) and optional `varList` (variable list)

### Parameter Example

```json
{
  "tableId": "myTable",
  "name": "Run Automation",
  "action": "CallAutomatic",
  "actionSetting": {
    "automaticId": "vc3xpthwbf8ne",
    "varList": [
      { "value": "${tableSelectedRecordList}" },
      { "value": "${user.id}" }
    ]
  },
  "buttonSetting": {
    "type": "primary"
  }
}
```

### Supported Variables

- `${user}` — current user object with id, name, roleList, departmentList; use `${user.id}` to get user ID
- `${tableSelectedRecordList}` — list of records selected by the user in the data table
- `${moduleKey}` — current module identifier

## Data Table Form Toolbar Button Calling Automation

You can create a button on the data table form toolbar that calls an automation when clicked.

### Creation Steps

1. First create the automation (using `_automatic_save_define`)
2. Use `_table_create_form_tool_bar_btn` to create the form toolbar button with `action` set to `CallAutomatic`
3. In `actionSetting`, configure `automaticId` (automation ID) and optional `varList` (variable list)

### Parameter Example

```json
{
  "tableId": "myTable",
  "name": "Submit Approval",
  "action": "CallAutomatic",
  "actionSetting": {
    "automaticId": "vc3xpthwbf8ne",
    "varList": [
      { "value": "${formRecord}" }
    ]
  },
  "buttonSetting": {
    "type": "primary"
  }
}
```

### Supported Variables

- `${user}` — current user object with id, name, roleList, departmentList; use `${user.id}` to get user ID
- `${formRecord}` — current form record data
- `${formModuleKey}` — form module identifier

## Calling via HTTP

After enabling HTTP invocation, the automation can be called via an HTTP request at the following URL:

```
https://{host}/web${cluster}/automatic/${appId}/${automaticId}?args=${args}
```

- `${host}` — service deployment address
- `${cluster}` — deployment cluster ID; `0` for single-node deployment
- `${appId}` — application ID (not the identifier)
- `${automaticId}` — automation identifier
- `${args}` — request parameters; the parameters passed to the automation are an array, in JSON format

A successful call returns the automation's return value in the configured format.
Note: Automations called via HTTP cannot contain any interactive output steps.

## Workflow-Triggered Automation

Workflows (BPMN) can be configured with listeners to automatically call automations when specific events occur. Workflows configure `BpmnListenerSetting` on a process definition; each listener can bind multiple event types and multiple automations. When an event triggers, the system passes the `BpmnEvent` object as the first input parameter of the automation.

### Listener Configuration

Each workflow process definition can have multiple listeners (`BpmnListener`); each listener contains:

| Field | Type | Description |
|------|------|------|
| id | String | Listener identifier |
| name | String | Listener name |
| eventList | List\<String\> | List of event types being listened to |
| automaticList | List\<String\> | List of automation IDs to trigger |
| isEnable | boolean | Enabled or not |

### Event Types

Workflows support the following event types, grouped into three categories:

#### 1. User Task Events

| Event Type | Description |
|---------|------|
| TASK_CREATED | User task created |
| TASK_COMPLETED | User task completed (approved, etc.) |
| TASK_ASSIGNED | User task assigned to handler |
| TASK_OWNER_CHANGED | Task owner changed |
| TASK_DUEDATE_CHANGED | Task due date changed |

#### 2. Process Instance Events

| Event Type | Description |
|---------|------|
| PROCESS_CREATED | Process instance created |
| PROCESS_STARTED | Process instance started |
| PROCESS_COMPLETED | Process instance ended normally |
| PROCESS_CANCELLED | Process instance cancelled |

#### 3. Activity Node Events

| Event Type | Description |
|---------|------|
| ACTIVITY_STARTED | Activity node starts |
| ACTIVITY_COMPLETED | Activity node completes |
| ACTIVITY_CANCELLED | Activity node cancelled |
| MULTI_INSTANCE_ACTIVITY_STARTED | Multi-instance activity starts |
| MULTI_INSTANCE_ACTIVITY_COMPLETED | Multi-instance activity completes |
| MULTI_INSTANCE_ACTIVITY_COMPLETED_WITH_CONDITION | Multi-instance activity completes by condition |
| MULTI_INSTANCE_ACTIVITY_CANCELLED | Multi-instance activity cancelled |

### BpmnEvent Object Structure

The first parameter received by the automation is a `BpmnEvent` object containing:

| Field | Type | Description |
|------|------|------|
| appId | String | Application ID |
| moduleUuid | String | Module UUID |
| moduleId | String | Module Key |
| type | String | Event type name |
| processDefinitionId | String | Process definition ID |
| tenantId | String | Tenant ID |
| instance | BpmnInstance | Process instance info (see table below) |
| task | BpmnTask | Task info, only for user task events |
| activityEvent | BpmnActivityEvent | Activity event info, only for activity node events |
| processEvent | BpmnProcessEvent | Process event info, only for process instance events |
| numberOfInstances | Integer | Total multi-instance count, only for multi-instance events |
| numberOfActiveInstances | Integer | Active multi-instance count, only for multi-instance events |
| numberOfCompletedInstances | Integer | Completed multi-instance count, only for multi-instance events |
| sequential | Boolean | Whether multi-instance is sequential, only for multi-instance events |

#### BpmnInstance (Process Instance Info)

All events contain the `instance` field:

| Field | Type | Description |
|------|------|------|
| id | String | Process instance ID |
| name | String | Process instance name |
| businessKey | String | Business key (linked data record ID) |
| procDefId | String | Process definition ID |
| startTime | Date | Start time |
| endTime | Date | End time |
| startUserId | String | Initiator user ID |
| tenantId | String | Tenant ID |
| procDefName | String | Process definition name |
| deleteReason | String | Delete reason |

#### BpmnTask (Task Info)

Only present for user task events (TASK_CREATED, TASK_COMPLETED, TASK_ASSIGNED, TASK_OWNER_CHANGED, TASK_DUEDATE_CHANGED):

| Field | Type | Description |
|------|------|------|
| id | String | Task ID |
| name | String | Task name |
| taskDefKey | String | Task definition key (node identifier) |
| assignee | String | Current handler user ID |
| owner | String | Task owner user ID |
| procInstId | String | Process instance ID |
| procDefId | String | Process definition ID |
| procDefName | String | Process definition name |
| procInstName | String | Process instance name |
| executionId | String | Execution ID |
| tenantId | String | Tenant ID |
| dueDate | Date | Due date |
| claimTime | Date | Claim time |
| startTime | Date | Task creation time |
| delegation | String | Delegation status |

#### BpmnActivityEvent (Activity Event Info)

Only present for activity node events (ACTIVITY_STARTED, ACTIVITY_COMPLETED, ACTIVITY_CANCELLED, and multi-instance activity events):

| Field | Type | Description |
|------|------|------|
| activityId | String | Activity node ID |
| activityName | String | Activity node name |
| activityType | String | Activity type (e.g. userTask, serviceTask) |
| behaviorClass | String | Behavior class full name |
| executionId | String | Execution ID |
| type | String | Event type |
| processInstanceId | String | Process instance ID |
| processDefinitionId | String | Process definition ID |

#### BpmnProcessEvent (Process Event Info)

Only present for process instance events (PROCESS_CREATED, PROCESS_STARTED, PROCESS_COMPLETED, PROCESS_CANCELLED). Contains an `entity` field (BpmnExecutionEntity):

| Field | Type | Description |
|------|------|------|
| entity.id | String | Execution entity ID |
| entity.name | String | Name |
| entity.activityId | String | Current activity ID |
| entity.businessKey | String | Business key |
| entity.businessStatus | String | Business status |
| entity.currentActivityId | String | Current activity node ID |
| entity.deleteReason | String | Delete reason |
| entity.deploymentId | String | Deployment ID |
| entity.processDefinitionId | String | Process definition ID |
| entity.processDefinitionKey | String | Process definition Key |
| entity.processDefinitionName | String | Process definition name |
| entity.processDefinitionVersion | Integer | Process definition version |
| entity.processInstanceId | String | Process instance ID |
| entity.processInstanceBusinessKey | String | Process instance business key |
| entity.startTime | Date | Start time |
| entity.startUserId | String | Initiator user ID |
| entity.tenantId | String | Tenant ID |

### Workflow User Task Completion Trigger

Workflow user task nodes can be configured with `completeAutomaticId`. When the task is completed (approved, etc.), the system automatically calls the specified automation. The first input parameter passed to the automation is a `BpmnTaskArgs` object.

> **Execution environment**: This scenario is **server-side** — the automation **must not contain any `Output*` interactive steps**.

#### BpmnTaskArgs Object Structure

| Field | Type | Description |
|------|------|------|
| procDefId | String | Process definition ID |
| procInstId | String | Process instance ID |
| activityId | String | Task node definition Key (activity ID) |
| taskId | String | Task ID |

#### Automation varList Configuration

The automation needs a `BpmnTaskArgs`-typed input parameter to receive the task arguments:

```jsonc
// varList definition
[
  { "id": "BpmnTaskArgs", "name": "taskArgs", "optional": false }
]
```

#### Accessing Parameters in the Automation

- `${taskArgs.procDefId}` — get process definition ID
- `${taskArgs.procInstId}` — get process instance ID
- `${taskArgs.activityId}` — get task node definition Key
- `${taskArgs.taskId}` — get task ID

#### Usage Example

Use `CallScript` to invoke a script function for task-completion business logic:

```jsonc
{
  "funcSettingList": [
    {
      "type": "CallScript",
      "retValues": [{ "id": "result", "name": "outcome" }],
      "callScriptFuncSetting": {
        "scriptId": "bpmnScript",
        "func": "onTaskComplete",
        "args": [{ "valueVar": "${taskArgs}" }]
      }
    }
  ]
}
```

### Per-Scenario Event Object Content Mapping

| Scenario | type | instance | task | activityEvent | processEvent | Multi-instance fields |
|------|------|----------|------|---------------|--------------|-----------|
| User task created | TASK_CREATED | ✓ | ✓ | ✗ | ✗ | ✗ |
| User task completed | TASK_COMPLETED | ✓ | ✓ | ✗ | ✗ | ✗ |
| User task assigned | TASK_ASSIGNED | ✓ | ✓ | ✗ | ✗ | ✗ |
| Task owner changed | TASK_OWNER_CHANGED | ✓ | ✓ | ✗ | ✗ | ✗ |
| Task due date changed | TASK_DUEDATE_CHANGED | ✓ | ✓ | ✗ | ✗ | ✗ |
| Process created | PROCESS_CREATED | ✓ | ✗ | ✗ | ✓ | ✗ |
| Process started | PROCESS_STARTED | ✓ | ✗ | ✗ | ✓ | ✗ |
| Process completed | PROCESS_COMPLETED | ✓ | ✗ | ✗ | ✓ | ✗ |
| Process cancelled | PROCESS_CANCELLED | ✓ | ✗ | ✗ | ✓ | ✗ |
| Activity started | ACTIVITY_STARTED | ✓ | ✗ | ✓ | ✗ | ✗ |
| Activity completed | ACTIVITY_COMPLETED | ✓ | ✗ | ✓ | ✗ | ✗ |
| Activity cancelled | ACTIVITY_CANCELLED | ✓ | ✗ | ✓ | ✗ | ✗ |
| Multi-instance activity started | MULTI_INSTANCE_ACTIVITY_STARTED | ✓ | ✗ | ✓ | ✗ | sequential |
| Multi-instance activity completed | MULTI_INSTANCE_ACTIVITY_COMPLETED | ✓ | ✗ | ✓ | ✗ | ✓ all |
| Multi-instance activity completed with condition | MULTI_INSTANCE_ACTIVITY_COMPLETED_WITH_CONDITION | ✓ | ✗ | ✓ | ✗ | ✓ all |
| Multi-instance activity cancelled | MULTI_INSTANCE_ACTIVITY_CANCELLED | ✓ | ✗ | ✓ | ✗ | sequential |

### Accessing Event Parameters in the Automation

In the automation, `BpmnEvent` is passed as the first input parameter. Event data can be referenced through the input parameter, for example:

- `${param1.type}` — get the event type
- `${param1.instance.id}` — get the process instance ID
- `${param1.instance.businessKey}` — get the linked business data record ID
- `${param1.instance.startUserId}` — get the process initiator
- `${param1.task.assignee}` — get the current task handler (only for task events)
- `${param1.task.name}` — get the current task name (only for task events)
- `${param1.activityEvent.activityName}` — get the activity node name (only for activity events)
- `${param1.activityEvent.activityType}` — get the activity node type (only for activity events)
