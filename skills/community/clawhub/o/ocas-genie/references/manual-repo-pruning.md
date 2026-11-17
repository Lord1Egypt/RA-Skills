# Manual Repo Pruning — Decision Gate & Blockers

Companion to the "Manual Repo Pruning" section in SKILL.md. Use when the user
asks to delete cloned repos beyond Genie's automated inactive-clone Tier 1
(`git_clone_max_age_days`). The automated tier only removes *clean, untouched,
has-remote* clones; user-requested deletion often targets repos with work in
progress, which must be synced first or excluded.

## Decision gate (per repo)

1. **Eligible — delete now.** All true:
   - working tree clean (`git status --porcelain` empty)
   - has a remote (`git remote get-url origin` non-empty) → re-clonable
   - untouched > `git_clone_max_age_days` (5d default)
   - NOT a protected path: live skill dirs (`profiles/*/skills/*`),
     `indigokarasu-site-commons/*`, the active working repo, `indigo-study`,
     `ferry-fairy`
2. **Needs sync — commit, push, re-verify, then delete.**
   - `dirty>0`: `git add -A` + commit with a real author
     (`Indigo Karasu <mx.indigo.karasu@gmail.com>`).
   - push (see blockers below).
   - **Gate:** after push, `dirty==0 && ahead==0`
     (`git rev-list --count HEAD@{u}..HEAD`). Only then `rm -rf`.
   - If the gate fails, **keep the repo** — do not delete unsynced work.
3. **Exclude — never delete.**
   - Stale mirrors: a local clone behind/smaller than the live source
     (e.g. `indigo-repo` = 104 skills vs live 141). If local HEAD == remote
     HEAD, a local-only delete is safe; expect a daily skill-sync to recreate it.
   - Protected live-skill directories (above).

## Blocker playbook (real cases from a 15-repo pruning session)

| Blocker | Symptom | Fix |
|---|---|---|
| Dead local `origin` | `origin` = `/root/Graze` (not a repo); push → "Could not read from remote" | The real GitHub upstream is often present under a misnamed remote (`github`, `nithub`). `git push <real-remote> <branch>` instead of `origin`. |
| Nested git repo / submodule | Parent shows ` M subrepo`; `git add -A` won't stage it | The nested dir is a separate repo (e.g. `headhunter` = `util-head-hunter`). Sync the nested repo (`add/commit/push` to ITS remote), then commit the parent gitlink + `git pull --rebase` + push parent. No `.gitmodules` needed if already a gitlink (`160000` mode in `git ls-files --stage`). |
| Pull-rebase conflict on stale mirror | `git pull --rebase` stops on a conflict (e.g. README) | If the clone is a stale mirror superceded by remote (remote has many newer sanitize/beautify commits, both SKILL.md same version, live skill is source of truth), `git reset --hard origin/main` then delete. Confirm with user before discarding local commits. |
| Husky pre-push test stalls | push → "pre-push script failed (code 1)" or the test hangs past timeout | **Do NOT** `--no-verify`. The hook is a real CI gate. Diagnose/fix the suite, or (after user confirms) drop the clone without pushing. |
| LFS pre-receive hook decline | "Try to push them with `git lfs push --all`" | Repo uses `.gitattributes` LFS filters (`*.db`, `*.lbug`, etc.). Either `git lfs push --all origin` or, for a stale mirror, local-only delete (GitHub already holds the commit). |
| Non-fast-forward (remote advanced) | push → "fetch first" | `git pull --rebase origin <branch>` (resolve any conflict per above) then push. |

## Verification after deletion
- `df -h /` — confirm freed space moved (note: a WAL checkpoint or cron may
  shift the number independently of your deletes — don't claim credit for
  space you didn't free).
- Re-list target paths to confirm they're gone.
- For stale-mirror deletes, expect recreation on the next skill-sync tick;
  that's a sync-design behavior, not a failed delete.

## Hard rules
- Never delete a repo that fails the sync-verify gate (unsynced work = data loss).
- Never bypass a hook (husky/CI) to force a push.
- Never rewrite a remote's `origin` to a guessed URL without confirming it's
  the intended upstream.
