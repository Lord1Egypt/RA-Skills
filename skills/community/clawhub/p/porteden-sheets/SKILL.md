---
name: porteden-sheets
description: Secure Google Sheets Management - permission-based create, read, write, and append spreadsheet data, plus file management (share, permissions, rename, delete).
homepage: https://porteden.com
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["porteden"],"env":["PE_API_KEY"]},"primaryEnv":"PE_API_KEY","install":[{"id":"brew","kind":"brew","formula":"porteden/tap/porteden","bins":["porteden"],"label":"Install porteden (brew)"},{"id":"go","kind":"go","module":"github.com/porteden/cli/cmd/porteden@latest","bins":["porteden"],"label":"Install porteden (go)"}]}}
---

# porteden sheets

Use `porteden sheets` for Google Sheets data operations and file management. **Use `-jc` flags** for AI-optimized output.

If `porteden` is not installed: `brew install porteden/tap/porteden` (or `go install github.com/porteden/cli/cmd/porteden@latest`).

Setup (once)

- **Browser login (recommended):** `porteden auth login` — opens browser, credentials stored in system keyring
- **Direct token:** `porteden auth login --token <key>` — stored in system keyring
- **Verify:** `porteden auth status`
- If `PE_API_KEY` is set in the environment, the CLI uses it automatically (no login needed).
- Drive access requires a token with `driveAccessEnabled: true` and a connected Google account with Drive scopes.

## Sheets commands (`porteden sheets`)

### Data operations

- Create new spreadsheet: `porteden sheets create --name "Q1 Budget"`
- Create in folder: `porteden sheets create --name "Data" --folder google:0B7_FOLDER`
- Spreadsheet metadata (tabs, dimensions): `porteden sheets info google:SHEETID -jc`
- Read cell range: `porteden sheets read google:SHEETID --range "Sheet1!A1:C10" -jc`
- Read whole sheet: `porteden sheets read google:SHEETID --range "Sheet1" -jc`
- Write cells (JSON): `porteden sheets write google:SHEETID --range "Sheet1!A1:B2" --values '[["Name","Score"],["Alice",95]]'`
- Write cells (CSV string): `porteden sheets write google:SHEETID --range "Sheet1!A1:B2" --csv "Name,Score\nAlice,95"`
- Write cells (CSV file): `porteden sheets write google:SHEETID --range "Sheet1!A1" --csv-file ./data.csv`
- Append rows (JSON): `porteden sheets append google:SHEETID --range "Sheet1!A:B" --values '[["Bob",87]]'`
- Append rows (CSV): `porteden sheets append google:SHEETID --range "Sheet1!A:B" --csv "Bob,87"`

### File management

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
- `--values`, `--csv`, and `--csv-file` are mutually exclusive — provide exactly one.
- `--csv` inline: use `\n` as row separator (e.g., `"Name,Score\nAlice,95\nBob,87"`).
- `--raw` flag disables formula evaluation (values written literally, not parsed as formulas).
- `porteden sheets download` returns **URLs only** — no binary content is streamed.
- `accessInfo` in responses describes active token restrictions.
- `delete` moves to trash (reversible). Files can be restored from Google Drive trash.
- Confirm before sharing or deleting.
- Environment variables: `PE_API_KEY`, `PE_PROFILE`, `PE_FORMAT`, `PE_COLOR`, `PE_VERBOSE`.
