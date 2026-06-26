# Create Implementation Guide

Create a new implementation guide from an RFC specification.

## Prerequisites

Before creating an implementation guide, ensure:

1. **RFC exists**: The source RFC document is available and in Frozen or Draft status
2. **Scope is clear**: You know which module/crate/package will implement the RFC
3. **Language is known**: Target programming language and framework are specified
4. **Project context**: You understand the existing codebase architecture

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| RFC Document | Yes | Path to source RFC specification |
| Target Module | Yes | Name of implementing module/crate/package |
| Language | Yes | Target programming language (e.g., Rust, Python, TypeScript) |
| Framework | No | Framework if applicable (e.g., Tokio, Actix, React) |
| Output Path | No | Where to save the guide (default: `docs/impl/`) |

## Process

### Step 1: Analyze RFC Specification

Read the RFC document and extract:

1. **Core Concepts**: Key abstractions and entities defined
2. **Requirements**: What must be implemented (MUST, SHALL)
3. **Constraints**: Limitations and invariants
4. **Interfaces**: Expected APIs and protocols
5. **Data Structures**: Defined types and schemas
6. **Behaviors**: Expected runtime behavior
7. **Dependencies**: Related RFCs and external systems

Create a checklist of all extractable requirements.

### Step 2: Design Architecture

Based on RFC analysis, design:

1. **Module Structure**: Directory layout and file organization
2. **Type Mappings**: How RFC concepts map to language types
3. **Dependency Graph**: Internal and external dependencies
4. **Data Flow**: How data moves through the system
5. **Error Strategy**: How errors are represented and handled

### Step 3: Define Concrete Types

For each RFC concept, define concrete types:

```rust
// Example: Rust type definition
/// Documentation referencing RFC section
pub struct ConceptName {
    /// Field documentation
    pub field_name: FieldType,
}
```

Include:
- Full type definitions with all fields
- Documentation comments referencing RFC
- Visibility modifiers appropriate to the language
- Generic parameters if needed

### Step 4: Define Interfaces

For each required behavior, define interfaces:

```rust
// Example: Rust trait definition
/// Trait documentation referencing RFC section
pub trait BehaviorName {
    /// Method documentation
    fn method_name(&self, param: ParamType) -> Result<ReturnType>;
}
```

Include:
- All required methods
- Parameter and return types
- Error types
- Async markers if applicable

### Step 5: Document Implementation Details

For complex algorithms or protocols:

1. Describe the algorithm step-by-step
2. Include diagrams if helpful
3. Reference RFC sections for requirements
4. Note any implementation choices and rationale

### Step 6: Generate Guide Document

Use the template from `assets/impl-guide-template.md`:

1. Fill in all sections
2. Include code examples
3. Add diagrams where helpful
4. Reference source RFC throughout
5. Document any interpretations of ambiguous specs

## Output

A complete implementation guide document containing:

- Overview and architectural position
- Module structure
- Complete type definitions
- Interface/trait definitions
- Implementation details
- Error handling strategy
- Configuration options
- Testing strategy

**Naming Convention**: Implementation guides should follow the naming pattern `IG-<number>-semantic-short-desc.md` (e.g., `IG-053-cli-command-nesting.md`).

## Validation

After creating the guide:

1. Run `validate-guide.md` operation to check for contradictions
2. Review against project coding standards
3. Verify all RFC requirements are addressed

## Example

**Input**:
- RFC: `docs/specs/RFC-042-message-queue.md` (Message Queue Protocol)
- Target Module: `acme-queue`
- Language: Rust
- Framework: Tokio (async runtime)

**Output**: `docs/impl/IG-042-message-queue-protocol.md`

The guide would include:
- Crate structure for `acme-queue`
- Rust struct definitions for `QueueMessage`, `MessageEnvelope`, etc.
- Trait definitions for producer and consumer interfaces
- Persistence layer implementation details
- Message serialization schema
