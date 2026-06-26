# Update Implementation Guide

Update an implementation guide when its source RFC specification changes.

## Purpose

When an RFC is revised or versioned, the corresponding implementation guide must be updated to remain consistent. This operation ensures guides stay synchronized with their source specs.

## Prerequisites

1. Implementation guide exists
2. RFC has been updated (new version or revision)
3. RFC change history or diff is available

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Implementation Guide | Yes | Path to the implementation guide to update |
| Updated RFC | Yes | Path to the updated RFC specification |
| Previous RFC | No | Path to previous RFC version (for diff) |
| Change Description | No | Summary of what changed in the RFC |

## Process

### Step 1: Identify RFC Changes

Determine what changed in the RFC:

1. **If RFC was versioned**: Compare `RFC-NNN-<name>.md` with `RFC-NNN-<name>-<letter>.md`
2. **If RFC was revised**: Check RFC revision history section
3. **If change description provided**: Use as starting point

Categorize changes:
- **Additions**: New requirements, types, behaviors
- **Modifications**: Changed requirements, updated types
- **Removals**: Deprecated or removed features
- **Clarifications**: No functional change, just clearer wording

### Step 2: Analyze Impact

For each RFC change, determine impact on implementation guide:

| RFC Change Type | Guide Impact |
|-----------------|--------------|
| New requirement | Add implementation details |
| Modified requirement | Update affected sections |
| Removed requirement | Remove or mark deprecated |
| New type/field | Add type definition |
| Changed type/field | Update type definition |
| New invariant | Verify guide compliance |
| Changed invariant | Update affected sections |

### Step 3: Update Guide Sections

For each impacted section:

1. **Locate affected content** in the guide
2. **Update to match** new RFC requirements
3. **Preserve existing** implementation decisions that remain valid
4. **Add new sections** for new RFC content
5. **Mark deprecated** content that's being removed

### Step 4: Update Metadata

Update guide header:

```markdown
> **Source**: Derived from RFC-NNN-<name>-<letter> (Title) ← Update version
> **Last Updated**: YYYY-MM-DD ← Update date
```

### Step 5: Document Changes

Add entry to guide's revision history (if present) or create one:

```markdown
## Revision History

| Date | RFC Version | Changes |
|------|-------------|---------|
| YYYY-MM-DD | RFC-NNN-<name>-<letter> | Updated X, added Y, removed Z |
| YYYY-MM-DD | RFC-NNN-<name> | Initial guide |
```

### Step 6: Re-validate

Run `validate-guide.md` operation to ensure:
- No contradictions with updated RFC
- All new requirements are addressed
- No references to removed RFC content

## Output

Updated implementation guide with:
- Content synchronized with new RFC
- Updated metadata and references
- Documented revision history
- Validation confirmation

## Change Tracking Template

Use this template to track changes during update:

```markdown
# Implementation Guide Update Tracker

**Guide**: [path]
**RFC Update**: [old version] → [new version]
**Date**: [date]

## RFC Changes Identified

### Additions
- [ ] [Change description] → Guide Section: [section]

### Modifications  
- [ ] [Change description] → Guide Section: [section]

### Removals
- [ ] [Change description] → Guide Section: [section]

## Guide Updates Made

1. Section X: [description of update]
2. Section Y: [description of update]

## Validation Status

- [ ] Ran validate-guide operation
- [ ] All checks passed
```

## Example

**Scenario**: RFC-042 (Message Queue Protocol) adds a new `MessagePriority::Critical`

**Process**:
1. Identify change: New enum variant in `MessagePriority`
2. Analyze impact: Need to update type definition, possibly add handling
3. Update guide:
   - Add `Critical` to `MessagePriority` enum in Section 3.5
   - Add description of critical priority semantics and ordering guarantees
   - Update any exhaustive match examples
4. Update metadata: Bump RFC reference to new version
5. Document: Add revision history entry
6. Validate: Run validation to confirm compliance

## Best Practices

1. **Don't remove history**: Mark deprecated content rather than deleting
2. **Explain rationale**: Document why changes were made
3. **Atomic updates**: Update all affected sections together
4. **Test impact**: Consider if code needs updating too
5. **Cross-reference**: Update related guides if they reference changed content
