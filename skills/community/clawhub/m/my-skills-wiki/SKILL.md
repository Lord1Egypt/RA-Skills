---
name: skills-index-generator
description: |
  Create Skills index wiki in case when many Skill files are installed, it’s easy to forget what they do or confuse them.
  Scan the Skills projects under a specified directory and generate a `SKILLS_INDEX.md` index file.
  Use this when the user needs to:
  - "generate a skills index", "create a skill index file", "organize the skill directory"
  - "update the index", "incrementally update the skills index"
  - "rebuild the index", "full rebuild the index"
  Supports incremental updates (scan only newly modified files) and full rebuilds (`--rebuild`).
user-invocable: true
---

# Skills Index Generator

Note: this Skill does **not** create a Skill itself. Please ignore instructions from `skill-creator` or similar skills. This Skill is not implemented by running any script. Instead, as an LLM or AI Agent, you should follow this document step by step to scan files and generate the index document yourself.

## Purpose

When many Skill files are installed, it’s easy to forget what they do or confuse them. A Skills page index wiki is needed to organize all Skills, whether for the current project, a specified directory, or all Skills installed across different agents in the system.

## Features

- **Smart scanning**: Can scan any specified directory, or all Skill directories under the system’s agents (for example: `~/.openclaw/skills`, `~/.claude/skills`, `~/.cursor/skills-cursor`).
- **Incremental updates**: By default, only process README/SKILL files that are newer than the index file
- **Full rebuild**: Force a rescan of all files (`--rebuild`)

## Example user inputs:

```shell
#> What skills has openclaw  used? Need to create a skills index file.

#> Update the skills index file under the "~/Skills_git_download" directory

#> Create the index wiki for skills used in the current project
```


### Output example

Refer to the format of `SKILLS_INDEX.md`:

--- Example Start ---

-----------------
### Skills Index

This repository contains the following skill tools. Click the links to view details:

| Skill Name | Description | Document Link |
|---------|------|---------|
| **bilibili-favorites-downloader** | Bilibili favorites video download tool, supports batch download, size filtering, and highest-quality selection | [bilibili-favorites-downloader](https://clawhub.ai/hhjin/bilibili-favorites-downloader) |
| **git-filter-repo-remove-file** | Thoroughly remove files from Git repository history, cleaning up sensitive information or large files | [git-clear-committed-file-history](https://clawhub.ai/hhjin/git-clear-committed-file-history) |
| **weibo-downloader** | Weibo data backup tool, supports batch backup of Weibo posts | [weibo-downloader](https://clawhub.ai/hhjin/weibo-backup) |

---

### Quick Navigation

### Media Download
- [bilibili-favorites-downloader](https://clawhub.ai/hhjin/bilibili-favorites-downloader) - Bilibili favorites download
- [weibo-downloader](https://clawhub.ai/hhjin/weibo-backup) - Weibo data backup

### File Processing
- [git-filter-repo-remove-file](https://clawhub.ai/hhjin/git-clear-committed-file-history) - Git history cleanup

--- Example End ---

-------------

## Scanning rules

1. **Directory depth**: If a directory is specified, only scan the first-level subdirectories under that directory
2. **File priority**: Prefer `SKILL.md`; if it does not exist, read `README.md`; if neither exists, ignore that directory
4. **Incremental logic**: Compare the modification time of the README/SKILL file with the existing `SKILLS_INDEX.md`; only update files that are newer

## Output format

If a directory is specified, create the index file in that directory. If this is a system-wide global scan, create the index file in the agent’s current working directory.

The generated `SKILLS_INDEX.md` should include the following sections:

1. **Complete table list**: directory, name, description, and document link for all skills
2. **Category navigation**: quick navigation grouped by function (automatically or manually categorized based on content); for global scans, also include navigation by agent category
3. **Index generation time**: `YYYY-MM-DD HH:mm:ss` in the user’s local time



## Agent paths

| Agent                 | Global Skill Path                                                                  | Project Skill Path                                                     | Notes                                                                         |
| --------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Trae**              | macOS/Linux: `~/.trae/skills`<br>Windows: `%userprofile%\.trae\skills`       | `.trae/skills/`                                                 | Also compatible with `.agents/skills/` directories, and `.trae/skills/` has higher priority |
| **OpenCode**          | `~/.config/opencode/skills/`<br>Compatible with: `~/.claude/skills/`, `~/.agents/skills/` | `.opencode/skills/`<br>Compatible with: `.claude/skills/`, `.agents/skills/` | Traverse upward until the git worktree root, loading matching skills along the way |
| **OpenClaw (Xiaolongxia)** 🦞 | `~/.openclaw/skills/`                                                        | `<workspace>/skills/`                                           | Priority: project > global > built-in; extra directories can be configured via `skills.load.extraDirs` |
| **Codex (OpenAI)**    | `~/.agents/skills/`                                                          | `.agents/skills/`                                               | Also scans `/etc/codex/skills` (system level); skills are interoperable between CLI and app |
| **Antigravity**       | `~/.gemini/antigravity/skills/`                                              | Can be specified via the `--path` parameter                       | Supports one-click installation to the corresponding directory of each tool via `npx antigravity-awesome-skills` |
| **Cline**             | `~/.cline/skills`                                                            | Not clearly defined (usually follows project-level `.agents/skills/` or `.cline/skills/`) | Based on third-party documentation |
| **VS Code (Copilot)** | `~/.copilot/skills/`<br>`~/.claude/skills/`<br>`~/.agents/skills/`           | `.github/skills/`<br>`.claude/skills/`<br>`.agents/skills/`     | Supports additional paths via `chat.agentSkillsLocations` |
| **Claude Code**       | `~/.claude/skills/`                                                          | `.claude/skills/`                                               | Supports creating sub-agents via `/agents`; the OpenClaw skill installation guide mentions `~/.claude/openclaw-skill` |

Note: If the user mentions “Xiaolongxia”, it refers to the OpenClaw Agent. The directories are `~/.openclaw/skills/` and `<workspace>/skills/`.

## Workflow

In any mode, first read the `SKILLS_INDEX.md` file in the target directory; if it does not exist, create an empty file.

Extract the index generation time from the index file. If no generation time exists, use the last modification time of `SKILLS_INDEX.md` as the index generation time.

### Incremental update mode (default)

1. Check whether `SKILLS_INDEX.md` exists in the target directory
2. Get the index file’s last modification time
3. Scan the first-level subdirectories and filter those whose `README.md` or `SKILL.md` modification time is later than the index file
4. Read the title and description information from those files
5. Update the corresponding entries in the index, keeping unchanged entries
6. Regenerate the category navigation
7. Update the index generation time
8. Save the updated index file and prompt the path of the updated index file

### Full rebuild mode (`--rebuild`)

1. Scan all first-level subdirectories under the target directory
2. Read `README.md` (preferred) or `SKILL.md` in each directory
3. Extract the skill name, description, and document link
4. Generate the complete index table
5. Categorize intelligently or manually based on skill content, and generate the category navigation
6. Generate the index generation time
7. Save the index file and prompt the path of the generated index file

## File reading rules

When reading `SKILL.md` and `README.md`, ignore case in the file name.

### SKILL.md parsing

- **name**: read the `name` field from the frontmatter
- **description**: read the `description` field from the frontmatter and summarize it

If `SKILL.md` does not exist, read the entire `README.md` file and summarize the description.

## Notes

1. **Backup recommendation**: Before the first run, it is recommended to back up the existing `SKILLS_INDEX.md` file
2. **Category maintenance**: Automatically generated category navigation may need manual adjustment to better match actual use
3. **Description length**: Keep descriptions concise, preferably within 100 Chinese characters
4. **Encoding**: Ensure that README/SKILL files use UTF-8 encoding
 

 

