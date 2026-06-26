# Identity and Auth

`gh` CLI is the first-choice GitHub interface. Owner-based commit-author identity mapping. `gh auth refresh` scope management. `GH_TOKEN` env fallback for org-repo 404.

## When to use

- Before every commit on a repo whose remote owner you have not verified this session
- Before every PR creation / push that requires push authorization
- On 404 / 403 from `gh repo view`, `gh issue create`, `gh pr create`, etc.
- When switching between multiple `gh auth` accounts (multi-account workflows)
- When invoking `gh run`, `gh workflow`, `gh release`, `gh copilot` and getting a scope error

## gh CLI first (HARD STOP)

**For ALL GitHub-related work (PR view, review, comment, merge, etc.), `gh` CLI is the first-choice tool.** Forbid escape-to-browser-agent (`browser_subagent`) for routine GitHub tasks.

| # | Don't | Do |
|---|-------|-----|
| 1 | Invoke a browser agent to verify / consolidate PR review | Combine `gh pr view`, `gh api`, `gh pr checks` to extract data from CLI |
| 2 | Skip CLI on the subjective belief "the browser is more accurate" | `gh` CLI is the most reliable source — authentication and context are preserved. Consider the browser ONLY when CLI fails |
| 3 | Wait for browser-rendering of a simple data query (e.g., comment list) | `gh api` with JSON parse. Much faster, fewer tokens |

The browser agent is reserved for **situations CLI cannot handle** (e.g., complex GUI configuration, visual layout verification), with user pre-approval.

## Owner-based commit-author identity mapping (HARD STOP)

**`gh` account mapping applies not only to push / PR auth but also to commit-author identity.** When committing to an org repo (PUBLIC included), if the `gh` active account is a different identity (e.g., leftover from a different repo's work), the commit author gets stamped wrong and the wrong identity becomes permanent in PUBLIC history.

**Before commit: switch `git author identity` + `gh account` to match the repo owner.**

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Commit to an org repo with the active account left from a previous workflow → wrong author stamped | Before commit: `git -C <repo> config user.name "<name-for-owner>" && git -C <repo> config user.email "<email-for-owner>"` |
| 2 | Push / PR uses the right identity but commit author left unchanged | Author + committer + push + PR all use the same identity. PUBLIC history permanently records the author, so consistency is mandatory |
| 3 | "Auth is needed only at push time" reasoning | Commit author is stamped at commit time. An already-wrong author can only be fixed via amend / rebase |
| 4 | Commit without checking the repo owner | Right before commit, run `git remote get-url origin` to confirm the owner → set identity per the owner-identity mapping |

### Self-check (every time before commit — owner-based)

1. `git -C <repo> remote get-url origin` — determine the owner
2. Look up the owner in your **owner-identity mapping table** (workspace-specific; live in `~/.agents/.claude/rules/identity.md` or a workspace `.claude/rules/identity.md`, NOT in this generic skill)
3. Set `git config user.name` + `user.email` + `gh auth switch` (or inject `GH_TOKEN`) to match the owner mapping
4. If `git config user.email` does not match the mapping, fix BEFORE commit. If already committed wrong AND **unpushed**: `git commit --amend --reset-author` (no force-push needed)
5. PR creation also uses the matched account (`gh pr create` consumes the active account → pre-switch via `gh auth switch` or inject `GH_TOKEN`)

### Self-check (every time before push / PR creation — push-identity track)

**Commit-author identity ≠ PR-creator identity.** Commit `author` is stamped from `git config user.*` at commit time and is independent from the `gh` account or SSH key used at push or PR-create time. GitHub assigns **PR `author` = the gh account that runs `gh pr create`** (or, on the web UI, whichever account is signed in when "Create pull request" is clicked) — *not* the commit's `author` field, and not "whoever pushed" as a separate step. In the standard CLI flow that account is the one whose token/SSH key also authorized the immediately preceding push, so push identity and PR author usually coincide, but the canonical source is the PR-create action, not the push by itself. A wrong PR-create identity records a wrong PR author and **cannot be fixed by `git commit --amend`** — the PR `author` is immutable on GitHub once recorded.

1. `git -C <repo> remote get-url origin` — determine the owner (same step as commit track)
2. Look up the owner in the owner-identity mapping table → `<expected gh account>`
3. **Primary-source check** — confirm the active push identity matches:
   - `gh auth status` → identify the `Active account` line. It must equal `<expected gh account>`
   - `gh api user --jq '.login'` → the response login must equal `<expected gh account>`
   - SSH-only repos: `ssh -T git@github.com 2>&1 | grep -oE 'Hi [^!]+!'` → the matched name must equal `<expected gh account>`
4. Mismatch → `gh auth switch --user <expected>` (or inject `GH_TOKEN="$(gh auth token --user <expected>)"`), and for SSH ensure `core.sshCommand` or `ssh-add -l` points to the key registered on `<expected gh account>`
5. **Only after Steps 3-4 pass** → run `git push` or `gh pr create`
6. If push already happened with the wrong identity → the PR `author` is immutable. Options: (a) close the wrong-author PR + reopen from the correct account on a fresh branch; (b) accept the wrong author (PR `author` shows on the PR forever)

### Don't / Do (push-identity track)

| # | Don't | Do |
|---|-------|-----|
| 1 | Trust that `git config user.email` matches → assume push identity is also right | Run `gh api user --jq '.login'` separately. Commit identity and push identity are independent tracks |
| 2 | Push first, "fix the author later via `--amend`" | `--amend --reset-author` only fixes commit author. PR `author` (GitHub user that pushed) is immutable once the PR is created |
| 3 | Skip the SSH-key check when remote is `git@github.com:...` | SSH-only repos route through the loaded key's GitHub account. `ssh -T` test must return the expected name |
| 4 | Switch `gh auth` after `gh pr create` already ran | `gh pr create` consumes the active account at call time. Switch BEFORE the call |
| 5 | Multi-account setup: rely on memory ("I think DrumRobot is active") | Always run `gh auth status` + `gh api user` immediately before push/PR-create. The `gh` active account can drift between sessions |

### Owner-identity mapping (defined elsewhere)

The actual `<owner> → <git author identity>` + `<gh account>` mapping table is **workspace-scoped**, not part of this skill. Maintain it in `~/.agents/.claude/rules/identity.md` (per-user) or `<workspace>/.claude/rules/identity.md` (per-project). Example shape (the specifics belong elsewhere):

```text
| Owner           | git author identity                   | gh account     |
| --------------- | ------------------------------------- | -------------- |
| org-A           | Identity-for-org-A <email-A@host>     | gh-account-A   |
| org-B           | Identity-for-org-B <email-B@host>     | gh-account-B   |
```

### Failure pattern

See failed-attempts.md HOT entry "PUBLIC repo commit with leftover account identity" — a PUBLIC-repo commit landed with the previous workspace's account as author. Caught while still unpushed and corrected via `git commit --amend --reset-author`.

## `gh` CLI scope (by task)

### Common scope cheat sheet

| Task | Required scopes | Note |
|------|----------------|------|
| Read public repo | `repo` (or `public_repo`) | |
| Private repo (org) | `repo`, `read:org` | Required for org-owned private repos |
| PR create / edit / merge | `repo` | |
| Issue create / edit / comment | `repo` | |
| GitHub Actions workflow query / dispatch | `repo`, `workflow` | `gh run`, `gh workflow` |
| Release create / upload | `repo` | |
| Discussions | `repo`, `read:discussion` | |
| Codespaces | `codespace` | |
| Copilot config (e.g., reviewer add) | `copilot` | |
| User email read | `user:email` | |
| Gist create / edit | `gist` | |
| Pages management | `repo`, `pages` | |

**Recommended combined scope (Ralph / autonomous workflows)**: `repo,read:org,workflow,copilot`

### Permission-grant batching rule (HARD STOP)

**On 404 detection or any "scope insufficient" instruction, refresh the FULL recommended scope set in ONE `-s`-flag call. Forbid splitting into multiple browser auth prompts.**

| # | Don't | Do |
|---|-------|-----|
| 1 | Refresh only `repo,read:org` first, then later refresh `copilot` separately → user opens browser twice | On the first scope-shortage detection, refresh the **entire** recommended scope set with a single `--scopes "repo,read:org,workflow,copilot"` call |
| 2 | Multi-account scope refresh done one account at a time with inefficient `switch` repetition | Minimize the number of `gh auth switch` + browser auth-window openings via a streamlined design that supports one-click bulk apply |

```bash
# Refresh including copilot in a single call
env -u GITHUB_TOKEN gh auth refresh --user <account> --scopes "repo,read:org,workflow,copilot"
```

## Org-repo 404 troubleshooting (self-resolve in order)

Run these in order BEFORE asking the user:

1. **Account switch check**: `gh auth status` → confirm the active account has access to the org
2. **Scope check**: `gh auth status` output's "Token scopes" — verify against the table above. If missing scope → `gh auth refresh --user <account> --scopes "..."`
3. **`GH_TOKEN` env injection (most frequent fix)**: even after `gh auth switch`, some commands fail to honor the active account due to a known gh CLI bug. Use this pattern to bypass:

   ```bash
   GH_TOKEN="$(gh auth token --user <account>)" gh repo view <org>/<repo>
   ```

   If this succeeds, your scope / membership is fine — it was a gh CLI internal issue, no user intervention needed.
4. **Org membership confirmation**: if steps 1-3 all fail with 404, ask the user about membership status

## Self-check (before any gh-auth-requiring command)

1. Is the target an org repo? — `gh repo view <org>/<repo> --json owner -q '.owner.login'`
2. If org → confirm the active `gh auth status` user has access
3. If 404 → run the troubleshooting list above (steps 1 through 4) before asking the user
4. About to refresh scopes? → use the **single** combined scope refresh (don't split into multiple browser prompts)

## Related topics

- `merge` — merge requires `repo` scope for write operations
- `pr` — PR creation requires `repo` scope; check `dependencies` for `addBlockedBy` GraphQL mutations
- `push-guards` — `gh run list` (used in force-push CI status check) requires `repo`, `workflow` scope
