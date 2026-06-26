# Spec-Kit Output Reference

This reference defines the artifact formats produced by the `speckit` function. All output follows the spec-kit spec-driven development standard (github/spec-kit).

## Artifact Tree

A complete `speckit` function run produces:

```
specs/[###-feature-name]/
  spec.md              -- Feature specification
  plan.md              -- Implementation plan
  data-model.md        -- Entity definitions
  contracts/           -- Interface contracts (API specs, CLI schemas)
  tasks.md             -- Dependency-ordered task list
  checklists/
    requirements.md    -- Validation checklist
memory/
  constitution.md      -- Project principles (if not already present)
```

## spec.md Template

```markdown
# [Feature Name]

## Overview
[One-paragraph description of the feature and its purpose]

## User Scenarios

### US1: [Scenario Name]
**As a** [role]
**I want to** [action]
**So that** [outcome]

**Acceptance Criteria:**
- Given [precondition], When [action], Then [expected result]
- Given [precondition], When [action], Then [expected result]

### US2: [Scenario Name]
...

## Functional Requirements

### FR1: [Requirement Name]
[Description]
- [Detail]
- [Detail]

### FR2: [Requirement Name]
...

## Key Entities
| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| [Name] | [Purpose]   | [Fields]       |

## Success Criteria
- [ ] [Measurable criterion]
- [ ] [Measurable criterion]

## Out of Scope
- [Explicitly excluded item]

## Open Questions
- [NEEDS CLARIFICATION] [Question]
```

## constitution.md Template

```markdown
# Project Constitution

## Core Principles

### 1. [Principle Name]
[Description of the principle and why it matters]

### 2. [Principle Name]
...

## Governance
- Constitutional changes require [process]
- Violations must be justified in the plan with rationale

## Version
v1.0.0 -- [Date] -- Initial constitution
```

## data-model.md Template

```markdown
# Data Model

## [Entity Name]

### Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id    | UUID | Yes      | Primary key |

### Relationships
- Has many [Entity] (via [field])
- Belongs to [Entity] (via [field])

### State Transitions
[State A] -> [State B]: [Trigger]
[State B] -> [State C]: [Trigger]

### Validation Rules
- [Field] must [constraint]
- [Field] cannot [constraint]
```

## tasks.md Template

```markdown
# Tasks

## Phase 1: Setup
- [ ] [T001] [P] [US1] Description `path/to/file`
- [ ] [T002] [US1] Description `path/to/file`

## Phase 2: Foundation
- [ ] [T003] [P] [US1,US2] Description `path/to/file`

## Phase 3: User Stories
- [ ] [T004] [US1] Description `path/to/file`

## Phase 4: Polish
- [ ] [T005] [P] Description `path/to/file`
```

Task format key:
- `[T###]` -- Task ID (sequential)
- `[P]` -- Parallelizable (can run concurrently with other [P] tasks in same phase)
- `[US#]` -- Maps to user story from spec.md
- Backtick path -- Primary file affected

## Ambiguity Markers

Use `[NEEDS CLARIFICATION]` for any item that cannot be resolved from interview decisions alone. These markers must be resolved before implementation begins. Maximum 3 per artifact.

## Constitution Compliance

Every plan.md must include a constitution check section:

```markdown
## Constitution Check
| Principle | Status | Notes |
|-----------|--------|-------|
| [Name]    | PASS   |       |
| [Name]    | JUSTIFY| [Rationale for deviation] |
| [Name]    | FAIL   | [Must resolve before proceeding] |
```

No artifact may proceed to implementation with a FAIL status.
