# Generate History

## Objective

Scan all RFC files in the specs directory and generate/update `rfc-history.md` with chronological lifecycle events.

## Inputs

- **Specs Directory**: Path to the specs directory

## Steps

1. **Scan RFC Files**
   - Find all files matching pattern `RFC-*.md` in the specs directory
   - Exclude: `rfc-history.md`, `rfc-index.md`, `rfc-namings.md`, `rfc-standard.md`
   - Include both base RFCs (e.g., `RFC-001-world-view.md`) and versioned RFCs (e.g., `RFC-001-world-view-001.md`)

2. **Extract Metadata from Each RFC**
   For each RFC file, extract:
   - RFC number (from filename or title)
   - Title (from `# RFC-NNN-<name>: Title`)
   - Status (from `**Status**: ...`)
   - Created date (from `**Created**: YYYY-MM-DD`)
   - Last Updated date (from `**Last Updated**: YYYY-MM-DD`)
   - Version number (if versioned RFC, from filename `RFC-NNN-<name>-<letter>.md`)

3. **Categorize Events**
   For each RFC, create events:
   - **Created**: When RFC was created (use Created date)
   - **Updated**: When RFC was last updated (if different from Created date, and not versioned)
   - **Version Released**: When a versioned RFC was created (for versioned RFCs)

4. **Group Events by Date**
   - Group all events by date (YYYY-MM-DD)
   - Sort dates in descending order (most recent first)

5. **Generate History Content**
   Format each date section as:
   ```markdown
   ### YYYY-MM-DD
   - **Created**: RFC-NNN-<name> - Title
   - **Updated**: RFC-NNN-<name> - Title
   - **Version Released**: RFC-NNN-<name> version <letter> - RFC-NNN-<name>-<letter>.md
   ```

6. **Update rfc-history.md**
   - Read existing `rfc-history.md`
   - Find the section `## 3. Change History`
   - Replace content between `## 3. Change History` and `## 4.` with generated content
   - Update `**Last Updated**:` field to today's date (YYYY-MM-DD)
   - Preserve all other sections unchanged

## Event Detection Rules

- **Created Event**: Always record when `Created` date exists
- **Updated Event**: Only record if `Last Updated` differs from `Created` AND RFC is not versioned
- **Version Released Event**: Record for all versioned RFC files (RFC-NNN-<name>-<letter>.md format)

## Date Format

- Use YYYY-MM-DD format consistently
- Sort dates in descending order (newest first)
- Group multiple events on the same date together

## Output Format

The generated history section should follow this structure:

```markdown
## 3. Change History

### 2026-01-28
- **Created**: RFC-001 - Title of RFC
- **Updated**: RFC-002 - Another RFC Title
- **Version Released**: RFC-001 version 001 - RFC-001-001.md

### 2026-01-27
- **Created**: RFC-002 - Another RFC Title
```

## Verification

After updating, verify:

- All RFC files are represented in the history
- Dates are in correct format and sorted
- No duplicate events
- Version releases are properly recorded
- Last Updated date is current

## Notes

- Only include active RFCs (exclude deprecated ones if Status is "Deprecated")
- Preserve existing history entries if they're manually maintained
- If an RFC has no Created date, skip it or use file modification date as fallback
