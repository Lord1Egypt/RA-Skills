<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: frontend-standards.md (CONDITIONAL)

**Generate IF:** Container Design includes SPA/UI containers OR BFF extension active.

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Container Design + Technology Stack | date: {generation-date} -->

# Frontend Standards

## Frontend Identity
**Framework:** {framework}  |  **State:** {state mgmt}  |  **Styling:** {approach}  |  **Bundler:** {tool}

## Component Architecture
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| FE-COMP-01 | Structure: {atomic design / feature-based} |
| FE-COMP-02 | One component per file |
| FE-COMP-03 | Smart vs. Presentational separation |
| FE-COMP-04 | Props: typed — no `any` |
| FE-COMP-05 | Max ~200 lines per component |
<!-- end: AP-sourced -->

## State Management
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| FE-STATE-01 | Global: only auth/theme/tenant |
| FE-STATE-02 | Server state: {data fetching lib} |
| FE-STATE-03 | Form state: {form lib} |
| FE-STATE-04 | Prefer local over global |
<!-- end: AP-sourced -->

## API Communication
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| FE-API-01 | Single configured HTTP client |
| FE-API-02 | Auth: configured once in client |
| FE-API-03 | Global error interceptor |
| FE-API-04 | Loading states for all async |
<!-- end: AP-sourced -->

## Accessibility
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| FE-A11Y-01 | Target: {WCAG level} |
| FE-A11Y-02 | Semantic HTML |
| FE-A11Y-03 | Keyboard navigation |
| FE-A11Y-04 | ARIA when needed |
| FE-A11Y-05 | Color contrast: AA ratio |
| FE-A11Y-06 | Focus management |
<!-- end: AP-sourced -->

## Testing
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| FE-TEST-01 | Unit: component logic (Testing Library) |
| FE-TEST-02 | Integration: page flows with mocked API |
| FE-TEST-03 | E2E: critical journeys only |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/containers-to-frontend.md`.
