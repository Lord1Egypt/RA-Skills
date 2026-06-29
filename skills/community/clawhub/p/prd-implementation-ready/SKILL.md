---
name: prd-implementation-ready
description: Use when writing, reviewing, or filling gaps in PRDs, product requirements, BRDs, functional specs, or SaaS/admin workflows that must become implementation-ready. Especially useful for business flows, object states, page UX, data sources, permissions, exceptions, finance/payment/reconciliation/profit-sharing, formulas, and post-event writebacks.
---

# PRD Implementation Ready

## Core Principle

The job is not "fill in a document." The job is **to figure out the product together with the user** — align on the real need, research the domain, design the whole flow and UX — and then capture that as a doc a developer (or an AI) can implement directly. Work progressively: confirm what the business is trying to do, identify the flow shape, scan business possibilities, reconstruct every business flow, then expand into object flow, data flow, linkage, rules, exceptions, object status changes, data, page structure, and final detail. Do not force a real parallel, master-child, state-machine, event-driven, or cycle workflow into one artificial sequential mainline. **Be complete but lean** — do not add words, entities, statuses, pages, fields, or components unless they make the product clearer, safer, more usable, or more testable. **Never dump every checklist at the user at once, and never let a generated detail enter the PRD without a source or a 待确认 mark.**

## Definition of Done — The One Bar

A good PRD passes one test: **a developer or AI can implement it without coming back to ask a single business question. The only thing left open is technical 选型 (framework, library, storage), never business behavior.**

Concretely, every one of these must be answered in the doc, not in the reader's head:

- **Flow** — who triggers each step, preconditions, what object/state changes, what gets written back, who handles failure.
- **Boundaries** — what is explicitly in scope and out of scope; what the system does NOT do.
- **Exceptions** — every reverse/abnormal path. Transactional: 驳回, 失败, 作废, 重复提交, 回调重复/乱序/延迟, 并发, 金额为零或负. Content/social/C端: 内容删除后悬空引用, 拉黑/举报, 重复操作(重复点赞/打卡), 权限变更(关注后对方转私密), 上传失败重试, 跨时区日界. Pick the abnormal paths that actually exist in *this* domain.
- **Pages** — every page's content: list fields + data source, filters/sort/Tabs in business language, detail/drawer/modal behavior, operations + which states allow them, empty/loading/disabled/submitting/success/error states, high-risk 二次确认.
- **Data** — each field's source object/snapshot, authoritative source, include/exclude conditions, refresh timing.
- **Rules** — every formula decomposed into operands (no black-box 计价口径); uniqueness keys from stable fields; idempotency; permissions and 端-level data isolation.

If a reader would have to ask "but what happens when…" or "where does this number come from?", it is not done. Do not multiply 待确认. When a safe working口径 can be derived from business anchors, source data, existing system behavior, or a low-risk best-practice default, close the decision with that default and its basis. Use **待确认 + recommended default** only when the user explicitly leaves it open, sources conflict, or no safe default exists.

**When the user's draft is a downgrade of a doc that already exists**, do not silently backfill it into a fresh "complete" version — that creates two contradictory docs. Diff the draft against the existing locked doc, reconcile to its 口径, and ask the user which differences are intentional changes vs accidental omissions. Treat a regression as a question, not a gap to quietly fix.

## The Other Bar — Is the Product Any Good?

Definition of Done checks whether the doc is *complete*. But a complete doc can still describe a clumsy product. A good PRD also has to pass a **quality bar**: the flow is smooth and the UX is good — not just fully specified. Both bars must hold; completeness without quality ships a well-documented bad product.

So part of the job is to actively make the product better, not just record it:

- **Find best practice / research the domain** — before locking a flow, look at how mature products in this domain (and adjacent ones) solve the same problem. Aligning to a proven pattern beats inventing one. (Research Is a Hard Gate, below.)
- **Analyze flow smoothness and optimize it** — for the agreed flow, ask: redundant steps, things the user re-enters, a step that could be validated earlier, one object carrying too many jobs, offline coordination the system could remove. Where the flow is awkward, say so and propose a cleaner one with the tradeoff. (`references/research-and-flow.md`)
- **Analyze UX quality and optimize it** — judge whether each page/interaction is the right carrier (list vs detail vs drawer vs wizard), the right information density, the right defaults, the right empty/loading/error/confirm behavior. Good UX is a product decision tied to the workflow, not decoration. (`references/page-ui.md`)

Guide the user toward the better product; do not merely transcribe what they first described. Every improvement is a recommendation until confirmed.

## When NOT to Use

- Editing one field label, copy, or visual style — just do it.
- A simple, single-step requirement with no money/state/data-source/cross-system risk — answer directly.
- Non-business tasks (pure code, infra, docs unrelated to product requirements).

## Progressive Workflow

1. **Business First** — plain-language business context, agreed mainline, non-negotiable premises, scope (in/out), users, role glossary, core concepts, business objects.
2. **Flow Shape Next** — identify whether the requirement is single-line, parallel, master-child, state-machine, event-driven, cycle/periodic, or a mix. For parallel flows, name each independent line and its convergence points instead of flattening it into one sequential story.
3. **Navigation and Flow Diagrams Before Detail** — in the main PRD / 00 主文件, output a side/module/page/function navigation map and a business flow atlas before detailed rules, page specs, or field tables. Use Mermaid diagrams to show where each function lives, global relationships, each independent flow, key convergence points, and object status changes.
4. **Research Before Locking** — see "Research Is a Hard Gate" below.
5. **Rules After Flow** — only after the flow shape and diagrams are clear, drill into states, source documents, idempotency, data sources, permissions, exceptions, boundaries, and rollback.
6. **Pages After Business Shape** — menu/page organization, page-level Tabs vs list Tabs, design.md/UI conventions, interaction habits.
7. **Write After Confirmation** — show confirmed rules, recommended defaults, open high-risk decisions, out-of-scope. Wait for confirmation.

## Main PRD Flow Diagrams

When producing the main PRD file, begin with a **business flow atlas** before detailed rules, page specs, field tables, or acceptance criteria. Pick the diagram set based on the flow shape:

- For a single-line flow, draw one Mermaid `flowchart` for the full path.
- For parallel or master-child flows, draw one global relationship/convergence diagram plus one Mermaid `flowchart` per independent flow line.
- For event-driven or cycle/periodic flows, draw the trigger/timing loop and the downstream side effects/writebacks.
- For every key business object with a lifecycle, draw a Mermaid `stateDiagram-v2` showing object status changes, allowed transitions, rollback/reopen paths, terminal states, and which flow step triggers each transition.
- Mark convergence points explicitly: which flow depends on which object status, which data is written back, which downstream flow is unlocked/frozen, and which exceptions interrupt another flow.

Diagrams clarify structure; they do not replace rules. After each diagram, still write the trigger, preconditions, actors, input/output, persisted object, status changes, exception branches, downstream impact, and testable acceptance criteria.

## Main File Navigation Map

For a multi-module or multi-side PRD, the 00 主文件 must include an information architecture / mind map before module details so users can immediately see where each function lives. This map complements the business flow atlas: the atlas explains how the business runs; the navigation map explains where users find and operate each capability.

Use Mermaid `mindmap` or `flowchart`:

- Level 1: 端 / side / touchpoint, such as platform-side, customer portal, supplier portal, contractor portal, mobile, API/system job.
- Level 2: 模块 / module.
- Level 3: 页面 / page, page-level Tab, workbench, detail page, drawer, or server-only flow.
- Level 4: 功能点 / function point, key operation, list, import/export, exception handling, report, or configuration.

For each node with meaningful difference, mark default entry, target role, permission, data scope, and cross-side / 跨端 linkage. Do not bury this in module text. The reader of 00 should know which side/module/page owns each function before detailed module PRDs begin.


## Business Possibility Scan

Before locking flows, actively scan for business shapes that are easy to miss. This is especially important for SaaS, marketplace, platform, finance, approval, and partner-collaboration products.

Treat multi-tenant / 多租户 and SaaS compatibility as a first-class possibility, not a late technical detail. Check whether the same customer, same legal entity, account, supplier, contractor, employee, or asset can appear in multiple tenants, multiple organizations, or multiple roles at the same time.

For each possibility, decide whether it is in scope, out of scope, or closed by a recommended default:

- Same customer across multiple tenants: one customer cooperates with several tenants, branches, service providers, or projects.
- Same legal entity in multiple roles: customer, supplier, contractor, payer, receiver, approver, operator, or platform account at different times.
- Tenant isolation vs shared identity: which data is tenant-private, which identity/account can be shared, and what users see when the same subject exists in several spaces.
- Data ownership and cross-tenant permissions: who owns records, who can view/export/operate, and whether cross-tenant aggregation is allowed.
- Duplicate, merge/split, migration, and compatibility: existing data import, tenant migration, tenant merge/split, customer re-bind, account reuse, historical snapshot, and backward compatibility.
- Billing, settlement, invoice, contract, and approval boundaries across tenants or roles.
- Integration compatibility: callbacks, external IDs, source systems, webhooks, and third-party records that may not follow the product's tenant model.

Do not add all of these to the PRD as features. Use them as a possibility scan to prevent wrong assumptions. If the answer is "not supported in MVP", write the boundary and the safe behavior.

## Resource and Value Flow Gate

Many PRD mistakes are not finance mistakes. They are resource-flow mistakes. Use this gate for any controlled resource or value object, not only finance: money, credit, inventory, coupon, points, quota, seat capacity, delivery capacity, task capacity, appointment slots, assets, vehicle energy, content permission, membership rights, API usage, approval authority, visibility rights, or any scarce/controlled thing.

Before writing modules, prove the closed loop:

1. **Source**: where the resource/value comes from, who owns it, and which authoritative anchor proves it exists. Do not invent an anchor such as creation time, receipt time, sync time, or approval time unless that field is truly authoritative for the business object.
2. **Eligibility**: which states, roles, tenants, contracts, periods, objects, or source records make it usable/selectable.
3. **Reserve / occupy**: when the resource becomes unavailable to others, what pool is affected, whether source trace is only audit or controls release, and whether one-to-one pairing is required.
4. **Allocate / combine**: whether one action can combine multiple sources or pools when partial insufficiency happens. Avoid single-source flows unless explicitly confirmed.
5. **Consume / settle**: which event actually uses the resource/value and what downstream object/status/writeback it creates.
6. **Release / reverse**: cancel, reject, timeout, refund, rollback, rebuild, disable, or correction behavior.
7. **Role perspective and visibility**: which actor sees the resource, the counterparty context, the disabled reason, and the history.

This is the same thinking behind fund flow, but it also applies to non-finance business. For example, an appointment quota, coupon balance, inventory stock, API quota, and content permission all need source, reserve, allocate, consume, release, trace, and role perspective.

## Reader-First Module PRD Structure

Module PRDs should be easy for humans to read first, then detailed enough for implementation. Do not open a module with dense rule tables unless the user explicitly asks for a checklist-only artifact.

Use this top-level order for each concrete module:

1. **Module Purpose**: What this module does, who uses it, which business problem it solves, what is in/out for this release, and the core objects it owns.
2. **Main Flow**: The module's business flow diagram and step list. Each step says who acts, what happens, what object is created/updated, and which status changes.
3. **Page Presentation**: What pages/Tabs/entry points exist and what the user sees first. Describe layout, information hierarchy, list/detail/drawer/modal carriers, and the primary path before listing every field.
4. **Key Operations**: The important actions users can take, grouped by page and object state.
5. **Risks and Exceptions**: The abnormal paths, irreversible points, failure recovery, concurrency, permission, and data-missing cases that matter for this module.

After the reader-first section, write implementation detail inside the page/action/server-flow where it belongs. Do not create separate generic sections for "fields and data source", "status and writeback", and "permissions and idempotency" when those details are easier to understand in the page context.

For each page, include **Page Implementation Details**:

- Page purpose, target user, entry, permission, and default view.
- Page layout: page-level Tabs vs list Tabs, filter area, table/list columns, key status tags, operation area, detail/drawer/modal placement, empty/loading/error/disabled states.
- Fields: display name, business meaning, required/optional, editability, validation, default, visibility, export behavior, and whether it appears in list/detail/form.
- Data source: where each list, field, option, statistic, default, and selectable record set comes from; source authority; generation/sync timing; fallback and consistency check.
- Status/writeback: which object status changes on this page, what is written back to source/downstream objects, and what gets locked/unlocked.
- Operations: trigger, preconditions, allowed states, input, confirmation, result, failure behavior, audit trace, and recovery.
- Permissions and idempotency: who can view/operate/export, how repeated clicks/submits/imports/callbacks are handled, and the unique business key when needed.
- Acceptance checks for the page and its important operations.

For **server-only automatic flows** that do not need page participation, still keep them inside the owning module. Write them as "后台自动流程" or "系统自动处理": trigger/timing, input source, processing rule, persisted object, status/writeback, idempotency/retry, failure/compensation, visibility/log/alert entry, downstream impact, and acceptance checks. Do not hide business behavior in a technical appendix just because no one clicks a page.
## What a Locked Mainline Must Contain

"Align the mainline first" is meaningless without saying what a complete mainline is. **The mainline is the closed loop of how value/money is created, flows through objects, and is finally settled — not a one-line process summary.** A summary like "成本归集 → 应收 → 分润 → 支付" is usually an *open* line: it emits 应收 but never says how the money comes in or gets collected. Modules hung on an open mainline will not reconcile.

A mainline is not locked until all of these are present and the loop closes end-to-end:

1. **Value / business goal** — who it serves, what value it creates. Without it, scope and tradeoffs can't be judged.
2. **Parties (roles)** — who triggers each step, who receives each result. Every step needs a "who".
3. **Core object chain (the nouns)** — value rides on objects: 运单 → 成本单 → 应收/应付 → 分润单 → 付款单. This chain is the skeleton modules are cut along.
4. **Steps & triggers (the verbs)** — for each step: who triggers, precondition, which object it creates/changes, what it writes back.
5. **End-to-end value loop — the most-often-missed, most-fatal element.** Where value enters, how it flows, where it exits, who closes the loop. **This is not only about money.** In a transactional product the loop is monetary (every 应收 has a matching 收; every 应付 a matching 付; every 授信/预存 a matching 核销/解冻). In a habit/content/social product it is a motivation loop (user invests → gets immediate payoff → social/feedback reward → that reward drives the next visit). In a tooling product it is a job-to-done loop (input → transform → trusted output the user acts on). If you think "my product has no money so this doesn't apply," you are about to skip the single most important thing to lock. Whatever the currency, if the loop has an open end, the mainline is incomplete.
6. **Irreversible / key nodes** — where things lock, where 打款 happens, what cannot be undone. These anchor the state-machine trunk and the risk points.
7. **口径 anchors on the mainline** — the high-risk口径 the flow depends on (计价/结算/唯一性/幂等). Even if details are still 待确认, mark which step each hangs on, or modules will each invent their own.
8. **Reverse paths on the trunk** — not every exception, only the ones that *change the shape of the mainline*: 作废, 退款, 红冲. They decide whether the loop runs in reverse.

**Acceptance bar:** can you cut every module out by following the mainline, and does each module map back to a step on it? Does the money loop connect head-to-tail with no open end? If not, the mainline is not locked yet — keep working it before writing any module.

Before locking, the mainline can be challenged and improved (Progressive Workflow #2). Once locked, it becomes an anchor that generic best practices must not override (Operating Rules). Challenge first, anchor after.

## Research Is a Hard Gate, Not an Optional Step

Before locking the flow or defaults, you MUST first read what already exists: project docs (design.md, ui-design-spec.md, old PRDs, screenshots), the code/data layer if relevant, and mature market/open-source patterns. Aligning to an existing 口径 beats inventing a new one.

**If a more complete version of this exact doc/module already exists in the repo, diff against it first.** Do not rewrite a mature PRD back into a draft. Reconcile to its 口径, merge any genuinely new intent, and surface conflicts — handing the team two contradictory docs is worse than handing them none.

Under time pressure this is the first thing skipped. Do not. If you genuinely cannot read sources now, write the affected口径 as 待确认 — never as confirmed.

## When Someone Demands the Full PRD Now ("别问了，直接写完整版")

This is the highest-pressure failure point. The wrong move is to abandon confirmation and write a PRD full of invented-but-unmarked rules. The right move:

- **You may write the full PRD immediately** — pages, fields, states, exceptions all present.
- **Every detail you were not given must either be closed with a sourced/reasonable recommended default, or marked 待确认** when the user explicitly leaves it open, sources conflict, or no safe default exists. Confirmed items come from the user's words, existing docs, source data, or a default you clearly state as the working口径.
- **Lead with the main flow + the 3-6 highest-risk口径** (especially 计价/结算/唯一性/打款幂等) as a confirm-first block, so the reviewer sees known gaps, not buried landmines.
- Money/contract/invoice/settlement formulas: never invent a concrete formula and present it as decided. Decompose into fields and leave the formula as a 评审必锁项.

Speed and rigor are not in conflict: deliver fast AND mark every unsourced detail. Skipping the 待确认 marks is not "saving time," it is shipping landmines.

## Write Incrementally, One Module at a Time

A multi-module PRD does not have to be written in one sitting. Writing all modules at once is high-pressure and produces modules that silently contradict each other. Instead:

1. **Align the mainline first** — agree the main flow, core objects, and highest-risk口径 with the user before writing any module.
2. **Write the core/global doc** (`00_总览`) — main flow, core objects, global rules, cross-module dependencies, in/out scope. This is the authority; modules must not contradict it.
3. **Write modules one at a time**, in dependency order. Each module carries only its own rules; shared state axes / 幂等 / 回写 stay in the core doc. Finish and confirm one before starting the next — small, low-pressure steps.
4. **Review them together at the end** — a cross-module linkage pass so the whole set tells one consistent story.

### Change Propagation — the discipline that prevents contradictions

While writing one module you will often discover a change. Handle it by **where the change lands, immediately — do not just note it and keep writing the current module:**

- **Touches the mainline / a global口径 / core object** → stop, fix the core doc (`00`) completely first, then cascade to every module that references it. Never patch it only in the current module.
- **Touches another module** → go change that other module too, now, so the two never disagree. Do not leave it for "later."
- **Local to this module** → just handle it here.

The failure mode this prevents: six modules that each look internally complete but disagree on the same formula/status/wording. Detecting that at final review is far more expensive than propagating each change when you find it. If a change to a confirmed mainline anchor is involved, confirm it with the user before cascading.

## Load References as Needed

Read only the references needed for the current stage:

| Situation | Read |
|---|---|
| Starting a PRD conversation or deciding the next stage | `references/stage-gates.md` |
| Deciding whether to add an object, state, field, page, component, flow step, table, section, exception, or detailed rule | `references/necessity-gate.md` |
| Capturing user-agreed business mainline, obvious domain premises, non-negotiable constraints, or preventing later rewrites from losing them | `references/business-anchors.md` |
| Reader may not understand the business, roles, domain terms, business model, special concepts, or value/money flow | `references/business-context.md` |
| Need broad coverage across business objects, object flow, or information introduced during each step without dumping all questions at once | `references/coverage-matrix.md` |
| Need to clarify data flow, cross-object linkage, side effects, writebacks, notifications, statistics, locks, rollback, or downstream impacts | `references/data-flow.md` |
| Requirement says a transaction completion, payment success, audit pass, refund success, callback, batch creation, sync/import, or cancellation updates another object/field such as last time, payment month, eligibility marker, summary counter, or next-period flag | `references/data-flow.md`, then `references/business-consistency.md` |
| A list/detail field such as last time, last month, last paid-through period, handled-through period, next period, progress marker, or eligibility marker is used to default, lock, or limit the next create/action flow | `references/data-flow.md`, then `references/business-consistency.md` and `references/page-ui.md` |
| Requirement involves any controlled resource/value such as inventory, coupon, quota, capacity, permission, entitlement, slot, balance, support credit, or visibility right | `references/coverage-matrix.md`, then `references/data-flow.md`, `references/business-consistency.md`, and domain-specific references |
| Requirement mixes platform-side/admin-side/finance-side/operator wording, or a page can switch viewed subjects | `references/page-ui.md`, then `references/business-context.md` and `references/coverage-matrix.md` |
| Requirement says "single total", "summary only", "按总额", "不按明细", or removes a detail dimension used for analysis | `references/data-flow.md` and `references/business-consistency.md` |
| Requirement contains formula operators or vague formula nouns such as guarantee/保底, max/min/取大取小, cap/floor/封顶兜底, tier/阶梯, threshold/门槛, base amount, adjustment, rate, coefficient, or "plus/minus items" | `references/business-consistency.md`, then `references/coverage-matrix.md` and domain-specific references |
| Requirement includes annual/prepaid/cross-period costs, one-time payments recognized over time, or amortization/accrual | `references/finance-operations.md`, then `references/data-flow.md` |
| Requirement involves costs entering bills/reconciliation/profit sharing, payroll, vehicle fees, supplier costs, insurance, or paid/unpaid cost inclusion | `references/finance-operations.md`, then `references/business-consistency.md` and `references/data-flow.md` |
| Requirement involves customer/shipper billing, monthly charter, transport-volume billing, platform service fee, profit sharing, settlement, or duplicate reconciliation | `references/finance-operations.md`, `references/data-flow.md`, and `references/business-consistency.md` |
| Requirement creates payment orders or says payment completion triggers downstream business actions, supplier output, payroll distribution, push, callback, unlock, or recovery | `references/finance-operations.md`, then `references/data-flow.md` |
| Requirement involves support credit, operating credit, frozen funds, contractor advances, grant, occupation, repay, release, or centralized fund governance | `references/finance-operations.md`, then `references/page-ui.md` |
| Requirement has missing required links such as unmatched vehicle, customer, supplier, contract, source detail, or external record | `references/page-ui.md`, `references/data-flow.md`, and `references/review-checklists.md` |
| User describes workflow, says "你来决定", or flow seems awkward | `references/research-and-flow.md` |
| Reviewing multiple docs, finding contradictory口径, or checking money / formula / fund movement computability | `references/business-consistency.md` |
| Finance operations include cost periods, fund priority, fund-flow, support credit, recharge/payment, sync data, supplier states, reconciliation, invoice, red flush / void, or cross-module jumps | `references/finance-operations.md` |
| Details may be unsupported, data source unclear, state axes / initial states uncertain, technical terms or 计价口径-type words appear | `references/source-language-guards.md` |
| Discussing target端, touchpoints, menus, page Tabs, UX, component choice, UI style, design.md, interaction habits | `references/page-ui.md` |
| User asks for full PRD, multiple docs, index/global rules, final structure | `references/output-structure.md` |
| Before claiming a PRD is complete, or reviewing an existing PRD | `references/review-checklists.md` |

## Operating Rules

- Recommend best-practice defaults when the user hasn't decided, but label them as recommendations until confirmed.
- Keep questions small: 3-6 decisions per batch, each with a recommended option and tradeoff.
- Do not invent terms. Use the user's wording, existing system labels, or confirmed business terms. If a new short label is needed, mark it as 建议命名 and keep the old wording nearby until confirmed.
- Close pending decisions by default: when existing business anchors, source data, system behavior, or a low-risk best-practice default is enough, write the recommended default as the working requirement instead of leaving it as 待确认. Leave 待确认 only when the user explicitly says it is undecided, sources conflict, or the decision is high-risk and has no safe default.
- Before locking flows, run a business possibility scan for SaaS/multi-tenant, multiple-role, cross-organization, migration, compatibility, and external-system variants. Close each as supported, blocked, later, or a recommended default.
- Treat short answers ("加 / 不需要 / 你来 / 按最佳实践") as decisions to digest, not missing context.
- Use the minimum structure that makes the product buildable, testable, and understandable. Do not add entities, statuses, pages, components, tables, or prose just to look complete.
- **Formula Operand Semantics Gate:** Before writing any formula with guarantee/保底, max/min/取大取小, cap/floor, tier, threshold, rate, base amount, detail-calculated amount, or adjustment, define every operand's business meaning, source, entity scope, period, eligibility, comparison basis, rounding, and boundary behavior. A formula is not complete until a tester can compute it from source records without asking "保底是什么保底 / guarantee of what?"
- **Finance Fund-Flow Gate:** Before finalizing any balance, credit, support fund, prepayment, recharge, refund, freeze, occupation, release, write-off, profit sharing, or payment rule, prove the fund loop closes: source pool, usable amount, deduction/occupation order, mixed funding behavior, ledger effect, source trace, closure path, reversal, page visibility, and cross-module side effects. Do not invent a single-source, single-period, one-to-one, or audit-heavy path just because it is easy to write.
- **Settlement and Payment Closure Gate:** Before finalizing cost inclusion, reconciliation, billing, payment, or profit sharing, prove the state and money loop closes: audit status, payment status, locked cost period, duplicate prevention key, preserved detail dimensions, platform service fee, profit-sharing funds waterfall, payment order origin payload, payment completion side effects, centralized credit management, and void/rollback. A neat formula is not enough if the business event cannot be operated, paid, reversed, and audited.
- **Post-Event Writeback Gate:** Before finalizing any completion event, list the writeback inventory for existing objects: target object, exact persisted field, source event timestamp, business period, writeback policy, consumer, idempotency, and reverse/correction behavior. Created downstream records are not enough if later eligibility, duplicate checks, reports, or next-period logic read a field such as last labor payment time or labor payment month.
- **Progress-Control Field Loop:** When a field means "last/previous/handled-through/paid-through/next/progress" and the next action reads it, define the full loop: where the user sees it, which action reads it, how the next period/default is derived, whether the user can edit it, what duplicate/continuity rule it enforces, which success event advances it, which failures do not advance it, and what void/reissue/correction does. Treat this as business behavior, not a passive display field.
- In the main PRD file, draw the business flow atlas first. Include Mermaid flowcharts for each flow line and Mermaid `stateDiagram-v2` diagrams for key object status changes when objects have lifecycles.
- When proposing a flow, page, component, or rule, explain the product constraint it solves and what would break without it.
- Write from the user-agreed business mainline. Generic best practices and polished wording must not override confirmed business facts.
- Every extension beyond the confirmed mainline needs a basis: user confirmation, business anchor, source data, existing system behavior, market research marked as recommendation, or "待确认".
- Keep PRD wording business-readable. SQL, code enums, interface params, database names inform the work but stay out of PRD正文 (technical appendix only).
- If a flow, field, or rule cannot be made testable, keep decomposing before writing it as final口径.

## Red Flags — STOP, you are about to violate the skill

- About to output exception matrices / page-Tab tables / state machines **before** business + main flow are confirmed.
- About to flatten parallel, master-child, event-driven, cycle/periodic, or state-machine flows into one linear mainline.
- About to omit lifecycle/state diagrams for objects whose statuses govern operations, writebacks, locks, or downstream flows.
- About to write the full PRD **without** marking invented details as 待确认, because the user said "别问、直接写".
- About to lock口径 / write defaults **without** first reading existing project docs (skipping research under time pressure).
- About to model a finance action as "choose one balance source" when partial insufficiency could require mixed funding, or as "automatic audit/payment" when the business only needs a deterministic ledger adjustment.
- About to tie a refund/release to the same receipt/source detail without proving that the occupied pool and the source trace have a one-to-one pairing.
- About to call a supplier pre-recharge or operating payment an internal ledger registration without checking whether real external payment happens.
- About to equate "finance-side" with the whole platform-side without defining organization scope, operator role, and whether platform can see all subjects.
- About to collapse detail dimensions into a single total before deciding which downstream calculation uses summary calculation and which report needs dimension analysis.
- About to mention invoice, payment trace, exception record, allocation detail, or any child object only inside an operation row without its own lifecycle/page/visibility.
- About to put unmatched or missing-link data into an exception status without an exception workbench, manual completion path, recalculation, and re-enter downstream flow.
- About to write "保底 / guarantee / 取大 / take greater / 加减项" without explaining guarantee of what, comparison basis, period, entity scope, eligibility, proration, and whether adjustments happen before comparison or after comparison.
- About to write an abstract term (计价口径 / 统计口径 / 结算口径 / 规则 / 策略) into a uniqueness key, filter, or acceptance rule **without** decomposing it into fields.
- About to let a cost enter a bill/report/profit-sharing flow without separating audit status, payment status, cost recognition, locked cost period, and late/missing source handling.
- About to write customer billing, monthly charter, transport-volume billing, or profit sharing without preserving vehicle/waybill/project dimensions needed for analysis.
- About to write platform service fee or profit sharing without payer, receiver/platform pocket, rate snapshot, profit-sharing funds waterfall, zero/negative handling, continuing deduction, and profit-sharing void fund rollback.
- About to create a payment order without source business object, payer/payee, receiver account, amount split, transaction metadata, and payment completion attached actions.
- About to list only created downstream records after a transaction completion, without exact persisted field writebacks to existing objects such as last labor payment time, labor payment month, eligibility marker, summary counter, or next-period flag.
- About to describe a last/previous/paid-through/handled-through/progress field as display-only while a create/action flow actually reads it to default, lock, or prevent duplicate work.
- About to scatter support credit/grant/occupation/repay/release rules across modules without a centralized credit management owner or page/workbench.
- About to put `status=1` / `incomeStatus in (...)` / code enums into PRD正文.
- Adding an entity/status/page/field just to look complete, with no product constraint behind it.
- Gave only one flow version when 原始/推荐/MVP comparison would help.

**Any of these means: stop and return to the progressive workflow.**

## Default First Response Shape

For a rough requirement, start with: (1) one-sentence plain-language business goal, (2) known/unknown about scope/users/objects/risk, (3) initial flow-shape judgment and business flow atlas plan, clearly marked as inferred if needed; if multiple flows may run in parallel, name each flow and its convergence points, (4) inferred high-risk control loops, especially repeated/cyclic operations where a last/previous/paid-through/handled-through field may drive the next create/action flow, and (5) the 3-6 highest-value confirmation questions with recommended defaults. Do not open with exception matrices, page-level Tab tables, or detailed state machines before the business and flow shape are clear.
