---
name: execute-plan
description: Execute phases from an implementation plan
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---

# Execute Plan

Execute phases from an implementation plan, following complexity-based grouping.

## What It Does

1. Reads the plan file and identifies phases
2. Groups phases based on complexity scores
3. Presents phase details before implementation
4. Implements each phase following project patterns
5. Marks tasks as complete
6. Runs build verification

## Usage

```
/execute-plan <plan_file> [phase]
```

**Arguments:**
- `plan_file` (required): Path to the plan file
- `phase` (optional): Phase number, range, or "next". Default: next incomplete phase

**Phase Options:**
- `1` - Execute phase 1
- `1-3` - Execute phases 1 through 3
- `next` - Execute next incomplete phase
- `all` - Execute all remaining phases

## Execution Strategy

Based on combined complexity scores:

| Combined Score | Strategy |
|----------------|----------|
| ≤ 6 | **Aggregate**: Execute multiple phases together |
| 7-10 | **Cautious**: Execute 1-2 phases, then verify |
| > 10 | **Sequential**: Execute one phase at a time |

## Phase Execution Flow

For each phase:

1. **Present**: Show phase details and approach
2. **Implement**: Write code following project patterns
3. **Update**: Mark tasks complete in plan file
4. **Verify**: Run build verification

## Example

```
/execute-plan @flow/plans/plan_user_auth_v1.md phase:1
```

**Output:**
```
Executing Phase 1: Types and Schemas
Complexity: 3/10

Tasks:
- [ ] Create User type definitions
- [ ] Create Zod validation schemas

Implementing...

✓ Phase 1 Complete
- Created src/types/user.ts
- Created src/schemas/user.ts

Build verification: npm run build ✓
```

## Critical Rules

- **Follow Patterns**: Always follow existing project patterns
- **Build After Each Phase**: Verify build passes before proceeding
- **Update Plan**: Mark completed tasks in the plan file
- **Tests Last**: Execute test phase only after all other phases complete

## Next Command

After executing all phases, run `/review-code` to review your changes before committing.
