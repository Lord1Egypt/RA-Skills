# ghq Clone

Workflow for automatically registering in SourceGit after `ghq get`.

## When to Use

- User runs `ghq get <url>`
- User mentions "ghq clone", "ghq get", "clone repository"
- Skill arguments contain URL (https:// or git@)

## Workflow

### Step 0: Pre-Clone Check (verify existing repository)

**CRITICAL**: Check for existing repository before running ghq get

#### 0-1. Check existing paths

Extract repo name from URL and check related paths:

```bash
# 1. ghq default repository (ghq checks automatically - skip)
# ~/ghq/host/group/repo

# 2. Check bare repository (ghq does NOT check this!)
ls ~/ghq/host/group/repo.git 2>/dev/null

# 3. Check existing worktree paths (paths registered in SourceGit)
# ~/works/group/repo format
```

#### 0-1a. Handle broken clone remnants

If a directory with only an empty `.git` remains from a previously failed clone, `ghq get` will skip it as "exists":

```bash
# Detect broken repository
cd ~/ghq/host/group/repo && git status 2>&1
# → "fatal: not a git repository" → broken state

# Move broken directory and re-clone
mv ~/ghq/host/group/repo ~/.claude/.bak/repo_$(date +%Y%m%d)
```

#### 0-2. When bare repository exists

If a bare repository (`~/ghq/.../repo.git`) is found:

1. **Check status**: Verify connected worktrees and changes
2. **Convert if needed**: Can convert to regular repository using `migrate` topic

#### 0-3. Check SourceGit registration path

Check if existing repository is registered in SourceGit:

```bash
# Search for repo name in preference.json
grep -l "repo-name" ~/Library/Application\ Support/SourceGit/preference.json
```

If a registered path is found:

1. Check for changes at that path
2. Check if `.git` is a file (recommend conversion if it's a worktree)

### Step 1: Clone with ghq

After pre-check passes:

```bash
ghq get <url>
```

Parse cloned path from output:

- Extract path from `clone https://... -> /path/to/repo` format

### Step 2: Parse Repository Info

Extract host/group/repo from URL:

- `https://github.com/org/repo.git`
  - Host: `github.com`
  - Group: `org`
  - Repo: `repo`

### Step 3: Check SourceGit Status

```bash
pgrep -x SourceGit
```

- **Running**: **Skip** SourceGit registration and report clone path only. When SourceGit exits, it overwrites preference.json on disk with its in-memory version, so edits made while running will be lost.
- **Not running**: Proceed with registration

### Step 4: Read preference.json

```bash
cat ~/Library/Application\ Support/SourceGit/preference.json
```

### Step 5: Find or Create Group

Find group in RepositoryNodes:

1. Search by group name (e.g., `org-name`)
2. If not found, create new group:

```json
{
  "Id": "uuid-v4",
  "Name": "org-name",
  "Bookmark": 0,
  "IsRepository": false,
  "IsExpanded": true,
  "Status": null,
  "SubNodes": []
}
```

### Step 6: Add Repository to Group

Add to the group's SubNodes:

```json
{
  "Id": "/Users/user/ghq/github.com/org/repo",
  "Name": "repo",
  "Bookmark": 0,
  "IsRepository": true,
  "IsExpanded": false,
  "Status": null,
  "SubNodes": []
}
```

### Step 7: Save and Report

Edit preference.json with Edit tool and report result:

```
Clone and SourceGit registration complete:
- Path: ~/ghq/github.com/org/repo
- Group: org

Will be reflected when SourceGit is restarted.
```

## Group Naming Strategy

| URL Host    | Group Name                          |
| ----------- | ----------------------------------- |
| github.com  | github.com > org hierarchy          |
| Other       | host > group hierarchy              |

## GitHub Multi-Account Clone

When `gh auth switch` bug prevents active account switching, specify `GH_TOKEN` directly for cloning:

```bash
# 1. Clone with target account's token
TOKEN=$(gh auth token --user <GITHUB_USER> 2>/dev/null)
git clone "https://<GITHUB_USER>:${TOKEN}@github.com/org/repo.git" ~/ghq/github.com/org/repo

# 2. Always remove token from origin after cloning
git -C ~/ghq/github.com/org/repo remote set-url origin "https://github.com/org/repo.git"
```

**gh auth switch bug detection**:
```bash
gh auth switch --user <GITHUB_USER> 2>&1  # "Switched" message output
gh api user --jq '.login'                  # still shows other user → bug
```

In this case, `ghq get` uses the default account token and fails. Use `git clone` + direct `GH_TOKEN` instead.

## No Questions Asked

**Important**: This workflow proceeds automatically without user confirmation.

- ghq get succeeds → SourceGit registration (only when SourceGit is not running)
- Group doesn't exist → auto-create
- **SourceGit is running → skip registration** (in-memory content overwrites disk on exit)
