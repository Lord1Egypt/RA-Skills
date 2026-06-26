# Implement Code

Write code from an existing implementation guide, including unit and integration tests.

## Purpose

When an implementation guide already exists, this operation takes it and produces working code. It skips the guide creation step and starts from coding plan generation.

## Prerequisites

1. **Implementation guide exists**: A concrete impl guide document is available
2. **Source RFC available**: The RFC that the guide was derived from, for reference
3. **Codebase access**: Write access to the target directories
4. **Project context**: Understanding of existing codebase architecture and conventions

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Implementation Guide | Yes | Path to the implementation guide |
| Source RFC | Yes | Path to source RFC specification |
| Auto Mode | No | Skip coding plan confirmation (default: false) |

## Process

### Step 1: Read Guide and RFC

- Read the implementation guide thoroughly
- Read the source RFC for context and requirements
- Treat both as source of truth: code is a **realization**, not a source of new requirements

### Step 2: Generate Coding Plan

Break the guide into ordered implementation tasks:

1. **Enumerate deliverables**: List all modules, types, interfaces, and tests from the guide
2. **Define task order**: Order tasks by dependency (foundations first, then consumers)
3. **Pair with tests**: Each functional task has a corresponding test task
4. **Scope each task**: Describe what to create/modify, reference guide sections

Use the template from `assets/coding-plan-template.md`.

**Confirmation Gate**: Present the plan to the user unless auto mode is active.

### Step 3: Execute Coding Tasks

For each task in the plan:

1. **Create or modify files** as specified
2. **Follow the guide precisely**: Do not add undocumented behavior
3. **Use language idioms**: Leverage target language and framework conventions
4. **Integrate with existing code**: Imports, wiring, configuration as described in the guide

### Step 4: Write Tests

For each component implemented:

1. **Unit tests**: Test individual functions, types, and methods in isolation
   - Cover happy paths and error paths
   - Test edge cases documented in the guide
   - Verify invariants from the RFC

2. **Integration tests**: Test cross-component interaction
   - Verify data flow between modules
   - Test end-to-end scenarios described in the guide
   - Validate behavior requirements from the RFC

### Step 5: Verify

1. Ensure the project builds without errors
2. Run all tests and verify they pass
3. Check that all guide sections have corresponding code
4. Verify RFC requirements are covered by tests

## Output

- **Source code** implementing the guide
- **Unit tests** for individual components
- **Integration tests** for cross-component behavior
- All code traceable to the implementation guide and RFC

## Handling Missing Information

If the implementation guide is incomplete or ambiguous:

1. **Do not invent behavior**: Never add functionality not described in the guide or RFC
2. **Document the gap**: Note what is missing and where
3. **Suggest guide update**: Recommend updating the guide before implementing the missing piece
4. **Ask the user**: When ambiguity blocks progress, ask for clarification

## Example

**Input**:
- Guide: `docs/impl/IG-001-user-authentication.md`
- RFC: `docs/specs/RFC-001-user-authentication.md`

**Coding Plan** (simplified):
1. Create `src/auth/types.ts` — User, Session, Token types
2. Create `src/auth/service.ts` — AuthService with login, logout, verify
3. Create `src/auth/middleware.ts` — Express middleware for route protection
4. Create `src/auth/errors.ts` — AuthError types
5. Create `tests/unit/auth/service.test.ts` — AuthService unit tests
6. Create `tests/unit/auth/middleware.test.ts` — Middleware unit tests
7. Create `tests/integration/auth/flow.test.ts` — Full auth flow integration test

**Output**: Working authentication module with tests
