---
name: product-requirement-delivery
description: Convert a lightweight product request plus related signed-in pages into a product-confirmed requirements baseline published as one Feishu document. Use when a product manager asks Codex to investigate existing pages, clarify roles and business rules, capture complete route-aware screenshots, define user stories and exception scenarios, obtain product confirmation, and write the final requirement to Feishu for downstream development and testing. Also use for requests such as “按现有页面出需求”“把需求写到飞书”“补齐角色、用户故事、异常场景和验收标准”.
---

# Product Requirement Delivery

Turn a lightweight requirement card into one clear, reviewable Feishu requirement document. Keep the product manager responsible for business decisions. Do not require the product manager to prescribe code, APIs, database design, development plans, or test plans.

## Required workflow

### 1. Audit the intake

Read [references/intake-card.md](references/intake-card.md). Extract the requirement name, related pages, current problem, target users, desired result, known rules, exclusions, and references.

Do not ask the user to write a full PRD. Discover page facts independently. Propose low-risk business defaults. Ask only questions whose answers materially change roles, permissions, visible behavior, state changes, data meaning, exception handling, or acceptance results.

### 2. Investigate the real product

Open every related page and inspect its navigation, fields, filters, states, operations, terminology, permissions visible to the current account, empty states, and adjacent flows. Use the user's signed-in Chrome session when login state matters, after reading the applicable Chrome/browser skill.

Read and obey [references/ui-evidence-rules.md](references/ui-evidence-rules.md). For every page, capture both route evidence and complete page evidence. Preserve an unannotated original; annotations are supplemental.

Classify statements as:

- `Observed`: directly verified on the live page.
- `User stated`: supplied by the user.
- `Recommended`: proposed for product confirmation.
- `Unverified`: inaccessible or not provable from the current page state.

Never fabricate a replacement interface. If a state is unavailable, define the required business behavior and mark placement or current behavior unverified.

### 3. Draft the requirements baseline

Create `<requirement-name>-需求基线-v0.1.md` using [references/fact-source-schema.md](references/fact-source-schema.md). The local Markdown is the auditable source used to publish the Feishu document.

The draft must include:

- roles and permission boundaries;
- core user stories and preconditions;
- explicit normal-flow rules;
- state, default, editability, visibility, effective-time, and historical-data rules;
- exception and boundary scenarios;
- scope in/out;
- observable Given/When/Then acceptance criteria;
- complete URLs and screenshot evidence.

Use stable IDs: `ROLE-*`, `US-*`, `REQ-*`, `EX-*`, `AC-*`, and `UV-*`. Every AC must reference at least one REQ, US, or EX.

Run:

```powershell
python scripts/validate_fact_source.py <requirement.md> --expected-status draft
```

### 4. Audit ambiguity before review

For every operation, make the following answerable without guessing:

1. Which role can see or perform it?
2. What preconditions and business states allow it?
3. What is the default value and which values are legal?
4. What exactly triggers success, and when does the result become visible?
5. What changes, what remains unchanged, and how is history treated?
6. What happens for no permission, invalid state, empty/not-found data, duplicate action, stale or concurrent modification, timeout, partial batch failure, and retry?
7. What feedback does the user receive on success and failure?
8. Which behavior is explicitly out of scope?

Do not use vague expressions such as “按需”“适当”“视情况”“正常处理” unless they are immediately converted into objective conditions and results.

### 5. Stop for product confirmation

Present only unresolved business decisions, each with a recommended default and impact. Do not publish the final Feishu document until the product manager explicitly confirms the rules.

### 6. Freeze the baseline

After confirmation:

- change status to `已确认（可发布到飞书）`;
- set version to `v1.0` or later;
- record confirmation date and decisions;
- remove tentative language from confirmed rules;
- keep inaccessible page facts as `Unverified` without weakening confirmed business behavior.

Run the validator with `--expected-status confirmed`.

### 7. Publish one Feishu requirement document

Read [references/deliverable-contract.md](references/deliverable-contract.md). Then read and follow the `lark-doc` skill and its required shared authentication instructions.

- If the user provides an existing Feishu document, update that document.
- Otherwise create one document titled `<requirement-name>-产品需求-v<version>` in the user-specified folder, or the authenticated user's default document location when no folder is specified.
- Publish the confirmed source as readable Feishu content, not as an attached DOCX.
- Upload and insert the original complete screenshots and, when useful, annotated copies.
- Put the copyable full URL next to every screenshot group even when the browser address bar is visible.
- Do not create development-Agent packages, test-Agent packages, interface specifications, database designs, or implementation checklists unless the user separately asks for them.

### 8. Read back and verify

Fetch the published Feishu document and verify:

- title and version;
- all required headings and IDs;
- roles, user stories, rules, exceptions, scope, and ACs;
- every associated page URL;
- every required screenshot is embedded and readable;
- no confirmed rule reverted to tentative wording.

Create an audit manifest from [references/audit-manifest.example.json](references/audit-manifest.example.json), save the fetched Markdown, and run:

```powershell
python scripts/audit_delivery.py --manifest <manifest.json> --source <confirmed.md> --published <fetched.md>
```

Fix the Feishu document and repeat the read-back audit until it passes.

## Non-negotiable gates

- One confirmed requirements baseline governs the Feishu document.
- No final Feishu publication before product confirmation.
- Every involved role has an explicit permission boundary.
- Every core business goal has at least one user story and one acceptance criterion.
- Normal, state, permission, empty/not-found, duplicate/retry, concurrency/stale-data, failure, and batch-partial-failure behavior are either defined or explicitly marked not applicable with a reason.
- Route evidence includes the browser address bar; page evidence covers the complete relevant page with continuous context.
- Screenshots never replace copyable full URLs.
- No fabricated product UI or unverified technical implementation presented as fact.
- No mandatory development or test package is produced from this skill.
- Preserve the user's existing files and unrelated workspace changes.

## Handoff

Lead with the Feishu document link and confirmed version. State any remaining `Unverified` page facts and what evidence was unavailable. Do not expose internal work files unless requested.
