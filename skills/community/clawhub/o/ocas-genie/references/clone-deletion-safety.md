# Clone deletion safety (incident + gate)

## What happened (2026-08-16)

`clean_git_clones()` deleted any directory under the clones path that was
(1) a git repo, (2) had a `url =` line in `.git/config`, and (3) was older
than `git_clone_max_age_days`. That is all it checked. `SKILL.md` meanwhile
documented four further gates — clean tree, no stashes, no unpushed commits,
protected paths — none of which existed in code.

The gap was invisible for weeks because the feature was itself dead: a
sanitization pass had replaced the clones path with a literal `<fs-root>`
placeholder, so the scan pointed at a path that does not exist. Restoring the
real path re-armed the unguarded deletion, and the next `--clean` removed a
905 MB clone.

That clone turned out to be a pristine third-party reference checkout whose
HEAD existed on its public remote, so nothing unique was lost — but that was
luck. The same code would have deleted a clone holding unpushed commits.

**Two lessons.** A documented gate that is not in code does not exist. And
re-enabling a dormant destructive feature is a change that deserves the same
review as writing it fresh — audit what it will do *before* the first run.

## The gate (v1.8.0)

`clone_delete_blockers(path, protected)` returns a list of reasons a clone
must not be deleted; empty means safe. It **fails closed**: any probe that
errors returns a blocker, so an unreadable repo is never deleted.

| Blocker | Probe |
|---|---|
| protected path | basename/substring match against `git_clones_protected` |
| uncommitted changes | `git status --porcelain` non-empty |
| stashed work | `git stash list` non-empty |
| unpushed commits | per branch: `git rev-list --count <upstream>..<branch>` != 0 |
| unverifiable branch | branch has no configured upstream |
| unreadable repo | any git probe fails |

Covered by `tests/test_clone_delete_gate.py` (7 cases, including the
fail-closed and protected-path paths).

## Proving a clone is disposable by hand

`ahead=0` alone is not proof. Use these, in order of strength:

1. **Patch-equivalence** — `git cherry <remote-branch> HEAD`; every line
   prefixed `-` is already upstream. This survives rebases, where commit IDs
   differ but the content is present.
2. **Commit existence on the remote** — for a public host, query the API for
   the SHA (`gh api repos/<owner>/<repo>/commits/<sha>`). A 200 proves the
   object is on the server, not merely that a local ref agreed.
3. **Every branch, not just HEAD** — enumerate `refs/heads` and check each
   one; work is routinely stranded on a side branch.

If a clone cannot pass these, it is not cleanup — it is deletion of the only
copy. Report it and let the owner decide.

## What an adversarial audit found in the fix (2026-08-16)

Three independent reviewers attacked the v1.8.0 gates by building real
repositories and calling the functions, then each finding was handed to a
separate reviewer whose job was to refute it. Six survived — **three of them
created by the fix itself**, which is the point: a safety change deserves the
same adversarial treatment as the bug it repairs.

| Hole | Why the gate missed it |
|---|---|
| branch deleted upstream; remote repo deleted | `rev-list <upstream>..<branch>` reads refs/remotes, a local cache — the remote is never contacted |
| `.env` / `data/` git-ignored | `git status --porcelain` hides ignored paths by design |
| commit held only by a tag | the per-branch loop enumerates refs/heads only |
| undated live directory in a backup root | live-copy protection was scoped to `os.path.isfile` |
| `latest -> 2026-08-16` symlink | every probe followed the link; retention kept the link, deleted the target |
| `invoice-90210347.pdf` | `\d{8}` matched any eight digits, so account and epoch numbers looked like dates |

**Method worth reusing.** Give each reviewer a distinct lens (exotic git state,
environment/config, regex edges), require an executed reproduction rather than
a hypothesis, then have a *different* reviewer try to refute each claim. Two
claims were correctly refuted this way — an under-deletion complaint and a
by-design archive rule — which is what keeps the confirmed set trustworthy.

### The second wave (v1.8.2)

The first fix pass addressed the findings visible in the audit's early
returns. Reading the completed run showed 25 confirmed findings rather than
six — a reminder that **a partial result is not a result**. The rest fell into
two families:

*The probe can be lied to.* A safety check that shells out inherits both the
environment and the repository's configuration, and either can disarm it:
`GIT_DIR` redirects every command at another repo; `status.showUntrackedFiles=no`
hides never-committed files; `diff.ignoreSubmodules=all` hides submodule work;
`git stash list` reads a reflog that may have expired while `refs/stash` still
holds the data. Scrub the environment, force the config with `-c`, and prefer
plumbing (`rev-parse --verify refs/stash`) over porcelain.

*The repository is bigger than its working tree.* Submodules and linked
worktrees are separate stores that the parent's `status` says nothing about,
and deleting the parent takes them with it.

And in retention: grouping matters as much as ordering. A global "keep 1"
across unrelated roots means the newest backup anywhere deletes every other
system's only copy, and a completeness score used as the primary sort key will
happily discard today's backup in favour of a year-old one.
