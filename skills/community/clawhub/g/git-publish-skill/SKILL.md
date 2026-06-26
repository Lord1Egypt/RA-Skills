---
name: git-publish
description: Publish the current project to a GitHub remote repository. Use this skill whenever the user wants to push code to GitHub, publish to a remote, upload a project to GitHub, set up remote tracking, or says things like "push to github", "publish this repo", "上传到GitHub", "推送到GitHub". This skill handles git initialization, remote setup, auto-commit of uncommitted changes, and pushing.
---

# Git Publish

Push the current project to a GitHub remote repository with a single workflow.

## Workflow

Follow these steps in order:

### Step 1: Resolve the remote URL

Before doing anything else, determine the GitHub repository URL.

1. Read the repo mapping file at `references/repo-map.json` (relative to this skill's directory). This file maps local project paths to their GitHub URLs.
2. Compare the current working directory (the project the user wants to push) against the keys in the mapping.
3. **If a mapping is found:** Use the stored URL. Tell the user: "检测到该项目对应的仓库：<URL>，直接使用。"
4. **If no mapping is found:** Ask the user to provide the GitHub repository URL. Accept formats like:
   - `https://github.com/user/repo.git`
   - `git@github.com:user/repo.git`
   - `https://github.com/user/repo`

   If the user hasn't provided a URL yet, ask: "请提供GitHub仓库地址（例如 https://github.com/user/repo.git）："

### Step 2: Check and initialize Git if needed

Run `git status` to check if the current directory is a Git repository.

**If NOT a Git repository:**
1. Run `git init`
2. Run `git add .` to stage all files
3. Run `git commit -m "Initial commit"`
4. Run `git remote add origin <URL>` to add the remote
5. Run `git branch -M <current-branch>` to rename to the detected branch name

**If already a Git repository:**
1. Check if a remote named `origin` already exists:
   - Run `git remote get-url origin`
   - If the URL differs from what the user provided, ask the user whether to update it
   - If no remote `origin` exists, run `git remote add origin <URL>`

### Step 3: Handle uncommitted changes

Check for uncommitted changes with `git status --porcelain`.

**If there are uncommitted changes:**
1. Run `git diff --cached` to see staged changes
2. Run `git diff` to see unstaged changes
3. Stage all changes: `git add .`
4. Analyze the staged changes and generate a commit message by summarizing the diff. The commit message should:
   - Follow conventional commit format: `type(scope): brief summary`
   - Types: `feat` (new feature), `fix` (bug fix), `chore` (maintenance), `docs`, `refactor`, `style`, `test`
   - Title no more than 50 characters
   - Body lists the affected files and what changed
5. Run `git commit -m "<generated message>"`

**If there are no uncommitted changes:**
Proceed directly to push.

### Step 4: Push to GitHub

1. Detect the current branch: `git branch --show-current`
2. Try normal push first: `git push -u origin <branch>`
3. **If the push fails with a connection error** (e.g., "Could not connect to server", "Failed to connect", timeout, network unreachable), check if the remote URL uses HTTPS protocol:
   - Run `git remote get-url origin` to inspect the current URL.
   - If the URL starts with `https://`, retry up to **3 times** with a short pause between retries.
   - If all 3 HTTPS retries fail, **automatically switch the remote to SSH**:
     - Convert the URL: `https://github.com/user/repo.git` → `git@github.com:user/repo.git`
     - Run `git remote set-url origin git@github.com:user/repo.git`
     - Try pushing again with SSH.
   - If the remote is already using SSH and the connection fails, retry up to 3 times, then report the error to the user.
4. **If the push fails for other reasons** (e.g., divergent histories, non-fast-forward), present the error to the user and ask: "普通推送失败，是否使用强制推送？这可能会覆盖远程仓库的历史。(y/n)"
   - If user agrees: `git push -u origin <branch> --force`
   - If user declines: stop and report the situation

### Step 5: Save the mapping and confirm success

After a successful push:

1. **Save the mapping** — Update `references/repo-map.json` to record the current project path and its GitHub URL, so future pushes for this project won't need to ask for the URL again. Read the file, add or update the entry, and write it back. The key is the absolute path of the project directory, the value is the remote URL.

2. **Confirm success** — Report:
   - The remote URL
   - The branch that was pushed
   - The commit message(s) that were pushed

## Reference files

- `references/repo-map.json` — Local path to GitHub URL mappings. Read this first to resolve the remote URL; update it after each successful push.

## Self-Evolution Mechanism

After each execution of this Skill:

1. Evaluate whether the output achieved the intended goal: **pass / fail**.
2. If it fails, reflect on the cause of failure and append a “failure case + improvement suggestion” to `diary/YYYY-MM-DD.md`.
3. If a certain improvement suggestion is repeatedly mentioned in the most recent three executions, refine it into a formal rule and submit a PR to modify this `SKILL.md`.
