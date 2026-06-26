---
name: git-cli
description: Helper for using the Git CLI to inspect, stage, commit, branch, and synchronize code changes. Use when the user wants to understand or perform Git operations from the command line, including safe status checks, diffs, branching, stashing, and syncing with remotes.
---

# Git CLI Helper

This skill explains how to use the **Git command line** for everyday development tasks in a repository.

## When to Use

Use this skill when:

- The user wants to know “what changed” in the working tree.
- The user wants to stage, unstage, or commit files.
- The user wants to create or switch branches.
- The user wants to pull from or push to a remote.
- The user needs help with stashing, viewing history, or inspecting diffs.

## Requirements

- Git is installed and available on the PATH (for example `git --version` succeeds).
- The current directory is either:
  - Inside a Git repository, or
  - A location where the user intends to run `git init` or `git clone`.

When uncertain, suggest the user run:

```bash
git status
```

to see whether the current folder is a Git repository.

## Safety Guidelines

- Prefer **read-only commands** first (`git status`, `git diff`, `git log`) before suggesting changing commands.
- Avoid destructive suggestions such as:
  - `git reset --hard`
  - `git clean -fdx`
  - `git push --force`
- Only mention or recommend such commands if the user explicitly asks and understands the risk.

## Common Workflows

### 1. Inspect current state

Check what has changed and whether there are untracked files:

```bash
git status
```

See detailed changes in the working tree:

```bash
git diff           # unstaged changes
git diff --staged  # staged (to-be-committed) changes
```

### 2. Stage and unstage changes

Stage a specific file:

```bash
git add path/to/file
```

Stage all tracked and untracked changes:

```bash
git add .
```

Unstage a file (keep changes in the working tree):

```bash
git restore --staged path/to/file
```

### 3. Create commits

Create a commit with a message:

```bash
git commit -m "short, descriptive message"
```

If the user prefers a multi-line message, suggest:

```bash
git commit
```

which opens their editor.

### 4. Branching and switching

Create and switch to a new branch:

```bash
git checkout -b feature/my-branch
```

Switch to an existing branch:

```bash
git checkout main
```

List local branches:

```bash
git branch
```

### 5. Synchronize with remote

If the repository already has a remote (for example `origin`):

- Fetch latest remote data:

```bash
git fetch
```

- Pull latest changes into current branch:

```bash
git pull
```

- Push the current branch and set upstream:

```bash
git push -u origin <branch-name>
```

For subsequent pushes on the same branch:

```bash
git push
```

### 6. Cloning and initializing

Clone an existing remote repository:

```bash
git clone <repo-url>
```

Initialize a new repository in the current folder:

```bash
git init
```

Optionally add a remote:

```bash
git remote add origin <repo-url>
```

### 7. Stashing work-in-progress

When the user needs to temporarily put aside local changes:

```bash
git stash
```

List stashes:

```bash
git stash list
```

Apply and keep the top stash:

```bash
git stash apply
```

Apply and drop the top stash:

```bash
git stash pop
```

## Viewing History and Blame

Show recent commits (compact format):

```bash
git log --oneline --decorate --graph --all
```

See who last changed each line of a file:

```bash
git blame path/to/file
```

## Troubleshooting Tips

- If Git reports “not a git repository”, suggest:
  - Running commands in the correct project folder, or
  - Initializing with `git init` (if appropriate), or
  - Cloning with `git clone <repo-url>`.
- If a push is rejected because the remote has new commits, suggest:
  - `git pull --rebase` or `git pull` (depending on the team’s policy), then retry `git push`.
- If there are merge conflicts, explain:
  - The user must edit the conflicted files,
  - Mark conflicts as resolved by `git add`,
  - Then complete the merge or rebase with `git commit` or `git rebase --continue`.

