# Recover Conceptual Design

Generate a Conceptual Design RFC from codebase scan results.

## Objective

Produce a Draft RFC that captures the system's vision, principles, taxonomy, and invariants — the foundational spec that all other RFCs depend on.

## Inputs

| Input | Source |
|-------|--------|
| Scan synthesis | From scan-project.md |
| Confirmed RFC plan | From plan-modular-specs.md |
| RFC number | From plan (default: 001) |
| Spec-kind template | `assets/specs/template-conceptual-design.md` |

## Recovery Process

### Step 1: Extract Vision

From the scan synthesis, formulate the system's vision:

**Sources** (in priority order):
1. README description and project tagline
2. Package/crate/module descriptions in build files
3. Top-level doc comments in main/lib entry points
4. Test names and descriptions (reveal intent)

**Output**: 2-4 sentence abstract answering "What is this system and why does it exist?"

### Step 2: Infer Design Principles

From patterns observed across the codebase, infer what design philosophy guided development:

| Code Pattern | Likely Principle |
|-------------|-----------------|
| Immutable data structures, no update/delete operations | Append-only / Immutability |
| Extensive input validation, boundary checks | Defense in depth / Fail-fast |
| Small interfaces, dependency injection | Separation of concerns / Loose coupling |
| Strong typing, no `any`/`Object`, sum types for states | Type safety / Make illegal states unrepresentable |
| Comprehensive error types, no panics/throws | Explicit error handling / Resilience |
| Async everywhere, message passing | Concurrency-first / Non-blocking |
| Feature flags, optional dependencies | Modularity / Progressive disclosure |
| Detailed logging, metrics, tracing | Observability / Transparency |
| Pure functions, no side effects in core | Functional core / Imperative shell |
| Version fields, migration code | Backward compatibility / Evolution |

**Process**:
1. Review the scan's design pattern catalog and invariant list
2. Match observed patterns to likely principles
3. Formulate 3-5 principles with clear descriptions
4. Order from most fundamental to most specific

### Step 3: Build Taxonomy

From domain types, naming patterns, and shared vocabulary:

1. **Collect terms**: All named types, concepts, and abstractions from the scan's type catalog
2. **Filter**: Keep terms that represent domain concepts (not language mechanics)
3. **Define**: Write a 1-sentence definition for each term
4. **Trace**: Note which module introduces each term
5. **Organize**: Group related terms, alphabetize within groups

### Step 4: Identify Invariants

From assertions, error types, validation rules, and test expectations:

1. **Collect**: All enforced rules from the scan's behavioral analysis
2. **Categorize**: System-wide vs. module-specific (keep only system-wide for conceptual)
3. **Formulate**: State each invariant as a MUST/MUST NOT rule
4. **Explain**: Brief description of what the invariant means and why it matters

### Step 5: Draft the Spec

Using the `template-conceptual-design.md`:

1. Fill in metadata (RFC number, title, authors, date, depends on: "---")
2. Write Abstract (from Step 1)
3. Write Scope (what this spec covers) and Non-Goals
4. Write Background & Motivation
5. Write Design Principles (from Step 2)
6. Write Conceptual Model (from the scan's conceptual clusters)
7. Write Taxonomy table (from Step 3)
8. Write Invariants (from Step 4)
9. Write Relationship to Other RFCs (list planned architecture RFCs)
10. Mark any Open Questions

### Step 6: Present to User

Show the complete Draft RFC to the user:

> "Here is the recovered Conceptual Design spec (RFC-001). Key points:
> - Vision: [1-sentence summary]
> - Principles: [list principle names]
> - Terms defined: [count]
> - Invariants: [count]
>
> Please review. Should I adjust anything before saving?"

After user approval, write the file to the specs directory.

## Quality Checklist

Before presenting the spec:

- [ ] Abstract is 2-4 sentences, clearly states what the system is
- [ ] Scope explicitly lists what is and is not covered
- [ ] Principles are inferred from code patterns, not generic platitudes
- [ ] Taxonomy terms are project-specific, not language-generic
- [ ] Invariants are actually enforced in the code (not aspirational)
- [ ] No schemas, APIs, or code blocks in the spec (those belong in architecture/interface specs)
- [ ] Relationships section lists the planned architecture RFCs

## Common Pitfalls

- **Generic principles**: "Code should be clean" is useless. Principles must be specific and traceable to code patterns.
- **Over-scoping**: The conceptual spec covers vision and principles, not architecture. Don't describe component structure.
- **Under-scoping**: Don't produce a 3-paragraph RFC. Extract enough principles, terms, and invariants to be meaningful.
- **Ungrounded invariants**: Only list invariants actually enforced in code. If the code doesn't enforce it, it's aspirational, not an invariant.

## Notes

- The spec is always **Status: Draft** — the user will review and refine
- The agent may iterate with the user before finalizing
- After writing the file, update rfc-history.md with a "Created" event
