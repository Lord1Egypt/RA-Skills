# Validate Implementation Guide

Validate that an implementation guide does not contradict its source RFC specification.

## Purpose

Implementation guides **supersede** RFC specs in the sense that they provide concrete details, but they **MUST NOT contradict** the specs. This operation verifies compliance.

## Prerequisites

1. Implementation guide document exists
2. Source RFC document(s) are available
3. Project terminology reference is available (`docs/specs/rfc-namings.md`)

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Implementation Guide | Yes | Path to the implementation guide |
| Source RFC(s) | Yes | Path(s) to source RFC specification(s) |
| Namings Reference | No | Path to terminology reference (default: `docs/specs/rfc-namings.md`) |

## Validation Categories

### 1. Invariant Preservation

Check that all RFC invariants are respected in the implementation guide.

**Process**:
1. Extract all invariants from RFC (look for "MUST", "MUST NOT", "invariant", "never")
2. For each invariant, verify the guide does not violate it
3. Check that invariants are explicitly mentioned or clearly preserved

**Example Invariants**:
- "Storage MUST be append-only"
- "Events MUST NOT be modified after emission"
- "RST MUST NEVER depend on DES"

### 2. Requirement Coverage

Verify all RFC requirements are addressed.

**Process**:
1. Extract all requirements from RFC (MUST, SHALL, REQUIRED)
2. Map each requirement to guide sections
3. Verify each requirement has corresponding implementation detail
4. Flag any unaddressed requirements

### 3. Constraint Compliance

Check that RFC constraints are followed.

**Process**:
1. Extract constraints (limits, boundaries, conditions)
2. Verify guide respects these constraints
3. Check for any constraint violations

### 4. Terminology Consistency

Verify correct use of RFC-defined terms.

**Process**:
1. Load terminology from `rfc-namings.md`
2. Check guide uses canonical terms
3. Flag deprecated or incorrect terminology
4. Verify definitions match RFC definitions

### 5. Contradiction Detection

Find statements that conflict with RFC.

**Process**:
1. Compare guide statements with RFC statements
2. Identify semantic conflicts
3. Check for incompatible type definitions
4. Verify behavior descriptions match

## Output: Validation Report

```markdown
# Implementation Guide Validation Report

**Guide**: [path to guide]
**Source RFC(s)**: [list of RFCs]
**Validation Date**: [date]

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Invariant Preservation | PASS / FAIL | N |
| Requirement Coverage | PASS / FAIL | N |
| Constraint Compliance | PASS / FAIL | N |
| Terminology Consistency | PASS / FAIL | N |
| Contradiction Detection | PASS / FAIL | N |

**Overall Status**: COMPLIANT / NON-COMPLIANT

## Detailed Findings

### Invariants Verified
- [x] Invariant 1: [description] - Guide Section X
- [x] Invariant 2: [description] - Guide Section Y

### Requirements Covered
- [x] Requirement 1: [description] - Guide Section X
- [ ] Requirement 2: [description] - **NOT ADDRESSED**

### Contradictions Found
1. **[CRITICAL]** Guide states X, but RFC-NNN-<name> Section Y states Z
   - Guide: "[quote from guide]"
   - RFC: "[quote from RFC]"
   - Recommendation: [how to fix]

### Terminology Issues
1. Guide uses "foo" but RFC defines canonical term as "bar"
   - Location: Guide Section X
   - Recommendation: Replace "foo" with "bar"

## Recommendations

1. [Priority] [Recommendation]
2. [Priority] [Recommendation]
```

## Severity Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| CRITICAL | Direct contradiction of RFC | Must fix before implementation |
| HIGH | Missing required functionality | Should fix before implementation |
| MEDIUM | Terminology or style issues | Fix when convenient |
| LOW | Suggestions for improvement | Optional |

## Example

**Input**:
- Guide: `docs/impl/IG-042-message-queue-protocol.md`
- RFC: `docs/specs/RFC-042-message-queue.md`

**Validation**:
1. Check RFC-042-message-queue invariants (at-least-once delivery, message ordering)
2. Verify all Message Queue requirements are in the guide
3. Confirm type definitions match RFC schemas
4. Check terminology against project naming conventions

**Output**: Validation report with compliance status
