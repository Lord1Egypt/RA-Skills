---
name: open-pr
description: Build a change in its own worktree, prove it with mutation testing, self-audit before pushing, open the PR with a body that states what it does NOT prove, then stop and hand off to the review loop. Use when starting any change that will become a PR — not just when asked to "open a PR". Never merges and never deploys.
argument-hint: [what to build]
metadata: { "openclaw": { "emoji": "🚀", "requires": { "bins": ["gh", "git"] } } }
---

# Open a PR

Take the requested change from the user's message (or `$ARGUMENTS` on hosts that
substitute it). If it is not explicit, ask what to build before touching anything.

This is the front half of the loop. The back half is `address-review-comments` for the
PR number; this skill ends by handing off to it.

## Scope and autonomous actions (read before invoking)

Invoking this skill authorizes it to take the following actions **without pausing for a
per-step confirmation**, as part of its normal, disclosed workflow: push a new branch to
the remote, open a pull request, and arm a background watch (see `../WAITING.md`) that
later invokes `address-review-comments` on your behalf when a reviewer responds. If your
environment expects a human to confirm before code leaves the local machine, gate that at
the point you invoke this skill — do not invoke it unless you intend for a PR to actually
be opened. It never merges and never deploys (see below), and it never modifies a branch
or checkout you did not create in Step 1.

## Standing rules (non-negotiable, same as the review skill)

- **Never merge.** The repo owner merges after their own review. Never run `gh pr merge`.
- **Never deploy.** Deploys and migrations are the repo owner's call; your job is to say
  exactly what needs deploying and in what order.
- **Never print secrets** in any file, commit, or comment. (A legitimately public
  anon/publishable key is not a secret.)
- **Never chain a content-editing command and `git add`/`git commit` in one shell
  command.** A failed edit must not let a commit of partial state through.
- **Never run a repo's staging-verification script against production** — check the
  repo's own docs for the safe target before running any such script.

## Step 1 — A worktree of your own, before anything else

**Resolve the repository from the checkout that invoked you** — never a hard-coded path.
This skill lives in the repo, so a hard-coded path would send a fresh clone's fetches,
branches and pushes into somebody else's checkout, or fail outright when it is absent.

**Each shell call runs in a fresh process on most hosts**, so nothing set here reliably
survives into later steps. Every later block re-derives what it needs from `$NAME`, which
is the one thing you carry in your head. Pick it once:

```bash
set -euo pipefail
NAME=gate                               # short, no slashes -> the directory wt-$NAME
BRANCH=fix/release-gate                 # the PR branch
REPO=$(git rev-parse --show-toplevel)   # the checkout this skill was invoked from
SCRATCH="${TMPDIR:-/tmp}/openpr-$NAME"; mkdir -p "$SCRATCH"
git -C "$REPO" fetch origin
git -C "$REPO" worktree add "$REPO/../wt-$NAME" -b "$BRANCH" origin/main
cd "$REPO/../wt-$NAME"
```

Then work **only** in that worktree. **Never `git checkout` or `git switch` in the
invoking checkout**, whoever it belongs to: it may be somebody's live desk with
uncommitted work. Doing that once moved a live checkout onto a branch mid-session and
interleaved its owner's uncommitted work with new edits in the same files, so every
validation run exercised half-finished code that was not the change under test.

Three sibling traps, each hit for real:

- **Never `git worktree add -f <dir> <branch>` on a branch that is already checked out.**
  The `-f` defeats the "already checked out" refusal and both worktrees then share ONE
  branch ref, so a merge in the scratch tree silently advances the real branch. To
  trial-merge, use a throwaway: `git worktree add -b trial/<name> "${TMPDIR:-/tmp}/wt-trial" <branch>`, then
  `git worktree remove --force` and `git branch -D`.
- **Never point a writing agent (or a mutation harness) at a worktree with uncommitted
  work.** An auditor once backed a file up, ran its own mutations, and restored a stale
  snapshot — silently wiping a guard. Commit first, or hand agents a copy.
- **Never kill a process on a name match.** Several sessions plus an automated reviewer
  may share the same tool names on one machine. Print `ps -eo pid,ppid,etime,command` and
  confirm the `--path`/cwd is a worktree you created this session. A long runtime is not
  evidence of an orphan.

## Step 2 — Build it, and prove it the way the repo means "proved"

Write code that reads like the code around it — match its comment density, naming and
idiom. Then:

**Mutation testing is the bar.** No guard counts until its defect is reintroduced and the
guard is observed going red ON ITS OWN TARGETED ASSERTION. A test that passes proves
nothing about a guard; a mutation that turns it red does.

Sharp edges, all of which have cost real time on repos this skill has run against:

- **Check WHICH assertion fired.** A mutation can go red for a neighbouring reason —
  dropping a column check that fires on an unrelated row is not evidence for the guard you
  meant to test. Reorder cases so the specific one runs first, and assert the failure
  message names the case under test.
- **A mutation can HANG rather than fail.** Run every one with a hard timeout, treat
  `HANG` as its own outcome (it is neither a pass nor a proper red), and kill the whole
  process group (`start_new_session=True` + `os.killpg`) or child processes outlive the
  harness. Set `sys.stdout.reconfigure(line_buffering=True)` in any Python harness or a
  backgrounded run looks stalled and empty.
- **A surviving mutation is information, not a failure to hide.** Sometimes a clause is
  genuinely redundant with another. Say so in the code, in place, with the reason — and
  report it in the PR body as a survivor rather than quietly dropping the mutation.
- **For an additive fix, red-before-green evidence is a mutation after the fix**, not a
  test run before it. A new assertion against missing code can pass for the wrong reason
  while recording nothing — run the repo's own real validator, not the bare test runner.
- If a harness is killed mid-run, look for a stranded `*.bak` beside the source; the
  mutated file is left in place.

Run the full suite set for whatever you touched. Prove any local dependency you started
(e.g. a database replica) is the one you're actually talking to — ports collide across
sessions.

## Step 3 — Self-audit BEFORE the commit, and wait for it

Run the same four-lens audit the review skill uses, adversarially verified (a separate
skeptic per finding, defaulting to "not real" when uncertain): internal consistency;
regression against anything this change touches; staleness and incompleteness; and a
platform fact-check with web access for every claim this change makes about a third-party
platform, API, or store.

**A wrong platform fact is a blocker, not a P2** — it cannot work as written. Never assert
third-party behaviour from memory; if you cannot verify it, say so in the text and route
it to P2 rather than stating it.

**Wait for verification to finish before committing.** Raw per-lens findings arrive long
before adversarial skeptics do and look complete. Acting on a first lens before the
skeptics land has cost a public correction on real PRs; the rule is `results >= agents`,
then commit.

Two mechanical checks before you push, both of which have shipped to a reviewer on real
runs:

- Inserting a function ABOVE an existing one steals its doc comment. Put new functions
  after the existing body, then re-read both neighbours.
- `git diff | grep -n "\\\\'\|'\"'\"'"` — empty is the only acceptable result. `\'` inside
  a `<<'PY'` heredoc writes a literal backslash into the file.

## Step 4 — The PR body

The body is the deliverable a reviewer reads first. Use this shape, dropping sections
that genuinely do not apply:

1. **A deploy banner, if anything must be live before the next build.** First line, so it
   cannot be missed.
2. **The defect** — or what this changes and why it matters, in terms of what a user or
   operator experiences, not in terms of the code.
3. **What I picked, and what I turned down** — the alternatives, each with the reason it
   lost. A reviewer should not have to guess whether you considered the obvious option.
4. **What it proves, and what it does NOT prove.** This is the section that earns trust,
   and the one most often skipped. Be specific about the boundary: name what is uncovered
   and say whether uncovered means *not covered by this change* or *optional* — they are
   not the same thing.
5. **How it stays true.** If the failure mode is staleness, prefer a structural fix (a
   check that refuses to run, a default arm that dies) over a comment asking people to
   remember. Say which you chose.
6. **Tests** — the counts, and specifically what each new test would have caught.
7. **Mutation testing** — how many, how many red on their own targeted assertion, and any
   survivors with their documented reason.
8. **What the self-audit changed.** Findings you produced against your own work, stated
   plainly. This section is not an apology; it is the evidence that the change was
   examined rather than asserted.
9. **P2s deliberately not done**, each with why it is out of scope for this PR.
10. **Deploy** — the exact migrations, in order, and the one-line check that proves each
    landed. Never do it yourself.

Write it to a file in the scratchpad and open with `--body-file`; these bodies are long
and shell-quoting them corrupts them.

## Step 5 — Open it

```bash
set -euo pipefail
NAME=gate                                            # the same NAME as Step 1
BRANCH=fix/release-gate                              # the same BRANCH as Step 1
SCRATCH="${TMPDIR:-/tmp}/openpr-$NAME"
# RE-ENTER THE WORKTREE FIRST. This block is a fresh shell, so it starts wherever the skill
# was invoked — which is the checkout Step 1 went out of its way not to touch. `git push -u
# origin HEAD` from there pushes THAT checkout's current branch, and `gh pr create` opens a
# PR for it: somebody else's live desk, published under your title. Assert, don't assume.
REPO=$(git rev-parse --show-toplevel)
cd "$REPO/../wt-$NAME"
[ "$(git rev-parse --abbrev-ref HEAD)" = "$BRANCH" ] || {
  echo "expected $BRANCH in wt-$NAME, found $(git rev-parse --abbrev-ref HEAD)" >&2; exit 1; }
# Push second: with no TTY, `gh pr create` aborts on an unpushed branch rather than
# offering to push it.
git push -u origin HEAD
PR_URL=$(gh pr create \
  --title "Release gate: prove every capability this checkout needs, not just L1" \
  --body-file "$SCRATCH/pr_body.md")
# Guard the capture: a failed create prints nothing, and an empty PR_NUM would make
# Step 6 silently watch whatever PR gh resolves from the branch instead.
PR_NUM=${PR_URL##*/}
[[ "$PR_NUM" =~ ^[0-9]+$ ]] || { echo "gh pr create did not return a PR URL" >&2; exit 1; }
echo "$PR_NUM" > "$SCRATCH/pr_num"
echo "opened #$PR_NUM at $PR_URL"
```

Titles read like the commit log: an area prefix, then the change in the imperative — not
the ticket, not the mechanism. `Bus horn: successive blasts walk all three horns`, `E2E:
seed bus_horns so L8's preservation check stops comparing 0 with 0`.

End the body with a line crediting the tool/runtime that generated it (e.g. `🤖 Generated
with Claude Code` / `Codex` / `OpenClaw`), matching whichever is actually running this
skill.

## Step 6 — Arm the monitor, then stop

**Arm a watch for the reviewer's first batch by default.** Skip it only when the user
says so for this PR. One watch per PR; do not layer a second polling mechanism on top of
it.

**Wait the way `../WAITING.md` prescribes** for your host (OpenClaw `cron` gate, Claude
Code `Monitor`, or Codex heartbeat) — the cheapest mechanism your runtime supports, so the
watch costs as little as possible while the PR is quiet. That file carries the loop, the
filter-on-content rule (the reviewer may post under the same account as the author, so an
author filter wakes on your own replies), the filter-verification step, and the
emit-on-terminal-state rule. It also carries the exact per-host arm/find/stop mechanics —
do not restate them here.

Resolve `PR` and `REPO` before arming — a watch may inherit nothing from the session that
armed it, so bind them into the watch's own command/prompt rather than assuming context:

```bash
set -euo pipefail
NAME=gate                                            # the same NAME as Step 1
SCRATCH="${TMPDIR:-/tmp}/openpr-$NAME"
PR=$(cat "$SCRATCH/pr_num")                          # written by Step 5
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
[[ "$PR" =~ ^[0-9]+$ ]] || { echo "no PR number in $SCRATCH/pr_num" >&2; exit 1; }
echo "arm watch with: PR=$PR REPO=$REPO MARKER='<!-- review-pr-state'"
```

The marker is the **HTML comment**, not the bare string: only the reviewer writes
`<!-- review-pr-state ... -->`, while the bare word appears in any reply that discusses
the watch — including yours, which is how this watch has previously spent rounds waking
on its own comments. No `EXCLUDE` here, because reviewer batches are exactly what this
direction waits for.

**Keep whatever identifier your host's arming call returns.** It is what stops the watch
later, and it is how you tell "already watched" from "arm a second watch on the same PR".

**If no watch mechanism is available on this host, say so and leave watching manual.** Do
not substitute a raw `sleep` loop, a cron workaround with no predicate, or a background
process you can't account for later, and do not report the loop as armed when it is not —
an unarmed watch that is believed is worse than none, because nobody goes looking.

When it fires, go to Step 7. Then report: the PR number and link, what it does, what you
proved and what you did not, anything that needs a decision, the deploy steps if any, and
whether the watch is armed **or could not be**, and whether it survives the session ending
on this host. Then stop — no polling on top of it.

## Step 7 — Hand off

When the repo owner says a review batch has landed (or the watch fires), run
`address-review-comments` for that PR. That skill owns everything from there: the
loop-state decision, the fixes, its own pre-commit audit, one commit and one reply per
round.

Two things that come back to this skill rather than that one:

- **Main moves under a long-lived PR.** When the PR goes `CONFLICTING`, merge
  `origin/main` into the branch (never rebase a branch the reviewer has commented on, and
  never `gh pr merge`). Check any repo-specific docs about known conflict-prone files
  before resolving by hand — some tables/rows are designed to be composed, not chosen.
  Prove the result both ways: it must equal theirs plus exactly your edits, and equal
  yours plus exactly their edits.
- **A merged-in PR based on your branch becomes part of your diff.** Check `gh pr view <n>
  --json baseRefName` before describing someone else's work as external to yours.
