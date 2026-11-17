---
name: lifeos
description: "Read, query and edit a LifeOS / Obsidian PARA vault (notes, tasks, periodic notes, theme notes, tags, AI Wiki) from the command line via the `lifeos` CLI — headless, no Obsidian or Aino needed. Use when the user asks about their tasks or 待办; periodic notes — daily/weekly/monthly/quarterly/yearly review or 日记/周记/月记/季记/年记; theme notes / PARA — projects/areas/resources/archives or 项目/领域/资源/归档/主题; tags / theme tags or 标签/主题标签; the LifeOS AI Wiki / `.AI.md` topic synthesis pages or 整理主题 / 更新 AI Wiki; or wants to find/search notes, capture a thought, or check/update what's on their plate in their LifeOS vault."
---

# LifeOS

Drive a LifeOS vault through the `lifeos` CLI. It is **config-aware** — it reads
the user's real PARA folder names, periodic-note formats and section headers from
their own plugin / Aino settings — and **headless**, working directly on the vault
folder without Obsidian running. Query results match what the user sees in the app.

## Core concepts (核心概念)

LifeOS organises a vault as two complementary kinds of note. Knowing which one a
request is about tells you which command to reach for.

**Periodic notes (周期笔记)** — organised by **time**. One file per period; resolve
its path with `npx -y @life-os/cli <period>`. The longer the period the less predictable it is,
so longer periods are for goals and shorter ones for tasks:

- **yearly (年记)** / **quarterly (季记)** — long-term: **goal management (目标管理)**,
  set the direction for the year / quarter.
- **monthly (月记)** / **weekly (周记)** — short-term: **task management (任务管理)**,
  break those goals into this month's / week's tasks.
- **daily (日记)** — daily records: real-time capture of thoughts, tasks and time
  tracking. Most capture lands here.

**Theme notes (主题笔记)** — organised by **subject**, usually via **PARA**. These live
in the user's PARA folders (see `npx -y @life-os/cli config`); reach them with `search`/`read`.
The later→earlier order is increasing actionability (archive → resource → area → project):

- **project (项目)** — most actionable: a concrete goal with a deadline, e.g. 「完成季度报告」.
- **area (领域)** — an ongoing responsibility to maintain, e.g. 「健康」「财务」.
- **resource (资源)** — a topic of interest or reference material, e.g. 「读书笔记」.
- **archive (归档)** — finished or inactive projects / areas / resources.
- PARA is just the common shape; a theme can be any subject (e.g. 「#节日」).

**The link between them — theme tags (主题标签)**: each theme note is identified by a
unique tag. Any task / fleeting note / file anywhere — including inside a daily or
other periodic note — that carries that tag is **automatically indexed** into the
theme note. This is what makes capture stress-free: jot with the right `#tag` now,
find it under the theme later.

- **Top-down (自上而下)**: tasks planned in a theme note surface in the daily note on
  their planned date, so `tasks due=today` reflects project/goal plans.
- **Bottom-up (自下而上)**: a tagged thought or todo in the daily note is collected
  back into the matching theme note via its tag.

So: when a user talks about a 项目/领域/资源/主题, work in the theme note; when they
talk about a day/week/month/quarter/year or "what's on my plate today", work in the
periodic note — and reuse the theme's tag so the two stay linked.

**AI Wiki (`.AI.md`)** — a third layer that sits **beside** the topic note as a
sibling `{filename}.AI.md` file. It is the LifeOS AI Wiki: a synthesised
summary page of what the vault knows about that topic, maintained
incrementally by this skill. Only **topic / index notes** get one — never
captures, dailies, meeting notes, or other one-off source files. When the
user says "整理一下 X 主题"、"更新 AI Wiki"、"看看 AI Wiki 怎么说", follow the
rules in [`references/ai-wiki.md`](references/ai-wiki.md): it covers source
scope, page schema, ingest / query / lint flows, and the concrete CLI
recipes that touch `7 索引/7. AI Wiki 索引.md` and `7 索引/AI Wiki 变更日志.md`.

## Invocation

Run the CLI with **`npx -y @life-os/cli`** — npx fetches the published package on
first use and `-y` skips the install prompt; nothing needs to be installed
globally. Every example below is written in that form.

## First moves

1. Run `npx -y @life-os/cli config` to confirm which vault and settings are in
   effect. If it can't find a vault, ask the user for the path and pass
   `vault=<path>`.
2. `npx -y @life-os/cli help` is the authoritative command list. For exhaustive
   flags, output shapes and error codes, read
   [`references/commands.md`](references/commands.md).
3. For LifeOS AI Wiki maintenance (`.AI.md` topic pages, the central index,
   the changelog and lint checks), read
   [`references/ai-wiki.md`](references/ai-wiki.md).

## Syntax

- Options are `key=value` (e.g. `tag=work`, `limit=10`). `--key=value` also works.
- Flags are bare words after `--` (e.g. `--json`) or plain (`overwrite`, `case`).
- Quote values with spaces: `vault="~/My Vault/LifeOS"`.
- Add `--json` whenever you need to parse output programmatically.

## Vault selection

This skill is installed **inside the user's vault**, so you normally run from
within it — the CLI auto-detects the vault from the current directory. Resolution
order (first match wins): `vault=` → `$LIFEOS_VAULT` → walk up from cwd for
`.obsidian/`/`.lifeos/` → the folder Aino last opened (fallback). Only pass
`vault=` when the user means a _different_ vault than the one you're in.

## Commands at a glance

```bash
# every command is invoked as: npx -y @life-os/cli <args>
npx -y @life-os/cli config                          # vault + effective settings (run this first)
npx -y @life-os/cli tasks [todo|done|all]           # tasks; filters: tag= keyword= due=today|week|overdue limit=
npx -y @life-os/cli search query=<text>             # type=file (default) | tag | content ; add `case` for content
npx -y @life-os/cli read file=<name>|path=<p>       # print a note
npx -y @life-os/cli daily|weekly|monthly|quarterly|yearly        # show the period note's path + whether it exists
npx -y @life-os/cli <period>:read                   # print the period note
npx -y @life-os/cli <period>:create                 # create the period note from its configured template
npx -y @life-os/cli <period>:append content=<t>     # append (creates from template if missing)
npx -y @life-os/cli theme:create type=project|area|resource|archive|theme tag=<t> path=<p>   # create a PARA note from its template
npx -y @life-os/cli append path=<p> content=<t>     # append to an existing note
npx -y @life-os/cli create path=<p> [content=]      # create a plain note (no template; add `overwrite` to replace)
npx -y @life-os/cli task done|todo ref=<file>:<n>   # toggle a task by its file:line reference
```

**Template-aware creation:** `<period>:create`, `theme:create`, and the auto-create
inside `<period>:append` all render the user's **configured template** through the
same engine the plugin/Aino use — `{{snapshot:Project}}`, `{{if weekday}}`,
`{{date}}` etc. are expanded, and theme notes get their tag injected into
frontmatter. Plain `create path=…` stays template-free (use it for arbitrary notes).

## Recipes (chain commands like this)

**Morning review** — what's on my plate, then capture the plan:

```bash
npx -y @life-os/cli tasks due=today --json          # today's open tasks
npx -y @life-os/cli tasks due=overdue --json        # anything slipping
npx -y @life-os/cli daily:append section="日常记录" content="- 08:30 #计划 今天先做 ..."
```

**Quick capture** — "记一下：想法X" (drop a timestamped line into today's record section):

```bash
npx -y @life-os/cli daily:append section="日常记录" content="- 14:30 #摘抄 想法X"   # echoes the resolved path
```

**Find then act** — never write blind:

```bash
npx -y @life-os/cli tasks keyword="季度报告"        # locate the task, note its file:line
npx -y @life-os/cli task done ref="0. 周期笔记/2025/Daily/05/2025-05-30.md:14"
```

**Research a topic across the vault**:

```bash
npx -y @life-os/cli search query="超线性回报" type=content limit=20   # path:line + matching text
npx -y @life-os/cli read path="-1. 捕获/....md"                       # open the most relevant hit
```

**Weekly review**:

```bash
npx -y @life-os/cli weekly                          # confirm this week's note path / existence
npx -y @life-os/cli tasks done due=week             # what got done
npx -y @life-os/cli weekly:append content="## 复盘\n..."
```

## Journaling (日记)

The daily note is where most capture lands. Do it precisely:

1. **Locate** — `npx -y @life-os/cli daily` shows today's path and `Exists`. Pass
   `date=YYYY-MM-DD` for another day, `locale=` for weekday/month names.
2. **Insert in the right place** — append into the record section with
   `section=<header>`, not the file tail. The header is the daily note's main
   record heading (commonly `日常记录` / `Daily Record`); confirm it by reading a
   recent daily note. `section=` lands the line at the **end of that section**
   (e.g. before `习惯打卡` / `Habit`) and creates the section only if absent.
3. **Format** — default to `- HH:mm #tag 内容`. Use the current time from the
   environment; the user is usually in their local timezone. Reuse existing tags —
   `npx -y @life-os/cli search type=tag keyword=<x>` — rather than inventing
   fine-grained ones; 1–3 tags unless the entry needs more.
4. **Polish, don't transcribe** — lightly smooth the user's words while keeping
   their facts, stance, emotion and first-person voice; add no judgments, advice
   or conclusions they didn't make. When they say `原文`/`逐字`/`原样`/`摘抄`/verbatim,
   or paste a quote, keep it exact and only tidy Markdown.
5. **Creating a missing daily note** — just use `<period>:create` (or let
   `<period>:append` auto-create it). The CLI renders the user's configured
   template via the shared engine: `{{snapshot:Project}}` expands to the live PARA
   index list, `{{if weekday}}`/`{{date}}`/etc. are resolved, and LifeOS query
   blocks (`ProjectListByTime`, `TaskDueListByTime`) are kept verbatim for the
   plugin to render at view time. No manual template rendering needed — the
   resulting note matches what the plugin/Aino would create.

The same `section=` works on `weekly|monthly|...:append` and on plain
`append path=<p> section=<h>`, so you can log into any note's heading.

## Creating theme notes (项目/领域/资源/归档)

Use `theme:create` so the note is built from the PARA type's template and gets
its theme tag wired into frontmatter (so the theme index collects it):

```bash
# read config first for the real PARA folder names, then place the note yourself
npx -y @life-os/cli config
npx -y @life-os/cli theme:create type=project tag="项目/季度OKR" path="1. 项目/季度OKR/季度OKR.md"
```

- `type=` picks the template (`<type>TemplateFilePath` → `<typeDir>/Template.md` → built-in).
- `tag=` is the theme tag; it's injected into `tags`/`aliases` frontmatter.
- `path=` is yours to choose — the convention is `<paraDir>/<name>/<name>.md` (a
  folder + same-named index note, which is what `{{snapshot}}` lists). Add
  `overwrite` to replace.

## Upgrading the skill

The skill files inside `.agents/skills/lifeos/` should match your CLI version.
Run this after upgrading `@life-os/cli`:

```bash
npx -y @life-os/cli skill install
```

It copies the bundled SKILL.md + references into your vault's `.agents/skills/lifeos/`
from the npm package you just upgraded to — no manual download, no git clone.

## Writing safely

- Writes (`append`, `create`, `task`, `<period>:append`) take an **explicit
  `path=` / `ref=`** — they never guess a note from a loose name, so you won't
  write to the wrong same-named file. `search`/`tasks` first to get the exact
  target, then write.
- `create` errors with _"A note already exists…"_ unless you pass `overwrite`.
- Periodic `:append` **echoes the resolved path** and creates the note if missing.
  If `Exists: no` surprises you, the vault's format config may differ from how
  existing notes were named — surface the path to the user rather than creating a
  stray note.

## Interpreting results

- Tasks print `[ ]`/`[x] <text>  (due …  !priority  #tags)  — <file>:<line>`.
  The `<file>:<line>` is the stable reference for `task done|todo`.
- `tasks` defaults to open (todo); pass `done`/`all` to widen. `due=` queries also
  hide completed tasks by default.
- PARA folder names are the user's own (e.g. `1. 项目`) — see `npx -y @life-os/cli config`.
- Errors are human-readable and exit non-zero (e.g. file-not-found, already-exists).

## Performance

Index-backed commands (`tasks`, `search type=file|tag`) rebuild the index per run
(~1s on a ~5k-note vault); `search type=content` scans note bodies (~0.5s). Fine
for interactive use; avoid tight loops of many index queries.

## Scope

Reading, querying and editing note content (notes, tasks, periodic notes, PARA,
tags). **Not** in scope: Google Calendar / CalDAV sync, and the plugin's UI —
those live in the LifeOS plugin and Aino app.
