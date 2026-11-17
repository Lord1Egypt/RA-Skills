# RepairKhata Project Skill

## Purpose

Use this skill whenever working on RepairKhata. It gives the agent the product context, architecture assumptions, delivery discipline, QA expectations, release history, and roadmap needed to continue the project without re-discovering decisions or reintroducing solved problems.

The agent should behave as a senior product engineer + release engineer + design-system-aware implementation partner. The goal is not to redesign or reinvent RepairKhata. The goal is to finish it safely, consistently, and production-first.

---

## Product summary

RepairKhata is a repair-shop management product for Bangladesh, focused on mobile and PC repair shops.

Primary product goals:
- Mobile-first daily shop workflow.
- Fast, native-feeling use on 360–430px phones.
- Owner/manager operational visibility.
- Strong role and financial-data boundaries.
- Repair intake → service → payment → delivery workflow.
- Customers, inventory, suppliers, purchases, expenses, POS/sales, reports, staff, branches, invoices, warranty, photos, support.
- Bangla and English support.

Primary web properties:
- App: `https://app.repairkhata.com/`
- Marketing: `https://repairkhata.com/`

Canonical production repo/project history:
- GitHub repo: `noman-design/RepairKhata1`
- Canonical Vercel project: `repairkhata`
- `main` is the production branch.
- Vercel production deployment must be verified against the exact `main` SHA.

Do not assume `main` has not moved. Always fetch and inspect before work.

---

## Commercial / plan context

Planned product tiers:
1. Single user offline — phone/local storage — one-time purchase.
2. Small shop up to 5 members — local usage with owner dashboard sync, no cloud mode — one-time purchase.
3. Medium shop, 5–10 members — cloud mode — recurring.
4. Large shop, multi-branch — cloud mode — recurring.

Do not change plan architecture unless explicitly asked.

---

## Roles and permission model

Core roles:
- Owner
- Manager
- Technician
- Front desk / similar operational staff where present

Important rules:
- Owner sees full financial and operational information.
- Manager sees information allowed by current capability gates.
- Technician sees own work and operational repair data, but must not see restricted financial data such as buying prices, profit, cost, payments, supplier/purchase cost data, or other owner/manager-only information.
- Restricted pages should remain unavailable rather than being exposed and merely visually hidden.
- Never weaken RLS, role gates, branch scope, or financial permissions to make a UX flow easier.
- Settings is owner-only unless existing product rules say otherwise.
- Staff profile editing, performance, role permission editing, and invite flows must preserve current permission architecture.

Any permission change requires explicit evidence and review.

---

## Core repair workflow

The critical workflow is:

`Customer → Repair intake → Technician → Diagnosis → Parts/Services → Status progression → Payment → Ready for delivery → Delivery → Invoice → Public tracking → Dashboard/Reports`

Important repair behaviors already established:
- Owner with no staff can assign themselves as technician (`Me`).
- Repair tickets may include inventory parts, custom items, service price, intake photos, promised date, technician assignment, warranty, notes.
- Delivered repairs are locked from ordinary edits.
- Delivered lock must survive reload.
- Public tracking must not reveal data for a wrong phone number.
- Cost/buying price is never customer-facing.
- Payment amount may prefill current due but must remain visible/editable and only save on explicit action.
- Advance payment is visible during intake; estimated cost remains in More Details unless explicitly changed later.
- Allowed status transitions should derive from the canonical transition rule (`canTransition`) rather than parallel local copies.

Never create a second status-transition table.

---

## Accounting model

The current accounting model is deliberate. Do not simplify or reinterpret it.

Key principles:
- Revenue, COGS, operating expenses, inventory purchases, payments, and cash flow are distinct concepts.
- Profit is not cash flow.
- Reports use a unified net-profit concept such as:
  `Net profit = revenue − expenses − COGS`
- Labeling uses wording such as `Net of recorded expenses` where already implemented.
- Customer-facing billing must not expose cost.
- Costed custom repair line items can contribute to COGS without changing the customer bill.
- Inventory cost data must remain restricted.
- Payments are append-only where current rules require it.
- Financial RPCs must preserve auth/role enforcement.

Verified example used in QA:
- Revenue: ৳5,500
- COGS: ৳4,500
- Gross profit: ৳1,000

Another verified workflow example:
- Subtotal: ৳2,000
- Discount: ৳100
- Final bill: ৳1,900
- Payments: ৳300 advance + ৳600 + ৳1,000
- Due: ৳0

Always verify important accounting changes against the database / billing RPCs, not only rendered UI.

---

## Service worker / caching rule

A serious production issue was previously found where authenticated pages were served from a service-worker cache, causing stale repair/payment state and retaining shop content after logout.

The fix established these expectations:
- Authenticated shop pages must not be served as stale cached HTML/data.
- Only intended static assets should remain cached.
- Reload after status/payment/delivery must show current server state.
- After logout, Back/reload/revisit must not expose shop content.
- Offline behavior should show an offline state without leaking stale authenticated repair data.

Never change service-worker behavior casually. Any service-worker change requires dedicated regression.

---

## Authentication / invite / SMTP context

Production auth uses Supabase and custom SMTP through Resend.

Known working sender setup:
- Sender: `no-reply@auth.repairkhata.com`
- Sender name: `RepairKhata`
- SMTP host: `smtp.resend.com`
- Port: `465`
- Username: `resend`

Important historical lesson:
- Resend correctly rejects fake recipients such as `example.com` for real delivery testing.
- Do not diagnose SMTP as broken from fake-domain tests.
- Real-inbox tests are required for invite confirmation and password reset.

Desired invite flow:
`Invite link → set password once → email confirmation → authenticated session → invite validated/accepted → membership created exactly once → success/dashboard → logout/login works`

The flow must be idempotent and must never loop on signup or hang indefinitely on `Setting up your account…`.

Do not disable email confirmation or weaken auth to bypass a flow bug.

---

## Design system

A pre-Phase-4 normalization pass established a shared atomic design system.

Foundations/tokens include:
- semantic color roles
- spacing map
- radius
- borders
- shadows
- icon sizing
- control height
- touch target token (`44px` target convention)
- mobile nav spacing

Important shared primitives/components include:
- Button
- Badge
- Card
- Input
- SelectNative
- Label
- Checkbox
- Chip
- Avatar
- Spinner
- Dialog
- Sheet

Important composites include:
- FormField
- CheckboxField
- PaymentFormFields
- SectionHeader
- StickyActionBar
- FilterBar / MobileFilterSheet
- Stat
- ListCard
- PickerRow
- EmptyState
- Callout
- ConfirmPanel
- MoneySummary / SummaryRow
- PaymentRow
- JobStatusBadge
- PaymentStatusBadge
- MobilePageHeader

Rules:
- Reuse shared components before creating new ones.
- Extend shared components only when the need is genuinely reusable, additive, and defaults remain unchanged.
- Do not create a parallel component system.
- Prefer semantic tokens over page-specific values.
- Existing defaults should stay visually stable unless the current slice explicitly redesigns that screen.

---

## Mobile-first design rules

Target phone widths:
- 360px
- 390px
- 430px

Also verify:
- 768px
- 1024px
- 1440px

Important expectations:
- No horizontal scrolling.
- Whole-card rows where appropriate.
- Tables may become cards on phones when required.
- Primary actions should be easy to reach and normally 44px touch targets.
- Small visual controls are acceptable if contained in a 44px tappable row.
- Bottom navigation and sticky actions must not overlap.
- Mobile should not merely be desktop squeezed narrower; the primary daily workflow should feel native and fast.
- Bangla wrapping must be verified at each phone breakpoint.

---

## Phase 4 status and roadmap

Phase 4 is the mobile-first workflow redesign/hardening phase.

### Slice 1 — completed and verified in production
Scope:
- Dashboard
- Add Repair
- Repair Details
- Status
- Parts/services
- Payment
- Delivery

Key outcomes:
- Core repair workflow verified on desktop and phone.
- Advance Payment moved to the always-visible intake area.
- Estimated cost remains under More Details.
- Repair Details status, payment, parts/services, and delivered states improved.
- Service-worker defect was fixed and verified.

### Slice 2 — implemented and locally verified; production review/deploy is next unless status has advanced
Scope:
- Customers
- POS / Sales
- Inventory

Implemented items include:
- Customer search by name/phone.
- Customer cards on phones.
- Customer detail money tiles, repair history cards, sales/dues context.
- POS quantity stepper, sticky checkout, exact-amount helper.
- Sales history mobile cards/filter sheet.
- Inventory search/filter, stock-status cards, mobile item detail, collapsed Adjust Stock, movement history, sticky save.

Known follow-ups identified before production:
- sanitize raw search input on `/jobs` and `/suppliers` using the same safe pattern as Customers.
- fix front_desk post-customer-create redirect so the role does not land on an inaccessible `/customers` page.

Do not expand scope while applying those two fixes.

### Slice 3 — next after Slice 2 production verification
- Expenses
- Reports

Focus:
- mobile-first expense list/forms/categories/date filters
- owner/manager financial operations
- report filters and summaries
- preserve accounting model
- verify report numbers against database/RPCs

### Slice 4
- Staff
- Staff detail/performance
- Invite experience
- Branches
- Branch switching/filtering
- Multi-branch owner/manager UX

### Slice 5
- Settings
- Support
- remaining management-screen mobile polish

### Final design debt cleanup
Possible remaining items:
- mobile table-to-card conversions
- list breakpoint mismatch
- stat-card unification
- card elevation/shadow consistency
- remaining inline markup migration to shared composites
- MobilePageHeader rollout
- sticky CTA rollout
- small touch-target inconsistencies

### Localization cleanup
Deferred until major screen work is stable:
- remaining English server/validation errors
- Bangla date/time formatting
- printed invoice/receipt language behavior
- Bangla webfont only if low-risk and justified

---

## Testing and release discipline

Every meaningful slice should follow:

1. Fetch latest `main`.
2. Check branch divergence and unrelated incoming work.
3. Review diff scope before merge.
4. Run lint.
5. Run typecheck.
6. Run unit tests.
7. Run build.
8. Run relevant E2E.
9. Run responsive QA.
10. Run role QA.
11. Run Bangla + English QA.
12. Verify database/accounting figures where relevant.
13. Merge only after evidence is green.
14. Wait until Vercel production deployment is `READY`.
15. Verify exact `main` SHA is serving production.
16. Manually trigger a fresh GitHub E2E after deployment is READY when push-triggered CI may have raced the previous build.
17. Production smoke test.
18. Only then mark the slice verified.

Do not let a push-triggered E2E failure immediately imply product regression; it may have tested the previous deployment while Vercel was still building.

---

## E2E / test lessons

Past false failures came from:
- stale local server still listening on port 3000
- fixed sleeps racing server mutations
- selectors matching hidden mobile/desktop duplicate DOM
- branch CI testing live production before the branch UI was deployed
- redirect tests blocked only by sandbox network access
- missing technician CI credentials causing skips
- tests assuming a second technician exists
- tests expecting a tab bar that intentionally renders only with multiple tabs
- client-side prefetched requests confusing `networkidle`
- stale page state before a full reload

Rules:
- Root-cause every failure before patching.
- Classify failure as product regression, test regression, timing/flakiness, environment/network, missing config, or deployment race.
- Do not change product code to satisfy a broken test.
- Prefer database truth for disputed workflow state.
- Prefer explicit state/selector checks over arbitrary fixed waits.

Known CI caveat:
- technician E2E tests may skip if `E2E_TECH_EMAIL` / `E2E_TECH_PASSWORD` are absent.

---

## Search safety

Customer search was hardened using a search sanitizer before PostgREST `.or()` filters.

Apply the same safe pattern wherever raw search input is used in dynamic database filters, especially previously identified `/jobs` and `/suppliers` paths.

RLS is not a substitute for query-shape safety.

---

## Data / QA rules

QA often creates real demo-shop records through the product.

Rules:
- Never delete production/demo data without explicit approval.
- Do not manually mutate the DB as a shortcut for a user-facing workflow test when the product UI/action should be exercised.
- Direct DB reads are encouraged for verification.
- If a workflow test creates records, report them.
- Demo data may affect dashboard totals, low-stock counts, and “today” metrics; distinguish live-data differences from visual regressions.

---

## Current known non-blocking items

These have been deferred previously and should not be pulled into unrelated slices unless explicitly approved:
- Bangla webfont
- server/validation error translations
- date/time localization
- printed invoice/receipt localization
- list breakpoint change
- global MobilePageHeader rollout
- card elevation cleanup
- some header/filter controls below 44px
- some mobile tables/cards not yet converted
- duplicate Total/Paid/Due summary on Repair Details (intentional)
- confirmation prompts for Unrepairable/Cancelled/remove line
- payment amount prefilled with amount due
- technician CI secrets missing

Do not treat these as release blockers unless they create a real operational problem.

---

## Final completion roadmap

Continue until all of the following are done:

1. Slice 2 production verification.
2. Slice 3 Expenses + Reports.
3. Slice 4 Staff + Branches.
4. Slice 5 Settings + Support.
5. Remaining design-system/mobile debt cleanup.
6. Localization cleanup.
7. Full product regression.
8. Full business workflow QA.
9. QA-data review/cleanup plan.
10. Release freeze.
11. Pilot preparation.
12. 7–14 day pilot observation plan.
13. Pilot-driven blocker fixes only.
14. Commercial-launch preparation.
15. Commercial-launch readiness report.

Commercial launch readiness should cover:
- product readiness
- technical readiness
- QA state
- pilot readiness
- onboarding readiness
- support readiness
- pricing/plan presentation readiness
- activation/analytics readiness
- exact production SHA
- known non-blocking limitations

---

## Pilot guidance

Pilot with 1–3 real repair shops before broad paid acquisition.

Observe:
- onboarding/activation
- repair creation
- technician assignment
- status progression
- parts/services usage
- payments
- delivery
- inventory
- POS
- reports
- support requests
- confusion/friction
- repeated manual workarounds

Only fix during pilot:
- real blockers
- serious bugs
- confusing workflows
- operational essentials

Avoid feature creep.

---

## Commercial-launch guidance

After pilot validation:
- onboard first 10 paying shops manually
- use demos and WhatsApp support
- prove activation before scaling ads
- start small with paid acquisition rather than immediately spending the full planned budget
- measure lead → demo → activation → paying customer

Do not confuse signups with successful shop activation.

---

## Agent operating rules

When working on RepairKhata:

- Inspect evidence before acting.
- Do not blindly trust sub-agent reports.
- Personally verify high-risk claims.
- Preserve already-approved production behavior.
- Keep changes scoped to the current slice.
- Do not start the next major slice before the current one is production-verified.
- Never silently broaden backend/schema/auth/permission/accounting scope.
- If another session changes `main`, merge/rebase carefully and re-run the full relevant gate.
- Prefer fixes that maintain the existing architecture.
- Avoid speculative rewrites.
- Use the shared design system.
- Treat production correctness and security as higher priority than visual polish.
- Report uncertainty rather than guessing.

---

## Required checkpoint report format

At every major checkpoint, report:

```text
CURRENT STEP:
MAIN SHA:
BRANCH:
COMMITS:
SCREENS / AREAS CHANGED:
BACKEND / SCHEMA CHANGES:
COMPONENTS REUSED:
COMPONENTS EXTENDED:
NEW COMPONENTS:
UNIT TESTS:
E2E:
MOBILE QA:
DESKTOP QA:
BANGLA QA:
ROLE QA:
DATABASE / ACCOUNTING CHECK:
SERVICE WORKER CHECK:
KNOWN ISSUES:
DEFERRED:
BLOCKERS:
NEXT RECOMMENDED STEP:
```

End with one clear status, for example:
- `READY FOR PRODUCTION REVIEW`
- `VERIFIED IN PRODUCTION`
- `READY FOR NEXT SLICE`
- `BLOCKED — REVIEW REQUIRED`
- `PILOT READY`
- `COMMERCIAL LAUNCH READY`

---

## Start-of-session protocol

Whenever a new Claude/agent session begins:

1. Read this skill.
2. Read `PROJECT_STATUS.md` and `BUILD_STATUS.md` if present.
3. Fetch `origin/main`.
4. Record current `main` SHA.
5. Inspect active feature branches/worktrees before creating another one.
6. Determine the first unfinished roadmap step.
7. Do not repeat completed work.
8. Continue only from the current verified state.

