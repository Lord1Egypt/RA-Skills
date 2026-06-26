---
name: git-commit
description: >
  Smart git commit with remote sync, amend intelligence, and conventional commits.
  Use when the user asks to commit changes, stage and commit, "/commit", save work to git,
  push code, or sync and commit. Automatically checks remote for new commits before committing
  and syncs via rebase if needed. Analyzes whether current changes should amend the previous
  commit (with strict same-thing criteria). Generates conventional commit messages with
  agent/model info in the footer. TRIGGER this skill whenever the user mentions committing,
  staging changes, or saving work to version control — even if they just say "commit this"
  or "save my changes".
license: MIT
allowed-tools: Bash
---

# Smart Git Commit

Commit local changes safely: sync remote → analyze diff → stage → amend or new commit → push (if asked).

---

## Step 1 — Remote Sync Check

```bash
git fetch origin 2>&1
```

Then check if the remote branch has commits the local branch doesn't:

```bash
git status -sb          # shows tracking info, e.g. ## main...origin/main [behind 3]
git rev-list HEAD..@{u} --count 2>/dev/null   # 0 means in sync
```

**If the remote is ahead (count > 0):** sync via rebase:

```bash
git pull --rebase origin <current-branch>
```

Watch the output for conflict markers. If the rebase fails or conflicts are reported:

```bash
git rebase --abort
```

Then stop everything and tell the user:

> ⚠️ **Remote conflict — commit aborted**
>
> Remote has new commits that conflict with your local changes. The rebase was aborted automatically to keep your work safe.
>
> **To see which files conflict:**
> ```bash
> git diff --name-only --diff-filter=U
> ```
>
> **To resolve and continue:**
> ```bash
> # 1. Re-run the rebase
> git pull --rebase
>
> # 2. Open each conflicted file and fix the markers:
> #    <<<<<<< HEAD        ← your local changes
> #    (your code)
> #    =======
> #    (remote code)
> #    >>>>>>> abc1234     ← remote commit
>
> # 3. Stage each resolved file
> git add <file1> <file2> ...
>
> # 4. Continue the rebase
> git rebase --continue
>
> # 5. Repeat steps 2–4 for each conflicted commit, then run /commit again
> ```
>
> **To abort and restore your original state:**
> ```bash
> git rebase --abort   # already done — your branch is back to where it was
> ```

Do not proceed with staging or committing. Wait for the user to resolve.

If the rebase succeeds (no conflicts), continue.

---

## Step 2 — Inspect Staged / Unstaged Changes

```bash
git status --porcelain   # list of changed files
git diff --staged        # staged diff
git diff                 # unstaged diff
```

If nothing is staged and there are unstaged changes, stage everything that looks relevant (avoid committing secrets like `.env`, `*.pem`, `credentials.*`):

```bash
git add -A               # or specific files — use judgment
```

If there is truly nothing to commit, tell the user and stop.

---

## Step 3 — Amend Analysis (Strict Criteria)

Compare the current staged diff against the **last commit** to decide: new commit or `--amend`?

```bash
git log -1 --format="%H %s"   # last commit hash + subject
git show --stat HEAD           # files changed in last commit
git show HEAD                  # full diff of last commit
git log origin/<branch>..HEAD --oneline  # commits not yet pushed
```

**Only amend if ALL of the following are true:**

1. The last commit has **not been pushed** to the remote (it appears in `git log origin/<branch>..HEAD`).
2. The current staged change has the **same commit type** (feat/fix/docs/…) as the last commit.
3. The current staged change affects the **same scope** (same module/area) as the last commit.
4. The change is a **direct continuation or correction** of the exact same atomic operation — e.g., a typo fix in code just added, or a file that was accidentally omitted from the last commit.

**Do NOT amend in any of these cases:**

| Situation | Why |
|---|---|
| Last commit is `feat:`, this is `fix:` | Different type → different thing |
| Last commit is `feat:`, this adds tests | `test:` is a separate concern |
| Last commit is `feat:`, this reformats code | `style:` is a separate concern |
| Last commit is `feat:`, this updates config/CI | Different type |
| Last commit has already been pushed | Rewriting published history is dangerous |
| Scope differs (e.g., `auth` vs `user`) | Different areas |

When in doubt, create a **new commit**. The amend path is the exception, not the rule.

---

## Step 4 — Generate Commit Message

Analyze the staged diff to determine:

- **type**: What kind of change? (see table below)
- **scope** (optional): Which module, component, or area?
- **description**: One-line summary — imperative mood, present tense, under 72 chars
- **body** (optional): Why this change? What problem does it solve? Include only if non-obvious.
- **footer**: Breaking changes + issue refs + agent/model info

### Commit Types

| Type | Use for |
|------|---------|
| `feat` | New feature or behavior |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace (no logic change) |
| `refactor` | Code restructure (no feature or fix) |
| `perf` | Performance improvement |
| `test` | Add or update tests |
| `build` | Build system, dependencies |
| `ci` | CI/CD, pipeline configuration |
| `chore` | Maintenance, misc tooling |
| `revert` | Revert a prior commit |

### Footer — Agent & Model Info

Always append agent and model info in the footer. Use what's available from the environment:

```
Co-authored-by: Claude <noreply@anthropic.com>
AI-model: claude-sonnet-4-6
```

If the exact model ID is available (from the system context), use it. Otherwise use the family name.

### Full Format

```
<type>[optional scope]: <description>

[optional body — explain WHY, not WHAT]

[breaking change if any]
[issue refs if any]
Co-authored-by: Claude <noreply@anthropic.com>
AI-model: <model-id>
```

---

## Step 5 — Execute Commit

**New commit:**

```bash
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<optional body>

Co-authored-by: Claude <noreply@anthropic.com>
AI-model: <model-id>
EOF
)"
```

**Amend last commit** (only when criteria in Step 3 are fully met):

```bash
git commit --amend -m "$(cat <<'EOF'
<updated message>

Co-authored-by: Claude <noreply@anthropic.com>
AI-model: <model-id>
EOF
)"
```

---

## Step 6 — Push (only if user asked)

If the user explicitly asked to push:

```bash
git push origin <current-branch>
```

Never force-push to `main`/`master`. If a force push is needed, confirm with the user first.

---

## Safety Rules

- Never commit secrets: `.env`, `*.pem`, `credentials.*`, `*.key`
- Never skip hooks with `--no-verify` unless the user explicitly asks
- Never use `git reset --hard` or other destructive commands without explicit user request
- If a pre-commit hook fails: fix the issue, re-stage, create a **new** commit (never `--amend` after hook failure)
- If the rebase produces conflicts: `git rebase --abort` and stop — do not proceed

---

## Example Messages

```
feat(auth): add JWT refresh token rotation

Tokens now rotate on each use to limit exposure window.
Refresh tokens are stored hashed in Redis with a 7-day TTL.

Co-authored-by: Claude <noreply@anthropic.com>
AI-model: claude-sonnet-4-6
```

```
fix(api): handle null response from payment gateway

Gateway returns null instead of an error object on timeout;
guard added to prevent unhandled exception in checkout flow.

Closes #482

Co-authored-by: Claude <noreply@anthropic.com>
AI-model: claude-sonnet-4-6
```

```
docs: update contributing guide with commit conventions

Co-authored-by: Claude <noreply@anthropic.com>
AI-model: claude-sonnet-4-6
```
