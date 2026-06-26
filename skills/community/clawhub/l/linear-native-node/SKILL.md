---
name: linear-native-node
description: Direct Linear workspace helper using Linear's GraphQL API from native Node.js. Use when creating, listing, updating, commenting on, summarizing, or looking up Linear issues, projects, teams, workflow states, priorities, standup notes, or branch names. Can write to Linear via create/comment/status/priority/project-create commands. Reads LINEAR_API_KEY from the process environment only; no OAuth gateway, bash, Python, npm dependencies, or third-party service.
version: 1.0.15
risk_class: external-api-read-write-gated
---

# Linear Native Node

Version: 1.0.15 / publishable utility.

Use `scripts/linear.mjs` to talk directly to Linear's GraphQL API at `https://api.linear.app/graphql`.

Native Node 18+. Zero npm dependencies. Windows, macOS, and Linux friendly. No bash, Python, OAuth gateway, browser login, or third-party proxy.

## Security behavior

- Reads `LINEAR_API_KEY` and optional `LINEAR_DEFAULT_TEAM` from the process environment only.
- Does not read credential files or `~/.openclaw/.env`.
- Sends GraphQL requests only to `https://api.linear.app/graphql`.
- Does not write local files, log secrets, or print the API key.
- Linear personal API keys inherit the permissions of the user/account that created them. Treat output as workspace-sensitive; use the least-privileged key model Linear offers if scoped keys become available.
- Read-only commands are the default usage pattern.
- Write commands are explicit commands (`create`, `comment`, `status`, `priority`, `project-create`) and are fail-closed by default: the script exits unless `--execute` is present after explicit user approval for that specific Linear mutation.
- `--execute` is only a script-level flag gate. Mutation appropriateness is enforced by the operator/agent approval policy: do not run a write unless the current user instruction or approval names the Linear action, target, and intended mutation.
- Static-analysis note: env-var + network-send warnings are expected for this skill because it uses a named API key to call Linear's fixed GraphQL endpoint. Treat any broad env enumeration, dynamic endpoint, or key-printing behavior as a blocker.
- Read command output may include workspace names, user names, emails, issue titles, issue descriptions, and URLs from the connected Linear workspace. Redact that content before sharing logs or examples externally.


## Why this skill

This is the direct/local version of common Linear helper workflows:

- Keeps API access between this machine and Linear only.
- Uses `LINEAR_API_KEY` from the process environment only; never print the key.
- Avoids bash-oriented helpers that break on Windows.
- Avoids third-party OAuth/gateway tools or intermediary services.
- Keeps a tight auditable scope: viewer/org/team lookup, issue list/read/create/update/comment, practical personal summaries, and branch names.

## Setup

Create a Linear API key at:

```text
https://linear.app/settings/api
```

PowerShell session-only setup:

```powershell
$env:LINEAR_API_KEY = "<your-linear-key>"
$env:LINEAR_DEFAULT_TEAM = "TEAM"
```

macOS/Linux shell session-only setup:

```bash
export LINEAR_API_KEY="<your-linear-key>"
export LINEAR_DEFAULT_TEAM="TEAM"
```
`LINEAR_DEFAULT_TEAM` is optional. Examples below use `TEAM` and `TEAM-123` as placeholders; replace them with your Linear team key and issue identifiers.

## Run

From PowerShell, bash, zsh, or any shell with Node on PATH:

```bash
node "<skill-dir>/scripts/linear.mjs" help
node "<skill-dir>/scripts/linear.mjs" viewer
node "<skill-dir>/scripts/linear.mjs" issues --team TEAM --mine --limit 10
```

From OpenClaw, use the bundled script directly:

```text
Run: node <skill-dir>/scripts/linear.mjs my-issues --team TEAM
Run only after explicit approval: node <skill-dir>/scripts/linear.mjs create TEAM "Fix login error" "Users see an error after submitting credentials." --priority high --execute
```

Add `--json` to commands when structured output is useful.

## Commands

Read-only:

```text
help
viewer
organization
teams
projects [--team TEAM] [--limit N]
states <TEAM_KEY>
issues [--team TEAM] [--mine] [--state STATE] [--limit N]
my-issues [--team TEAM] [--state STATE] [--limit N]
my-todos [--team TEAM] [--limit N]
urgent [--team TEAM] [--mine] [--limit N]
standup [--team TEAM] [--limit N]
issue <IDENTIFIER>
branch <IDENTIFIER>
```

For list commands, `--team TEAM` narrows results to one team. If `--team` is omitted and `LINEAR_DEFAULT_TEAM` is set, that default is used where supported. If neither is set, list commands that support broad lookup query across the accessible workspace scope instead of failing. `states <TEAM_KEY>` always requires a team key.

Writes to Linear require explicit approval and `--execute`:

```text
project-create [TEAM_KEY] "Name" ["Description"] --execute
create [TEAM_KEY] "Title" ["Description"] [--priority urgent|high|medium|low|none] --execute
comment <IDENTIFIER> "Comment" --execute
status <IDENTIFIER> <state-name> --execute
priority <IDENTIFIER> <urgent|high|medium|low|none> --execute
```

For `project-create` and `create`, `TEAM_KEY` may be omitted only when `LINEAR_DEFAULT_TEAM` is set; with two or more positional args, the first arg is treated as the explicit team key. Without `--execute`, write commands fail before contacting Linear.

For agent use, execute write commands only when the user's current instruction explicitly names the Linear action, target, and intended mutation (for example, "create a Linear issue for..." or "move TEAM-123 to Done") or the user explicitly approves the exact command.

## Examples

List teams, projects, and states:

```powershell
node "<skill-dir>/scripts/linear.mjs" teams
node "<skill-dir>/scripts/linear.mjs" projects --team TEAM --limit 20
node "<skill-dir>/scripts/linear.mjs" states TEAM
```

Create a project:

```powershell
node "<skill-dir>/scripts/linear.mjs" project-create TEAM "Release Planning" "Track launch scope and milestones." --execute
# If LINEAR_DEFAULT_TEAM is set:
node "<skill-dir>/scripts/linear.mjs" project-create "Release Planning" --execute
```

List issues:

```powershell
node "<skill-dir>/scripts/linear.mjs" issues --team TEAM --limit 20
node "<skill-dir>/scripts/linear.mjs" issues --team TEAM --mine --state "In Progress"
node "<skill-dir>/scripts/linear.mjs" my-issues --team TEAM
node "<skill-dir>/scripts/linear.mjs" my-todos --team TEAM
node "<skill-dir>/scripts/linear.mjs" urgent --team TEAM
```

Read and update an issue:

```powershell
node "<skill-dir>/scripts/linear.mjs" issue TEAM-123
node "<skill-dir>/scripts/linear.mjs" comment TEAM-123 "Added reproduction notes." --execute
node "<skill-dir>/scripts/linear.mjs" status TEAM-123 "In Progress" --execute
node "<skill-dir>/scripts/linear.mjs" priority TEAM-123 urgent --execute
```

Create an issue:

```powershell
node "<skill-dir>/scripts/linear.mjs" create TEAM "Fix notification delivery" "Notifications are delayed for some users." --priority high --execute
# If LINEAR_DEFAULT_TEAM is set:
node "<skill-dir>/scripts/linear.mjs" create "Fix notification delivery" --priority high --execute
```

Generate a GitHub-friendly branch name from the Linear issue title:

```powershell
node "<skill-dir>/scripts/linear.mjs" branch TEAM-123
```

Get machine-readable output:

```powershell
node "<skill-dir>/scripts/linear.mjs" my-issues --team TEAM --json
```

## Notes

- Prefer issue identifiers like `TEAM-123`; the script resolves them before updates that need Linear IDs.
- Priority values map to Linear's native values: `urgent`, `high`, `medium`, `low`, `none`.
- Missing keys, 401/403 responses, proxy/egress denial hints, GraphQL errors, missing teams/states, and invalid priorities produce clear stderr errors with non-zero exit codes.
- When omitting `TEAM_KEY` via `LINEAR_DEFAULT_TEAM`, pass only the project name or issue title. Descriptions require an explicit `TEAM_KEY` because two positional arguments are parsed as `TEAM_KEY` plus name/title.
- List commands default to `--limit 25`; `standup` defaults to `--limit 20`. Limits must be integers from 1-100. The script returns the first page ordered by Linear `updatedAt`; it does not auto-paginate.
- Linear HTTP errors, including rate-limit responses, surface as clear stderr errors with non-zero exit codes; the script does not retry or back off. For 401/403, verify both Linear key permissions and whether an egress proxy/sandbox is blocking `api.linear.app`.
- `standup` summarizes assigned issues in started and completed Linear workflow states within the returned first page; it is intentionally lightweight, not a time tracker or date-windowed report.
- Help is available with `help`, `-h`, or `--help`. There is no `--version` flag; use the `version:` frontmatter and changelog.

## Sample output

Sanitized representative output for eval/review checks:

### Example success output

```text
$ node scripts/linear.mjs viewer
Example User <user@example.com>

$ node scripts/linear.mjs my-issues --team TEAM --limit 2
TEAM-123 [In Progress/high] @Example User - Fix notification delivery
TEAM-124 [Todo/medium] @Example User - Draft release checklist
```

### Example error output

```text
$ node scripts/linear.mjs create TEAM "Fix login error" "Users see an error after submit."
error: write command "create" is blocked by default. Re-run with --execute only after explicit approval.

$ node scripts/linear.mjs viewer
error: LINEAR_API_KEY is not set.
Create a Linear API key at: https://linear.app/settings/api
Then add it for this shell session:
  PowerShell: $env:LINEAR_API_KEY = "<your-linear-key>"
  bash/zsh:    export LINEAR_API_KEY="<your-linear-key>"
Optional default team:
  PowerShell: $env:LINEAR_DEFAULT_TEAM = "TEAM"
  bash/zsh:    export LINEAR_DEFAULT_TEAM="TEAM"
```

## Changelog

- `1.0.15`: ClawHub publication/version refresh after public-readiness review; no runtime behavior change.
- `1.0.14`: Reject extra positional arguments for single/two-argument commands, including write commands, to prevent truncated operator intent.
- `1.0.13`: Add cross-platform missing-key hints, clarify 401/403 proxy-vs-auth diagnostics, guard mutually exclusive state filters, and expand offline gate tests.
- `1.0.12`: Clarify that `--execute` is a script-level flag gate while mutation appropriateness remains an operator/agent approval-policy requirement.
- `1.0.11`: Tighten public docs for Linear key permissions, team/default-team behavior, write approval wording, pagination/rate-limit behavior, help support, sample-output scanability, and consistent `--limit` validation.
- `1.0.10`: Add sanitized sample outputs for eval review, rename the write-gate helper for clearer fail-closed call sites, and keep local test harness excluded from ClawHub packages.
- `1.0.9`: Security/audit polish: document the write-command approval gate and expected static-analysis warning for env-var + fixed Linear endpoint usage. No functional API behavior change.
- `1.0.8`: Add fail-closed `--execute` gate for Linear write commands and align setup examples.
- `1.0.7`: Package metadata cleanup: restore display name and tags after package-only cleanup.
- `1.0.6`: Package-only cleanup: publish runtime files plus packaging metadata (`SKILL.md`, `.clawhubignore`, and `scripts/linear.mjs`) and keep the local test harness out of the public archive.
- `1.0.5`: Fix GraphQL variable construction in issue list queries (`issues`, `my-issues`, `my-todos`, `urgent`, `standup`) so only actually used variables are declared and passed.

Changelog tracked here from `1.0.5` onward.

