# Generate Index

## Objective

Scan all RFC files in the specs directory and generate/update `rfc-index.md` with current RFC list, status, and quick links.

## Inputs

- **Specs Directory**: Path to the specs directory

## Steps

1. **Scan RFC Files**
   - Find all files matching pattern `RFC-*.md` in the specs directory
   - Exclude: `rfc-history.md`, `rfc-index.md`, `rfc-namings.md`, `rfc-standard.md`
   - Separate base RFCs (e.g., `RFC-001-world-view.md`) from versioned RFCs (e.g., `RFC-001-world-view-001.md`)

2. **Extract Metadata from Base RFCs**
   For each base RFC file (not versioned), extract:
   - RFC number (from filename, e.g., `RFC-001-world-view.md` → `0001`)
   - Title (from `# RFC-NNN-<name>: Title`)
   - Status (from `**Status**: ...`)
   - Created date (from `**Created**: YYYY-MM-DD`)
   - Last Updated date (from `**Last Updated**: YYYY-MM-DD`)

3. **Collect Version Information**
   For each base RFC, find all versioned files:
   - Pattern: `RFC-NNN-<name>-<letter>.md` where NNN and <name> match the base RFC
   - Extract version numbers (<letter>)
   - Sort versions numerically

4. **Generate Active RFCs Table**
   Create a markdown table with columns:
   - RFC (link to file)
   - Title
   - Status
   - Created
   - Last Updated
   - Version (list of version links or "001" if no versions)

   Format:
   ```markdown
   | RFC | Title | Status | Created | Last Updated | Version |
   |-----|-------|--------|---------|--------------|---------|
   | [RFC-001-world-view](RFC-001-world-view.md) | Title | Draft | 2026-01-26 | 2026-01-28 | 001 |
   ```

5. **Generate Quick Links**
   Create a list of links to all base RFCs:
   ```markdown
   - [RFC-001-world-view: Title](RFC-001-world-view.md)
   - [RFC-002-message-queue: Another Title](RFC-002-message-queue.md)
   ```

6. **Update rfc-index.md**
   - Read existing `rfc-index.md`
   - Find section `## 2. Active RFCs`
   - Replace the table content (between header row and `---`) with generated table
   - Find section `## 5. Quick Links`
   - Replace content with generated quick links
   - Update `**Last Updated**:` field to today's date (YYYY-MM-DD)
   - Preserve all other sections unchanged

## Table Generation Rules

- **Sort RFCs** by RFC number (numerically, ascending)
- **RFC Column**: Format as `[RFC-NNN-<name>](RFC-NNN-<name>.md)` where NNN is zero-padded
- **Version Column**:
  - If versions exist: `[va](RFC-NNN-<name>-a.md), [vb](RFC-NNN-<name>-b.md)`
  - If no versions: `-` (no versions)
- **Status**: Use exact status from RFC metadata
- **Dates**: Use YYYY-MM-DD format

## Quick Links Rules

- Only include base RFCs (not versioned)
- Format: `- [RFC-NNN-<name>: Title](RFC-NNN-<name>.md)`
- Sort by RFC number (ascending)
- Use exact title from RFC

## Output Format

### Active RFCs Table

```markdown
## 2. Active RFCs

| RFC | Title | Status | Created | Last Updated | Version |
|-----|-------|--------|---------|--------------|---------|
| [RFC-001-world-view](RFC-001-world-view.md) | MizarAlpha World View | Review | 2026-01-26 | 2026-01-28 | 001 |
| [RFC-002-message-queue](RFC-002-message-queue.md) | Message Queue Protocol | Draft | 2026-01-27 | 2026-01-27 | [v001](RFC-002-message-queue-001.md), [v002](RFC-002-message-queue-002.md) |
```

### Quick Links

```markdown
## 5. Quick Links

- [RFC-001-world-view: MizarAlpha World View](RFC-001-world-view.md)
- [RFC-002-message-queue: Message Queue Protocol](RFC-002-message-queue.md)
```

## Verification

After updating, verify:

- All base RFCs are in the table
- Version links are correct
- Quick links match table entries
- Dates are in correct format
- No broken links
- RFCs are sorted correctly

## Notes

- Only include base RFCs in the main table (not versioned files)
- Version links should point to actual version files
- If an RFC has no title, use filename as fallback
- Exclude deprecated RFCs if Status is "Deprecated" (or include with status shown)
