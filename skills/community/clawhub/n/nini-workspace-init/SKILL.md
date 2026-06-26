---
name: workspace-init
metadata: {"openclaw":{"emoji":"🚀","requires":{"bins":["git","jq"],"install":[{"type":"node","pkg":"openspec"}]}}}
description: >-
  Use this skill to initialize or update a multi-repo workspace created from
  dev-config-template. Invoke whenever the user wants to: set up a fresh workspace
  clone, fill in CLAUDE.md placeholders, clone sub-repos, configure dev environments,
  or sync workspace files with the latest template. Triggers on: "init workspace",
  "initialize", "set up my project", "configure workspace", "update template",
  "sync template", "update workspace", dev-config-template setup questions, or
  Chinese: 初始化工作区, 配置工作区, 更新工作区模板, 模板有更新吗. Do NOT trigger
  for: project scheduling, weekly reports, or individual git operations.
---

# Workspace Init

Interactive initialization for workspaces created from
[dev-config-template](https://github.com/niracler/dev-config-template).
Takes a blank template to a fully working multi-repo workspace in one session.

## Prerequisites

| Tool | Required | Install |
|------|----------|---------|
| git | Yes | Pre-installed on most systems |
| jq | Yes | `brew install jq` (macOS) / `sudo apt install jq` (Ubuntu) |
| openspec | Yes | `npm install -g openspec` |

> Do NOT verify prerequisites on skill load. Check them at the start of
> Phase 2 (before execution begins). If a tool is missing, provide install
> instructions and wait for the user to confirm before continuing.

## When to Use

- User just created a repo from dev-config-template and wants to set it up
- User says "initialize workspace", "set up my project", "configure workspace"
- User mentions dev-config-template and asks for help getting started
- User wants to update an existing workspace to match the latest template

## Workflow Overview

```text
Phase 1: Collect ──► Phase 2: Scaffold ──► Phase 3: OpenSpec
                                                    │
              Phase 5: Finalize ◄── Phase 4: Environments
```

All information is collected in Phase 1 (interactive). Phases 2-5 execute
without further prompts -- errors are reported with remediation steps.

## Phase 1: Information Collection

Ask the user for the following, one at a time. Wait for each answer before
asking the next question.

### 1.1 Project basics

1. **Project name** -- used for config.yaml, VSCode workspace file, commit messages.
   Example: "srhome-dev", "my-iot-platform"
1. **Project description** -- one sentence describing the workspace.
   Example: "Multi-tenant smart home management system"

### 1.2 User profile

1. **Role** -- what they do. Goes into CLAUDE.md `[ROLE]`.
   Example: "a backend developer", "a full-stack engineer"
1. **Experience level** -- "experienced" or "learning while developing".
   Goes into CLAUDE.md `[LEVEL]`.
1. **Preferred language** -- for AI conversations and documentation.
   Goes into CLAUDE.md `[YOUR_LANGUAGE]`.
   Example: "English", "简体中文", "日本語"

### 1.3 Tech stack and tooling

1. **Tech stack** -- "Python", "TypeScript", or "mixed".

After selection, present defaults and ask user to confirm or override:

| | Python | TypeScript |
|---|---|---|
| Formatter | `ruff format .` | `prettier --write .` |
| Linter | `ruff check .` | `eslint .` |
| Type checker | `mypy .` | `tsc --noEmit` |
| Test runner | `pytest` | `vitest` |
| Style guide | PEP 8 | Google TypeScript Style Guide |

Say something like:

> Based on your tech stack, here are the suggested tools:
>
> - Formatter: `ruff format .`
> - Linter: `ruff check .`
> - Type checker: `mypy .`
> - Test runner: `pytest`
>
> Want to keep these, or change any of them?

For "mixed", show both sets.

### 1.4 Sub-repositories

Collect repos one at a time in a loop:

1. For each repo, ask:
   - **Name** -- identifier, used as directory name. Example: "sunlite-backend"
   - **Git URL** -- clone URL. Example: `git@github.com:org/repo.git`
   - **Description** -- short description for CLAUDE.md table. Example: "Backend API service"

After each repo, ask: "Add another repo, or done?"

Continue until user says "done" (or equivalent like "完了", "没了", "that's all").

### 1.5 Confirm before executing

Summarize all collected info and ask for confirmation:

```text
Project: my-project
Description: A multi-repo IoT platform
Role: backend developer
Level: learning while developing
Language: 简体中文
Stack: Python (ruff format / ruff check / mypy / pytest)

Repos:
  1. iot-backend (git@github.com:org/iot-backend.git) -- Backend API
  2. iot-docs (git@github.com:org/iot-docs.git) -- Documentation

Proceed with setup?
```

## Phase 2: Scaffold Structure

### 2.1 Check prerequisites

Before making any changes, verify required tools:

```bash
which git && which jq && which openspec
```

If any tool is missing, stop and provide install instructions. Do not proceed
until all tools are available.

### 2.2 Write repos.json

Generate `repos.json` in the workspace root:

```json
{
  "repos": [
    {
      "name": "{name}",
      "url": "{git_url}",
      "path": "repos/{name}"
    }
  ]
}
```

### 2.3 Customize CLAUDE.md

Read the template CLAUDE.md and replace all placeholders. For the complete
mapping of placeholders to collected values, read `references/claude-md-fields.md`.

Key replacements:

- `[ROLE: e.g., ...]` -> collected role
- `[LEVEL: e.g., ...]` -> collected level
- `[YOUR_LANGUAGE: e.g., ...]` -> collected language (appears twice)
- `[YOUR_FORMAT_COMMAND]` -> confirmed formatter
- `[YOUR_LINT_COMMAND]` -> confirmed linter
- `[YOUR_TYPE_CHECK_COMMAND]` -> confirmed type checker
- `[YOUR_TEST_COMMAND]` -> confirmed test runner
- `[PROJECT_STYLE_GUIDE: e.g., ...]` -> style guide based on tech stack
- Repository table in section 1 -> generated from repo list

### 2.4 Clone sub-repos

Run `script/setup` to clone all repositories:

```bash
./script/setup
```

If this fails (e.g., authentication issues, network errors), report the error
and suggest the user fix it manually, then re-run.

## Phase 3: OpenSpec Initialization

### 3.1 Run openspec init

```bash
openspec init
```

### 3.2 Generate config.yaml

Read `references/config-template.yaml` and populate it with:

- `{project_name}` -> collected project name
- `{description}` -> collected description
- `{repos_list}` -> formatted repo list, one per line:

```text
  - **{name}**: {description}
```

Write the result to `openspec/config.yaml`.

## Phase 4: Environment Configuration

For each cloned sub-repo under `repos/`, detect project type and configure:

### 4.1 Python project (pyproject.toml detected)

```bash
cd repos/{name}
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]" 2>/dev/null || pip install -e .
```

If venv creation fails, report the error and continue with the next repo.

### 4.2 TypeScript project (package.json detected)

```bash
cd repos/{name}
# Use bun if bun.lockb exists, otherwise npm
if [ -f bun.lockb ]; then
    bun install
else
    npm install
fi
```

### 4.3 Pre-commit (if .pre-commit-config.yaml exists)

```bash
cd repos/{name}
pre-commit install
```

Skip silently if pre-commit is not installed.

### 4.4 No recognizable project config

If a repo has no pyproject.toml, package.json, or setup.py, skip it and note:

> "No pyproject.toml or package.json found in {name}. You may need to set up
> the environment manually."

### 4.5 VSCode workspace file

Generate `{project-name}.code-workspace`:

```json
{
  "folders": [
    { "path": ".", "name": "Config" },
    { "path": "repos/{name1}", "name": "{Name1}" },
    { "path": "repos/{name2}", "name": "{Name2}" }
  ]
}
```

## Phase 5: Finalize

### 5.1 Version tracking

Write the template commit SHA to `.workspace-init-version` for future updates:

```bash
gh api repos/niracler/dev-config-template/commits/main --jq '.sha' > .workspace-init-version
```

If `gh` is not available, write `unknown` -- update will still work but will
show all template changes instead of just the diff.

### 5.2 Initial commit

Stage and commit all generated/modified files:

```bash
git add repos.json CLAUDE.md openspec/ *.code-workspace .workspace-init-version
git commit -m "chore: initialize workspace"
```

Do NOT push -- let the user decide when to push.

### 5.3 Validate

Run the bundled validation script to verify everything is in place:

```bash
python3 <skill-path>/scripts/validate.py .
```

This checks: repos.json structure, CLAUDE.md placeholder replacement, sub-repo
cloning, OpenSpec config, environment setup, and VSCode workspace file.

If any ERROR-level checks fail, show the output and help the user fix the issues
before proceeding. WARNING-level items are informational -- note them but continue.

### 5.4 Next steps

Display a checklist:

```text
Workspace initialized! Here's what to do next:

1. Open the workspace in VSCode:
   code {project-name}.code-workspace

2. Start Claude Code and try a conversation:
   claude

3. Create your first change:
   /opsx:new

4. Set up project scheduling (optional):
   Ask Claude: "planning init {project-name}"

5. Push when ready:
   git push -u origin main
```

## Common Mistakes

| Error | Cause | Fix |
|-------|-------|-----|
| script/setup fails | jq not installed | `brew install jq` or `sudo apt install jq` |
| openspec init fails | openspec CLI missing | `npm install -g openspec` |
| Clone fails | SSH key not configured | Check SSH access to the git host |
| venv creation fails | Python not installed or wrong version | Install Python 3.10+ |
| CLAUDE.md placeholders remain | Placeholder format mismatch | Check `references/claude-md-fields.md` for exact tokens |
| Update shows no changes | `.workspace-init-version` missing | Run update anyway -- it compares against all template history |

## Update Mode

When the user asks to update the workspace template, follow this flow.

**Trigger phrases**: "update workspace", "update template", "sync template",
"更新工作区模板", "模板有更新吗", "template changed"

### Step 1: Check current version

Read `.workspace-init-version` to get the local template SHA.

```bash
cat .workspace-init-version 2>/dev/null || echo "unknown"
```

### Step 2: Fetch remote template state

```bash
gh api repos/niracler/dev-config-template/commits/main --jq '.sha'
```

If local SHA matches remote HEAD, report "Already up to date" and stop.

### Step 3: Show what changed

Fetch the diff between local version and remote HEAD:

```bash
gh api "repos/niracler/dev-config-template/compare/{local_sha}...main" \
  --jq '.files[] | "\(.status)\t\(.filename)"'
```

If local SHA is `unknown`, fetch the full file list instead and compare
against local files.

Display a summary:

```text
Template updates available (3 files changed):

  modified  script/setup        -- Updated clone logic
  modified  CLAUDE.md           -- Added new section 10
  added     .editorconfig       -- New file

Files that will NOT be touched (your customizations):
  repos.json
  openspec/config.yaml
  CLAUDE.md filled values ([ROLE], [LEVEL], etc.)
```

### Step 4: Apply updates (with confirmation)

Ask the user to confirm before applying.

For each changed template file:

**script/setup, .gitignore, .editorconfig** (non-customized files):

- Fetch the new version and overwrite directly

**CLAUDE.md** (partially customized):

- Fetch the new template version
- Extract the user's current filled values (role, level, language, commands, repo table)
- Apply the new template structure
- Re-fill the extracted values into the new template
- Show the user a diff of structural changes for review

**Files to NEVER touch**:

- `repos.json` -- user's repo configuration
- `openspec/` -- user's change management data
- `repos/` -- sub-repo contents
- `.claude/` -- user's Claude settings and skills

### Step 5: Update version and commit

```bash
gh api repos/niracler/dev-config-template/commits/main --jq '.sha' > .workspace-init-version
git add -A
git commit -m "chore: update workspace template"
```

### Step 6: Validate

Run `scripts/validate.py` to confirm the update didn't break anything.
