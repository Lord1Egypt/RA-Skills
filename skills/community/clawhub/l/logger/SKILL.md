---
name: logger
description: Google Sheets Log Automation. Use when the user wants to append log entries, record audit trails, or automate event logging to a pre-configured Google Sheet (PortEden Secure access).
version: 1.0.8
metadata: {"openclaw":{"emoji":"📋","homepage":"https://porteden.com","requires":{"bins":["porteden"]},"primaryEnv":"PE_API_KEY","envVars":[{"name":"PE_API_KEY","required":false,"description":"API key; if unset, credentials are read from the system keyring via `porteden auth login`"},{"name":"PE_SHEET_ID","required":false,"description":"Target spreadsheet ID; if unset, the skill finds the sheet by name (see body)"}],"install":[{"id":"brew","kind":"brew","formula":"porteden/tap/porteden","bins":["porteden"],"label":"Install porteden (brew)"},{"id":"go","kind":"go","module":"github.com/porteden/cli/cmd/porteden@latest","bins":["porteden"],"label":"Install porteden (go)"}]}}
---

# porteden sheets-logger

Append log entries to a Google Sheet with `porteden sheets`. This skill configures a **target log spreadsheet** via environment variable so agents can record events, activity logs, and audit trails without repeating the file ID. **Use `-jc` flags** for AI-optimized output.

If `porteden` is not installed: `brew install porteden/tap/porteden` (or `go install github.com/porteden/cli/cmd/porteden@latest`).

## Setup

### 1. Authenticate (once)

- **Browser login (recommended):** `porteden auth login` — opens browser, credentials stored in system keyring
- **Direct token:** `porteden auth login --token <key>` — stored in system keyring
- **Verify:** `porteden auth status`
- If `PE_API_KEY` is set in the environment, the CLI uses it automatically (no login needed).
- Drive access requires a token with `driveAccessEnabled: true` and a connected Google account with Drive scopes.

### 2. Set the target log sheet (one-time)

**If `PE_SHEET_ID` is already set**, skip to step 3 — the target sheet is configured.

**If `PE_SHEET_ID` is not set**, find the spreadsheet by name:

```bash
porteden drive files -q "Activity Log" --mime-type application/vnd.google-apps.spreadsheet -jc
```

Copy the `id` field from the result (already provider-prefixed, e.g., `google:1BxiMVs0XRA5...`) and set it:

```bash
export PE_SHEET_ID="google:1BxiMVs0XRA5nFMdKvBdBZjgmU..."
```

To persist across sessions, add to your shell profile (`~/.bashrc`, `~/.zshrc`) or `.env` file. Once set, this step does not need to be repeated.

### 3. Test the connection (one-time)

```bash
porteden sheets info $PE_SHEET_ID -jc
```

Expected: returns spreadsheet title, sheet tabs, and dimensions. If this fails, verify the file ID and that your token has Drive access. Once verified, skip this step in future runs.

### 4. Read the header row (one-time)

Before logging, confirm the column layout of the target sheet:

```bash
porteden sheets read $PE_SHEET_ID --range "Sheet1!1:1" -jc
```

Match your log entries to this column order. Once you know the schema, skip this step in future runs.

## Logging data

### Append a log entry

Append adds rows **after the last row with data**. Existing log entries are never overwritten.

- Single log entry:
  ```bash
  porteden sheets append $PE_SHEET_ID --range "Sheet1!A:E" --values '[["2025-01-15T09:30:00Z","deploy","production","v2.4.1 released","success"]]'
  ```

- Multiple log entries (batch):
  ```bash
  porteden sheets append $PE_SHEET_ID --range "Sheet1!A:E" --values '[["2025-01-15T09:30:00Z","deploy","production","v2.4.1 released","success"],["2025-01-15T09:31:12Z","healthcheck","production","all endpoints healthy","success"]]'
  ```

- Log entry from CSV string:
  ```bash
  porteden sheets append $PE_SHEET_ID --range "Sheet1!A:E" --csv "2025-01-15T09:30:00Z,deploy,production,v2.4.1 released,success"
  ```

- Bulk log import from CSV file:
  ```bash
  porteden sheets append $PE_SHEET_ID --range "Sheet1!A:E" --csv-file ./events.csv
  ```

### Verify logged entries

Read back recent rows to confirm the log was recorded:

```bash
porteden sheets read $PE_SHEET_ID --range "Sheet1" -jc
```

## Log schema examples

Structure your log sheet with a header row. Common schemas:

**Event log:** `Timestamp | Event | Source | Details | Status`

**Audit trail:** `Timestamp | Actor | Action | Resource | Before | After`

**Error log:** `Timestamp | Severity | Service | Message | Stack`

**Task log:** `Timestamp | Task | Agent | Input | Output | Duration`

## Best practices

1. **Always use append** — logging is append-only by nature. Never use write to overwrite log entries.
2. **Include a timestamp in every entry** — use ISO 8601 format (`2025-01-15T09:30:00Z`) for sortability and consistency.
3. **Use `--raw` for literal values** — prevents unintended formula evaluation (e.g., log messages starting with `=`).
4. **Batch entries when possible** — send multiple rows in one `--values` array rather than one-row-at-a-time to reduce API calls.
5. **Specify column range in append** (e.g., `A:E` not just `A`) — ensures data lands in the correct columns.
6. **Read the header row first** — confirm column order with `porteden sheets read $PE_SHEET_ID --range "Sheet1!1:1" -jc` before appending.
7. **Use `-jc` on read/info** — compact JSON output minimizes tokens for AI agents.

## Range format

- Open-ended columns (for append): `Sheet1!A:E`
- Specific cells: `Sheet1!A1:E10`
- Whole sheet: `Sheet1`
- Header row only: `Sheet1!1:1`

## Notes

- Credentials persist in the system keyring after login. No repeated auth needed.
- Set `PE_PROFILE=work` to avoid repeating `--profile`.
- `-jc` is shorthand for `--json --compact`: strips noise, limits fields, reduces tokens for AI agents.
- **File IDs are always provider-prefixed** (e.g., `google:1BxiMVs0XRA5...`). Pass them as-is.
- `--values`, `--csv`, and `--csv-file` are mutually exclusive — provide exactly one.
- `--csv` inline: use `\n` as row separator (e.g., `"ts,event,src\nts2,event2,src2"`).
- `--raw` flag disables formula evaluation (values written literally, not parsed as formulas).
- `accessInfo` in responses describes active token restrictions.
- Environment variables: `PE_API_KEY`, `PE_PROFILE`, `PE_SHEET_ID`, `PE_FORMAT`, `PE_COLOR`, `PE_VERBOSE`.
