---
name: porteden-sheets
description: Google Sheets Secure Management. Use when the user wants to create, read, write, or append spreadsheet data; manage tabs (read/add/delete); copy spreadsheets; or manage sharing, permissions, renames, and deletes.
version: 1.0.8
metadata: {"openclaw":{"emoji":"📊","homepage":"https://porteden.com","requires":{"bins":["porteden"]},"primaryEnv":"PE_API_KEY","envVars":[{"name":"PE_API_KEY","required":false,"description":"API key; if unset, credentials are read from the system keyring via `porteden auth login`"}],"install":[{"id":"brew","kind":"brew","formula":"porteden/tap/porteden","bins":["porteden"],"label":"Install porteden (brew)"},{"id":"go","kind":"go","module":"github.com/porteden/cli/cmd/porteden@latest","bins":["porteden"],"label":"Install porteden (go)"}]}}
---

# porteden sheets

Use `porteden sheets` for Google Sheets data operations and file management. **Use `-jc` flags** for AI-optimized output.

If `porteden` is not installed: `brew install porteden/tap/porteden` (or `go install github.com/porteden/cli/cmd/porteden@latest`).

## Setup (once)

- **Browser login (recommended):** `porteden auth login` — opens browser, credentials stored in system keyring
- **Direct token:** `porteden auth login --token <key>` — stored in system keyring
- **Verify:** `porteden auth status`
- If `PE_API_KEY` is set in the environment, the CLI uses it automatically (no login needed).
- Drive access requires a token with `driveAccessEnabled: true` and a connected Google account with Drive scopes.

## Sheets commands (`porteden sheets`)

### Data operations

- Create new spreadsheet (blank): `porteden sheets create --name "Q1 Budget"`
- Create in folder: `porteden sheets create --name "Data" --folder google:0B7_FOLDER`
- Create seeded with CSV: `porteden sheets create --name "Sales 2026" --csv-file ./sales.csv`
- Create seeded with inline CSV: `porteden sheets create --name "Data" --csv "Name,Score\nAlice,95"`
- Spreadsheet metadata (tabs, dimensions): `porteden sheets info google:SHEETID -jc`
- Read all tabs at once (best for AI agents — single upstream call): `porteden sheets content google:SHEETID -jc`
- Read all tabs with row cap: `porteden sheets content google:SHEETID --max-rows 500 -jc`
- Read specific ranges (no per-tab cap): `porteden sheets content google:SHEETID --ranges "Summary!A1:C100,Raw Data!A:Z" -jc`
- Read cell range (single range): `porteden sheets read google:SHEETID --range "Sheet1!A1:C10" -jc`
- Read whole sheet (single tab): `porteden sheets read google:SHEETID --range "Sheet1" -jc`
- Write cells (JSON): `porteden sheets write google:SHEETID --range "Sheet1!A1:B2" --values '[["Name","Score"],["Alice",95]]'`
- Write cells (CSV string): `porteden sheets write google:SHEETID --range "Sheet1!A1:B2" --csv "Name,Score\nAlice,95"`
- Write cells (CSV file): `porteden sheets write google:SHEETID --range "Sheet1!A1" --csv-file ./data.csv`
- Batch write multiple ranges (one atomic call): `porteden sheets write google:SHEETID --updates '[{"range":"Summary!A1:B1","values":[["Metric","Value"]]},{"range":"Detail!A1","values":[["x"]]}]'`
- Append rows (JSON): `porteden sheets append google:SHEETID --range "Sheet1!A:B" --values '[["Bob",87]]'`
- Append rows (CSV): `porteden sheets append google:SHEETID --range "Sheet1!A:B" --csv "Bob,87"`

### Tab management

- Read one tab in full (single call, no A1 range to compute): `porteden sheets read-tab google:SHEETID --title "Q2 Forecast" -jc`
- Read tab by numeric id: `porteden sheets read-tab google:SHEETID --sheet-id 0 -jc`
- Add a tab: `porteden sheets add-tab google:SHEETID --title "Q2 Forecast"`
- Add a tab with dimensions/position: `porteden sheets add-tab google:SHEETID --title "Q2 Forecast" --rows 200 --cols 12 --index 2`
- Delete a tab by title: `porteden sheets delete-tab google:SHEETID --title "Q2 Forecast" -y`
- Delete a tab by id: `porteden sheets delete-tab google:SHEETID --sheet-id 1843502915 -y`

### File management

- Copy (duplicate) the spreadsheet: `porteden sheets copy google:SHEETID --name "Q2 Forecast (copy)"`
- Copy into a folder: `porteden sheets copy google:SHEETID --folder google:0B7_FOLDER`

- Get export links (xlsx, pdf, csv): `porteden sheets download google:SHEETID -jc`
- Share: `porteden sheets share google:SHEETID --type user --role writer --email user@example.com`
- Share publicly: `porteden sheets share google:SHEETID --type anyone --role reader`
- List permissions: `porteden sheets permissions google:SHEETID -jc`
- Rename: `porteden sheets rename google:SHEETID --name "Q2 Budget"`
- Delete (trash): `porteden sheets delete google:SHEETID -y`

## Range format

- Full range: `Sheet1!A1:C10`
- Whole sheet: `Sheet1`
- Open-ended (for append): `Sheet1!A:B`

## Notes

- Credentials persist in the system keyring after login. No repeated auth needed.
- Set `PE_PROFILE=work` to avoid repeating `--profile`.
- `-jc` is shorthand for `--json --compact`: strips noise, limits fields, reduces tokens for AI agents.
- **File IDs are always provider-prefixed** (e.g., `google:1BxiMVs0XRA5...`). Pass them as-is.
- **Prefer `porteden sheets content` over multiple `porteden sheets read` calls** when you need more than one tab — it returns every tab in a single upstream call.
- `porteden sheets content` is **capped at 200 rows × 26 columns per tab by default**. Tabs with more data come back marked `clipped: true` with a `fullRange` string you can feed straight into `porteden sheets read --range <fullRange>` to drill in. Use `--max-rows 5000` to raise the cap, or `--ranges` to pass explicit A1 ranges with no cap.
- `porteden sheets create` accepts optional `--csv`/`--csv-file` to seed the first tab. Without them a blank spreadsheet is created. Both flags are mutually exclusive.
- **CSV-seeded spreadsheets get a tab named after the file, not `Sheet1`.** When Drive imports CSV the resulting tab takes the file's name (e.g., `--name "Q1 Numbers"` → tab title `Q1 Numbers`). Range examples below default to `Sheet1!...` which only works on truly blank spreadsheets created via the Google Sheets UI. For CSV-seeded sheets, first call `porteden sheets info <id> -jc` to discover the actual tab names, then quote them in your range: `'Q1 Numbers'!A1:C10`.
- On `sheets write` / `sheets append`: `--values`, `--csv`, and `--csv-file` are mutually exclusive — provide exactly one.
- **Batch write** (`sheets write --updates`): a JSON array of `{"range","values"}` objects, written in **one atomic call** (a bad range fails the whole batch — no partial writes). Up to **50 ranges / 50,000 cells**. `--updates` is mutually exclusive with `--range`/`--values`/`--csv`/`--csv-file`; `--raw` still applies request-wide. Prefer it over multiple `sheets write` calls when populating several tabs/ranges at once.
- `sheets read-tab` and `sheets delete-tab` take **exactly one** of `--title` or `--sheet-id`. `--sheet-id 0` is valid (the first tab is often sheetId 0). `read-tab` returns the tab's entire used range — no A1 range needed. `add-tab` returns the new tab's `sheetId`; titles must be unique within the spreadsheet.
- `sheets copy` duplicates the whole spreadsheet (not idempotent — calling twice makes two copies) and returns the new file's id. It's a wrapper over `drive copy`.
- `--csv` inline: use `\n` as row separator (e.g., `"Name,Score\nAlice,95\nBob,87"`).
- `--raw` flag disables formula evaluation (values written literally, not parsed as formulas).
- `porteden sheets download` returns **URLs only** — no binary content is streamed.
- `accessInfo` in responses describes active token restrictions.
- `delete` moves to trash (reversible). Files can be restored from Google Drive trash.
- Confirm before sharing or deleting.
- Environment variables: `PE_API_KEY`, `PE_PROFILE`, `PE_FORMAT`, `PE_COLOR`, `PE_VERBOSE`.
