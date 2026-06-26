---
name: porteden-docs
description: Secure Google Docs Management - permission-based create, read, and edit doc content; manage sharing, permissions, rename and delete.
homepage: https://porteden.com
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["porteden"],"env":["PE_API_KEY"]},"primaryEnv":"PE_API_KEY","install":[{"id":"brew","kind":"brew","formula":"porteden/tap/porteden","bins":["porteden"],"label":"Install porteden (brew)"},{"id":"go","kind":"go","module":"github.com/porteden/cli/cmd/porteden@latest","bins":["porteden"],"label":"Install porteden (go)"}]}}
---

# porteden docs

Use `porteden docs` for Google Docs content operations and file management. **Use `-jc` flags** for AI-optimized output.

If `porteden` is not installed: `brew install porteden/tap/porteden` (or `go install github.com/porteden/cli/cmd/porteden@latest`).

Setup (once)

- **Browser login (recommended):** `porteden auth login` — opens browser, credentials stored in system keyring
- **Direct token:** `porteden auth login --token <key>` — stored in system keyring
- **Verify:** `porteden auth status`
- If `PE_API_KEY` is set in the environment, the CLI uses it automatically (no login needed).
- Drive access requires a token with `driveAccessEnabled: true` and a connected Google account with Drive scopes.

## Docs commands (`porteden docs`)

### Content

- Create new doc: `porteden docs create --name "Meeting Notes"`
- Create in folder: `porteden docs create --name "Brief" --folder google:0B7_FOLDER`
- Read content (plain text): `porteden docs read google:DOCID`
- Read structured (full Google Docs API JSON): `porteden docs read google:DOCID --format structured -j`
- Append text: `porteden docs edit google:DOCID --append "New paragraph."`
- Insert at start: `porteden docs edit google:DOCID --insert "Header text" --at 1`
- Find and replace: `porteden docs edit google:DOCID --find "old text" --replace "new text"`
- Multiple replacements: `porteden docs edit google:DOCID --find "foo" --replace "bar" --find "baz" --replace "qux"`
- Bulk ops from file: `porteden docs edit google:DOCID --ops-file ./ops.json`

### File management

- Get export links (pdf, docx, txt): `porteden docs download google:DOCID -jc`
- Share: `porteden docs share google:DOCID --type user --role writer --email user@example.com`
- Share publicly: `porteden docs share google:DOCID --type anyone --role reader`
- List permissions: `porteden docs permissions google:DOCID -jc`
- Rename: `porteden docs rename google:DOCID --name "New Title"`
- Delete (trash): `porteden docs delete google:DOCID -y`

## Ops file format

`--ops-file` accepts a JSON array of operations:

```json
[
  {"type": "appendText", "text": "New paragraph at end."},
  {"type": "insertText", "text": "Header", "index": 1},
  {"type": "replaceText", "find": "old phrase", "replace": "new phrase", "matchCase": true}
]
```

## Notes

- Credentials persist in the system keyring after login. No repeated auth needed.
- Set `PE_PROFILE=work` to avoid repeating `--profile`.
- `-jc` is shorthand for `--json --compact`: strips noise, limits fields, reduces tokens for AI agents.
- **File IDs are always provider-prefixed** (e.g., `google:1BxiMVs0XRA5...`). Pass them as-is.
- `porteden docs read` returns plain text by default; use `--format structured` for full API JSON with headings and formatting.
- `--find` and `--replace` are repeatable and must be used in matched pairs. `--ops-file` is mutually exclusive with inline edit flags.
- `porteden docs download` returns **URLs only** — no binary content is streamed.
- `accessInfo` in responses describes active token restrictions.
- `delete` moves to trash (reversible). Files can be restored from Google Drive trash.
- Confirm before sharing or deleting.
- Environment variables: `PE_API_KEY`, `PE_PROFILE`, `PE_FORMAT`, `PE_COLOR`, `PE_VERBOSE`.
