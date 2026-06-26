# Recover Implementation Interface Design

Generate Implementation Interface Design RFCs from codebase scan results. Only execute when explicitly requested by the user.

## Objective

Produce Draft RFCs that capture cross-boundary API contracts, naming conventions, type definitions, and interface signatures.

## Prerequisites

- User has explicitly requested impl interface specs
- Conceptual Design RFC is generated
- Architecture Design RFCs are generated
- The confirmed RFC plan includes impl interface specs

## Inputs

| Input | Source |
|-------|--------|
| Scan synthesis | From scan-project.md |
| Confirmed RFC plan | From plan-modular-specs.md |
| Architecture Design RFCs | Generated in recover-architecture.md |
| RFC numbers | From plan |
| Spec-kind template | `assets/specs/template-impl-interface-design.md` |

## Recovery Process

### Step 1: Identify API Boundary Surfaces

From the scan and architecture specs, identify where distinct subsystems communicate:

1. **Cross-subsystem interfaces**: Traits/interfaces used between architecture-spec subsystems
2. **Shared types**: Types that appear in multiple subsystems' public APIs
3. **Integration points**: Where subsystems connect (events, messages, function calls, shared storage)

For each boundary, determine if it warrants a separate interface spec or should be combined.

### Step 2: Catalog Cross-Boundary APIs

For each identified boundary surface:

1. **List all public interfaces** that cross this boundary
   - Trait/interface definitions
   - Exported function signatures
   - Event/message types
   - Shared configuration types

2. **Document each interface**:
   - Name and purpose
   - Methods/functions with signatures
   - Parameter and return types
   - Error types
   - Async/sync nature

### Step 3: Extract Naming Conventions

From the scan's naming analysis, document observed patterns:

1. **Method naming**: `get_*`, `create_*`, `update_*`, `delete_*`, `on_*`, `handle_*`
2. **Type naming**: `*Service`, `*Repository`, `*Handler`, `*Factory`, `*Builder`
3. **Module naming**: How modules are organized and named
4. **Constant naming**: UPPER_SNAKE, PascalCase, etc.

Present as a pattern table with purpose and examples.

### Step 4: Document Data Structures

For each shared type that crosses API boundaries:

1. **Full type definition** in the project's language
2. **Field-level documentation**: Type, purpose, constraints
3. **Usage context**: Which interfaces use this type
4. **Validation rules**: Any constraints on field values

### Step 5: Define Contracts

For each interface, document the behavioral contract:

1. **Preconditions**: What must be true before calling
2. **Postconditions**: What is guaranteed after calling
3. **Error semantics**: What errors can occur and what they mean
4. **Threading/async model**: Concurrency expectations
5. **Idempotency**: Whether operations are idempotent

### Step 6: Draft the Spec

Using the `template-impl-interface-design.md`:

1. Fill in metadata (RFC number, title, authors, date, depends on: relevant architecture RFCs)
2. Write Abstract
3. Write Scope (which API boundaries this covers)
4. Write Naming Conventions (from Step 3)
5. Write Data Structures (from Step 4)
6. Write Interface Contracts (from Steps 2 and 5)
7. Write Implementation Patterns (common patterns used across interfaces)
8. Write Examples (concrete usage examples from the codebase)
9. Write Relationship to Other RFCs

### Step 7: Present to User

Show the Draft RFC:

> "Here is the recovered Implementation Interface Design spec (RFC-000N). Key points:
> - Interfaces documented: [count]
> - Shared types: [count]
> - Naming conventions: [count patterns]
> - Depends on: [list architecture RFCs]
>
> Please review. Should I adjust anything before saving?"

## Quality Checklist

Before presenting:

- [ ] Interfaces are cross-boundary (not internal to a single module)
- [ ] Code blocks use the project's actual language
- [ ] Naming conventions are observed from code, not prescriptive
- [ ] Data structures include field-level documentation
- [ ] Contracts include error semantics
- [ ] Dependencies reference the correct architecture RFCs
- [ ] No implementation algorithms or internal details

## Common Pitfalls

- **Documenting everything**: Only document cross-boundary interfaces, not every function
- **Prescriptive naming**: Document observed conventions, don't invent new ones
- **Missing error types**: Error handling is a critical part of interface contracts
- **Language-agnostic when it shouldn't be**: Interface specs MAY be language-specific — use actual signatures

## Notes

- This operation is **optional** — only run when user explicitly requests it
- The spec is **Status: Draft**
- After writing, update rfc-history.md, rfc-index.md, and rfc-namings.md
