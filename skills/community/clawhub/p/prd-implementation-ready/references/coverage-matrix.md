# Universal PRD Coverage Matrix

Use this after identifying the business goal and core objects. The purpose is to cover requirements generically without dumping a giant checklist on the user.

## Method

1. Extract core business objects from the user's notes.
2. Map each object through the coverage axes below.
3. Apply `necessity-gate.md`: keep only axes/details that materially affect business flow, implementation, testing, UX, risk, or operation.
4. Ask only the highest-risk missing decisions in the current stage.
5. Mark each item as confirmed, recommended default,待确认, or out of scope.
6. Re-run the matrix after the main flow changes.

## Coverage Axes

| Axis | What To Check | Typical Miss |
|---|---|---|
| Business purpose | Why this object exists and what outcome it supports | Writing pages before business goal |
| Source / creation | Where the object comes from, who creates it, sync/import/manual rule | "列表展示 X" without data source |
| Lifecycle | Creation, initial state, transitions, terminal states, rebuild/reopen | Starting at audit/payment midway |
| Information delta | What new information is introduced at each step, where it comes from, and where it is stored | State changes without explaining data source |
| Data flow | Source, transform, persistence, consumer, writeback, sync timing | Data displayed but not traceable |
| Post-event writeback | After transaction completion, payment success, audit pass, refund success, callback, batch creation, or sync completion, list target object, exact persisted field, timestamp, business period, update policy, consumer, and reverse behavior | Only new downstream records are written, while existing fields used by next steps are omitted |
| Linkage / side effect | Linked objects, modules, messages, reports, locks, permissions, reverse effects | "联动处理" without affected objects |
| Actor / permission | Who can view, create, edit, approve, cancel, export, jump | One backend role assumed too broadly |
| Time / period | Attribution date, month boundary, current month rule, late data | "按月汇总" without date source |
| Amount / formula | Source amount, formula, operand semantics, comparison basis, rate, rounding, split, snapshot | Fund or profit amount not computable |
| Cost inclusion state | Audit status, payment status, recognition state, locked cost period, inclusion/exclusion states, late/missing source behavior | Cost enters downstream bills before it is audited, paid, recognized, or recoverable |
| Settlement/payment closure | Payment order origin payload, receiver account, transaction metadata, platform service fee, profit-sharing funds waterfall, payment completion side effects | "Enter payment management" or "generate profit sharing" without enough data/action closure |
| Resource / value flow | Any scarce or controlled resource: inventory, coupon, quota, points, capacity, permission, balance, entitlement. Check source, eligibility, reserve, allocate, combine, consume, release, trace, and role perspective | Treating non-finance resources as simple fields instead of closed-loop objects |
| State axes | Business, audit, payment, invoice, receipt, push, exception separated | Mixed "status" field |
| Data fields | Required fields, optional fields, display source, editability | Field list copied without source |
| Query / list | Filters, default sorting, Tab meaning, include/exclude rules | Global doc contains page-level filters |
| Interaction | Empty/loading/disabled/submitting/success/failure/high-risk confirmation | "可勾选/默认全选" invented |
| Lock / occupation | When source records are occupied, released, rolled back | Reconciliation source reused twice |
| Reverse / exception | Cancel, reject, refund, red flush, void, retry, timeout, partial success | Only happy path written |
| Cross-system | Push, callback, duplicate, delay, sync timestamp, stale data | Sync data treated as instant truth |
| Cross-module | Source action, target page/Tab, params, default filters, permissions | "查看详情跳转" unspecified |
| Audit trail | Operation log, before/after value, operator, time, reason | High-risk finance action no trace |
| Necessity | Whether this object/detail must exist or can merge/defer/remove | Complete-looking but bloated PRD |

## Output Shape

Use a compact table during discussion:

| Object | High-Risk Missing Axis | Current Understanding | Recommended Default | Need User Confirm |
|---|---|---|---|---|

## Object Flow and Information Ledger

For each core object, do not stop at a status list. Build a step ledger that explains how the object moves and what information is added or changed along the way.

| Object | Step | From State | Action / Event | Actor / System | New Information Introduced | Information Source / Authority | Validation | Persisted To | Side Effect / Next Object | Failure / Retry | Confirm |
|---|---|---|---|---|---|---|---|---|---|---|---|

Rules:

- If a step introduces no new data, explicitly say "no new information; only status / lock / visibility changes" and define the side effect.
- If a step creates or updates another object, add that object to the core object list and run the coverage matrix for it too.
- Treat selected records, uploaded files, approval opinions, timestamps, amounts, invoice numbers, payment results, callback results, sync timestamps, exception reasons, jump parameters, and manual adjustments as information that needs a source.
- Separate authoritative source from copied/displayed fields. A copied value still needs a source and update rule.
- When new information can arrive late, be corrected, or be re-synced, define whether it updates the current object, creates a version, or is blocked after lock/audit.
- If the source of a new information item is unknown, mark that step "信息来源待确认" instead of writing the value as final PRD口径.
- If the step moves data across objects, systems, pages, or reports, also use `data-flow.md` to create a data flow map and linkage map.

## Child Object Lifecycle Gate

If a module mentions a child/secondary object, do not leave it as a column in an operation table. Invoice, payment trace, exception record, allocation detail, attachment, adjustment, receipt, refund, approval task, message, or external sync record may each need its own lifecycle, page placement, visibility, and rollback.

For each child object, define:

| Parent Module | Child Object | Why It Exists | Source / Creation | Lifecycle | Page / Entry | Key Fields | Role Visibility | Writeback | Reverse / Delete | Confirm |
|---|---|---|---|---|---|---|---|---|---|---|

If the child object is not needed as an independent object, say why it is only a display field or log line. If users must query, audit, correct, export, or operate it, treat it as a real object.

## Missing Link Exception Closure

When required linkage is missing, "mark exception" is not enough. Missing vehicle, customer, supplier, contract, source detail, external record, owner, permission, or mapping must have a page and recovery path.

Define:

| Missing Link | Detection Timing | Exception Workbench / Page | Manual Completion Fields | Validation | Recalculate / Rebuild | Re-enter Downstream Flow | Audit / History | Confirm |
|---|---|---|---|---|---|---|---|---|

Manual completion must say what users can fill, what source becomes authoritative after completion, which downstream records recalculate, and which flow step the record re-enters. Do not strand data in an exception status with no operator action.

## Formula Operand Semantics Gate

Use this before accepting any formula, not only finance. Formula words such as 保底/guarantee, 取大/take greater, max/min, cap, floor, tier, threshold, rate, coefficient, base amount, detail-calculated amount, and adjustment are not self-explanatory. Each operand must be a business object or source-derived value that a tester can compute.

For each formula, define:

| Formula | Operand | Business Meaning | Source / Authority | Entity Scope | Period | Eligibility | Unit | Comparison Basis | Proration | Rounding | Boundary / Exception | Confirm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Rules:

- Ask "保底是什么保底 / guarantee of what?" before writing a guaranteed amount as final wording.
- For max/min or take greater/take smaller, define the comparison basis: same period, same driver/customer/order/resource, same tax/currency/unit, and whether zero/negative values participate.
- For base amount vs detail-calculated amount, define whether the base is configured, contracted, manually adjusted, or generated, and whether the detail amount comes from orders, waybills, usage, inventory movement, or source records.
- Define adjustment timing: whether加减项/adjustments happen before comparison, after comparison, inside each operand, or as separate ledger lines.
- Define proration for partial periods, onboarding/offboarding, inactive days, missing source details, and no-activity cases.

## Resource / Value Flow Gate

Use this not only finance. Any non-finance controlled resource can break the product if its loop is vague: inventory, coupon, quota, points, seat capacity, task capacity, appointment slots, membership rights, content permission, API usage, visibility rights, or approval authority.

For each resource/value object, define:

| Resource | Source / Authoritative Anchor | Eligibility | Reserve / Occupy | Allocate / Combine | Consume / Settle | Release / Reverse | Pool vs Trace | Role Perspective | Confirm |
|---|---|---|---|---|---|---|---|---|---|

Rules:

- Do not invent the authoritative anchor. A created time, sync time, approval time, or receipt time is only valid when the business object truly uses it as the anchor.
- If partial insufficiency can happen, decide whether users/system can combine multiple resources or sources; do not force a single-source rule without confirmation.
- Separate pool from trace. The current available pool controls use; source trace explains history. A one-to-one source pairing is required only when the business says so.
- Define reserve/release even when there is no money: stock reservation, coupon lock, appointment slot hold, content permission grant, quota occupation, task capacity allocation.
- Show the role perspective: the acting user, owner, approver, counterparty, platform/admin, or tenant may need different visibility and disabled reasons.

Do not ask every axis for every object at once. Prioritize:

- money, contract, invoice, payment, settlement, approval;
- cross-system/source data;
- irreversible or hard-to-roll-back actions;
- state or formula contradictions;
- items the user marked "待产品确认" or "待更新".

## Confirmation Discipline

When the user says "你来 / 按最佳实践", give a recommended default and mark it as pending confirmation unless it is harmless and reversible.

When a note says "待产品确认 / 待产品提供 / 暂无 / 留空", preserve it as an explicit open item or out-of-scope rule. Do not silently complete it.
