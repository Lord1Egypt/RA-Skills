# RFC Specifications & Management Guide

This document defines the process, conventions, and guidelines for creating and managing RFCs (Requests for Comments) in the {{PROJECT_NAME}} project.

---

## Table of Contents

1. [Overview](#overview)
2. [Spec Kinds](#spec-kinds)
3. [RFC Process](#rfc-process)
4. [Naming Conventions](#naming-conventions)
5. [Status Management](#status-management)
6. [Versioning Rules](#versioning-rules)
7. [RFC Template](#rfc-template)
8. [Best Practices](#best-practices)
9. [Metadata Fields Reference](#metadata-fields-reference)
10. [FAQ](#faq)

---

## Overview

RFCs are the authoritative specifications for the {{PROJECT_NAME}} system. They define:

- Core architectural decisions
- Data models and semantics
- API contracts and interfaces
- System behavior and invariants

RFCs serve as:

- **Design documents** during development
- **Implementation contracts** for engineers
- **Reference documentation** for users
- **Historical record** of design decisions

### Important: RFC Purpose and Scope

RFCs are designed to record **high-level design decisions**, not implementation details. Focus on:

- **Abstract**: Clear summary of the design intent and rationale
- **Architecture**: Component structure, responsibilities, and interactions
- **Protocol**: Communication patterns, message formats, and flow control
- **Data structures**: Key entities, relationships, and invariants

RFCs should **NOT** include:

- Detailed code examples beyond interface signatures
- Step-by-step implementation instructions
- Language-specific optimizations
- Testing strategies (those belong in implementation guides)

### File Size Limit

Each RFC file should be **under 800 lines**. If an RFC exceeds this limit:

- Split into multiple RFCs with clear dependencies
- Move detailed specifications to child RFCs
- Keep the parent RFC focused on high-level architecture
- Consider if the RFC is too detailed (it may belong in an implementation guide instead)

---

## Spec Kinds

{{PROJECT_NAME}} RFCs fall into three kinds, each with a distinct purpose and level of abstraction:

### Conceptual Design

**Purpose**: Define the system's vision, principles, taxonomy, and invariants.

**Contains**:
- System goals and design philosophy
- Fundamental abstractions and conceptual model
- Core terminology and taxonomy
- System-wide invariants

**Does NOT contain**: Schemas, APIs, code, storage formats, component boundaries.

**When to use**: Starting a new system or subsystem; defining foundational concepts that other specs depend on.

### Architecture Design

**Purpose**: Define components, layers, responsibilities, data flow, and constraints.

**Contains**:
- Component/module structure and responsibilities
- Data flow between components
- Invariants (MUST/MUST NOT rules)
- Abstract schemas and dependency constraints

**Does NOT contain**: Concrete API signatures, language-specific code, implementation details.

**When to use**: Designing system architecture, layer boundaries, storage models, or subsystem structure.

### Implementation Interface Design

**Purpose**: Define API contracts, naming conventions, and interface signatures.

**Contains**:
- Naming patterns and conventions
- Type/struct definitions
- Trait/interface signatures
- Error handling patterns and flow control semantics

**May be language-specific**: Code blocks in the target language are appropriate.

**When to use**: Defining cross-component API contracts, data access patterns, or shared interfaces.

### Dependency Flow Between Kinds

```
Conceptual Design → Architecture Design → Implementation Interface Design
```

Each kind builds on the previous. Conceptual specs typically have no RFC dependencies; architecture specs depend on conceptual; impl-interface specs depend on architecture. This is guidance, not a hard rule.

---

## RFC Process

### When to Create an RFC

Create an RFC when:

- Defining a new subsystem or layer
- Specifying public API contracts
- Establishing semantic guarantees or invariants
- Making cross-cutting architectural decisions
- Proposing significant changes to frozen RFCs

Do NOT create an RFC for:

- Implementation details that don't affect contracts
- Internal optimizations invisible to other layers
- Temporary workarounds or experiments
- Documentation updates without semantic changes

### RFC Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft: Create RFC
    Draft --> Review: Request review
    Review --> Draft: Revisions needed
    Review --> Frozen: Approved
    Frozen --> Amendment: Need changes
    Amendment --> Frozen: Create versioned RFC

    note right of Draft
        Editable in place
        May be incomplete
    end note

    note right of Frozen
        Immutable
        Production reference
    end note

    note right of Amendment
        Creates RFC-NNN-<letter>.md
        Version increments by 1
    end note
```

#### Stage 1: Draft

- RFC is created with `Status: Draft`
- Author iterates on design
- May be edited freely in place
- Incomplete sections are acceptable
- Other engineers may provide feedback

#### Stage 2: Review

- Author requests review when RFC is complete
- Core team reviews for:
  - Completeness
  - Consistency with other RFCs
  - Technical correctness
  - Clarity and readability

#### Stage 3: Frozen

- RFC is marked `Status: Frozen`
- Becomes immutable production reference
- Implementation may begin or continue
- Any changes require creating a versioned update

### Who Can Freeze an RFC

- Core team members with architecture responsibility
- Project maintainers
- Requires consensus among reviewers

---

## Naming Conventions

### Numbered RFCs

**Filename convention**: RFC spec files MUST be named `RFC-NNN-<brief-semantic-name>.md`.

- `RFC`: Capital letters (literal)
- `NNN`: 3-digit zero-padded number (001, 002, etc.)
- `<brief-semantic-name>`: Kebab-case brief description (e.g., `message-queue`, `user-auth`)
- Sequential numbering
- Numbers are reserved once assigned, even if RFC is deleted

**Examples**:
- `RFC-001-world-view.md` - First RFC (conceptual: world view)
- `RFC-042-message-queue.md` - Forty-second RFC (architecture: message queue)
- `RFC-100-api-gateway.md` - One hundredth RFC (impl-interface: API gateway)

### Special RFCs

**Format**: `rfc-{name}.md`

Used for cross-cutting RFCs: `rfc-namings.md`, `rfc-index.md`, etc.

### Versioned RFC Updates

**Format**: `RFC-NNN-<brief-semantic-name>-<letter>.md`

- `NNN`: Original RFC number (3-digit padded)
- `<brief-semantic-name>`: Same semantic name from base RFC (preserved across versions)
- `<letter>`: Single lowercase letter (a, b, c, ... z) for minor versions
- Used only for updates to frozen RFCs

**Examples**:
- `RFC-001-world-view-a.md` - First update to RFC-001-world-view.md
- `RFC-001-world-view-b.md` - Second update to RFC-001-world-view.md
- `RFC-042-message-queue-j.md` - Tenth update to RFC-042-message-queue.md

---

## Status Management

### Status Values

| Status | Meaning | Editable? |
|--------|---------|-----------|
| **Draft** | Work in progress | Yes |
| **Review** | Ready for review | Yes (with feedback) |
| **Frozen** | Immutable production reference | No (create version) |
| **Deprecated** | No longer active | No |

### Changing Status

- **Draft → Review**: Complete the RFC, update status, request review
- **Review → Frozen**: Address feedback, ensure consensus, update status, commit with `docs: freeze RFC-NNN-<name>`
- **Frozen → Amendment**: Create new file `RFC-NNN-<name>-<letter>.md` with full content, commit with `docs: add RFC-NNN-<name> version <letter>`

---

## Versioning Rules

### For Draft and Review RFCs

- Edit in place
- Update `Last Updated` field when making changes
- No version numbers needed
- Once frozen, versioning rules apply

### For Frozen RFCs

Frozen RFCs are **immutable**. To make updates:

1. Create `RFC-NNN-<name>-<letter>.md` (next sequential letter; first version is a)
2. Copy full content from original (version files are standalone and complete, not diffs)
3. Make changes
4. Update metadata:

```markdown
# RFC-NNN-<name>-<letter>: [Title] (Update <letter>)

**Status**: Frozen
**Parent RFC**: RFC-NNN-<name>
**Version**: <letter>
**Authors**: [Author names]
**Created**: YYYY-MM-DD
**Changes**: [Brief summary]
**Supersedes**: RFC-NNN-<name> or RFC-NNN-<name>-b
**Depends on**: [RFC-XXX-<name>, RFC-YYY-<name>]
```

5. Update [rfc-index.md](rfc-index.md) with the new version entry

### Version Increment Rules

- Versions are sequential letters: a, b, c, ... z
- No gaps in version letters
- Version a supersedes the base RFC-NNN-<name>
- Version b supersedes RFC-NNN-<name>-a
- And so on
- Maximum 26 versions per RFC (a-z); after z, create a new RFC number

---

## RFC Template

Use this template when creating new RFCs:

```markdown
# RFC-NNN-<brief-semantic-name>: [Title]

**Status**: Draft
**Authors**: [Your name(s)]
**Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD
**Depends on**: [RFC-XXX-<name>, RFC-YYY-<name>, or "---" if none]
**Supersedes**: [RFC-ZZZ-<name> or "---" if none]
**Stage**: [Optional: e.g. Core | Storage | API]
**Kind**: [Conceptual Design | Architecture Design | Implementation Interface Design]

---

## 1. Abstract

[2-4 sentences summarizing what this RFC defines and why it matters]

---

## 2. Scope and Non-Goals

### 2.1 Scope

This RFC defines:
* [What is specified]
* [Key concepts covered]
* [Boundaries of specification]

### 2.2 Non-Goals

This RFC does **not** define:
* [What is explicitly excluded]
* [What is covered by other RFCs]
* [Future work not in scope]

---

## 3. Background & Motivation

[Why is this RFC needed? What problem does it solve?]

---

## 4. Design Principles

[Core principles guiding the design, typically 3-5 items]

1. **Principle 1**: Description
2. **Principle 2**: Description
3. **Principle 3**: Description

---

## 5. [Main Content Sections]

[Organize your specification into logical sections]

### 5.1 [Subsection]

[Detailed specification content]

---

## 6. Examples

[Concrete examples demonstrating the specification]

---

## 7. Relationship to Other RFCs

[How this RFC relates to and depends on other RFCs]

* **RFC-XXX-<name>**: [Relationship]
* **RFC-YYY-<name>**: [Relationship]

---

## 8. Open Questions

[Optional: Unresolved questions or future work]

* [Question 1]
* [Question 2]

---

## 9. Conclusion

[1-2 paragraphs summarizing the key takeaways]

> **Optional quotable summary of the RFC's core contribution**
```

### Template for Versioned RFCs

```markdown
# RFC-NNN-<name>-<letter>: [Title] (Update <letter>)

**Status**: Frozen
**Parent RFC**: RFC-NNN-<name>
**Version**: <letter>
**Authors**: [Author names]
**Created**: YYYY-MM-DD
**Changes**: [Brief summary of what changed in this version]
**Supersedes**: RFC-NNN-<name> or RFC-NNN-<name>-b
**Depends on**: [RFC-XXX-<name>, RFC-YYY-<name>]

---

## Changes in This Version

[Detailed description of changes from previous version]

### Modified Sections

- **Section X**: [What changed and why]
- **Section Y**: [What changed and why]

### New Sections

- **Section Z**: [What was added and why]

### Deprecated Content

- **Section W**: [What was removed and why]

---

[Full RFC content follows - complete document, not diffs]

## 1. Abstract

[...]
```

---

## Best Practices

### Writing Style

1. **Be precise**: Use normative keywords (MUST, SHOULD, MAY) consistently
2. **Be clear**: Avoid ambiguity; prefer explicit specifications
3. **Be complete**: Cover all relevant cases and edge conditions
4. **Be concise**: Remove unnecessary words; focus on content
5. **Use examples**: Illustrate complex concepts with concrete examples

### Normative Keywords

Follow RFC 2119 conventions:

- **MUST / REQUIRED / SHALL**: Absolute requirement
- **MUST NOT / SHALL NOT**: Absolute prohibition
- **SHOULD / RECOMMENDED**: Strong recommendation, exceptions possible
- **SHOULD NOT / NOT RECOMMENDED**: Strong discouragement
- **MAY / OPTIONAL**: Truly optional

### Structure

- Use consistent heading levels
- Group related concepts together
- Put foundational concepts before advanced topics
- Include a Table of Contents for long RFCs (>1000 lines)
- Use tables for comparisons and categorization
- Use code blocks for syntax and examples
- Use diagrams (mermaid) for complex relationships

### Dependencies

- Explicitly list all RFC dependencies in metadata
- Reference specific sections when citing other RFCs
- Avoid circular dependencies
- Prefer depending on frozen RFCs over drafts

### Cross-References

Use markdown links for all RFC references:

- Link to RFCs: `[RFC-NNN-<name>](RFC-NNN-<name>.md)`
- Link to sections: `[RFC-NNN-<name>, Section 4](RFC-NNN-<name>.md#4-design-principles)`
- Link to versions: `[RFC-NNN-<name>-<letter>](RFC-NNN-<name>-<letter>.md)`

### Terminology Management

The [rfc-namings.md](rfc-namings.md) file **MUST** always reflect the latest terminology from active RFCs.

- **MUST** keep rfc-namings.md synchronized with terminology in active RFCs
- **MUST NOT** include version history in rfc-namings.md (version history belongs in rfc-history.md)
- **MUST** update rfc-namings.md when new terms are introduced
- **MUST** remove deprecated terms when RFCs are deprecated

---

## Metadata Fields Reference

### Required Fields (All RFCs)

| Field | Format | Description |
|-------|--------|-------------|
| `Status` | `Draft`, `Review`, `Frozen`, `Deprecated` | Current RFC status |
| `Authors` | Free text | RFC author(s) |
| `Created` | `YYYY-MM-DD` | Date RFC was created |
| `Last Updated` | `YYYY-MM-DD` | Date of most recent change |
| `Depends on` | `RFC-NNN-<name>, RFC-MMM-<name>` or `---` | RFC dependencies |
| `Supersedes` | `RFC-NNN-<name>` or `---` | RFC this replaces |

### Optional Fields

| Field | Format | Description |
|-------|--------|-------------|
| `Stage` | Free text | Development stage or subsystem |
| `Kind` | `Conceptual Design`, `Architecture Design`, `Implementation Interface Design` | Spec kind |

### Additional Fields (Versioned RFCs Only)

| Field | Format | Description |
|-------|--------|-------------|
| `Parent RFC` | `RFC-NNN-<name>` | Original RFC being updated |
| `Version` | `<letter>` | Version letter (a, b, c, ... z) |
| `Changes` | Free text | Summary of changes |

---

## FAQ

### Q: When should I freeze an RFC?

**A**: Freeze an RFC when:
- Implementation is starting or in progress
- Other RFCs need to depend on it with stability
- The design is reviewed and approved
- You want to prevent accidental changes

### Q: Can I edit a frozen RFC to fix typos?

**A**: No. Even typo fixes require creating a new version. This preserves the historical record and ensures immutability.

### Q: What if I need to make a small change to a frozen RFC?

**A**: Create a new version (`RFC-NNN-<name>-a.md`) with the full content. Even small changes require versions. This maintains consistency and traceability.

### Q: How do I know what version letter to use?

**A**: Find the highest existing version letter and use the next letter. If no versions exist, use a. Check both the filesystem and [rfc-index.md](rfc-index.md).

### Q: Can I skip version letters?

**A**: No. Versions must be sequential letters with no gaps (a, b, c, ...).

### Q: Should I delete old versions?

**A**: No. Keep all versions for historical reference and traceability.

### Q: What if my RFC depends on a Draft RFC?

**A**: That's fine while both are drafts. Consider:
- Freezing dependencies first
- Moving both forward together
- Merging related drafts

### Q: How do I handle breaking changes?

**A**: Create a new version and:
- Clearly document breaking changes in "Changes" section
- Provide migration guidance
- Consider deprecation period if widely implemented
- Update dependent RFCs if needed

---

**For questions about RFC management, contact the {{PROJECT_NAME}} core team.**
