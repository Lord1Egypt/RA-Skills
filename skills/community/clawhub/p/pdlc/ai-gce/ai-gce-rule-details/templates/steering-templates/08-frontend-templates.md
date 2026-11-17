<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Frontend Steering Templates

> **Purpose:** Used by the project-init-agent to generate frontend-related steering files
> in the target project's `rules/` folder. These templates encode component architecture,
> state management, accessibility requirements, and API integration patterns derived from
> `frontend-standards.md` (conditional — only if UI containers exist).

---

## frontend-core.md (Always — within frontend scope)

**Generates**: `rules/frontend-core.md`
**Condition**: Generated only IF `frontend-standards.md` exists in workspace steering
**Derived From**: frontend-standards.md + tech-stack.md + module-structure.md

```markdown
---
inclusion: always
---

# Frontend Architecture Standards

## Component Structure
- ALL pages MUST be in {page_location_pattern}
- ALL shared components MUST be in {shared_component_pattern}
- {component_file_structure}
- {component_props_requirements}

## Naming Conventions
- Pages: {page_naming_pattern}
- Feature components: {feature_component_naming}
- Shared components: {shared_component_naming}

## State Management
- ALL module state MUST use {state_management_library}
- State files location: {state_file_pattern}
- NEVER store UI-only state in global store (use component-local state for: {local_state_examples})
- API calls MUST go through {api_call_mechanism}, NEVER directly from components

## API Integration
- ALL API clients MUST be {api_client_strategy}
- NEVER hardcode API URLs — use {configuration_mechanism}
- ALL API calls MUST handle errors ({error_display_strategy})
- ALL list endpoints MUST use pagination (never load all records)

## Loading States
- ALL data-fetching components MUST show {loading_indicator_type} while loading
- NEVER show blank screens — always {loading_placeholder_strategy}
- Loading indicators MUST match the final layout shape
```

---

## frontend-accessibility.md (Always — within frontend scope)

**Generates**: `rules/frontend-accessibility.md`
**Condition**: Generated alongside frontend-core.md (accessibility is non-negotiable)
**Derived From**: frontend-standards.md + WCAG requirements

```markdown
---
inclusion: always
---

# Accessibility Requirements ({accessibility_standard})

## Mandatory for ALL Components
- ALL interactive elements MUST be keyboard accessible (Tab, Enter, Escape)
- ALL form inputs MUST have associated label elements (or aria-label)
- ALL images MUST have alt text (or aria-hidden="true" if decorative)
- ALL color-coded information MUST have a non-color alternative (icon, text, pattern)
- ALL focus states MUST be visible (minimum {focus_contrast_ratio} contrast ratio)
- ALL dynamic content updates MUST use aria-live regions

## Data Display Components
- MUST use proper semantic roles with {table_grid_role_strategy}
- MUST support keyboard navigation between cells
- MUST announce state changes via aria-live
- {virtual_scroll_accessibility}

## Forms
- MUST use aria-required="true" for required fields
- MUST use aria-invalid="true" and aria-describedby for error messages
- MUST group related fields with {form_grouping_mechanism}
- MUST NOT rely on placeholder text as the only label

## Modals/Dialogs
- MUST trap focus inside (Tab cycles within modal)
- MUST return focus to trigger element on close
- MUST close on Escape key
- MUST have role="dialog" and aria-labelledby
```

---

## frontend-testing.md (FileMatch `{frontend_test_pattern}`)

**Generates**: `rules/frontend-testing.md`
**Condition**: Generated IF frontend-standards.md defines frontend testing requirements
**Derived From**: frontend-standards.md + testing-strategy.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{frontend_test_pattern}"
---

# Frontend Testing Standards

## Component Testing
- {component_test_library}: {component_test_approach}
- Test user interactions, not implementation details
- Mock API calls at the {api_mock_layer} level
- Verify accessibility in component tests ({a11y_test_tool})

## E2E Testing
- {e2e_framework}: {e2e_approach}
- Cover critical user journeys: {critical_journey_examples}
- NEVER depend on specific test data IDs
- Tests MUST be independent (no shared state between tests)

## Visual Testing
- {visual_test_strategy}
- Snapshot tests for {snapshot_scope}
- Review visual diffs before approving
```
