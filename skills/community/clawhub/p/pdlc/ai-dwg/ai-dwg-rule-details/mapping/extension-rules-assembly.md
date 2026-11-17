<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: ADLC + UXD + TGE → aidlc-rules/extensions/ (AI-DLC v1 Extension Rules Bundle)

## Purpose

Assembles the **extension rules bundle** that AI-DLC v1 consumes alongside the Vision Document and Technical Environment Document. Extension rules provide specialized governance that AI-DLC v1 applies during code generation — security constraints, accessibility requirements, and testing directives.

**Output:** `{workspace-root}/aidlc-rules/extensions/`

**Condition:** Generate IF `adlc-state.md` OR `uxd-state.md` is present (at least one source of extension rules exists).

**Cluster:** Cross-cluster (assembled from multiple peer inputs)

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think about AI-DLC v1 as the consumer — extension rules are constraints it enforces during code generation
- Package rules in AI-DLC v1's expected format — not our internal steering format
- Each extension file is focused on ONE concern (security OR accessibility OR testing)
- Rules are actionable constraints, not documentation — AI-DLC v1 uses them to PREVENT wrong code

### Anti-Patterns for This Activity
- Do NOT duplicate full steering files into extensions — extract only the AI-DLC v1-relevant subset
- Do NOT include architecture decisions or rationale — just the enforceable rules
- Do NOT package testing extensions from DWG if TGE is activated — TGE owns testing governance

---

## Source Inputs

### Security Extension (from ADLC)

| AP Document | What to Extract | Extension Rule |
|---|---|---|
| Security Architecture | Auth method, token rules, RBAC constraints | `security.md` |
| Security Architecture | Encryption requirements, secrets management | `security.md` |
| Security Architecture | OWASP mitigations, input validation rules | `security.md` |
| ADRs (security-related) | Security pattern decisions | Referenced in `security.md` |

### Accessibility Extension (from UXD)

| UXP Document | What to Extract | Extension Rule |
|---|---|---|
| Accessibility Baseline | WCAG level, specific criteria | `accessibility.md` |
| Design System (a11y section) | Focus, contrast, ARIA, motion, targets | `accessibility.md` |
| Component Inventory (a11y notes) | Per-component a11y requirements | `accessibility.md` |

### Testing Extension (from TGE or DWG)

| Source | Condition | Extension Rule |
|---|---|---|
| AI-TGE test strategy output | IF TGE activated | `testing.md` (from TGE) |
| DWG `testing-strategy.md` | IF TGE NOT activated | `testing.md` (from DWG) |

---

## Output Structure

```
{workspace-root}/aidlc-rules/extensions/
├── security.md          ← IF ADLC present (extracted from Security Architecture)
├── accessibility.md     ← IF UXD present (extracted from Accessibility Baseline)
└── testing.md           ← IF TGE activated → from TGE output; ELSE IF ADLC → from DWG testing-strategy
```

---

## Template: security.md

```markdown
<!-- AI-DWG generated | source: AI-ADLC Security Architecture | date: {generation-date} -->

# Security Extension Rules

## Authentication
- {auth-method} MUST be used for all authenticated endpoints
- Token expiry: {duration} — MUST NOT exceed this
- Refresh strategy: {approach}

## Authorization
- {authorization-model} MUST be enforced on every endpoint
- Role definitions: {role-list}
- Default deny: unauthenticated requests MUST be rejected

## Data Protection
- Encryption at rest: {algorithm} REQUIRED for all persistent data
- Encryption in transit: {TLS-version} MINIMUM
- Secrets: MUST use {secrets-management-approach} — NEVER hardcode

## Input Validation
- All user input MUST be validated before processing
- SQL injection: parameterized queries ONLY
- XSS: output encoding REQUIRED
- CSRF: {protection-method} REQUIRED on state-changing operations

## Sensitive Data
- PII fields: {list} — MUST be masked in logs
- Audit trail: {what-to-log} on {which-operations}
```

## Template: accessibility.md

```markdown
<!-- AI-DWG generated | source: AI-UXD Accessibility Baseline | date: {generation-date} -->

# Accessibility Extension Rules

## Compliance Target
- WCAG {level} compliance is REQUIRED — not optional
- All new code MUST pass automated accessibility checks before merge

## Visual Rules
- Color contrast: {ratio} minimum for normal text; {ratio-large} for large text
- Color MUST NOT be the only means of conveying information
- Focus indicators: MUST be visible with {min-contrast} contrast

## Interactive Elements
- All interactive elements MUST be keyboard accessible
- Touch targets: MUST be ≥{size} (minimum)
- Tab order MUST follow logical reading order
- No keyboard traps (except modals with explicit trap/release)

## Dynamic Content
- Content changes MUST use aria-live regions
- Loading states MUST be announced to screen readers
- Error messages MUST be programmatically associated with inputs

## Motion
- All animations MUST respect `prefers-reduced-motion`
- Auto-playing media MUST have pause/stop controls
- Flashing content: MUST NOT flash more than 3 times per second

## Forms
- Every input MUST have a visible or programmatic label
- Error messages MUST identify the field AND describe the error
- Required fields MUST be indicated (not just by color)
```

## Template: testing.md

```markdown
<!-- AI-DWG generated | source: {AI-TGE output / DWG testing-strategy.md} | date: {generation-date} -->

# Testing Extension Rules

## Coverage Requirements
- Unit tests: {target}% coverage minimum
- Integration tests: all API endpoints covered
- E2E tests: critical user journeys ({list})

## Test Patterns
- Test structure: {pattern — e.g., Arrange-Act-Assert}
- Mocking: {approach — e.g., dependency injection, not monkey-patching}
- Test data: {approach — e.g., factories, not hardcoded fixtures}

## Quality Gates
- All tests MUST pass before merge
- Coverage MUST NOT decrease on any PR
- Performance tests: {SLO thresholds — if defined}

## Accessibility Testing
- Automated a11y scan: REQUIRED on all UI components
- Tool: {specified-tool — e.g., axe-core}
- Manual testing: required for {scenarios}
```

---

## Assembly Logic

### Step 1: Determine Available Sources

```
IF adlc-state.md present → security extension: YES (from AP Security Architecture)
IF uxd-state.md present  → accessibility extension: YES (from UXP Accessibility Baseline)
IF TGE activated         → testing extension: YES (from TGE output)
ELSE IF adlc-state.md    → testing extension: YES (from DWG testing-strategy.md)
ELSE                     → testing extension: NO
```

### Step 2: Extract and Transform

For each available extension:
1. Read the source document(s)
2. Extract ONLY the enforceable rules (not rationale, not architecture decisions)
3. Transform into AI-DLC v1's constraint format (action-oriented, binary compliance)
4. Write to `aidlc-rules/extensions/{name}.md`

### Step 3: Create Directory

If any extension is generated, ensure `aidlc-rules/extensions/` directory exists. If no extensions are applicable (unlikely — requires no ADLC AND no UXD AND no TGE), skip this entire mapping.

---

## Testing Extension — Delegation Rule (Design Law 4)

| Condition | Testing Extension Source | DWG Behavior |
|---|---|---|
| TGE activated | TGE's test strategy output (reads ADLC directly + POLC/UXD enrichment) | DWG SKIPS testing-strategy.md AND uses TGE output for the extension |
| TGE NOT activated | DWG's own `testing-strategy.md` (derived from ADLC quality attributes) | DWG produces basic testing-strategy AND uses it for the extension |

**User is always informed** which path applies:
- "Testing governance delegated to TGE — extension rules sourced from TGE output."
- "TGE not activated — basic testing extension sourced from DWG testing-strategy."

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| ADLC present but Security Architecture is minimal | Generate `security.md` with available rules. Mark gaps: `<!-- Incomplete: {what's missing} -->` |
| UXD present but no explicit Accessibility Baseline doc | Use `uxd-state.md` WCAG Target field + DS-A11Y rules from `design-system.md` as source |
| TGE activated but hasn't run yet | Skip testing extension for now. Note in generation summary: "Testing extension pending — run TGE first" |
| No extensions applicable (edge case) | Skip `aidlc-rules/extensions/` entirely. Note in summary. |
| ADLC security conflicts with UXD accessibility | Cross-input conflict — surface via conflict gate. Example: ADLC says "disable paste in password field" vs. UXD says "all inputs must support paste for accessibility" |

---

## Output Validation

- [ ] Security rules are extractive (from AP), not invented
- [ ] Accessibility rules match UXP baseline exactly
- [ ] Testing source correctly identified (TGE vs. DWG)
- [ ] All rules use prescriptive language (MUST/MUST NOT)
- [ ] No architectural rationale in extension files (just constraints)
- [ ] Directory structure matches AI-DLC v1 expected format
- [ ] Provenance comments present in each file
