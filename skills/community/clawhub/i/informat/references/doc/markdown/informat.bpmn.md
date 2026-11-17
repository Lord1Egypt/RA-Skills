<!-- DOCKEY: bpmn-9f4c1 -->

This is the Informat workflow (BPMN) design document. You MUST read it fully before creating any workflow — a qualified workflow is multi-node, has branching gateways, complete sequence flows, is bound to a data table, and has a clear layout. It is never "just one node with no connections".

# Informat Workflow (BPMN) Design Document

## 0. Mandatory prerequisites

- A node's assignee, flow conditionExpression, auto-assignments, etc. are **expressions**; before writing them you MUST call `_read_informat_expression_doc` for the Informat expression spec. No JavaScript/SQL style.
- Every approval node's (UserTask) `formSetting.tableId` MUST be **exactly the same** as the start form tableId in `_bpmn_update_start_setting` — the whole process revolves around this single main business table.
- The StartEvent is system-provided; **do NOT create it**. But you MUST create one sequence flow out of the StartEvent — no "start event with no connections".

## 1. Creation order (six steps, none skippable)

1. **Create module** `_bpmn_create_module` → get moduleId.
2. **Create process define** `_bpmn_create_process_define` → get processDefineId.
3. **Start setting** `_bpmn_update_start_setting`: `enableStartForm=true` + `formSetting.tableId` (bind the main table) + `tableFieldSettingList`. This determines the process's main data table.
4. **Query process define** `_bpmn_query_process_define`: get the **real StartEvent node id** (don't guess; use the query result) for the first sequence flow.
5. **Create nodes** `_bpmn_create_or_update_node`: build UserTasks (approval nodes) + EndEvent. Approval nodes must fully configure taskSetting/formSetting (Section 2).
6. **Create flows** `_bpmn_create_or_update_flow`: StartEvent→first node→…→EndEvent; branch nodes get multiple conditional flows (Section 3).

> A real process has **at least**: 1 StartEvent (built-in) + ≥2 UserTasks + 1 EndEvent + all the flows wiring them. A single node with no flows = unqualified.

> **Failure-retry rule**: if a call in steps 5 or 6 errors out, correct the parameters and retry on the **same moduleId / processDefineId**. Do not fall back to steps 1–2 to recreate the module or a new process define just because one step failed — that leaves a named but empty process define (a duplicate shell). Create the module and process define for a process exactly once.
>
> **Completion criterion**: in orchestration counting, a workflow is tallied as "built" only once its processDefineId has **both a node and a flow**; an empty shell with only a process define is not counted, and the finish self-check (`_app_check_setting`) blocks on the shortfall. This directly counters the shortcut of "declaring a rich process but landing only an empty shell".

## 2. Depth config required on approval nodes (UserTask)

When `type=userTask`, `taskSetting.formSetting` is required and must be complete:

- **`tableId`**: same as the start form.
- **`tableFieldSettingList`**: which fields this node's approver can view/edit (each `id/editable/visible`). Different nodes usually differ (finance node can edit amount, dept node read-only).
- **`toolBarButtonList`**: this node's action buttons, **at least one positive and one rejection**:
  - Approve/pass: `action=TaskComplete`, `actionSetting.enableComment=false`.
  - Reject/return: `action=TaskMoveToActivity`, `actionSetting.enableComment=true`, `activityId`=node id to jump back to (e.g. initiator or previous node).
  - Button id is a fixed 10 lowercase letters, unique within the node; fill `bpmnModuleId/taskIdExpression(${task.id})/tableId` in `actionSetting`.
- **`completeSetVarList`** (optional but recommended): write back business fields on completion (e.g. set `status` to "approved"); `expression` may reference `form`.
- **assignee**: single approver returns a single user id via `${...}` (e.g. `${Array.first(User.superiorUsers(initiator))}`); countersign/or-sign see Section 4.
- **`taskCopySetting`** (optional): CC users expression + `copyType` (start/end).

## 3. Branching & gateways (the key to "flows with logic")

Informat has no standalone "gateway node" type — **branching is done by drawing multiple conditional flows out of the same source node**; the canvas auto-renders a diamond gateway.

- From the same `sourceRef`, create multiple `_bpmn_create_or_update_flow`, each with a different `conditionExpression` (`${...}`-wrapped, returning boolean, using only `initiator` and `form.xxx` start-form fields).
- **Always keep one default flow** (no `conditionExpression`) as fallback, so the process doesn't stall when no condition matches.
- Conditions must be mutually exclusive and cover all cases. E.g. budget approval:
  - `Flow_to_finance`: `${form.budget >= 100000}` → finance approval
  - `Flow_to_ceo`: `${form.budget >= 1000000}` → CEO approval
  - `Flow_direct_pass`: default (no condition) → straight to end
- Give each flow a meaningful `name` (e.g. "budget≥100k - to finance") so the canvas has readable labels.

> **Return / cycle rule (hard constraint)**: "Reject / return to a previous step" should be done via an approval node's button (`toolBarButtonList` with `action=TaskMoveToActivity` + `actionSetting.activityId`=the node to jump back to), **not** by an unconditional sequence flow pointing back to an earlier node. Once a set of all-unconditional flows forms a cycle, it is an infinite loop and is rejected on save (exit 10). If you really must express "return" with a sequence flow, that flow **must** carry a `conditionExpression` (`${...}` returning boolean) so the cycle has at least one conditional edge.
>
> **Assignee required**: every UserTask node must set `assignee` (an approver expression; a single user ID for one approver, `${elementVariable}` for countersign/or-sign). A UserTask missing its assignee is rejected on save.

## 4. Countersign / or-sign (multi-instance)

Configure `multiInstanceLoopCharacteristics` on the node:
- `collection`=user-set expression (e.g. `${User.usersWithRole(Array.of('finance'))}`), `elementVariable`=element var name (e.g. `manager`); then the node `assignee` must be `${manager}`.
- Completion: countersign `${nrOfCompletedInstances == nrOfInstances}`; or-sign `${nrOfCompletedInstances > 0}`.

## 5. Layout (without x/y everything piles up ugly — set them)

`node.x` / `node.y` control canvas coordinates:
- Start node x≈180; main flow increments left-to-right, spacing 200–300.
- Main flow line y≈120; branch nodes stagger vertically (upper branch y≈0, lower y≈240) to avoid node/line overlap.
- Put EndEvent at the far right.

## 6. Bind to a data table (let users start it from the table)

A workflow is not isolated — let users start it with one click from the **main business table**:
- Use `_table_create_tool_bar_button` / `_table_create_form_tool_bar_btn` to add a button on that table/form that starts this process; or use an automation's `OutputBpmnProcess` step (opens the start form dialog) bound to a table button.
- Only then does the workflow have an "entry" and close the loop with the data table, instead of being built and unusable.

## 7. Self-check list (verify each after building)

- [ ] StartEvent has an outgoing flow; no orphan start
- [ ] ≥2 UserTasks, each with full formSetting (fields + buttons incl. approve/reject)
- [ ] Branch nodes: multiple conditional flows + one default, conditions mutually exclusive and covering
- [ ] All nodes wired to EndEvent, no dead ends
- [ ] No cycle formed purely by unconditional flows (a return edge either carries a conditionExpression or uses a TaskMoveToActivity button)
- [ ] Every UserTask has an assignee
- [ ] Node x/y set, layout non-overlapping
- [ ] Start button bound on the main business table
- [ ] All expressions follow the Informat DSL (expression doc read)
