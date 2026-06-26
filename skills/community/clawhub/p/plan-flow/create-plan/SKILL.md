---
name: create-plan
description: Create a structured implementation plan with phases and complexity scores
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---

# Create Plan

Create a structured implementation plan based on a discovery document or user input.

## What It Does

1. Extracts requirements from discovery document (or user input)
2. Analyzes scope and complexity
3. Structures phases with complexity scores (0-10)
4. Assigns tasks to each phase
5. Ensures tests are always the last phase

## Usage

```
/create-plan <discovery_document>
/create-plan "<feature_description>"
```

**Arguments:**
- `discovery_document`: Path to discovery document (recommended)
- `feature_description`: Direct description of feature (if no discovery)

## Output

Creates: `flow/plans/plan_<feature>_v<version>.md`

## Complexity Scoring

| Score | Level | Description |
|-------|-------|-------------|
| 0-2 | Trivial | Simple, mechanical changes |
| 3-4 | Low | Straightforward implementation |
| 5-6 | Medium | Moderate complexity, some decisions |
| 7-8 | High | Complex, multiple considerations |
| 9-10 | Very High | Significant complexity/risk |

## Plan Structure

```markdown
# Plan: [Feature Name]

## Overview
Brief description

## Goals
- Goal 1
- Goal 2

## Phases

### Phase 1: [Name]
**Scope**: What this phase covers
**Complexity**: X/10

- [ ] Task 1
- [ ] Task 2

**Build Verification**: Run `npm run build`

### Phase N: Tests (Final)
**Scope**: Write comprehensive tests
**Complexity**: X/10

- [ ] Unit tests
- [ ] Integration tests

## Key Changes
1. **Category**: Description
```

## Example

```
/create-plan @flow/discovery/discovery_user_auth_v1.md
```

## Critical Rules

- **No Code**: Plans describe what to implement, not how to code it.
- **Tests Last**: Tests are always the final phase.
- **No Auto-Chaining**: Do NOT auto-invoke `/execute-plan`.

## Next Command

After creating a plan, review it and then run `/execute-plan @flow/plans/plan_<feature>_v1.md`.
