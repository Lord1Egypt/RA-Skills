# Recover Architecture Design

Generate Architecture Design RFCs from codebase scan results, one per major subsystem.

## Objective

Produce Draft RFCs that capture each major subsystem's component structure, responsibilities, data flow, invariants, and dependency constraints.

## Inputs

| Input | Source |
|-------|--------|
| Scan synthesis | From scan-project.md |
| Confirmed RFC plan | From plan-modular-specs.md |
| Conceptual Design RFC | Generated in recover-conceptual.md |
| RFC numbers | From plan (e.g., 002, 003, ...) |
| Spec-kind template | `assets/specs/template-architecture-design.md` |

## Recovery Process

Repeat the following for each architecture RFC in the confirmed plan.

### Step 1: Define Subsystem Scope

From the confirmed RFC plan, identify which modules belong to this subsystem:

1. List the modules/packages/crates that fall within this subsystem
2. Clarify the boundary: what is in scope vs. neighboring subsystems
3. Note the subsystem's role in the overall system (from conceptual design)

### Step 2: Map Components

From the scan's structural analysis, for each module in this subsystem:

1. **Name**: Module/package name
2. **Responsibility**: What it does (infer from public API, doc comments, naming)
3. **Dependencies**: What it depends on (internal to subsystem, external)
4. **Public surface**: What it exposes to other modules/subsystems

Organize components into a component diagram or table.

### Step 3: Trace Data Flow

From the scan's behavioral analysis, map how data moves within and through this subsystem:

1. **Entry points**: How data enters this subsystem (API calls, events, scheduled tasks)
2. **Transformations**: What happens to data as it flows through
3. **Exit points**: Where data leaves (to other subsystems, storage, external systems)
4. **Primary flows**: The 1-3 most important data paths

Draw the data flow as a simple diagram:

```
Input → [Component A] → [Component B] → Output
```

### Step 4: Extract Invariants and Constraints

From the scan's invariant list, filtered to this subsystem:

1. **Architectural invariants**: Rules about component relationships
   - "Module A MUST NOT depend on Module B"
   - "Data MUST flow from X to Y, never the reverse"
   - "Component C MUST be stateless"

2. **Dependency constraints**: Rules about what can depend on what
   - Unidirectional dependencies (one-way imports)
   - Forbidden dependencies (circular deps prevented by structure)
   - Optional dependencies (feature-gated)

3. **Data constraints**: Rules about data within this subsystem
   - Immutability rules
   - Validation requirements
   - Ordering guarantees

### Step 5: Identify Abstract Schemas

From the scan's type catalog, identify the conceptual data models for this subsystem:

1. Select key types that represent this subsystem's domain
2. Abstract away language-specific details (no generics syntax, no lifetimes, etc.)
3. Present as abstract schemas with field names, types (in plain language), and descriptions
4. Focus on types that cross component boundaries or represent core concepts

### Step 6: Draft the Spec

Using the `template-architecture-design.md`:

1. Fill in metadata (RFC number, title, authors, date, depends on: RFC-001)
2. Write Abstract (what this subsystem is and its role)
3. Write Scope (which modules, what's in/out)
4. Write Background & Motivation (why this subsystem exists)
5. Write Architecture Overview with component diagram (from Step 2)
6. Write Components section with responsibilities (from Step 2)
7. Write Data Flow section (from Step 3)
8. Write Invariants and Constraints (from Step 4)
9. Write Abstract Schemas (from Step 5)
10. Write Relationship to Other RFCs (conceptual design + sibling architecture RFCs)

### Step 7: Present to User

Show each Draft RFC to the user:

> "Here is the recovered Architecture Design spec for [subsystem] (RFC-000N). Key points:
> - Components: [list names]
> - Data flow: [1-sentence summary]
> - Invariants: [count]
> - Depends on: RFC-001
>
> Please review. Should I adjust anything before saving?"

After user approval, write the file to the specs directory.

## Quality Checklist

Before presenting each spec:

- [ ] Abstract clearly states this subsystem's purpose and role
- [ ] Scope lists specific modules that belong to this subsystem
- [ ] Components have clear, distinct responsibilities
- [ ] Data flow diagram shows the primary 1-3 flows
- [ ] Invariants are specific and traceable to code structure
- [ ] Dependency constraints reflect actual code dependency direction
- [ ] Abstract schemas are language-neutral (no generics syntax, no lifetimes)
- [ ] No concrete API signatures or method-level detail (those belong in interface specs)
- [ ] Depends on RFC-001 (conceptual design)

## Common Pitfalls

- **Too detailed**: Architecture specs should describe "what components exist and how they relate," not method signatures
- **Too abstract**: Don't just say "this is the storage layer." Name the specific modules, their responsibilities, and the data flow
- **Missing constraints**: The most valuable part of an architecture spec is the invariants and constraints. Don't skip them
- **Ignoring dependencies**: Always specify the dependency direction between components and with other subsystems
- **Overlapping scope**: Each architecture spec should cover a distinct set of modules. No module should appear in two specs

## Cross-References

After generating all architecture specs:

1. Ensure each references the conceptual design (RFC-001)
2. Ensure sibling architecture specs reference each other where they interact
3. Update the conceptual design's "Relationship to Other RFCs" section if needed

## Notes

- Each spec is **Status: Draft**
- Generate architecture specs in RFC number order (002, 003, ...)
- After writing each file, update rfc-history.md with a "Created" event
- After all architecture specs are generated, update rfc-index.md and rfc-namings.md
