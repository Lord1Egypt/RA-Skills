# Revert evidence pitfall: artifacts in the wrong commit history

## What happened
A regression was detected and a `git revert` auto-rollback was performed correctly.
However, separate rollback evidence (`pre.txt`, `post.txt`, `rollback.txt`) was added
after the revert, in a second unrelated commit.

## Why it matters
Post-deploy validation evidence should be committed atomically with the state it describes:
- `pre.txt` / `post.txt` describe the deploy that regressed
- `rollback.txt` documents why the revert happened

If those land in a follow-up commit, a reviewer or dashboard reading git history sees
code rollback first, then "evidence of a rollback" afterwards. That breaks the audit
chain: from history alone, the second commit looks like a new change rather than
evidence for the prior revert.

## Rule
Commit revert evidence files together with the revert commit, in the same changeset.
Use `git revert --no-commit HEAD`, then `git add` the reverted source files **and**
the evidence files together, then `git commit` once. Do not scatter post-hoc evidence
across later commits.

## Minimal recipe
```bash
git revert --no-commit <deploy-sha>
git checkout -- pre.txt post.txt rollback.txt  # restore evidence from working tree, or recreate
git add pre.txt post.txt rollback.txt <reverted source files>
git commit -m "rollback: revert <deploy-sha> due to regression"
```

If evidence files are currently absent, recreate them from logs/metrics before
completing the revert commit; never leave the revert as an unsupported "code moved
back without explanation."

## Check
After commit, confirm with `git log --stat` that one commit contains both the restored
source files and the evidence files. If they are split, squash them into one commit.
