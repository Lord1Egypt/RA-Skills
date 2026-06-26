# Miro CLI Scripts Reference

Helper scripts for common Miro CLI workflows.

## export-team-boards.sh

Export all boards from a team as PDF, PNG, or SVG files.

**Usage:**
```bash
./scripts/export-team-boards.sh <team-id> [output-dir] [format]
```

**Arguments:**
- `team-id` (required) — The Miro team ID
- `output-dir` (optional) — Directory to save files (default: current directory)
- `format` (optional) — Export format: pdf, png, or svg (default: pdf)

**Examples:**
```bash
# Export all boards from team as PDF
./scripts/export-team-boards.sh abc123def456

# Export to custom directory
./scripts/export-team-boards.sh abc123def456 ~/exports

# Export as PNG
./scripts/export-team-boards.sh abc123def456 ~/exports png

# Export as SVG
./scripts/export-team-boards.sh abc123def456 ~/exports svg
```

**Output:**
- Creates files named: `{board-name}_{board-id}.{format}`
- Shows progress: `[1/10] Exporting: Design System`
- Summary at end with output directory

**Features:**
- Sanitizes board names for safe filenames
- Shows progress counter
- Handles errors gracefully
- Creates output directory if needed

---

## list-boards-detailed.sh

List boards with detailed information in various formats.

**Usage:**
```bash
./scripts/list-boards-detailed.sh [format]
```

**Formats:**
- `table` (default) — Readable table with columns: Name, Owner, Board ID
- `json` — Full JSON output
- `csv` — CSV format (importable to spreadsheet)
- `owners` — Board count grouped by owner
- `teams` — Board count grouped by team

**Examples:**
```bash
# Show boards in table format (default)
./scripts/list-boards-detailed.sh
./scripts/list-boards-detailed.sh table

# Output as JSON (for scripting)
./scripts/list-boards-detailed.sh json

# Export to CSV for spreadsheet
./scripts/list-boards-detailed.sh csv > boards.csv

# Analyze by owner
./scripts/list-boards-detailed.sh owners

# Analyze by team
./scripts/list-boards-detailed.sh teams
```

**Output Examples:**

**Table format:**
```
BOARD NAME                     OWNER              BOARD ID
Design System                  Alice Smith        abc123def456
Q1 Roadmap                     Bob Jones          ghi789jkl012
Product Backlog                Charlie Brown      mno345pqr678
```

**Owners format:**
```
📊 Board Count by Owner

5 boards | Alice Smith
3 boards | Bob Jones
2 boards | Charlie Brown
```

**CSV format:**
```
Board Name,Owner,Team ID,Board ID,Created,Modified
Design System,Alice Smith,team1,abc123def456,...,...
Q1 Roadmap,Bob Jones,team2,ghi789jkl012,...,...
```

---

## Common Patterns

### Export all boards from your organization
```bash
# Get all team IDs first
mirocli teams list --json | jq -r '.[] | .id' | while read TEAM_ID; do
  ./scripts/export-team-boards.sh "$TEAM_ID" ~/exports
done
```

### Find and export specific boards
```bash
# Export boards matching a name pattern
mirocli boards list --json | jq -r '.[] | select(.name | contains("Design")) | .id' | while read BOARD_ID; do
  mirocli board-export "$BOARD_ID" --format pdf
done
```

### Generate board inventory report
```bash
# CSV report with all board details
./scripts/list-boards-detailed.sh csv > board-inventory-$(date +%Y%m%d).csv
```

---

## Requirements

**Required Binaries:**
- `mirocli` — Miro CLI tool (installed via `npm install -g mirocli`)
- `bash` — Bash shell interpreter
- `jq` — JSON query processor (for filtering; usually pre-installed on macOS)
- `column` — Text column formatter (standard on macOS/Linux)

**Prerequisites:**
- mirocli context configured: `mirocli context add`
- mirocli authenticated: `mirocli auth login`
- Credentials stored in system keyring (handled by mirocli, not by scripts)

## Tips

1. **Run script with full path (safest):**
   ```bash
   ~/.openclaw/workspace/skills/miro-cli/scripts/export-team-boards.sh abc123
   ```

2. **Add to PATH (optional, only if you understand PATH modification):**
   ```bash
   # This adds the scripts directory to your PATH
   # Only do this if you understand what PATH does
   export PATH="$PATH:$HOME/.openclaw/workspace/skills/miro-cli/scripts"
   
   # Then you can run:
   export-team-boards.sh abc123
   ```
   ⚠️ **Warning:** Modifying PATH can affect how your shell finds commands. Only add this if you understand the implications.

3. **Pipe to other commands:**
   ```bash
   # Count boards
   ./scripts/list-boards-detailed.sh json | jq 'length'
   
   # Find oldest board
   ./scripts/list-boards-detailed.sh json | jq 'sort_by(.created_at) | first'
   ```

4. **Run from anywhere without PATH modification:**
   ```bash
   # Use full path
   /Users/you/.openclaw/workspace/skills/miro-cli/scripts/export-team-boards.sh abc123
   
   # Or create an alias
   alias export-team-boards='~/.openclaw/workspace/skills/miro-cli/scripts/export-team-boards.sh'
   ```
