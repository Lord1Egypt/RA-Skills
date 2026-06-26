---
name: obsidian-remote
description: "Full remote control of a running Obsidian desktop app via the built-in obsidian CLI. Use INSTEAD of the older obsidian-cli skill packaged with OpenClaw — this skill covers the real, feature-complete CLI that ships with Obsidian itself. Handles reading/writing/searching notes, daily notes, tasks, properties/frontmatter, tags, backlinks, templates, plugins, sync, publish, bookmarks, bases, themes, CSS snippets, file history, and dev tools (CDP, DOM, eval JS, screenshots). Triggers on obsidian, vault, daily note, obsidian tasks, obsidian search, obsidian properties, obsidian plugins, obsidian sync, obsidian publish, obsidian bookmarks, obsidian bases, obsidian templates, obsidian tags. Requires Obsidian desktop app running. NOT the same as obsidian-cli (URI-based tool)."
---

# Obsidian Remote

> **This skill replaces the older `obsidian-cli`-based skill.** The `obsidian` binary is
> Obsidian's own built-in CLI with full app control. Prefer it for everything.

## Prerequisites

- Obsidian desktop app **running** (the CLI talks to the live app process)
- `obsidian` binary on PATH (installed with the desktop app; on macOS it's a shell wrapper at `/opt/homebrew/bin/obsidian` → `Obsidian.app`)

Quick check: `obsidian version`

## Core Concepts

- **file=\<name\>** — resolves like wikilinks (fuzzy, by note name)
- **path=\<path\>** — exact path relative to vault root (e.g. `Folder/Note.md`)
- Most commands default to the **active file** when file/path is omitted
- **vault=\<name\>** — target a specific vault (omit for default/only vault)
- Quote values with spaces: `name="My Note"`
- Use `\n` for newline, `\t` for tab in content values
- Output formats available on many commands: `format=json|tsv|csv|text|md`

## Vault & File Discovery

```bash
obsidian vaults                         # list known vaults
obsidian vaults verbose                 # include vault paths
obsidian vault                          # active vault info (name, path, files, folders, size)
obsidian vault info=path                # just the vault path

obsidian files                          # list all files
obsidian files folder="Projects"        # filter by folder
obsidian files ext=canvas               # filter by extension
obsidian files total                    # file count

obsidian folders                        # list folders
obsidian folder path="Projects" info=files  # folder info

obsidian recents                        # recently opened files
```

## Reading & Writing Notes

```bash
obsidian read file="Meeting Notes"          # read by name
obsidian read path="Projects/spec.md"       # read by exact path

obsidian create name="New Note" content="# Hello" open  # create + open
obsidian create path="Journal/idea.md" template="Default" overwrite

obsidian append file="Log" content="- entry"     # append
obsidian append file="Log" content=" suffix" inline  # append without newline
obsidian prepend file="Log" content="# Header"   # prepend

obsidian delete file="Old Note"                  # trash
obsidian delete path="tmp/scratch.md" permanent  # permanent delete

obsidian move file="Draft" to="Archive/Draft.md" # move/rename
obsidian rename file="Draft" name="Final"        # rename in place

obsidian open file="Todo" newtab                 # open in new tab
obsidian random                                  # open random note
obsidian random:read folder="Journal"            # read random note from folder
```

## Search

```bash
obsidian search query="project plan"             # file-name search
obsidian search query="plan" path="Work" limit=5 # scoped, limited

obsidian search:context query="API key" case     # full-text with line context
obsidian search:context query="bug" format=json  # JSON output
```

## Daily Notes

```bash
obsidian daily                                   # open today's daily note
obsidian daily:path                              # get daily note path
obsidian daily:read                              # read daily note contents
obsidian daily:append content="- 3pm standup"    # append to daily
obsidian daily:prepend content="## Morning"      # prepend to daily
```

## Tasks

```bash
obsidian tasks                          # all tasks
obsidian tasks todo                     # incomplete only
obsidian tasks done                     # completed only
obsidian tasks todo verbose             # grouped by file with line numbers
obsidian tasks file="Project" todo      # tasks in specific file
obsidian tasks daily todo               # tasks from daily note
obsidian tasks status="/" format=json   # custom status filter

obsidian task file="Todo" line=5 toggle # toggle done/todo
obsidian task file="Todo" line=5 done   # mark done
obsidian task file="Todo" line=5 todo   # mark todo
obsidian task daily line=3 toggle       # toggle task in daily note
```

## Properties / Frontmatter

```bash
obsidian properties                              # all properties across vault
obsidian properties file="Note" format=yaml      # properties for a file
obsidian properties counts sort=count            # property usage stats

obsidian property:read name="status" file="Task" # read property
obsidian property:set name="status" value="done" file="Task"
obsidian property:set name="tags" value="work,urgent" type=list file="Task"
obsidian property:remove name="draft" file="Task"
```

## Tags

```bash
obsidian tags                           # all tags
obsidian tags counts sort=count         # tag usage sorted by count
obsidian tags file="Note"               # tags in specific file
obsidian tag name="project" verbose     # tag info with file list
```

## Links & Graph

```bash
obsidian links file="Hub"               # outgoing links
obsidian backlinks file="API"           # incoming links
obsidian backlinks file="API" counts    # with link counts
obsidian orphans                        # files with no incoming links
obsidian deadends                       # files with no outgoing links
obsidian unresolved                     # broken links
obsidian aliases                        # all aliases
```

## Bookmarks

```bash
obsidian bookmarks                              # list bookmarks
obsidian bookmark file="Important.md"           # bookmark a file
obsidian bookmark file="Note.md" subpath="## Section"  # bookmark heading
obsidian bookmark search="todo" title="My Search"      # bookmark a search
obsidian bookmark url="https://example.com" title="Ref" # bookmark URL
```

## Templates

```bash
obsidian templates                      # list available templates
obsidian template:read name="Meeting"   # read template content
obsidian template:read name="Meeting" resolve title="Q1 Review"  # resolve vars
obsidian template:insert name="Meeting" # insert into active file
```

## Plugins

```bash
obsidian plugins                              # installed plugins
obsidian plugins filter=community versions    # community with versions
obsidian plugins:enabled                      # enabled plugins

obsidian plugin id="dataview"                 # plugin info
obsidian plugin:install id="dataview" enable  # install + enable
obsidian plugin:enable id="dataview"          # enable
obsidian plugin:disable id="dataview"         # disable
obsidian plugin:uninstall id="dataview"       # uninstall
obsidian plugins:restrict on                  # toggle restricted mode
```

## Themes & Snippets

```bash
obsidian theme                                # active theme
obsidian themes versions                      # installed themes
obsidian theme:install name="Minimal" enable  # install + activate
obsidian theme:set name="Minimal"             # switch theme
obsidian theme:uninstall name="Minimal"       # remove

obsidian snippets                             # CSS snippets
obsidian snippets:enabled                     # enabled snippets
obsidian snippet:enable name="custom"         # enable
obsidian snippet:disable name="custom"        # disable
```

## Sync

```bash
obsidian sync:status                    # sync status
obsidian sync on                        # resume sync
obsidian sync off                       # pause sync
obsidian sync:history file="Note"       # version history
obsidian sync:read file="Note" version=2   # read specific version
obsidian sync:restore file="Note" version=2 # restore version
obsidian sync:deleted                   # deleted files in sync
```

## Publish

```bash
obsidian publish:site                   # site info
obsidian publish:list                   # published files
obsidian publish:status                 # pending changes
obsidian publish:add file="Guide"       # publish file
obsidian publish:add changed            # publish all changed
obsidian publish:remove file="Draft"    # unpublish
obsidian publish:open file="Guide"      # open on published site
```

## File History (Local)

```bash
obsidian history:list                   # files with history
obsidian history file="Note"            # version list
obsidian history:read file="Note" version=1  # read old version
obsidian history:restore file="Note" version=1  # restore
obsidian diff file="Note" from=1 to=3  # diff versions
```

## Bases (Obsidian Databases)

```bash
obsidian bases                                # list base files
obsidian base:views                           # views in current base
obsidian base:query file="Tracker" format=json  # query base
obsidian base:query file="Tracker" view="Active" format=md
obsidian base:create file="Tracker" name="New Item" content="..." open
```

## Outline & Word Count

```bash
obsidian outline file="Report"          # heading tree
obsidian outline file="Report" format=md  # markdown format
obsidian wordcount file="Essay"         # word + char count
obsidian wordcount file="Essay" words   # words only
```

## Commands & Hotkeys

```bash
obsidian commands                       # all available commands
obsidian commands filter="editor"       # filter by prefix
obsidian command id="editor:toggle-bold"  # execute command
obsidian hotkeys                        # all hotkeys
obsidian hotkey id="editor:toggle-bold" # hotkey for command
```

## Tabs & Workspace

```bash
obsidian tabs                           # open tabs
obsidian tabs ids                       # with tab IDs
obsidian tab:open file="Note.md"        # open in new tab
obsidian workspace                      # workspace tree
obsidian workspace ids                  # with item IDs
```

## Dev Tools

For automation, debugging, or extending Obsidian:

```bash
obsidian eval code="app.vault.getName()"              # run JS
obsidian dev:screenshot path="screenshot.png"          # take screenshot
obsidian dev:dom selector=".workspace" text            # query DOM
obsidian dev:dom selector="h1" all                     # all h1 elements
obsidian dev:css selector=".nav-header" prop="color"   # CSS inspection
obsidian dev:console                                   # console messages
obsidian dev:console level=error                       # errors only
obsidian dev:errors                                    # captured errors
obsidian dev:cdp method="Page.reload"                  # CDP command
obsidian dev:debug on                                  # attach debugger
```

## Tips

- Prefer `file=` for interactive lookups (fuzzy, like wikilinks). Use `path=` when you know the exact location.
- Pipe to `jq` or `grep` for filtering JSON output.
- For bulk operations, prefer `format=json` and parse programmatically.
- `obsidian reload` reloads the vault; `obsidian restart` restarts the app.
- The CLI may hang or timeout if Obsidian is not running — always verify with `obsidian version` first.
