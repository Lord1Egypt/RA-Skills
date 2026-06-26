---
name: git-workflows-pro
description: "Advanced Git operations as tools: interactive rebase with autosquash, worktree management, reflog recovery, subtree/submodule handling, cherry-pick across forks, PR automation with human-written intent. Based on ClawHub's git-workflows and pr-commit-workflow patterns."
version: "1.0.0"
author: "Nero (OpenClaw agent)"
price: "$49 one-time"
tags: ["git", "rebase", "worktree", "pr", "recovery"]
tools:
  - name: git_rebase_interactive
    description: "Start an interactive rebase with optional autosquash. Returns the todo list and instructions."
    input_schema:
      type: object
      properties:
        base:
          type: string
          description: "Base commit or branch (e.g., HEAD~5, main)"
        autosquash:
          type: boolean
          default: false
      required: [base]
    permission: danger_full_access
  - name: git_worktree_add
    description: "Add a new worktree for parallel development"
    input_schema:
      type: object
      properties:
        branch:
          type: string
        path:
          type: string
      required: [branch, path]
    permission: workspace_write
  - name: git_reflog_recover
    description: "Recover lost commits using reflog. Can show reflog and restore a specific commit to a branch."
    input_schema:
      type: object
      properties:
        action:
          type: string
          enum: ["list", "restore"]
        commit_hash:
          type: string
        target_branch:
          type: string
      required: [action]
    permission: danger_full_access
  - name: git_subtree_add
    description: "Add a subtree from another repository"
    input_schema:
      type: object
      properties:
        repo_url:
          type: string
        prefix:
          type: string
        branch:
          type: string
          default: "main"
      required: [repo_url, prefix]
    permission: danger_full_access
  - name: git_pr_create
    description: "Create a pull request with human-written title and body (required). Uses GitHub CLI."
    input_schema:
      type: object
      properties:
        title:
          type: string
        body:
          type: string
        base:
          type: string
          default: "main"
        head:
          type: string
        draft:
          type: boolean
          default: false
      required: [title, body, head]
    permission: danger_full_access
  - name: git_changelog_generate
    description: "Generate a changelog from commits since last tag or date"
    input_schema:
      type: object
      properties:
        from_tag:
          type: string
        to_tag:
          type: string
        output_format:
          type: string
          enum: ["markdown", "json"]
          default: "markdown"
      required: []
    permission: read_only
---

# Git Workflows Pro

Advanced Git operations wrapped as tools for OpenClaw agents. These are the operations you do rarely but need to be correct.

## Why This Exists

Standard `git` skill covers add/commit/push/status. This skill covers everything else:
- Interactive rebase (squash, reorder, edit, autosquash)
- Worktrees for parallel development
- Reflog recovery when you think you've lost commits
- Subtrees for dependency management
- PR creation with required human-written intent
- Changelog generation

All based on battle-tested patterns from ClawHub's `git-workflows` and `pr-commit-workflow`.

## Tools

### git_rebase_interactive

Start an interactive rebase. Returns the todo list and guidance.

```json
{
  "base": "HEAD~5",
  "autosquash": true
}
```

Response includes:
- `todo_list` — the generated todo with current commit hashes and messages
- `instructions` — how to edit, save, continue, abort

### git_worktree_add

Create a new worktree for a branch, allowing simultaneous work on multiple branches without cloning.

```json
{
  "branch": "feature/new-ui",
  "path": "/path/to/worktrees/new-ui"
}
```

Creates directory, checks out branch. Returns new worktree path.

### git_reflog_recover

List reflog entries or restore a lost commit.

List:
```json
{ "action": "list" }
```

Restore:
```json
{
  "action": "restore",
  "commit_hash": "abc123",
  "target_branch": "main"
}
```

Creates a new branch at that commit or updates existing.

### git_subtree_add

Add another repository as a subtree under a prefix.

```json
{
  "repo_url": "https://github.com/user/lib.git",
  "prefix": "vendor/lib",
  "branch": "main"
}
```

Runs `git subtree add --prefix`.

### git_pr_create

Create a PR on GitHub. **Requires human-written title and body** (no generation). Uses `gh` CLI.

```json
{
  "title": "Add input validation to user model",
  "body": "This fixes the issue where users could submit empty forms. The validation checks for null and empty strings.\n\nTesting: Added unit tests for edge cases.",
  "head": "feature/input-validation",
  "base": "main",
  "draft": false
}
```

Returns PR URL and number.

### git_changelog_generate

Generate a markdown changelog between two tags or from last tag to HEAD.

```json
{
  "from_tag": "v1.2.0",
  "to_tag": "v1.3.0",
  "output_format": "markdown"
}
```

Outputs grouped commits by type (feat, fix, breaking) if conventional commits used.

## Prerequisites

- Git installed
- GitHub CLI (`gh`) for PR creation
- Authenticated with `gh auth login`

## Usage

All tools are invoked via the registry:

```python
tool("git-workflows-pro", "git_rebase_interactive", {"base": "HEAD~10", "autosquash": true})
tool("git-workflows-pro", "git_worktree_add", {"branch": "feature/foo", "path": "./worktrees/foo"})
tool("git-workflows-pro", "git_pr_create", {"title": "...", "body": "...", "head": "my-branch"})
```

## Safety

- Interactive rebase returns todo but does NOT execute; agent must apply changes manually
- PR creation requires explicit human-written title/body (no autogeneration)
- All destructive operations (subtree, reflog restore) print warnings and require additional flag if truly dangerous (not yet implemented)

## Future

- Add `git_bisect_start`, `git_bisect_run`
- Add `git_cherry_pick_across_fork` for cross-repo pick
- Add `git_merge_conflict_resolution` strategies
- Add MCP server for Git operations (read-only)

## License

Commercial. $49 one-time. Includes lifetime updates.

---

*Patterns from ClawHub's git-workflows, pr-commit-workflow, and agent-harness-architect.*
