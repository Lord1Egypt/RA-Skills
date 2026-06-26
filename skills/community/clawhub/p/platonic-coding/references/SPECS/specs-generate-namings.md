# Generate Namings

## Objective

Extract terminology from all active RFC files and update `rfc-namings.md` to reflect the current state of terminology used in the project.

## Inputs

- **Specs Directory**: Path to the specs directory

## Important Rules

1. **NO VERSION HISTORY**: rfc-namings.md MUST NOT contain version history. Version history belongs in rfc-history.md.
2. **CURRENT STATE ONLY**: rfc-namings.md reflects only the current terminology from active RFCs.
3. **REMOVE DEPRECATED**: Terms from deprecated or removed RFCs must be removed.

## Steps

1. **Identify Active RFCs**
   - Scan for files matching `RFC-*.md` pattern
   - Exclude: `rfc-history.md`, `rfc-index.md`, `rfc-namings.md`, `rfc-standard.md`
   - Exclude versioned RFCs (RFC-NNN-<name>-<letter>.md format)
   - Exclude RFCs with Status "Deprecated"
   - Only process RFCs with Status: Draft, Review, or Frozen

2. **Extract Terms from Each Active RFC**
   For each active RFC, identify terminology definitions:
   
   **Pattern 1**: Bold term followed by colon
   - Look for: `**Term**: Definition` or `**Term (Abbreviation)**: Definition`
   - Extract term name and definition
   - Note the RFC number and section if available
   
   **Pattern 2**: Definition lists
   - Look for: `- **Term**: Definition` in lists
   - Extract term and definition
   
   **Pattern 3**: Tables with term definitions
   - Look for tables with columns like "Term | Definition | Source"
   - Extract terms from table rows
   
   **Pattern 4**: Explicit definitions
   - Look for phrases like "X is defined as..." or "X refers to..."
   - Extract term and definition

3. **Organize Terms**
   Group terms by category (if identifiable):
   - System-level terms
   - Architecture-level terms
   - Data structure terms
   - Design principle terms
   - Time model terms
   - Runtime control terms
   - External system terms

4. **Generate Terminology Index Table**
   Create a table with columns:
   - Term
   - Source RFC (format: RFC-NNN-<name> or RFC-NNN-<name> §X.Y)
   - Brief Description (first 100 characters of definition)

   Format:
   ```markdown
   | Term | Source RFC | Brief Description |
   |------|-----------|-------------------|
   | World Model | RFC-001-world-view | A continuously running process... |
   ```

5. **Update rfc-namings.md**
   - Read existing `rfc-namings.md`
   - Find section `## 2. Terminology Index`
   - Replace the table content (between header row and `---`) with generated table
   - Update `**Last Updated**:` field to today's date (YYYY-MM-DD)
   - **CRITICAL**: Ensure no version history section exists
   - Preserve sections: Overview, Usage Guidelines, Related Documents

## Term Extraction Guidelines

- **Extract only defined terms**, not every capitalized word
- **Include abbreviations** if explicitly defined (e.g., "RST (Raw Sensory Trace)")
- **Extract from definitions**, not just mentions
- **Note source RFC** and section number when available
- **Create brief descriptions** by truncating definitions to ~100 characters

## Removal Rules

- **Remove terms** from RFCs that are deprecated
- **Remove terms** from RFCs that have been removed
- **Remove duplicate terms** (keep the most recent or authoritative source)
- **Remove version history** if it exists in rfc-namings.md

## Output Format

### Terminology Index

```markdown
## 2. Terminology Index

| Term | Source RFC | Brief Description |
|------|-----------|-------------------|
| World Model | RFC-001 | A continuously running process that transforms irreversible experience traces... |
| Stream | RFC-001 §3.1 | The fundamental abstraction of world observation as a directed flow of states |
| RST | RFC-001 §5.1 | Raw Sensory Trace: Direct multi-modal recordings with minimal interpretation |
```

## Verification

After updating, verify:

- All active RFCs are represented
- No deprecated terms remain
- No version history section exists
- Terms are sorted alphabetically (optional but recommended)
- Source RFCs are correctly formatted
- Brief descriptions are clear and concise

## Notes

- **Focus on canonical terms** - terms that are explicitly defined, not just mentioned
- **Preserve existing organization** if rfc-namings.md has a good structure
- **Update Last Updated date** to today
- **Remove any "Version History" section** if present
- **Keep Usage Guidelines section** unchanged unless updating rules

## Error Handling

- If a term appears in multiple RFCs, prefer the RFC with higher number (more recent)
- If section numbers are unclear, use RFC number only
- If definition is too long, truncate intelligently (at sentence boundary if possible)
