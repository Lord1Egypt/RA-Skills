<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-ADLC AP (tech patterns) + AI-UXD UXP (UI component patterns)"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: examples/ Directory (SKELETON)

**Generate IF:** At least one peer input is present (any valid input set).
**Cluster:** Cross-cluster (tech patterns from ADLC, UI patterns from UXD)
**Purpose:** Provide AI-DLC v1 and developers with copy-paste starter patterns that demonstrate the correct way to implement common code patterns in this workspace. Seeded from architecture decisions (ADLC) and design system components (UXD).

## Directory Structure

```
{workspace-root}/examples/
├── README.md                       ← This file (index + usage guide)
├── api-endpoint.{ext}              ← IF ADLC: REST endpoint boilerplate
├── database-query.{ext}            ← IF ADLC: Query pattern (ORM/raw)
├── service-layer.{ext}             ← IF ADLC: Service/use-case pattern
├── error-handling.{ext}            ← IF ADLC: Error pattern
├── test-unit.{ext}                 ← IF ADLC: Unit test pattern
├── test-integration.{ext}          ← IF ADLC: Integration test pattern
└── ui-component.{ext}              ← IF UXD: Component using design system tokens
```

## Template: examples/README.md

```markdown
<!-- AI-DWG generated | source: AP + UXP example patterns | date: {generation-date} -->

# Code Examples

Starter patterns demonstrating the correct implementation approach for this workspace. These examples are **prescriptive** — they show the ONE correct way, not alternatives.

## How to Use

1. Find the pattern closest to what you're building
2. Copy the file as a starting point
3. Replace placeholders with your implementation
4. Follow the inline comments for guidance

## Available Patterns

| Pattern | File | Source | When to Use |
|---------|------|--------|-------------|
| API Endpoint | `api-endpoint.{ext}` | AP: API Architecture + Tech Stack | New REST/GraphQL endpoint |
| Database Query | `database-query.{ext}` | AP: Data Architecture + Tech Stack | New data access method |
| Service Layer | `service-layer.{ext}` | AP: Component Design patterns | New business logic unit |
| Error Handling | `error-handling.{ext}` | AP: Error patterns + API standards | Custom error scenarios |
| Unit Test | `test-unit.{ext}` | AP: Testing strategy + Tech Stack | New unit under test |
| Integration Test | `test-integration.{ext}` | AP: Testing strategy | New integration scenario |
| UI Component | `ui-component.{ext}` | UXP: Design System + Component Inventory | New frontend component |

## Rules

- MUST follow these patterns — don't invent new approaches
- MUST use the project's design tokens (see `design-system.md`) for UI components
- MUST follow naming conventions (see `naming-conventions.md`)
- Patterns are kept in sync with steering files during reconciliation
```

## Template: examples/ui-component.{ext} (UXD-Seeded)

**Generate IF:** `uxd-state.md` present.
**Extension:** Determined by AP Technology Stack (`.tsx`, `.vue`, `.svelte`, etc.)

```markdown
<!-- AI-DWG generated | source: AI-UXD Design System + Component Inventory | date: {generation-date} -->
```

```{ext}
/**
 * Example: UI Component using Design System tokens
 * 
 * This pattern demonstrates:
 * - Using design tokens (NEVER hardcode values)
 * - Following component structure from design-system.md
 * - Implementing all required states (loading, error, empty)
 * - Accessibility compliance (keyboard nav, ARIA, focus)
 * - Responsive behavior
 *
 * Source: AI-UXD Component Inventory → DS-CMP-NN
 * Tokens: See rules/design-system.md
 */

// Token usage — ALWAYS reference tokens, NEVER hardcode
// color: var(--color-primary)        ← DS-COL-01
// spacing: var(--space-md)           ← DS-SPC-04
// font: var(--font-family-primary)   ← DS-TYP-01
// shadow: var(--shadow-sm)           ← DS-ELEV-01
// duration: var(--duration-normal)   ← DS-MOT-02

// Component states — ALL MUST be handled:
// - default: normal rendering
// - loading: show skeleton (DS-INT-01)
// - empty: show illustration + message + CTA (DS-INT-02)
// - error: show error message with retry (DS-INT-03)
// - disabled: reduced opacity, no interaction

// Accessibility requirements (DS-A11Y):
// - Keyboard navigable (tab + enter/space)
// - ARIA labels for non-text content
// - Focus visible (3:1 contrast min)
// - Motion respects prefers-reduced-motion
// - Touch target ≥44×44px

// {Framework-specific implementation pattern here}
// Placeholder — filled from AP Technology Stack at generation time
```

## Template: examples/api-endpoint.{ext} (ADLC-Seeded)

**Generate IF:** `adlc-state.md` present.
**Extension:** Determined by AP Technology Stack.

```{ext}
/**
 * Example: API Endpoint following workspace standards
 *
 * This pattern demonstrates:
 * - URL naming (kebab-case per api-standards.md)
 * - Request validation
 * - Error response format (per api-standards.md)
 * - Authentication/authorization check
 * - Response envelope format
 *
 * Source: AI-ADLC API Architecture + Security Architecture
 */

// {Framework-specific implementation pattern here}
// Placeholder — filled from AP Technology Stack at generation time
```

## Filling Instructions

| Example File | Primary Source | Key Rules to Follow |
|---|---|---|
| `api-endpoint` | AP API Architecture + Technology Stack | `api-standards.md` rules |
| `database-query` | AP Data Architecture + Technology Stack | `database-rules.md` rules |
| `service-layer` | AP Component Design + Technology Stack | `module-structure.md` rules |
| `error-handling` | AP Error patterns + API standards | `error-handling.md` rules |
| `test-unit` | AP Testing strategy + Technology Stack | `testing-strategy.md` rules |
| `test-integration` | AP Testing strategy + Technology Stack | `testing-strategy.md` rules |
| `ui-component` | UXP Design System + Component Inventory | `design-system.md` + `frontend-standards.md` |

### Key Principles

1. **Examples are prescriptive.** They show THE correct approach — not one of several alternatives.
2. **Technology-specific.** File extensions and patterns match the actual tech stack. Generic fallback only for unlisted stacks.
3. **Token-first for UI.** The `ui-component` example MUST demonstrate token usage, not hardcoded values.
4. **Reconciliation-aware.** Examples update when architecture changes (Mode 2).
5. **Not runnable as-is.** They're patterns/templates, not complete applications. Commented placeholders for project-specific values.
