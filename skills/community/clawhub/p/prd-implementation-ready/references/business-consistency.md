# Business Consistency and Computability

Use this when reviewing multiple PRD files, finance/payment/settlement requirements, or any flow involving funds, payment orders, audit, refunds, allocation, cost, profit sharing, amount calculation, inventory, coupon, quota, permission, capacity, entitlement, or other resource/value movement.

## P0 Rule

Treat these as P0 blockers. Do not continue writing detailed PRD口径 until the user confirms them:

- A confirmed business anchor is contradicted, weakened, or replaced by generic wording.
- A user changes the business mainline / anchor, but the PRD is patched locally without impact analysis across affected business, object, data, linkage, page, and acceptance sections.
- A derived implementation detail cannot trace back to user confirmation, a business anchor, source data, existing system behavior, research recommendation pending user confirmation, or待确认.
- A list, field, status, statistic, formula operand, selectable record set, or default value uses data but has no visible data source marker in the PRD.
- A named data source cannot be verified as real in the confirmed flow, conflicts with another module, or lacks authority / timing / update rules.
- Internal generated data is described as "system generated" without trigger, input, generation rule, persisted object, authority, and correction behavior.
- The same object/action/status is described differently in different files or sections.
- The document index, file references, reading order, or "higher than 01-07" style scope statement points to deleted, merged, or nonexistent docs.
- A topic is marked pending / out of scope / not in acceptance in one place but later written as confirmed detailed implementation.
- A money movement says funds increase/decrease/split/freeze/refund, but does not define the calculation rule.
- A non-finance resource movement says inventory/coupon/quota/permission/capacity is granted, reserved, allocated, consumed, released, or revoked without source, authoritative anchor, pool, trace, one-to-one rule, or reversal.
- A cost enters a monthly bill, reconciliation, profit sharing, or report without a Cost Inclusion State Gate: audit status, payment status, cost recognition state, locked cost period, inclusion/exclusion states, and rebuild behavior.
- A duplicate prevention key blocks business work without proving whether parallel projects, project/contract/billing unit, partial reconciliation, or source-detail occupation allow multiple valid bills in the same broad period.
- A billing or profit-sharing rule collapses vehicle, waybill, customer, supplier, contract, route, project, cost type, or period dimensions before deciding which downstream calculations use totals and which analytics preserve detail.
- A platform service fee appears without payer, receiver/platform pocket, rate snapshot, fee base, ledger effect, and collection/deduction timing.
- A profit-sharing flow lacks a profit-sharing funds waterfall: customer funds, frozen funds, platform-granted credit, contractor own-funded advances, platform service fee, remaining profit, insufficient/continuing deduction, zero/negative profit sharing, and profit-sharing void fund rollback.
- A payment order lacks payment order origin payload: source business object, business type, payer/payee, receiver account, amount split, transaction metadata, trigger/status, and reverse/retry rule.
- Payment completion changes only payment status while attached business actions, idempotency, retry, partial failure, visibility, and reverse behavior are not specified.
- Missing post-event writeback is a P0 blocker: transaction completion, payment success, audit pass, refund success, batch creation, sync completion, or callback completion changes existing objects but the PRD does not list the writeback inventory, target object, exact persisted field, source event timestamp, business period, writeback policy, consumer, idempotency, and reverse/correction behavior.
- Missing progress-control loop is a P0 blocker for repeated/cyclic operations: if a field like last paid month, handled-through period, next period, eligibility marker, or last issued time determines the next create/action range, the PRD must define who reads it, how the next value is derived and locked, what prevents duplicate/overlap/gap, which success event advances it, which failures do not, and how void/reissue/correction behaves.
- Credit/support fund logic appears only as side effects or account fields, without centralized credit management for grant, occupation, repay, release, limits, page operations, and ledger reconciliation.
- An amount field is used in a formula but has no authoritative source.
- A formula uses guarantee/保底, max/min/取大取小, cap/floor, tier, threshold, base amount, detail-calculated amount, rate, coefficient, or adjustment without defining operand semantics, comparison basis, period, entity scope, eligibility, proration, and adjustment timing.
- A period-based finance rule mentions current month, this month, this period, billing cycle, same month, next month, locked month, late data, backfill, or correction without an explicit attribution anchor and period boundary.
- A source-generated bill, reconciliation, settlement, payment, invoice, profit-sharing, or recovery flow says "select orders / select waybills / select details" without source detail eligibility, occupation, release rule, and unavailable reason.
- A relative period phrase such as "本月", "当月", "本期", "账期内", "周期内", or "同月" appears without naming the business object, authoritative time field, period boundary/timezone, and cross-month rule.
- A larger or older out-of-scope document is used to judge, replace, or import口径 into the user-selected scope without explicit user permission.
- A "payment order" is created but whether it triggers real payment is unclear.
- "Audit" is mentioned but the audited object, audit type, actor, and side effect are unclear.
- A status appears in body text, Tab names, filters, or exception handling but is missing from the state axis / enum / transition table.

## Cross-Document Consistency Scan

Run this scan only across documents inside the user-selected scope. If the user-selected scope is one directory or one file, sibling directories and old versions are out-of-scope document sources, even if they are larger or older. Ask before expanding scope.

When reviewing multiple docs, actively compare the same term across files. Use a table like:

| Object / Term | Location A | Location B | Conflict | Why It Blocks | Recommended Question |
|---|---|---|---|---|---|

Check especially:

- business anchors, pricing/fund/source/status premises, and "obvious" domain facts;
- visible data source markers, authoritative sources, generated-data rules, and copied-field update rules;
- attribution anchor, source detail eligibility, relative period phrase definitions, source occupation, and occupation release rules;
- document links, module numbers, reading order, and "this doc overrides..." statements;
- object names: cost bill, payment order, reconciliation bill, profit bill, invoice, receipt, refund;
- actions: create, submit, confirm, audit, pay, refund, reverse, void, rebuild, push;
- states: pending audit, pending payment, paying, failed, refunded, exception pending confirmation;
- money words: available, frozen, occupied, released, deducted, transferred, allocated, shared.
- non-finance resource words: inventory, coupon, quota, points, capacity, permission, entitlement, slot, reservation, grant, revoke, consume, release.

## Data Source Authenticity Guard

When a PRD names a data source, verify that the source is not only plausible but usable:

| Data Item | Claimed Source | Source Exists In Flow? | Authority Consistent? | Timing Valid? | Internal Generation Complete? | Conflict Location | Required Fix |
|---|---|---|---|---|---|---|---|

Include internal sources such as generated bills, snapshots, status counts, to-do tasks, callback results after idempotency, imported staging records, and manually adjusted records. They must be checked the same way as external systems.

## Money and Formula Computability Guard

Every amount or fund movement must be computable from business information. Require:

| Item | Must Define |
|---|---|
| Source amount | Which source document / contract / bill / fee item provides it |
| Formula | Operand, operator, rate, cap/floor, tax handling, rounding |
| Allocation | If one amount enters multiple pools, define split rule, priority, and conservation check |
| Snapshot | Whether the calculation freezes source data, rule version, and result |
| Timing | When the calculation happens and when it can be recalculated |
| Reversal | How cancel, refund, reject, or rebuild affects the amount |

If any part is missing, write "不可计算，需确认" and explain what cannot be tested.

Examples:

- "来账确认后增加货主冻结资金和运营支持金" is incomplete unless it defines how one receipt amount is split between the two pools.
- "分润金额" is incomplete unless it defines profit formula, sharing parties, sharing ratio/source, rounding, snapshot, and negative/zero handling.
- "按月包车应收金额" is incomplete unless it defines whether the source is shipper contract, monthly fixed amount, route/package agreement, manual adjustment, or imported bill.

## Formula Operand Semantics Gate

This gate catches the "the formula looks obvious, but the business term is undefined" failure. A formula is not complete because it has operators. It is complete only when each operand has business meaning and a source.

Use it for finance and non-finance formulas involving guarantee/保底, max/min, take greater/take smaller, cap, floor, tier, threshold, rate, coefficient, base amount, detail-calculated amount, adjustment, score, quota, usage, points, or ranking.

Require:

| Item | Must Define |
|---|---|
| Formula purpose | What business decision/result this formula creates |
| Operand semantics | What each operand means in business language, not only its label |
| Source / authority | Which contract, configuration, bill, order, waybill, attendance, usage, source record, or manual adjustment provides it |
| Entity scope | Driver, vehicle, customer, supplier, contractor, tenant, order, resource, or period owner |
| Period | Daily, monthly, billing cycle, service period, employment period, policy period, or custom cycle |
| Eligibility | Which records/people/resources qualify and which are excluded |
| Comparison basis | For max/min/take greater: same scope, same period, same unit/currency/tax basis, and comparable states |
| Proration | New join/leave, partial period, inactive days, no source records, missing mapping, or mid-period rule changes |
| Adjustment timing | Whether adjustments happen before comparison, after comparison, inside one operand, or as separate lines |
| Boundary behavior | Zero/negative, missing operand, tie, cap/floor, rounding, precision, locked period correction |

Diagnostic questions:

- 保底是什么保底 / guarantee of what: monthly guaranteed pay, daily guaranteed amount, route guarantee, vehicle guarantee, contract minimum, or platform subsidy?
- What is it compared with: detail-calculated amount, order amount, waybill-based freight, usage value, score, quota, or another configured base?
- Are plus/minus items included before comparison or after comparison?
- Does the result need explainable line items so users can audit why the max/min branch won?

Example:

Driver payroll is incomplete if it only says `max(guaranteed pay, waybill-based freight) + adjustments`. It must define the guaranteed pay source and period, which driver/entity scope it applies to, how waybill-based freight is calculated and filtered, whether absent/new/left drivers get proration, whether adjustments are before comparison or after comparison, and how the chosen branch is shown on the payslip.

## Resource and Value Computability Guard

This is the non-finance version of money computability. Any controlled resource/value must be testable and conserved.

Require:

| Item | Must Define |
|---|---|
| Source | Where the resource/value comes from and who owns it |
| Authoritative anchor | The business event/field that proves the resource exists or belongs to a period/object; do not invent one from an easy timestamp |
| Pool | Current available/reserved/occupied/consumed/released amount or state |
| Trace | Source record/history used for audit or source-level control |
| One-to-one rule | Whether use/release must match a specific source trace or can come from the current pool |
| Combine rule | Whether multiple resources/pools can combine under partial insufficiency |
| State effect | Which object status, visibility, or downstream flow changes |
| Reversal | How cancel, timeout, reject, disable, revoke, refund, rebuild, or correction restores or preserves the resource |
| Role perspective | What actor, owner, counterparty, tenant, or admin can see and operate |

Examples:

- Coupon use is incomplete unless it defines grant source, validity anchor, reserve-on-submit, consume-on-paid, release-on-cancel, and whether several coupons can combine.
- Inventory reservation is incomplete unless it defines source stock pool, reserve timing, partial insufficiency behavior, release timeout, and oversell prevention.
- Content permission is incomplete unless it defines who grants it, which object it attaches to, who can see it, revoke behavior, and downstream visibility changes.

## Audit / Payment Disambiguation

When a doc says "create payment order" or "audit", ask:

| Question | Purpose |
|---|---|
| Is the object a cost item, payment order, fund adjustment, or only an accounting record? | Avoid mixing cost audit and payment audit |
| Does it trigger real external payment? | Avoid fake payment orders creating payment status noise |
| Who audits it? | Separate contractor confirmation, operator audit, finance audit, platform risk audit |
| What changes after approval? | Define side effects: payable amount, paid amount, fund freeze, ledger entry, external call |
| Which state axis changes? | Avoid putting business confirmation, audit, and payment into one status |

## Ghost Status Guard

Every status label must close across the PRD:

| Mentioned In | Must Also Appear In |
|---|---|
| Body text | State axis or explicitly marked as sub-label |
| Tab / filter | Business inclusion / exclusion rule and source state |
| State machine | Trigger, actor, previous state, next state |
| Exception handling | Recovery path and terminal behavior |

If a label such as "异常待确认" appears but is absent from the status enum / state machine, decide whether it is:

- a primary state;
- a sub-status / risk flag under another primary state;
- a Tab label composed from multiple states;
- stale wording to delete.

If a Tab, field, or正文 mentions an in-process state such as "处理中", "待确认", "部分成功", "失败待处理", or "退款中", the state machine must show the intermediate state, its trigger, retry / cancel behavior, timeout handling, and terminal transition. Do not jump directly from "发起" to "已完成 / 已失败" while displaying a middle state elsewhere.

Do not leave ghost states in final PRD正文.
