---
name: implement
description: "Build a feature in an isolated worktrunk worktree, commit, and open a draft PR. Use whenever the user asks to implement, build, add, or fix something that touches code — e.g. '/implement', 'implement X', 'build X', 'add X', 'fix X', 'let's build it', 'ship it', 'drop this in', 'go code it up'. Skip for questions, explanations, research, and trivial one-line docs/config edits. Skip if already inside a worktrunk worktree (just implement directly)."
user-invocable: true
---

# Implement: worktrunk-isolated build, draft PR out

A lean implementation flow. You've already discussed what to build in the conversation — this skill takes it from there: isolate to a worktree, implement, commit, push, open a draft PR. Stay in the worktree so the user can iterate on review feedback without switching. The PR is the merge path; `wt merge` is never used.

## When NOT to invoke this skill

- Questions, explanations, code reading, research
- Trivial one-line edits to config/docs in the current repo (just edit in place)
- User explicitly says "do it here" / "don't branch"
- Already inside a worktrunk worktree (just implement + commit directly, no new worktree)
- Not in a git repo
- Change is genuinely multi-file with unclear scope and needs real architecture discussion — suggest the heavier `/worktree-dev:worktree-dev` flow instead

## Workflow

### 1. Scope check (one paragraph, no questions unless truly ambiguous)

State in one sentence what you're about to build. Trust the conversation context — don't open an AskUserQuestion loop.

- If the request is genuinely ambiguous (multiple valid interpretations, not just underspecified), ask one clarifying question inline and stop.
- If the change involves a **non-trivial design choice**, sketch 2–3 options with tradeoffs in a few lines and let the user pick before proceeding (per the user's brainstorm-first preference).
- If scope feels too big for this lean flow — multi-subsystem, needs real architecture work — recommend `/worktree-dev:worktree-dev` and stop.

### 2. Create the worktree

Pick a descriptive branch name. Use repo convention prefixes (`fix/`, `add/`, `feat/`, `chore/`, `refactor/`, `perf/`) — check `git log --oneline -10` if unsure.

```bash
wt switch --create <branch-name> --yes
```

This switches your working directory into the new worktree.

### 3. Implement

- Read the files you'll touch before editing. Match existing conventions exactly.
- Follow the repo's CLAUDE.md rules and the user's memory feedback (minimalism, no premature abstractions, no unnecessary comments, no em dashes).
- Keep the diff focused — no unrelated cleanup.
- If a fast typecheck exists (`tsc --noEmit`, `bun run lint`, `cargo check`, etc.), run it once before committing. Don't fabricate commands; if unsure what the repo uses, skip.

### 4. Commit

```bash
git commit -m "$(cat <<'EOF'
<short message — match recent commit style>
EOF
)"
```

Rules (same as `/commit`):
- Match recent commit style (`git log --oneline -10`).
- Focus on the "why" for non-trivial commits. For small chores, the "what" is enough.
- No Co-Authored-By lines, no "Generated with Claude" signature.
- If a pre-commit hook fails, fix the underlying issue, re-stage, and create a NEW commit. Never `--no-verify`. Never `--amend`.
- Before staging, scan the diff for obvious secrets (API keys, tokens, JWTs) — abort and warn the user if any appear.

### 5. Push and open a draft PR

```bash
git push -u origin <branch-name>
```

Detect the base branch:
```bash
gh repo view --json defaultBranchRef -q '.defaultBranchRef.name'
```

Open a **draft** PR:
```bash
gh pr create --draft --title "<short title, under 70 chars>" --body "$(cat <<'EOF'
## Summary
<1-3 bullets — what changed and why>

## Test plan
- [ ] <relevant check>
- [ ] <relevant check>
EOF
)"
```

- Base PR title + body on ALL commits on this branch vs. the default branch, not just the latest commit.
- If the branch name contains an issue number (`fix/DEV-123-...`, `feat/42-...`), include `Closes #<number>` in the body.
- No "Generated with Claude" line by default. User's preferred voice: lowercase, direct, no em dashes.

### 6. Start the dev server (if the repo has one)

The whole point of worktree isolation is that multiple features can run side-by-side on different ports. Next.js, Vite, and most modern frameworks auto-increment the port if the default is taken — no flags needed.

**Env files should already be present** — worktrunk's user-level `post-create` hook at `~/.config/worktrunk/config.toml` runs `wt step copy-ignored` after every `wt switch --create`, which copies `.env.local`, `.env.*`, `node_modules`, and other gitignored files from the source worktree. If the dev server fails on missing `process.env.X`, the hook didn't fire — fall back to a manual `wt step copy-ignored --from <source-branch>` before retrying.

1. Check `package.json` for a `dev` script. If none exists (or the project isn't web/JS), skip this step.
2. Detect the package manager: `bun.lockb` → `bun`, `pnpm-lock.yaml` → `pnpm`, `yarn.lock` → `yarn`, else `npm`.
3. Start in the background using Bash's `run_in_background: true`:
   ```bash
   <pkg-manager> run dev
   ```
4. Poll the background output with `BashOutput` until you see the "ready"/"local"/"listening" line that includes a port (`http://localhost:3001`, `:5174`, etc.).
5. Extract the port number.

If the ready line doesn't appear within ~15 seconds, report that startup is still in progress, give the expected port (default + worktree count), and continue — don't block the skill on server startup.

### 7. Report (tight — a few lines, not a wall)

Tell the user:
- Branch name + PR URL (the key output)
- **Dev server URL** (if started): `http://localhost:<port>`
- Files changed + commit hash
- Typecheck/test result if you ran one
- Any known limitations or follow-ups
- Reminder: "You're still in the worktree. When the PR merges, run `wt remove` to clean up."

### 8. Clean up background tasks

When the user signals the implement flow is done — PR approved, no more in-session iteration needed, or they switch topics — kill any background tasks this skill started so they don't leak across sessions.

- Dev server: `kill` the background task id, or `ps aux | grep -E "next.dev|vite|bun.*dev" | grep -v grep | awk '{print $2}' | xargs -r kill`
- Any other `run_in_background: true` tasks this skill started
- Do this proactively at end-of-flow; don't wait for the user to ask.

If the user is actively iterating (asking for follow-up edits in the same session), keep the server running — they'll want the preview. The trigger for cleanup is session boundary, not every tool call.

## What this skill does NOT do

- No `wt switch -` back to the original worktree — stay here for iteration.
- No `wt merge` — merging happens via the PR in GitHub.
- No `wt remove` — that's manual after PR merge.
- No parallel architect/reviewer agents — that's `/worktree-dev:worktree-dev`.
- No marking the PR ready — it stays draft until the user chooses.
- No force-push, no `--no-verify`, no amending existing commits.
