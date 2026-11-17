# `lifeos` — full command reference

Exhaustive reference for the `lifeos` CLI. The SKILL.md covers the common path;
load this when you need an exact flag, output shape, or error meaning.

## Conventions

- **Invocation**: run via `npx -y @life-os/cli <command> …` (npx fetches the
  published package on first use; `-y` skips the prompt). The command names below
  (`config`, `tasks`, …) are the `<command>` argument, e.g.
  `npx -y @life-os/cli tasks due=today`.
- **Options**: `key=value` (or `--key=value`). **Flags**: `--json`, or bare
  `overwrite` / `case`. Quote values containing spaces.
- **Output**: human-readable by default; `--json` (or `format=json`) emits a
  single JSON document on stdout.
- **`content=` escapes**: in write commands (`append`, `create`, `<period>:append`)
  the `content=` value interprets `\n` `\t` `\r` `\\`, so you can write multi-line
  content on one command line.
- **Exit codes**: `0` success, `1` on any error. Error text is human-readable.

## Vault selection

Resolved in order, first match wins:

1. `vault=<path>` option (`~` is expanded; relative paths resolve against cwd)
2. `$LIFEOS_VAULT` environment variable
3. Walk up from the current directory for a folder containing `.obsidian/` or `.lifeos/`
4. The folder Aino last opened (`<userData>/bootstrap.json` → `lastOpenedFolder`)

`config` reports which one was used via `Found by` / `discoveredVia`.

## Settings sources

Effective settings merge built-in defaults with these files (later overrides
earlier), the same set the plugin and Aino use:

1. `.obsidian/plugins/periodic-para/data.json` (legacy plugin id)
2. `.obsidian/plugins/lifeos-pro/data.json`
3. `.lifeos/settings.json` (Aino's vault-portable settings)

---

## Commands

### `config`

Show the resolved vault, how it was found, the config source files applied, and
key effective settings (PARA folders, periodic base, daily path format, and the
daily template path used when rendering a missing daily note). `--json` → `{ vault: {root, discoveredVia}, sources: string[], settings }`.

### `tasks [todo|done|all]`

List tasks. Positional status defaults to `todo`.

| Option                     | Meaning                                                             |
| -------------------------- | ------------------------------------------------------------------- |
| `tag=<tag>`                | tasks tagged `<tag>` (matches the tag and its sub-tags `<tag>/...`) |
| `keyword=<text>`           | substring match on task text                                        |
| `due=today\|week\|overdue` | filter by **due date**; status still applies (default hides done)   |
| `limit=<n>`                | max rows (default 50)                                               |
| `--json`                   | `{ totalCount, count, items: TaskItem[] }`                          |

`TaskItem`: `{ file, line, text, checked, dueDate?, priority?, tags?, ... }`.
Human line: `[ ]|[x] <text>  (due <date>  !<priority>  #<tags>)  — <file>:<line>`.

Notes: `due=*` over-fetches and post-filters by status, so a completed task with a
past due date is hidden unless you ask for `done`/`all`.

### `search query=<text>`

| Option                | Meaning                                                 |
| --------------------- | ------------------------------------------------------- |
| `type=file` (default) | match note name + path (case-insensitive substring)     |
| `type=tag`            | match tag names; output `#tag  (count)`                 |
| `type=content`        | full-text scan of note bodies; output `path:line  text` |
| `case`                | content search becomes case-sensitive                   |
| `limit=<n>`           | max results (default 20, capped at 100)                 |
| `--json`              | `{ type, query, count, items }`                         |

Content matching is plain substring (not regex). It reads files on demand and
stops at `limit`.

### `read file=<name> | path=<vault/rel/path>`

Print a note. `path=` is exact (vault-relative); `file=` resolves a loose name via
the index and errors if ambiguous (lists candidates). `.md` is added if omitted.
`--json` → `{ filePath, content }`.

### Periodic notes: `daily | weekly | monthly | quarterly | yearly`

Resolve the note path from `periodicNotesPath` + the per-type format
(`periodicNotesPathFormat<Type>`, falling back to LifeOS defaults), using the same
formatter as the plugin/Aino (ISO weeks for weekly). Weekday/month name tokens
(`dddd`/`MMMM`) honor `locale=` (default: system locale).

| Form                             | Effect                                                                                                                                          |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `<period>`                       | print `Type/Date/Path/Exists/Format`; `--json` adds `exists`                                                                                    |
| `<period>:read`                  | print the note (errors if it doesn't exist)                                                                                                     |
| `<period>:create [overwrite]`    | create the note from its configured template (rendered); errors if it exists unless `overwrite`                                                 |
| `<period>:append content=<text>` | append; **creates the note from its template if missing**                                                                                       |
| `section=<header>`               | insert at the end of that header's section (creates it if absent) instead of the file tail — e.g. `section="日常记录"` for daily-record logging |
| `date=YYYY-MM-DD`                | target a specific period (default: today)                                                                                                       |
| `locale=<bcp47>`                 | locale for name tokens, e.g. `zh-CN`                                                                                                            |

Template resolution: `periodicNotesTemplateFilePath<Type>` if set, else
`<periodicNotesPath>/Templates/<Type>.md`, else a built-in default. The template is
rendered with the shared engine: `{{snapshot:Project}}` → numbered `[[index|name]]`
list of PARA sub-folders that have an index note; `{{if weekday}}…{{endif}}`,
`{{date}}`, `{{date+N:FORMAT}}`, `{{title}}` are expanded; unknown `{{…}}` (LifeOS
query blocks) are left verbatim. `:create`/`:append` `--json` adds `created` /
`templatePath`.

Every form echoes the resolved path. `<period> read` / `<period>:read` are both
accepted.

### `theme:create type=<t> tag=<tag> path=<vault/rel/path> [overwrite]`

Create a PARA/theme note from its template. `type` ∈ `project|area|resource|archive|theme`.
Template resolution: `<type>TemplateFilePath` if set, else `<typeDir>/Template.md`,
else a built-in default. The template is rendered (same engine as periodic notes),
then `tag` is injected into the note's `tags`/`aliases` frontmatter so the theme
index collects it. `path=` is caller-supplied (read `config` for PARA folder
names); convention is `<paraDir>/<name>/<name>.md`. Errors if the note exists
unless `overwrite`. `--json` → `{ ok, filePath, created, templatePath, type, tag }`.

### `append path=<vault/rel/path> content=<text> [section=<header>]`

Append to an **existing** note. Errors if the note doesn't exist (use `create`).
Without `section=`, appends to the file tail with a newline boundary. With
`section=<header>`, inserts at the **end of that header's section body** (matching
the header at any `#` depth, ignoring case/whitespace) and creates the section at
the end of the file if the header is missing. `--json` →
`{ ok, filePath, created:false, section }`.

### `create path=<vault/rel/path> [content=<text>] [overwrite]`

Create a note (parent folders auto-created, `.md` added if omitted). Errors if it
exists unless `overwrite`. `--json` → `{ ok, filePath, created }`.

### `task done|todo ref=<file>:<line>`

Toggle one task's checkbox. `ref` is the `file:line` printed by `tasks` (only the
trailing `:<digits>` is the line number, so paths with colons are fine).
`--json` → `{ ok, filePath, action }`.

### `skill install [vault=<path>]`

Install or update the bundled LifeOS agent skill into
`.agents/skills/lifeos/` inside the resolved vault. The command overwrites
`SKILL.md` and `references/` with the files embedded in the current
`@life-os/cli` package, so it is the upgrade path after installing a newer CLI.

### `help`, `version`

Print usage / version.

---

## Errors

Surfaced as readable text with exit code 1. Common cases:

| Situation                      | Message                                                           |
| ------------------------------ | ----------------------------------------------------------------- |
| note missing (`read`/`append`) | `No such note in the vault.`                                      |
| `create` onto existing         | `A note already exists at that path. Add the \`overwrite\` flag…` |
| path escapes vault             | `Refusing to touch a path outside the vault.`                     |
| `task` ref not a checkbox line | `That line is not a \`- [ ]\` / \`- [x]\` task.`                  |
| bad `due=` / `date=` value     | explains the accepted values                                      |
| no vault found                 | explains the four resolution options                              |

---

## Performance (≈5k-note vault)

- Fixed startup (node + import): ~70 ms.
- `search type=content`: ~0.5 s worst case (scans bodies; stops at `limit`).
- Index-backed (`tasks`, `search type=file|tag`): ~1 s (rebuilds the index per
  process; there is no persistent cache yet). Avoid tight loops of many such calls.

## Out of scope

UI views, Google Calendar / CalDAV sync, two-way task↔calendar sync, Pomodoro and
daily-record sync — these remain in the LifeOS plugin and the Aino desktop app.
