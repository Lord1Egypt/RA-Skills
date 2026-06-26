---
name: google-drive-secured
description: Google Drive Secure Management. Use when the user wants to list, search, read text content, create files with inline content, upload binaries, create folders, rename, move, share, or manage permissions on Google Drive files (porteden secure alternative).
version: 1.0.8
metadata: {"openclaw":{"emoji":"📂","homepage":"https://porteden.com","requires":{"bins":["porteden"]},"primaryEnv":"PE_API_KEY","envVars":[{"name":"PE_API_KEY","required":false,"description":"API key; if unset, credentials are read from the system keyring via `porteden auth login`"}],"install":[{"id":"brew","kind":"brew","formula":"porteden/tap/porteden","bins":["porteden"],"label":"Install porteden (brew)"},{"id":"go","kind":"go","module":"github.com/porteden/cli/cmd/porteden@latest","bins":["porteden"],"label":"Install porteden (go)"}]}}
---

# porteden drive

Use `porteden drive` for Google Drive file and folder management. **Use `-jc` flags** for AI-optimized output.

If `porteden` is not installed: `brew install porteden/tap/porteden` (or `go install github.com/porteden/cli/cmd/porteden@latest`).

## Setup (once)

- **Browser login (recommended):** `porteden auth login` — opens browser, credentials stored in system keyring
- **Direct token:** `porteden auth login --token <key>` — stored in system keyring
- **Verify:** `porteden auth status`
- If `PE_API_KEY` is set in the environment, the CLI uses it automatically (no login needed).
- Drive access requires a token with `driveAccessEnabled: true` and a connected Google account with Drive scopes.

## Drive commands (`porteden drive`)

### List & inspect

- List files: `porteden drive files -jc`
- Search by keyword: `porteden drive files -q "budget report" -jc`
- Filter by folder: `porteden drive files --folder google:0B7_FOLDER_ID -jc`
- Filter by MIME type: `porteden drive files --mime-type application/pdf -jc`
- Filter by name: `porteden drive files --name "Q1" -jc`
- Shared with me: `porteden drive files --shared-with-me -jc`
- Modified in range: `porteden drive files --modified-after 2026-01-01 --modified-before 2026-02-01 -jc`
- All files (auto-paginate): `porteden drive files --all -jc`
- Get file metadata: `porteden drive file google:FILEID -jc`
- Get view/download links: `porteden drive download google:FILEID -jc`
- List permissions: `porteden drive permissions google:FILEID -jc`

### Read content

- Read text content of any file: `porteden drive content google:FILEID`
  - Google Docs export to `text/plain` inline
  - Text-like files (text/\*, JSON, XML, YAML, CSV) return as-is
  - Binary files return a `webViewLink` — open in browser
  - Spreadsheets/presentations are steered to: `porteden sheets content` / `porteden slides read`

### Create & upload

- Create file with inline content: `porteden drive create --name "Notes.md" --mime-type text/markdown --content "# Notes"`
- Create from local text file: `porteden drive create --name "Plan" --mime-type application/vnd.google-apps.document --content-file ./plan.md --content-mime-type text/markdown`
- Create CSV file: `porteden drive create --name "Data.csv" --mime-type text/csv --content-file ./data.csv`
- Upload binary file: `porteden drive upload --file ./report.pdf --name "Q1 Report.pdf"`
- Upload to folder: `porteden drive upload --file ./data.csv --name "Data.csv" --folder google:0B7_FOLDER`
- Create folder: `porteden drive mkdir --name "Project Files"`
- Create folder in folder: `porteden drive mkdir --name "Reports" --parent google:0B7_FOLDER`

### Manage

- Rename: `porteden drive rename google:FILEID --name "New Name.pdf"`
- Move: `porteden drive move google:FILEID --destination google:0B7_DEST_FOLDER`
- Share with user: `porteden drive share google:FILEID --type user --role reader --email user@example.com`
- Share with domain: `porteden drive share google:FILEID --type domain --role reader --domain example.com`
- Share publicly: `porteden drive share google:FILEID --type anyone --role reader`
- Delete (trash): `porteden drive delete google:FILEID` (prompts) or `porteden drive delete google:FILEID -y`

## Notes

- Credentials persist in the system keyring after login. No repeated auth needed.
- Set `PE_PROFILE=work` to avoid repeating `--profile`.
- `-jc` is shorthand for `--json --compact`: strips noise, limits fields, reduces tokens for AI agents.
- **File IDs are always provider-prefixed** (e.g., `google:1BxiMVs0XRA5...`). Pass them as-is.
- `porteden drive files --all` auto-paginates (safety cap: 50 pages). Check `hasMore` in JSON output.
- `porteden drive download` returns **URLs only** — no binary content is streamed.
- `porteden drive content` is the **universal text reader** — use it instead of `download` when you need the textual content of a file. For Google Workspace types (Sheets, Slides) it steers to the dedicated commands (`porteden sheets content`, `porteden slides read`) via stderr hints.
- `porteden drive create` uses **inline JSON** (UTF-8 text only, ≤ 10 MB). For binary content use `porteden drive upload`. For Workspace target MIME types (`application/vnd.google-apps.{document,spreadsheet,presentation}`) Drive auto-imports the content; otherwise the file is stored as-is.
- `accessInfo` in responses describes active token restrictions. Always check it to understand what data may be limited.
- `authWarnings` in list responses indicate provider connection issues.
- `delete` moves to trash (reversible). Files can be restored from Google Drive trash.
- Confirm before sharing or deleting files.
- Environment variables: `PE_API_KEY`, `PE_PROFILE`, `PE_FORMAT`, `PE_COLOR`, `PE_VERBOSE`.
