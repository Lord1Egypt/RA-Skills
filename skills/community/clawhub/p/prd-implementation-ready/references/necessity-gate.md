# Necessity Gate and Entity Economy

Use this throughout discussion, writing, and review. The goal is to co-create a strong product PRD with the user: complete enough to build and test, lean enough to read and reason about.

## Principle

Complete does not mean verbose. Rigorous does not mean adding more entities, pages, states, fields, flows, or tables. Add only what makes the product clearer, safer, more usable, more traceable, or more testable.

## Necessity Test

Before adding any object, status, field, page, component, flow step, exception, table, or document section, answer:

| Question | Why It Matters |
|---|---|
| What user/business need does it serve? | Avoid document decoration |
| Which process constraint does it express? | Tie detail to real workflow |
| What decision, implementation, test, or operation does it enable? | Keep PRD actionable |
| What breaks or becomes unclear if omitted? | Prove necessity |
| Can an existing object/status/page/component carry this instead? | Avoid needless entities |
| Is it confirmed, recommended, pending, or out of scope? | Avoid silent invention |

If the answer is weak, merge it, defer it, or remove it.

## Entity Economy

Do not add a new:

- business object if an existing object plus a clear state/field covers the need;
- status if it is only a display label, sub-status, reason, flag, or Tab filter;
- page/Tab if a filter, section, drawer, or detail area carries the job clearly;
- field if no user decision, calculation, rule, display, audit, or integration uses it;
- flow step if no actor, information change, state change, validation, risk control, or side effect happens;
- exception case if it cannot occur under the confirmed flow or has no different handling;
- table if a short paragraph or bullets communicate the rule better.

## Discussion Discipline

When talking with the user:

- Explain why a proposed item is needed, not just that "PRD should include it".
- Challenge awkward or inflated flows and offer a leaner flow when possible.
- Batch only the highest-risk decisions; do not overwhelm the user with every possible axis.
- Mark recommendations as recommendations until confirmed.
- Keep open items visible instead of filling them with invented detail.

## Page and Component Necessity

UI choices must follow workflow constraints:

| Constraint | Usually Justifies |
|---|---|
| Many comparable records | Table, filters, sort, batch tools |
| Need to preserve list context | Drawer or lightweight modal |
| Long independent workflow | Dedicated page |
| Sequential validation / setup | Wizard or stepper |
| High-risk irreversible action | Confirmation modal, reason input, audit log |
| Frequent exception handling | Exception workbench / queue |
| Historical accountability | Timeline, operation log, change diff |
| Mobile/on-site work | Mobile/H5/mini app instead of dense backend page |

If a component does not serve a user task, process constraint, risk control, or comprehension need, do not specify it.

## Writing Style

Prefer:

- one plain-language explanation before dense rules;
- compact decision tables only when comparison or acceptance needs structure;
- specific unresolved questions over vague "待确认";
- recommendations with tradeoffs over bloated exhaustive options.

Avoid:

- piling every checklist into the final document;
- adding "global rules" that belong inside a specific module/page;
- repeating the same rule in multiple places unless one is an index and one is the authoritative detail;
- writing technical or abstract terms when business wording is enough.
