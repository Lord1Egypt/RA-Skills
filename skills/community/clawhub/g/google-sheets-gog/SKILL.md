---
name: google-sheets-gog
description: Use this skill when you need to create, inspect, update, append to, or reorganize Google Sheets from a locally installed `gog` CLI. It is for local Google account auth and direct spreadsheet operations such as reading ranges, appending rows, updating cells, creating spreadsheets or tabs, and managing named ranges with confirmation before destructive changes.
homepage: https://github.com/steipete/gogcli
metadata: {"openclaw":{"emoji":"📊","homepage":"https://github.com/steipete/gogcli","skillKey":"gogSheets","requires":{"bins":["gog"],"config":["skills.entries.gogSheets.config.login","skills.entries.gogSheets.config.password"]},"install":[{"id":"brew","kind":"brew","formula":"gogcli","bins":["gog"],"label":"Install gog (Homebrew)"}]}}
---

# Google Sheets via gog

Use this skill to operate on Google Sheets through the local `gog` CLI instead of a hosted API bridge. It is intended for spreadsheet CRUD work on the user's own Google account with local OAuth.

## Prerequisites

- `gog` must be installed locally.
- OpenClaw only loads this skill when `skills.entries.gogSheets.config.login` and `skills.entries.gogSheets.config.password` are both set.
- The user must have a Google Cloud Desktop OAuth client JSON.
- The Google Sheets API must be enabled in that Google Cloud project.
- The agent should prefer the exact spreadsheet ID, tab name, and A1 range before running commands.

## OpenClaw Config

Use `gogSheets` as the OpenClaw config key:

```json5
{
  skills: {
    entries: {
      gogSheets: {
        enabled: true,
        config: {
          login: "you@gmail.com",
          password: "app-specific-or-local-secret"
        }
      }
    }
  }
}
```

`login` and `password` are load-time gating requirements for OpenClaw. They make the skill eligible to load, but the sheet operations below still use local `gog` OAuth unless you later add separate automation around those config values.

If you do not want to store raw secrets directly in `config`, prefer using `skills.entries.gogSheets.env` or `apiKey` alongside this config and keep prompts free of secrets.

## Setup

1. Store the OAuth client credentials:

```bash
gog auth credentials ~/Downloads/client_secret_....json
```

2. Authorize the account for Sheets:

```bash
gog auth add you@gmail.com --services sheets
```

3. If Sheets access is being added later to an existing account and Google does not return a refresh token, re-run with consent forced:

```bash
gog auth add you@gmail.com --services sheets --force-consent
```

4. Select the account for subsequent commands:

```bash
export GOG_ACCOUNT=you@gmail.com
```

Or pass `--account you@gmail.com` on each command.

## Working Rules

- Prefer `--json` for reads when the result will be parsed or summarized.
- Prefer precise spreadsheet IDs over titles.
- Prefer exact A1 ranges such as `Sheet1!A1:D20`.
- If a subcommand or flag is uncertain, inspect help with `gog sheets --help` or `gog <subcommand> --help` before executing.
- Keep commands scoped to Sheets by default. If sandboxing is needed, use `GOG_ENABLE_COMMANDS=sheets`.
- Remember that OpenClaw gating checks `gog` on the host at skill load time; sandboxed runs also need `gog` installed inside the container.
- For read-only inspection sessions, prefer re-auth with `--readonly` instead of assuming write scopes are acceptable.

## Safety Policy

Before any destructive or broad write, explicitly state:

- target spreadsheet ID
- target tab or named range
- exact range or object being changed
- operation being performed

Ask for confirmation before:

- `clear` on any range
- `find-replace` across a whole spreadsheet or large tab
- deleting tabs
- deleting named ranges
- broad formatting, merge, unmerge, resize, or freeze changes
- insert operations that shift existing rows or columns
- overwriting a large existing range with `update`

Direct reads and narrowly scoped appends or cell updates can proceed without a separate confirmation when the user request is already explicit.

## Common Tasks

### Read spreadsheet data

- Inspect metadata for spreadsheet structure.
- Read a specific A1 range.
- Read a named range when the spreadsheet already defines one.
- Use JSON output when the data will be transformed or summarized.

See [references/gog-sheets.md](references/gog-sheets.md) for command patterns.

### Create and extend spreadsheets

- Create a new spreadsheet with one or more tabs.
- Add a new tab to an existing spreadsheet.
- Rename a tab when requested.

### Update and append data

- Use `update` for direct cell or range replacement.
- Use `append` for new rows.
- If the sheet relies on data validation, preserve it with `--copy-validation-from` when appropriate.

### Organize structure

- Manage named ranges when the user refers to stable data blocks by name.
- Insert rows or columns only after checking whether data shifting is intended.
- Use formatting commands only when formatting itself is part of the task.

## Failure Handling

- If auth fails, verify credentials were stored with `gog auth credentials` and inspect account state with `gog auth status`.
- If a command fails due to insufficient scopes, re-auth with the needed service and `--force-consent`.
- If the spreadsheet target is ambiguous, stop and resolve the spreadsheet ID before mutating anything.
- If the requested operation may require broader Google access than Sheets alone, inspect `gog` help first rather than guessing.

## References

- Command examples: [references/gog-sheets.md](references/gog-sheets.md)
- Upstream docs: https://github.com/steipete/gogcli/blob/main/README.md
