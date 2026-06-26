---
name: gitrama
description: >
  Git history intelligence powered by AI. Use when the user asks about git history,
  commit messages, branch names, repo insights, code archaeology, or wants to understand
  what happened in a codebase. Triggers on: "git history", "commit message", "branch name",
  "who changed", "what happened", "repo summary", "code archaeology", "semantic search git",
  "generate commit", "smart commit", "git log analysis", "contributor insights".
version: 1.0.0
homepage: https://gitrama.ai
metadata:
  openclaw:
    emoji: "🌿"
    requires:
      bins:
        - git
        - pip
      binsAnyOf:
        - python3
        - python
    install:
      pip:
        - gitrama
---

# Gitrama — Git History Intelligence

Gitrama is a CLI tool that brings AI-powered semantic search and intelligence to your Git history. It includes **AskGIT**, an embedded AI assistant that understands your entire repo context.

All AI processing is handled server-side via `api.gitrama.ai`. No API keys required — just install and use.

## Capabilities

### 1. AskGIT — Semantic Git History Chat
Ask natural language questions about your repository:
- "What changes were made to the authentication module last month?"
- "Who has been the main contributor to the API layer?"
- "Summarize the last 20 commits"
- "What breaking changes happened between v1.0 and v2.0?"

**Command:** `gtr chat`

AskGIT automatically gathers context from 10 git subprocess calls (branch info, recent commits, diffs, contributors, file tree) and sends that context to api.gitrama.ai for intelligent analysis.

### 2. Smart Commit Message Generation
Generate conventional commit messages from staged changes:
- Analyzes your `git diff --staged`
- Produces properly formatted conventional commits (feat:, fix:, docs:, etc.)
- Respects your project's commit conventions

**Command:** `gtr commit`

### 3. Branch Name Generation
Generate clean, descriptive branch names from a task description:
- Follows git branch naming conventions
- Includes type prefixes (feature/, bugfix/, hotfix/)
- Keeps names concise and meaningful

**Command:** `gtr branch`

### 4. Git Log Analysis & Repo Insights
Get AI-powered analysis of your repository:
- Contributor activity patterns
- Code change frequency by area
- Release history summaries
- Technical debt indicators

**Command:** `gtr chat` then ask about repo insights

## Installation

Gitrama is distributed via PyPI:

```bash
pip install gitrama
```

Verify installation:

```bash
gtr version
```

## Configuration

No API keys or configuration needed. Gitrama connects to api.gitrama.ai for all AI processing out of the box.

Optional configuration available via:

```bash
gtr config
```

## Usage Examples

When the user asks about git history or repo context, run the appropriate gitrama command:

```bash
# Start an interactive chat about the repo
gtr chat

# Generate a commit message for staged changes
gtr commit

# Generate a branch name
gtr branch "add user authentication with OAuth"

# Quick shortcuts
gtr c   # alias for commit
gtr b   # alias for branch
gtr ch  # alias for chat
```

## Data Flow

```
Local CLI (gtr) → gathers git context locally → POST to api.gitrama.ai → AI response
```

- Git context (commits, diffs, branch info) is collected locally via git subprocess calls
- Context is sent to api.gitrama.ai for AI processing
- No API keys are stored or required on the user's machine
- No sensitive IP runs locally — the intelligence layer lives server-side

## Important Notes

- Gitrama must be run inside a git repository
- AskGIT maintains a 40-message conversation history for multi-turn context
- The tool collects repo context automatically — no manual configuration needed
- Repository data sent to api.gitrama.ai is used only for generating responses and is not stored

## Error Handling

If `gtr` is not found after install:
```bash
# Ensure pip scripts are on PATH
python3 -m gitrama --version
```

If connection errors occur:
```bash
# Verify api.gitrama.ai is reachable
curl -s https://api.gitrama.ai/health
```

## Links

- Website: https://gitrama.ai
- PyPI: https://pypi.org/project/gitrama/
