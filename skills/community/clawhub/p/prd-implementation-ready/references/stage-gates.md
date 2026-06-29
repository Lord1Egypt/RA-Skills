# Stage Gates

Use this file to keep the PRD process ordered. The most common failure mode is jumping into state tables, Tab filters, or exceptions before the user has confirmed what the business does and how the main flow should work.

At every stage, apply `necessity-gate.md`: add only the structure needed to make the product understandable, buildable, usable, or testable.

## Stage 0: Mode

If the user has not chosen a depth, recommend one:

| Mode | Use When | Output Depth |
|---|---|---|
| L2 快速 | Small requirement or early idea | Goal, scope, main flow, key rules |
| L3 标准 | Normal product requirement | Complete PRD with exceptions and fields |
| L4 详尽 | Finance, payment, contract, approval, settlement, multi-system workflow | Full objects, states, source docs, idempotency, data, UI, risk |

Default to L4 when money, contract, invoice, settlement, payment, approval, third-party callback, or cross-system data is involved.

## Stage 1: Business Understanding

Confirm before anything else:

- Plain-language business context: what business this is, who it serves, and how value/data/money moves.
- Business goal: what real-world business problem this solves, separate from the system construction goal.
- Agreed business mainline and business anchors: the non-negotiable premises, obvious domain facts, pricing/fund/source/status rules, and constraints that later details must not override.
- Scope: what this phase does / does not do.
- Users and roles.
- Role glossary and core concept dictionary, especially counterintuitive business or financial concepts.
- Core business objects, then run `coverage-matrix.md` lightly to identify the highest-risk missing axes.
- Business risk: money, contract, invoice, privacy, approval, integration, migration.
- Repeated/cyclic operations: whether the business has "next run", "last run", "paid through", "handled through", "already issued", "prevent repeat", or "auto default next period" behavior. If yes, identify the likely progress-control field and ask/derive the loop before page fields are written.
- Existing systems or historical constraints.

Output:

| Area | Current Understanding | Missing / Risk | Recommended Default | Need User Confirm |
|---|---|---|---|---|

Do not move to detailed states, exceptions, pages, or fields until the mainline and high-risk anchors are either confirmed or explicitly marked待确认.

## Stage 2: Main Business Flow

Only after Stage 1, reconstruct the flow:

| Flow Version | Summary | Benefits | Risks / Cost | Recommendation |
|---|---|---|---|---|
| User Original Flow |  |  |  |  |
| Recommended Flow |  |  |  |  |
| MVP Flow |  |  |  |  |

While reconstructing the flow, identify which core objects move through the flow, where new information is introduced, and which data/linkage paths are affected. For repeated/cyclic flows, explicitly identify what tells the system "where the previous run ended" and "what the next run should cover"; this is often the source of duplicate prevention and locked defaults. Keep this coarse at Stage 2; detail it in Stage 3.

Ask the user to confirm the flow before expanding detailed rules.

When recommending a better flow, explain whether it preserves or changes any business anchor.

## Stage 3: Rules After Flow

After the main flow is accepted, confirm:

- Extension basis: every derived rule, state, field, page, interaction, exception, and component traces to user confirmation, a business anchor, source data, existing system behavior, research recommendation, or待确认.
- Per-object coverage matrix: source/creation, lifecycle, actor, period, amount/formula, state axes, data fields, list/query, interaction, locking, reverse flow, cross-system, cross-module, and audit trail.
- Necessity of every proposed object, state, field, flow step, exception, and table; merge or defer anything that does not serve a confirmed user/business/process need.
- Object flow and information ledger: for every step, define action/event, actor/system, from/to state, new information introduced, authoritative source, validation, persistence target, side effect, failure/retry, and whether the step creates another object.
- Data flow and linkage map: for every important data item/action, define source/authority, transform/rule, validation, persisted object/field, consumer, writeback/sync timing, linked object/module, side effect, reverse/rollback, and failure behavior.
- Progress-control field loops: for every last/previous/paid-through/handled-through/progress field, define reader action, next-period/default derivation, editability, continuity/duplicate rule, advance event, non-advance events, reverse/correction, and recovery visibility.
- Core object lifecycle.
- State fields and transitions, including each object's creation point, initial state, pre-audit / pre-payment stages, actor, trigger, terminal states, and whether shared status labels really apply to every object.
- Cross-document consistency for repeated objects, actions, statuses, audit wording, payment wording, and money terms.
- Money movement and formula computability: source amount, split / allocation rule, rate, rounding, timing, snapshot, reversal, and side effects.
- Finance operation rules: period attribution, fund deduction priority, sync/incremental data handling, supplier disabled/history behavior, reconciliation source locking, invoice upload/status, receipt write-off, red flush/void rollback, and cross-module jump parameters.
- Source documents, unique constraints, idempotency.
- Data sources and authoritative sources.
- Permissions and visibility.
- Exceptions, boundary cases, concurrency, rollback.

## Stage 4: Pages and UI

After business objects and flow are clear, confirm:

- Target端 / touchpoint: PC backend, role portal, mobile/H5/mini app, message/todo center, API/system job, import/export tool.
- Menu and page structure.
- Page-level Tabs vs list filter Tabs.
- Page specs based on data volume, field count, lifecycle, frequency, role differences.
- UX carrier and component selection tied to workflow constraints: table, detail page, drawer, modal, wizard, batch bar, exception workbench, upload/download, timeline, operation log.
- design.md / ui-design-spec.md / existing system conventions.
- Interaction habits: empty, loading, disabled, submitting, success/failure, recovery, high-risk confirmation, reason input, audit trail.

## Stage 5: Full PRD

Before writing the full PRD, show a confirmation gate:

| Section | Confirmed Rule | Source | Still Open |
|---|---|---|---|

Run the outsider readability gate from `business-context.md`: a new developer/tester/product manager should understand the business, roles, key concepts, main flow, and scope before detailed rules.
Run the business anchor gate from `business-anchors.md`: confirmed anchors are preserved, and any change to them is explicitly confirmed.

Do not write final PRD until the user confirms "继续 / 按这个写 / 没问题 / 可以开始".
