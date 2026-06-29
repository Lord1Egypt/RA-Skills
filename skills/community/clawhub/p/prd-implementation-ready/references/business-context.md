# Business Context and Reader Onboarding

Use this at the start of PRD work and before final output. The goal is that a new developer, tester, product manager, or stakeholder who does not know the project can understand the business before reading rules.

## Outsider Readability Gate

Before detailed rules, make sure a new reader can answer:

- What business is this, in plain language?
- Who are the main roles and what relationship do they have?
- What real-world value, goods, service, data, or money moves between the roles?
- Why does the system need to exist?
- What are the core business objects?
- Which domain terms are special or counterintuitive?
- What is in scope now and what is explicitly pending / out of scope?

If these cannot be answered from the PRD, add a front section before rules, state machines, and page details.

## Required Front Section

For complex PRDs, especially money/settlement/approval/cross-system flows, add a 0-1 page front section:

| Section | Required Content |
|---|---|
| Business background | What business this is and what problem it solves |
| Business goal | Real-world business outcome, not only system construction goal |
| Role glossary | Who each role is, what they do, who pays/receives/approves/operates |
| Business model / value flow | How value or money moves among roles |
| Business anchors / iron laws | Non-negotiable premises that later details must preserve |
| Core concept dictionary | Terms that readers must understand before rules |
| Main flow in one paragraph | Plain-language start-to-end flow |
| Scope note | What this phase does, does not do, and what remains pending |

## Tenant, Organization, and Role Relationship

For SaaS, platform, partner, finance, or collaboration products, define tenant/organization relationships before page and permission details. A user-facing role is not enough; the same real-world subject may appear in several tenant spaces or play multiple roles.

Use:

| Subject / Entity | Tenant / Organization Scope | Possible Roles | Shared Identity? | Tenant Isolation Rule | Data Ownership | Cross-Tenant Visibility | Migration / Merge/Split Behavior | Confirm |
|---|---|---|---|---|---|---|---|---|

Check:

- Can the same customer appear across multiple tenants?
- Can the same legal entity have multiple roles in one tenant or across tenants?
- Are accounts global, tenant-scoped, organization-scoped, or project-scoped?
- Which identifiers are authoritative: platform ID, tenant-local ID, external system ID, tax/license ID, phone/email, contract number?
- What happens when a tenant, customer, supplier, contractor, branch, or account is merged, split, disabled, migrated, or re-bound?
- Which records must remain tenant-isolated even for users who belong to several tenants?
- Which reports, exports, notifications, callbacks, or admin tools may cross tenant boundaries?

If the product does not support cross-tenant collaboration in this release, say so explicitly and define safe behavior for duplicate names, duplicate external IDs, login switching, import conflicts, and permission denial.

## Role Glossary

Use:

| Term | Plain-Language Meaning | Relationship To Other Roles | Main Actions | Money/Data Responsibility | Confirm |
|---|---|---|---|---|---|

Do not use role names such as "contractor", "shipper", "platform", "service provider", or internal system names without defining them once.

## Core Concept Dictionary

For every important or counterintuitive concept, define:

| Concept | What It Is | Why It Exists | When It Is Created / Increased / Decreased | Who Can Operate | Related Objects | Common Misunderstanding | Confirm |
|---|---|---|---|---|---|---|---|

Avoid circular definitions. If A is defined only as equal to B, and B is defined only as equal to A, the business meaning is still missing.

For a special financial concept, explain:

- what problem it solves;
- why the design is needed;
- when the amount changes;
- who can trigger change;
- what can and cannot unlock/release it;
- what users see in the product;
- one concrete example.

## Business Goal vs System Goal

Separate:

| Type | Good Wording | Bad Wording |
|---|---|---|
| Business goal | Help carriers and shippers reconcile transport costs and payments accurately | Build a traceable finance management backend |
| System goal | Provide auditable, recoverable, permission-controlled tools for the business goal | Replace the business goal |

The PRD can include both, but the business goal must appear first.

## Plain-Language Flow

For money or transaction flows, add a compact flow before detailed tables:

| Step | Plain-Language Description | Role | Object/Data/Money Moved | Result |
|---|---|---|---|---|

This can be a table or a simple diagram. It should help readers understand the business before they encounter state axes, idempotency, or page specs.

## Pending Items Discipline

If a concept or feature is marked "待确认 / 待产品提供 / 不进入验收 / 本期不做", do not describe it later as a complete confirmed implementation. Either:

- keep it as an explicit pending item;
- mark detailed content as a recommendation / draft that does not enter acceptance;
- remove the detailed implementation from the current PRD scope;
- ask the user to confirm and then close the pending item.

## Anchor Discipline

Some business facts are more important than ordinary rules. If a premise defines how the business works, put it in the business anchor list, not only in a module detail. Later sections must reference and preserve it.
