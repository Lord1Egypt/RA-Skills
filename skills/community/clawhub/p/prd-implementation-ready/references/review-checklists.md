# Review Checklists

Use before saying a PRD is complete or when the user asks to review an existing PRD.

## Stage and Flow

- Does the PRD stay lean: no needless entities, fields, states, pages, components, tables, or repeated prose?
- For each added object/status/field/page/component/flow step, is the user/business/process need clear?
- Are the agreed business mainline and business anchors written explicitly before detailed rules?
- Did the assistant preserve user-confirmed anchors when recommending best practices, rewriting, or polishing?
- If the user changed the business mainline or an anchor, was the change handled through an impact table before rewriting?
- Were affected business context, scope, objects, lifecycles, data flows, linkage, rules, pages, exceptions, acceptance criteria, indexes, and module references updated together?
- Were obsolete downstream口径 removed or marked superseded instead of coexisting with the new mainline?
- Does every extension beyond the mainline have a basis: user confirmation, anchor, source data, existing behavior, research recommendation pending user confirmation, or 待确认?
- Are obvious insider premises written clearly enough for a new reader?
- Can a new reader understand what business this is before reading rules?
- Is the business goal written separately from the system construction goal?
- Are role glossary, core concepts, and special/counterintuitive terms defined in plain language?
- Do money/value/data flows among roles have a simple front-door explanation?
- Is every controlled resource/value closed loop before writing modules: source, reserve, allocate, consume, release, reverse, and role visibility?
- Are circular definitions avoided, especially for financial concepts?
- Is the business goal clear before details?
- Is scope explicit, including out-of-scope?
- Is the main flow confirmed before exceptions and states?
- Did the assistant compare original, recommended, and MVP flow when useful?
- Did it guide the user when flow was awkward?

## Coverage Matrix

- Are all core business objects extracted from the notes, not only page/menu names?
- Did the assistant apply the necessity gate before adding new entities or details?
- For each core object, were source/creation, lifecycle, information delta, data flow, resource/value flow, linkage/side effects, actor, time/period, amount/formula, state axes, data fields, query/list, interaction, locking, reverse flow, cross-system, cross-module, and audit trail considered?
- For each core object, is there a flow / information ledger showing each step, actor/system, state change, newly introduced information, source/authority, validation, persistence target, side effect, and failure/retry?
- When a step creates or updates another object, was that downstream object added to the object list and covered too?
- Are open items marked as confirmed, recommended default pending user confirmation, 待确认, or out of scope?
- Did the assistant ask only the highest-risk missing decisions first instead of dumping every axis at once?
- Was the matrix re-run after the main flow changed?

## Reader-First Completeness

- Treat "Readable but incomplete" as a red flag, not as a successful simplification.
- Does the PRD preserve complete information for implementation, testing, UX, risk, operation, money movement, source data, state changes, exceptions, and acceptance?
- Was a coverage ledger used or mentally checked so every build-critical coverage item is Covered, Missing but required, Recommended default, Pending confirmation, Out of scope, or External source required?
- Are Missing but required items either written into the local section, converted to a recommended default pending user confirmation, or left as explicit Pending confirmation / External source required instead of silently omitted?
- Are details placed near the workflow, page, operation, object state, or server-only flow where the reader needs them?
- Did the assistant avoid fixing readability by deleting fields, states, source rules, eligibility conditions, period anchors, failures, reversals, writebacks, permissions, idempotency, audit, or acceptance?

## Confirmation Discipline

- Treat "Unconfirmed final wording" as a P0 issue.
- Is every final rule confirmed by the user, copied from a user-confirmed in-scope source without changing meaning, or accepted as a best-practice default after user confirmation?
- Are best-practice defaults marked as recommended until the user says OK?
- Is every inference, external-source import, market pattern, low-risk default, and assistant proposal not silently promoted into final wording?
- If the user said "you decide" or "best practice", did the PRD still show the recommended default and wait for confirmation before finalizing it?

## Data Flow and Linkage

- Is there a data flow map for high-risk data: source/authority, trigger, transform/rule, validation, persistence target, consumer, writeback/sync timing, and failure handling?
- Does every list, field, status, statistic, formula operand, selectable record set, and default value show a visible data source marker in正文 or its local table?
- Were visible data source markers checked for真实性 and consistency: source exists in the flow, contains the data used, authority is clear, timing is valid, and cross-doc wording is consistent?
- For internal generated data, are trigger, input data, generation rule/version, persisted object, authority after generation, consumers, and correction/rebuild behavior clear?
- For non-finance resources such as inventory, coupon, quota, points, capacity, permission, entitlement, slots, or visibility rights, are source, authoritative anchor, pool, trace, reserve, allocate, combine, consume, release, partial insufficiency, and role perspective defined?
- Is there a linkage map for high-impact actions: linked objects/modules, linkage type, side effect, trigger timing, reverse/rollback, user visibility, and risk?
- For payment completion, are attached actions defined with idempotency, retry, partial failure handling, visibility, and reverse/compensation?
- For transaction completion / payment success / audit pass / refund success / batch creation / callback completion, is there a post-event writeback inventory covering target object, exact persisted field, source event timestamp, business period, writeback policy, consumer, idempotency, and reverse/correction behavior?
- For repeated/cyclic operations, did the assistant proactively identify any progress-control field such as last paid month, handled-through period, next period, eligibility marker, or last issued time, then define reader action, locked/default value, success event that advances it, non-advance events, duplicate prevention, and reverse/correction behavior?
- Are "同步更新 / 自动回滚 / 联动处理" decomposed into affected objects, affected fields, timing, and failure behavior?
- For reverse actions, are released locks, reverted data, recomputed data, non-reverted data, and audit reason clear?

## P0 Consistency and Computability

- If multiple PRD files exist, are the same objects, actions, statuses, and money terms consistent across files?
- Are business anchors consistent across all module docs?
- Before rewriting a section, were the original business conclusions preserved or explicitly changed with confirmation?
- If a confirmed anchor changed, does every downstream module now follow the new anchor and no stale wording remain?
- Are document links, file ranges, module indexes, and reading order accurate after docs are merged, deleted, or renumbered?
- If an item is marked pending / out of scope / not in acceptance, is it prevented from appearing later as confirmed implementation detail?
- Does every fund movement define source amount, split rule, timing, side effect, and reversal?
- Does every controlled resource/value movement define source, pool, trace, one-to-one rule, combine rule, state effect, role perspective, and reversal?
- If a page says platform-side, finance-side, admin-side, or operator-side, are system side, organization scope, operator role, viewed subject, and data/action scope separated?
- If the platform can see all records, is that platform scope preserved instead of being narrowed to one operator role's self view?
- Are invoice, payment trace, exception record, allocation detail, attachment, adjustment, receipt, refund, approval task, or external sync record treated with a child object lifecycle when users need to query/operate/audit them?
- If a rule uses a single total for summary calculation, are detail dimensions such as vehicle dimension, customer/shipper, supplier, contract, route, project, cost type, and period still preserved for dimension analysis when useful?
- For annual/prepaid/cross-period costs, are cash payment and cost recognition separated, with monthly amortization or another allocation rule when needed?
- Does every cost entering downstream bills pass a Cost Inclusion State Gate: audit status, payment status, recognition state, locked cost period, inclusion/exclusion states, and rebuild behavior?
- Does every formula define operand semantics, source/authority, entity scope, period, eligibility, comparison basis, proration, rates, caps/floors, tier, threshold, rounding, snapshot, and zero/negative handling?
- For guarantee/保底, max/min/取大取小/take greater, base amount, detail-calculated amount, and adjustments, does the PRD answer guarantee of what, what is being compared, and whether adjustments happen before comparison or after comparison?
- Does every amount field have an authoritative source document, contract, bill, fee item, import, or manual adjustment source?
- If a payment order is created, is it clear whether it triggers real external payment or only records a business/accounting action?
- If a payment order is created from another module, does it carry payment order origin payload: source object, business type, payer/payee, receiver account, amount split, transaction metadata, trigger/status, and reverse/retry?
- Are platform service fee payer, receiver/platform pocket, rate snapshot, fee base, ledger effect, and collection/deduction timing defined?
- Does profit sharing define the profit-sharing funds waterfall, contractor own-funded advances, insufficient/continuing deduction, zero/negative profit sharing, and profit-sharing void fund rollback?
- If credit/support fund is central to the product, is centralized credit management specified for grant, occupation, repay, release, limits, page operations, and ledger reconciliation?
- Is every "audit" tied to a specific audited object, audit actor, audit type, and post-approval side effect?
- Are ghost statuses eliminated: every status in body text, Tab/filter, exception handling, and state machine is defined in one consistent place?

## Finance Operations

- Was the general Resource / Value Flow Gate applied first, instead of treating finance as a special pile of isolated rules?
- Does every monthly aggregation define attribution date, month boundary, current-month exclusion, late data handling, and lock/freeze behavior?
- For payments/recharges, are payer, payee, balance types, deduction priority, insufficient-balance handling, ledger effects, and reversal defined?
- For costs, are audit status, payment status, cost recognition state, locked cost period, late/missing source handling, and zero payroll line behavior defined where relevant?
- For supplier reconciliation, are supplier types separated, and do non-prepaid supplier flows include payment trace, payment status, and invoice management?
- For insurance, rent, license, maintenance package, or other annual/prepaid costs, is cash payment separated from monthly amortization/cost recognition?
- For driver payroll or freight settlement, are guaranteed pay, waybill-based freight, comparison basis, adjustment timing, period/entity scope, eligibility, and proration defined?
- For synced supplier/cost data, are source system, sync direction, sync mode, cursor, duplicate/update rule, disabled/deleted data handling, and sync timestamp defined?
- If a supplier is disabled after use, are historical visibility, future selectable scope, notifications, and effects on existing bills/contracts/drivers defined?
- For reconciliation, are selectable source records, grouping, locking, audit effects, invoice lifecycle, write-off, cancel/reject rollback, red flush, and void behavior defined?
- For reconciliation duplicate prevention, does the unique key include the real billing unit, and does it allow parallel projects / project/contract/billing unit / partial reconciliation when the business allows them?
- For customer/shipper billing, does monthly charter stay by vehicle when the commercial object is vehicle-based, and does transport-volume billing use shipper freight on the waybill or confirmed receivable source?
- For billing/profit-sharing, are vehicle, waybill, customer, supplier, contract, route, project, cost type, and period dimensions preserved for analysis when useful?
- For cross-module jumps, are source action, target menu/page/Tab, parameters, default filters, empty state, and permission behavior defined?
- If confirm and view-detail reuse a modal, are confirm mode, view mode, pagination/search, grouping, and amount-summary consistency defined?

## Source and Language

- Does every added interaction/default/filter/list/field have a source or待确认?
- Are data source, authoritative source, include/exclude conditions, and refresh timing clear?
- Are data sources visibly marked where the PRD uses them, not only implied in reasoning?
- Are internal sources such as generated records, snapshots, callbacks after idempotency, statistics, tasks, and copied fields treated as data sources with authenticity and consistency checks?
- Are technical fields, SQL conditions, code enums, and interface params converted to business wording?
- Are abstract terms such as 计价口径 / 统计口径 / 规则 / 策略 decomposed into fields, enums, IDs, versions, or source document sets?

## Rules and Objects

- Are core objects identified?
- Are state fields separated by axis: business confirmation, audit, payment, invoice, receipt, profit sharing, push?
- For each object, is the lifecycle traced from creation / initial state instead of starting midway at audit or payment?
- If an object has a pre-audit stage such as confirmation, calculation, matching, claim, signing, or submission, is that stage modeled separately?
- Are shared status labels valid for every listed object, or should some objects have object-specific state axes?
- Are state transitions clear, with trigger, actor, next state, side effects, forbidden scenes?
- Are source documents, unique constraints, idempotency keys, and writebacks defined?
- Are idempotency keys made of stable, comparable fields?

## Exceptions and Boundaries

- Network, permission, data, concurrency, duplicate submit, callback delay, callback repeat, callback disorder.
- Partial success and retry.
- Rollback, cancel, refund, reverse, rebuild rules.
- Empty, max, min, invalid input, file, amount, date, pagination.

## Page and UI

- Does the 00 主文件 include a main file navigation map / information architecture mind map showing 端 / 模块 / 页面 / 功能点 before module details?
- Can a reader immediately tell where each function lives, including default entry, target role, permission, data scope, and cross-side / 跨端 links?
- Target端 / touchpoint confirmed from user task and working context, not assumed.
- Menu/page structure confirmed from business reality, not style taste.
- Each page, Tab, component, and interaction is tied to a workflow constraint, user task, risk control, or comprehension need.
- Page-level Tabs vs list filter Tabs are separated.
- UX carrier and components are specified for key pages/actions: table, detail, drawer, modal, wizard, batch action, exception workbench, upload/download, timeline/log.
- Important actions define primary/secondary actions, disabled reasons, confirmation copy, validation, recovery, and audit trace.
- High-density tables define key fields, default sort, pagination, frozen/important columns, empty state, and export needs.
- Cross-module links define target page/Tab, parameters, default filters, permission, and empty target behavior.
- design.md / existing UI conventions checked if available.
- Loading, empty, disabled, submitting, success, failure, high-risk confirmation covered.
- Exception workbench exists for missing vehicle/customer/supplier/contract/source mappings, with manual completion, validation, recalculation, and re-enter downstream flow.

## Output Placement

- Global overview contains only cross-module summary rules and main flow.
- Page-level Tab filters, field tables, button rules, and sort rules are in the relevant module/page.
- Detailed tables do not appear only in the index/global overview.

## Red Flags

- "通用上更正确" wording that replaces a user-confirmed business fact.
- "大家都知道 / 默认就是 / 这个不用写" around pricing, funds, roles, source data, or status.
- Detailed implementation that cannot point to a user discussion, anchor, source, existing behavior, or recommendation label pending user confirmation.
- "数据来源：系统生成 / 平台同步 / 自动统计" without trigger, input, rule, persisted object, authority, and consistency check.
- "按规则处理", "具体以实际为准", "计价口径", "有效单据" without definition.
- Long sections or tables that do not change behavior, testing, UX, risk, or implementation.
- New status/object/page/component added only for neatness, not because the flow requires it.
- `incomeStatus in (...)` or code enum in PRD正文.
- "可勾选", "默认全选", "自动处理" without source.
- Global overview stuffed with page-level Tab filter tables.
