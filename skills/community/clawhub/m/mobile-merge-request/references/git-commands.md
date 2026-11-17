# Git commands for the MR workflow

Load this for exact command sequences. Everything here assumes the remote is `origin` and the
target branch is `main`; substitute the project's names. Commands that rewrite history are for the
author's own, unshared branch only, and the agent runs them only after the user agrees.

## One-time setup

```bash
git config --global push.autoSetupRemote true   # first push of a new branch sets upstream
git config --global rebase.autoSquash true      # fixup! commits are folded automatically in rebase -i
git config --global rerere.enabled true         # remember conflict resolutions across rebases
git config --global pull.rebase true            # pulling your own branch rebases instead of merging
```

## Start a branch

```bash
git fetch origin
git switch -c feature/AH/PROJ-123-ble-reconnect-backoff origin/main
```

## Inspect before opening the MR

```bash
git log --oneline origin/main..HEAD             # commits that will be in the MR
git diff --stat --merge-base origin/main        # size and touched files
git diff --merge-base origin/main               # full diff, as the reviewer will see it
git diff --check --merge-base origin/main       # whitespace errors and leftover conflict markers
```

## Commit and amend

```bash
git add -p                                      # stage hunk by hunk, keeps commits focused
git commit -m "fix(ble): retry GATT connect with exponential backoff" -m "Refs: PROJ-123"
git commit --amend                              # last commit only, before it is pushed or reviewed
```

## Review fixes as fixups

```bash
git commit --fixup=a1b2c3d                      # content fix for commit a1b2c3d
git commit --fixup=reword:a1b2c3d               # message-only fix for commit a1b2c3d
git rebase -i --autosquash origin/main          # after approval: folds fixups into their targets
```

## Update a branch with main

```bash
git fetch origin
git rebase origin/main                          # own branch only
git range-diff origin/main @{u} HEAD            # compare pushed commits with rebased commits
git push --force-with-lease                     # refuses if someone else pushed since your fetch
```

- `git range-diff` shows per-commit differences between the old and new series. Use it before every
  force push to confirm the rebase did not drop or alter anything unintended.
- `--force-with-lease` protects against overwriting commits you have not fetched. Run it right after
  your own `fetch`, not after an automated background fetch that may have updated the lease.

For shared branches, merge instead of rebasing:

```bash
git switch release/3.2
git merge --no-ff origin/main
git push
```

## Open the MR from the command line

```bash
# GitLab push options: create the MR on push
git push -o merge_request.create -o merge_request.target=main

# GitHub CLI
gh pr create --base main --title "fix(ble): retry GATT connect with exponential backoff (PROJ-123)" \
  --body-file pr-description.md
gh pr create --draft --base main --fill

# GitLab CLI
glab mr create --target-branch main --draft
```

## Stacked MRs

Create the stack:

```bash
git switch -c feature/AH/PROJ-123-pairing-api origin/main
# ...commits, push, MR 1 targets main
git switch -c feature/AH/PROJ-124-pairing-ui
# ...commits, push, MR 2 targets feature/AH/PROJ-123-pairing-api
```

Parent changed during review (new fixups on PROJ-123), update the child:

```bash
git switch feature/AH/PROJ-124-pairing-ui
git rebase feature/AH/PROJ-123-pairing-api
git push --force-with-lease
```

Or rebase the whole stack at once from the top branch; intermediate branches move with it:

```bash
git switch feature/AH/PROJ-124-pairing-ui
git rebase --update-refs origin/main
git push --force-with-lease origin feature/AH/PROJ-123-pairing-api feature/AH/PROJ-124-pairing-ui
```

Parent was squash-merged into main. The child still contains the parent's original commits, which
main no longer has. Replay only the child's own commits:

```bash
git fetch origin
# local feature/AH/PROJ-123-pairing-api still points at the parent's pre-merge tip
git rebase --onto origin/main feature/AH/PROJ-123-pairing-api feature/AH/PROJ-124-pairing-ui
git push --force-with-lease
```

Then retarget MR 2 to `main` in the MR settings. Both GitLab and GitHub can retarget dependent MRs
automatically when the parent branch is deleted on merge; check the MR target afterwards anyway.

## Undo and recover

```bash
git rebase --abort                              # back to before the rebase started
git merge --abort                               # back to before the merge started
git reflog                                      # find the commit you had before a bad rebase
git switch -c rescue/PROJ-123 HEAD@{2}          # recover it on a new branch, nothing is lost
git revert <sha>                                # undo a merged commit on a shared branch
git revert -m 1 <merge-sha>                     # undo a merged MR that landed as a merge commit
```

Prefer recovery onto a new branch over moving the current branch, so nothing is overwritten.

## Commands the agent does not run without explicit approval

- `git push --force-with-lease` or any push that rewrites remote history.
- `git rebase` of a branch that has an open MR under review.
- Merging an MR, deleting a branch, or changing branch protection.
- Plain `git push --force` is never suggested.
