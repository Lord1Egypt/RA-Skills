# Review Checklist

Use this list after each output stage. Mark each item pass/fail before proceeding to the next stage or delivering to dev.

## Stage A: Business Architecture Review

- [ ] Are all functional modules identified and clearly named?
- [ ] Are dependencies between modules explicit (arrows, labels)?
- [ ] Does the architecture match the user's mental model (not the developer's)?
- [ ] Are any modules missing from the scenario flows described?
- [ ] Is the scope boundary clear? What is NOT in this architecture?
- [ ] Does the module count feel reasonable (too many = over-engineering, too few = missing abstraction)?

## Stage B: Interactive Prototype Review

- [ ] Can you complete every core scenario flow from start to finish without getting stuck?
- [ ] Does every page show an empty state (what user sees with 0 data)?
- [ ] Does every page show a loading state (what user sees while waiting)?
- [ ] Does every page show an error state (what user sees on failure)?
- [ ] Are success confirmations visible after key actions (submit, delete, save)?
- [ ] Is the visual style consistent across pages (colors, spacing, typography)?
- [ ] Do interactive elements behave as expected (buttons, forms, navigation)?
- [ ] Is the information hierarchy correct (most important info most prominent)?

## Stage C: PRD Review

- [ ] Is the problem statement free of solution language ("users need X" → "users experience pain Y")?
- [ ] Do acceptance criteria use Given/When/Then format?
- [ ] Are edge cases explicitly listed (0 items, 10000 items, special characters, long text)?
- [ ] Are success metrics measurable (not "better experience" but "reduce X by Y%")?
- [ ] Is the scope boundary explicit in "Out of Scope"?
- [ ] Can a developer implement this without asking additional clarifying questions?
- [ ] Are API endpoints clearly listed with request/response examples?

## Stage D: API Definition Review

- [ ] Does every endpoint have a complete request definition (params, body, headers)?
- [ ] Does every endpoint have a complete success response with example?
- [ ] Are error responses defined for all reasonable failure cases (400, 401, 403, 404, 500)?
- [ ] Are data model fields typed and constrained (string length, enum values, number ranges)?
- [ ] Are business rules that span multiple endpoints documented?
- [ ] Are performance/rate-limiting notes included where relevant?

## Handoff Readiness

Before delivering to development team, confirm:

- [ ] All four artifacts are internally consistent (prototype ↔ PRD ↔ API ↔ architecture)
- [ ] No artifact contradicts another
- [ ] The PRD includes a link/access to the prototype
- [ ] The API spec references the relevant PRD sections
- [ ] You've walked through at least one scenario end-to-end across all artifacts
