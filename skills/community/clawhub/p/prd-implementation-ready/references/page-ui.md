# Page, Menu, UX, and Component Guidance

Use this after the business objects and main flow are known. Page structure is part of broad UI / interaction style, not just visual design. The goal is to choose the right target端, page carrier, and components so users can understand the task, operate efficiently, and avoid mistakes. Apply `necessity-gate.md`: do not specify pages or components unless they solve a real user task, workflow constraint, risk, or comprehension need.

## Target端 / Touchpoint

Before designing menus or pages, decide where the user should complete the task.

| Touchpoint | Use When | Avoid When |
|---|---|---|
| PC backend / admin console | High information density, review, reconciliation, audit, configuration, batch work | Field user needs quick mobile action |
| Role-specific portal | External partner, supplier, contractor, customer, or service provider needs self-service | Internal-only operation or sensitive cross-tenant data |
| Mobile / H5 / mini app | On-site, driver, sales, approval on the go, photo/file capture, quick confirmation | Complex tables, heavy reconciliation, dense comparison |
| Message / todo center | User only needs to be notified, approve, retry, or handle exception | Full context or complex editing is needed |
| API / system job only | No human decision is needed and rules are deterministic | Business requires confirmation, exception handling, or audit |
| Import/export tool | Large batch correction, offline reconciliation, migration | Real-time guided operation is required |

Use:

| Scenario / Task | Primary User | Recommended端 / Touchpoint | Why | Fallback入口 | Confirm |
|---|---|---|---|---|---|

## Role vs Touchpoint Scope Gate

Do not confuse a system side, an organization scope, and an operator role. "Finance-side" is often an operator role inside the platform-side, not the whole platform scope. A platform-side page may let platform can see all subjects, while a finance operator role may only perform finance actions within that platform scope.

Define:

| Item | Must Define |
|---|---|
| System side / touchpoint | platform-side, customer portal, supplier portal, contractor portal, mobile, API/system job |
| Organization scope | tenant, platform, branch, project, contractor, customer, supplier, or cross-tenant |
| Operator role | finance, operations, admin, approver, auditor, external partner, system |
| Viewed subject | whether the page shows self only, all subjects, or a switchable subject such as contractor/customer/supplier |
| Data scope | what "all" means: all platform records, all tenant records, all authorized records, or only owned records |
| Action scope | which role can view, operate, export, audit, switch subject, and recover exceptions |

If a page says "财务端可切换承包人", check whether that really means "platform-side page; finance operator can switch contractor within authorized/all platform scope". Do not write a platform page as if it were only one finance user's personal account.

## Menu, Page, and UX Are Business Decisions

Do not choose target端, menu, page structure, or components by taste. Decide from:

- Business domain.
- Core objects and lifecycle.
- Data volume.
- Field count.
- Operation complexity.
- Role differences.
- Usage frequency.
- User's working context: desk work, mobile work, approval, exception handling, batch processing.
- Risk level: money, contract, invoice, privacy, irreversible action.
- Need for comparison, traceability, explanation, or guided operation.
- Existing navigation/design conventions.

## Common Page Organization Patterns

| Pattern | Use When | Avoid When |
|---|---|---|
| Few first-level menus + page-level Tabs | Same business domain, same users, related objects, left menu should stay shallow, each Tab is an independent work page | Tab objects have unrelated lifecycles or role groups |
| First-level + second-level menus | Submodules need frequent direct access | It creates deep left navigation for low-frequency pages |
| Single list + filter Tabs | Same object and same fields, only status/type differs | Tabs are different objects or different operation flows |
| Detail sections / detail Tabs | Same object has many details, logs, attachments | Each section has independent list workflow |
| Drawer / modal | Lightweight view/edit/confirm while preserving list context | Complex forms, independent lifecycle, long workflow |
| Wizard | Import, account opening, signing, batch processing | Simple single-step input |
| Dedicated detail page | Complex object, many related records, audit trail, repeated return visits | One-off quick check |
| Split pane / master-detail | Users compare list and detail repeatedly | Mobile or narrow screen |
| Batch operation bar | Users select many homogeneous records and apply same action | Per-record validation differs too much |
| Exception workbench | Users triage failures, retry, assign, or close exceptions repeatedly | Exceptions are rare and simple |

## Page Spec Output

| Business Domain | Object | User Task | Target端 | Lifecycle Independent? | Data / Field Complexity | Operation Complexity | Recommended Carrier | Why | Confirm |
|---|---|---|---|---|---|---|---|---|---|

If page-level Tabs are recommended:

| First-Level Menu | Page-Level Tab | Independent Work Page? | Own Filters | Own List | Own Detail | Own Actions | Default Entry | Permission Difference |
|---|---|---|---|---|---|---|---|---|

Page-level Tabs are independent work pages. List Tabs are filters. Do not mix the two.

## Side / Module / Page / Function Map

Before detailed page specs, build an information architecture map for the product or 00 主文件. It should answer where each function lives, which side owns it, and how users enter it.

Use:

| 端 / Side | 模块 | 页面 / Page | 功能点 | Default Entry | Target Role | Permission | Data Scope | Cross-side / 跨端 Link | Notes |
|---|---|---|---|---|---|---|---|---|---|

Rules:

- "端" is a touchpoint or system side: platform-side, customer portal, supplier portal, contractor portal, driver mobile, API/system job.
- "模块" is a business domain or object group, not just a left-menu label.
- "页面" includes page-level Tabs, detail pages, workbenches, drawers only when they are real work carriers, and server-only flows when there is no page.
- "功能点" is what users or systems do there: view, create, audit, reconcile, pay, sync, import, export, configure, recover exception, analyze.
- Put cross-side links on the map when one side creates data and another side views/operates it.
- If a function cannot be placed on this map, either it is missing a page/entry or it should be a server-only flow with visibility/log entry.

## Role Perspective and Resource Visibility

For any page involving a controlled resource/value, design the role perspective explicitly. This applies to finance and non-finance resources: inventory, coupon, quota, capacity, permission, entitlement, membership rights, appointment slots, task capacity, or content visibility.

| Role Perspective | Page Must Explain |
|---|---|
| Actor | What can I use, reserve, allocate, consume, release, revoke, or retry now? |
| Owner | Which pool/source is mine, what is available/reserved/occupied/consumed/released, and what changed it? |
| Counterparty | Which counterparty funds/resources/status explain this operation, disabled reason, or settlement/result? |
| Approver / operator | What source, trace, risk, exception, and downstream side effect am I confirming? |
| Platform/admin/tenant admin | Cross-role totals, abnormal locks, source traces, tenant/organization boundaries, and recovery entries |

Do not show only the acting user's local field when the operation depends on counterparty context. If an action is disabled because another party's pool, lock, status, quota, permission, or trace is insufficient, stale, frozen, occupied, or missing, the page must show that reason in business language.

## Centralized Credit and Settlement Operations Page

When credit/support fund/frozen fund/profit-sharing/payment rules affect several modules, decide whether the platform side needs a centralized page instead of hiding operations in separate detail pages.

Use a centralized page when users must manage or audit cross-object pools, especially: support credit grant, credit occupation, repay, release, freeze/unfreeze, contractor own-funded advances, shipper/customer frozen funds, platform service fee collection, abnormal locks, and downstream profit-sharing recovery.

Page must define:

| Area | Must Show / Support |
|---|---|
| Summary cards | current credit pool, available, occupied, frozen, repayable, released, outstanding, platform pocket/service fee totals |
| Subject switch | contractor, shipper/customer, supplier, project, contract, tenant, or all platform records depending on role scope |
| Ledger table | source, trace, business object, amount, status, period, counterparty, operator, time, reason, downstream object |
| Operations | grant, adjust, occupy, repay, release, freeze/unfreeze, export, retry side effect, jump to source bill/payment/profit-sharing record |
| Disabled reason | insufficient pool, locked period, occupied by source detail, pending payment, missing counterparty, permission, duplicate/parallel bill conflict |
| Exception recovery | failed payment completion side effect, missing source mapping, stale callback, negative/zero settlement, void rollback pending |

If the page is not needed, state which existing page/workbench owns each operation and how platform/admin users still see the whole fund/credit situation.

## UX and Component Selection
 
For each page or important action, specify the UX carrier and component behavior. Do not stop at "add a page" or "add a button".

| Need | Recommended Component / Pattern | Must Specify |
|---|---|---|
| Scan many records | High-density table, sticky key columns, column configuration | primary fields, frozen columns, default sort, pagination, empty state |
| Compare statuses / progress | Status tags, progress steps, timeline, state reason tooltip | state meaning, reason source, terminal states |
| Confirm high-risk action | Confirmation modal, reason input, secondary verification | risk copy, affected objects, irreversible effects, audit log |
| Edit simple fields | Inline edit or small modal | editable fields, validation, save/cancel, permission |
| Edit complex object | Dedicated edit page or drawer with sections | required fields, validation, draft, submit result |
| Long multi-step setup | Wizard / stepper | steps, back/forward, draft, validation per step |
| Select source records | Selection table, filter panel, selected summary | data source, eligibility, default selection, lock/occupation |
| Handle exceptions | Exception queue, reason classification, retry button, processing log | owner, retry rules, terminal handling |
| Upload/download | Upload component, file list, template, progress, result report | file type, size, duplicate, parse failure, partial success |
| View audit/history | Timeline / operation log / change diff | operator, time, before/after, reason |
| Navigate across modules | Link/button with parameters and default filters | target page/Tab, params, permission, empty target |

Do not add a component just because the design system has it. Tie each component to the process constraint it solves: comparison, selection, validation, risk confirmation, context preservation, exception recovery, traceability, or guided setup.

For each page, define:

| Page / Action | User Goal | Main Information Hierarchy | Key Components | Primary Action | Secondary Action | Error/Empty/Loading | Risk Control | Confirm |
|---|---|---|---|---|---|---|---|---|

## UX Quality Gate

Before accepting a page design, ask:

- Can the user tell what to do first within 5 seconds?
- Is each page, Tab, component, and action necessary for a user task or process constraint?
- Are high-frequency actions fewer clicks than low-frequency actions?
- Are dangerous actions visually and procedurally harder than safe actions?
- Can users understand why an action is disabled?
- Can users recover from failure without leaving the page?
- Does the page show enough context before asking for confirmation?
- Are dense tables readable without hiding critical fields?
- Are mobile/portal/API-only choices justified by the user's actual working context?

## design.md / Existing UI

If a project has design.md, ui-design-spec.md, screenshots, components, or prior pages, read them before recommending UI.

Extract:

- Page hierarchy.
- Navigation depth.
- Table density.
- Tab behavior.
- Drawer/modal usage.
- Toast/error/empty/loading rules.
- High-risk confirmation.
- Component library conventions.
- Form/table/filter/drawer/modal/button patterns.
- Responsive behavior.

Default broad UI recommendation for B端后台:

> 沿用现有后台风格；列表高信息密度；复杂详情优先详情页或抽屉；高风险动作必须二次确认。
