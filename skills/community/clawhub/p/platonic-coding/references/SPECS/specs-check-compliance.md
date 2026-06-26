# Check Standard Compliance

## Objective

Validate that all RFC files comply with the conventions defined in rfc-standard.md.

## Inputs

- **Specs Directory**: Path to the specs directory
- **Reference**: rfc-standard.md (for validation rules)

## Steps

1. **Read rfc-standard.md**
   - Understand required metadata fields
   - Understand status values and transitions
   - Understand structure requirements
   - Understand formatting conventions

2. **Scan All RFC Files**
   - Find all files matching `RFC-*.md` pattern
   - Exclude supporting files: `rfc-history.md`, `rfc-index.md`, `rfc-namings.md`, `rfc-standard.md`

3. **Check Metadata Fields**
   For each RFC, verify:
   - **Required fields present**: Status, Authors, Created, Last Updated
   - **Status value valid**: Must be Draft, Review, Frozen, or Deprecated
   - **Date format**: Must be YYYY-MM-DD
   - **RFC number format**: Must match RFC-NNN-<name> pattern
   - **Optional fields**: Depends on, Supersedes (if present, must be valid format)

4. **Check Structure**
   For each RFC, verify:
   - **Title format**: `# RFC-NNN-<name>: Title`
   - **Abstract section**: Section 1 should be Abstract
   - **Scope section**: Should have Scope and Non-Goals
   - **Proper heading levels**: Consistent use of ##, ###, etc.

5. **Check Frozen RFC Rules**
   For RFCs with Status: Frozen:
   - **No direct edits**: File should not be modified (only via versions)
   - **Version format**: If versioned, must follow RFC-NNN-<name>-<letter>.md format
   - **Version metadata**: Must have Parent RFC, Version, Changes fields

6. **Check Versioned RFC Rules**
   For versioned RFCs (RFC-NNN-<name>-<letter>.md):
   - **Parent exists**: Parent RFC must exist
   - **Version number**: Must be sequential (001, 002, 003...)
   - **Full content**: Must contain complete RFC, not just diffs
   - **Changes section**: Must document what changed

7. **Check Formatting**
   - **Markdown syntax**: Valid markdown
   - **Links**: Valid link format `[text](file.md)`
   - **Tables**: Valid table format
   - **Code blocks**: Properly formatted

8. **Generate Report**
   Create a report with:
   - **Errors**: Violations that must be fixed
   - **Warnings**: Issues that should be addressed

## Validation Rules

### Required Metadata Fields

- **Status**: MUST be present, MUST be one of: Draft, Review, Frozen, Deprecated
- **Authors**: MUST be present
- **Created**: MUST be present, MUST be YYYY-MM-DD format
- **Last Updated**: MUST be present, MUST be YYYY-MM-DD format

### Status Rules

- **Draft**: Can be edited in place
- **Review**: Ready for review, can be edited
- **Frozen**: Cannot be edited, must create version for changes
- **Deprecated**: No longer active

### Structure Rules

- **Title**: Must start with `# RFC-NNN-<name>: Title`
- **Abstract**: Section 1 must be Abstract
- **Scope**: Should have Scope and Non-Goals section
- **Sections**: Use consistent numbering (1, 2, 3...)

### Frozen RFC Rules

- **Immutability**: Frozen RFCs cannot be edited directly
- **Versioning**: Changes require creating RFC-NNN-<name>-<letter>.md
- **Version format**: <letter> must be a single lowercase letter (a, b, c, ... z)

### Versioned RFC Rules

- **Parent RFC**: Must specify Parent RFC field
- **Version**: Must specify Version field (001, 002...)
- **Changes**: Must specify Changes field describing what changed
- **Full content**: Must contain complete RFC content

## Output Format

### Errors

```
❌ Errors Found:
- RFC-001: Missing required field "Authors"
- RFC-002: Invalid status "Invalid" (must be Draft, Review, Frozen, or Deprecated)
- RFC-003: Frozen RFC was modified directly (should create version instead)
- RFC-004-001: Missing "Parent RFC" field
- RFC-005: Date format invalid "2026/01/28" (must be YYYY-MM-DD)
```

### Warnings

```
⚠️  Warnings:
- RFC-001: Missing "Abstract" section
- RFC-002: Section numbering inconsistent
- RFC-003: Depends on Draft RFC (prefer Frozen dependencies)
- RFC-004: Last Updated date is older than Created date
```

## Verification Checklist

After checking, verify:

- [ ] All required metadata fields are present
- [ ] All status values are valid
- [ ] All dates are in correct format
- [ ] Frozen RFCs are not modified directly
- [ ] Versioned RFCs follow correct format
- [ ] Structure follows rfc-standard.md conventions
- [ ] Formatting is consistent

## Notes

- **Errors** block compliance and should be fixed
- **Warnings** are suggestions for improvement
- **Frozen RFC edits** are critical errors
- **Missing required fields** are errors
- **Format issues** are usually warnings unless they break parsing

## Reference

Always refer to rfc-standard.md for:
- Exact field requirements
- Status transition rules
- Versioning rules
- Structure templates
- Formatting conventions
