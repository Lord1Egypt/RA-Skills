# Skill Repo Sync — Pushing Local Skill Directories to Existing GitHub Repos

## When to Use

- User asks to sync/push/update all OCAS skill repos
- A skill directory under `~/.hermes/skills/` has uncommitted changes or unpushed commits
- Checking whether local skills are in sync with GitHub

## Prerequisites

- `gh` CLI authenticated (`gh auth status` — should show `<agent-handle>` active)
- Git credential helper is `gh auth git-credential` (check: `git config --global credential.helper`)
- **Do NOT embed tokens in remote URLs.** Use clean URLs like `https://github.com/<agent-handle>/repo.git` and let `gh` handle auth. If a remote URL contains a corrupted/masked token (e.g., `ghp_rB...y5G7`), fix it:
  ```bash
  git remote set-url origin https://github.com/<agent-handle>/repo.git
  ```

## Full Sync Workflow

### 1. Audit All Skill Repos

```python
import os, subprocess

skills_dir = os.path.expanduser("~/.hermes/skills")
ocas_skills = sorted(d for d in os.listdir(skills_dir) if d.startswith("ocas-"))

for skill in ocas_skills:
    path = os.path.join(skills_dir, skill)
    if not os.path.isdir(os.path.join(path, ".git")):
        print(f"⚠ {skill}: no git — needs init")
        continue
    status = subprocess.check_output(["git", "status", "--porcelain"], cwd=path).decode().strip()
    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=path).decode().strip()
    try:
        upstream = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "@{upstream}"], cwd=path, stderr=subprocess.DEVNULL).decode().strip()
        unpushed = subprocess.check_output(["git", "rev-list", f"{upstream}..HEAD", "--count"], cwd=path, stderr=subprocess.DEVNULL).decode().strip()
    except:
        unpushed = "no-upstream"
    if status or (unpushed != "0" and unpushed != "no-upstream"):
        print(f"⚠ {skill}: {'uncommitted' if status else ''} {unpushed + ' unpushed' if unpushed not in ('0','no-upstream') else 'no upstream'}")
    else:
        print(f"✓ {skill}")
```

### 2. Fix Missing Git Repos

For skills with no `.git`:

```bash
cd ~/.hermes/skills/<skill>
git init
git remote add origin https://github.com/<agent-handle>/<repo-name>.git
git fetch origin
# Check if repo exists on GitHub (if ls-remote fails, create it first with gh repo create)
git branch -m master main   # rename if needed
```

### 3. Fix Broken or Missing Remotes

For skills with `.git` but no remotes, or corrupted token in URL:

```bash
cd ~/.hermes/skills/<skill>
# Remove broken remote if present
git remote remove origin
# Add clean URL (no embedded token)
git remote add origin https://github.com/<agent-handle>/<repo-name>.git
git fetch origin
```

### 4. Fix Detached HEAD / Stuck Rebase

```bash
# If mid-rebase:
git rebase --abort

# If truly detached (shows "(no branch)"):
git checkout -b main
# or if already on a branch that's ahead of origin:
git push -u origin <branch-name>
```

### 5. Commit and Push

```bash
git add -A
git commit -m "update: sync local changes (N files)"
```

### 6. Push — Handle Unrelated Histories

**The most common scenario for skill repos:** local and remote were initialized separately → "refusing to merge unrelated histories" error.

**Resolution:** Force push local. The local skill directory is the source of truth:

```bash
git push origin main --force
```

Do NOT attempt `git pull --allow-unrelated-histories` — it creates messy merge commits. The local directory is the real skill; the remote stub is a sync target.

### 7. Verify Clean State

```bash
# All repos should show:
git status --porcelain          # empty
git rev-list @{upstream}..HEAD --count   # 0
git rev-parse --abbrev-ref @{upstream}  # origin/main
```

## Edge Cases

| Situation | Fix |
|-----------|-----|
| Token embedded in remote URL is corrupted/masked | `git remote set-url origin https://github.com/<agent-handle>/repo.git` |
| Local branch is `master`, remote is `main` | `git branch -m master main && git push -u origin main --force` |
| Detached HEAD after interrupted rebase | `git rebase --abort`, then checkout/create branch |
| Repo doesn't exist on GitHub yet | `gh repo create <agent-handle>/repo-name --private --description "..."` then add remote and push |
| Skill reappears as uncommitted after push | A concurrent process may be generating files — commit and push again, then verify |

## Repo Name Mapping

Most `ocas-<name>` skills map to GitHub repos named `<name>`:
- `ocas-bones` → `bones`, `ocas-bower` → `bower`, etc.
- `ocas-spot` → `ocas-spot` (exception — full name)
- All others: strip the `ocas-` prefix

## Monorepo Skills (source: points to a subdirectory)

Some skills have `source:` pointing to a subdirectory within a monorepo, NOT a standalone repo. Example:
- `util-buy` → `source: https://github.com/<agent-handle>/utilities/tree/main/buy`
- `util-wiki` → `source: https://github.com/<agent-handle>/utilities/tree/main/wiki`

**CRITICAL:** Before creating a git repo for a skill, ALWAYS check the `source:` field in frontmatter. If it points to a monorepo subdirectory:
1. Do NOT create a standalone repo
2. Do NOT add `.git` to the local skill directory
3. Sync changes by copying files to the monorepo subdirectory and pushing the monorepo
4. The monorepo is the source of truth; local skill directories are copies

### Monorepo Sync Procedure

```bash
# 1. Clone the monorepo (if not already)
git clone https://github.com/<agent-handle>/utilities.git /tmp/utilities

# 2. Copy skill files to monorepo subdirectory
cp ~/.hermes/skills/util-buy/SKILL.md /tmp/utilities/buy/SKILL.md
rsync -a --delete ~/.hermes/skills/util-buy/references/ /tmp/utilities/buy/references/

# 3. Commit and push the monorepo
cd /tmp/utilities
git add -A
git commit -m "sync: update <skill-name> from local"
git push origin main
```

### Detecting Monorepo Skills

```python
import yaml, os, glob

skills_dir = os.path.expanduser("~/.hermes/skills")
for path in glob.glob(f"{skills_dir}/*/SKILL.md"):
    with open(path) as f:
        content = f.read()
    parts = content.split("---")
    if len(parts) >= 3:
        fm = yaml.safe_load(parts[1])
        source = fm.get("source", "")
        name = fm.get("name", os.path.basename(os.path.dirname(path)))
        if "/tree/" in source or "/blob/" in source:
            print(f"MONOREPO: {name} → {source}")
```

### Pitfall: Creating Standalone Repos for Monorepo Skills

The most common failure: agent sees "no .git in skill directory" → creates standalone repo → violates the skill's declared source. **Always read `source:` before any git operation.** (2026-06-22, from util-* 10khr sync that created 13 incorrect standalone repos.)

## Pitfalls

- **Don't use `--force-with-lease`** for skill syncs. Use plain `--force`. The remote is a sync target, not a collaborative branch.
- **Don't clone to a temp directory.** Work directly in `~/.hermes/skills/<skill>/` — that's where the skill is loaded from.
- **Don't try to merge unrelated histories.** Force push clean.
- **If a skill directory has no `.git`**, check whether the GitHub repo exists before initializing locally — you may need to pull first.
- **Skills can reappear as uncommitted** if a concurrent process modifies them between audit and commit. Just re-commit and push.