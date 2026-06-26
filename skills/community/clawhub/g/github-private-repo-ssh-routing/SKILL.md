---
name: github-private-repo-ssh-routing
description: Diagnose and manage SSH keys, host aliases, and Git remotes for GitHub private repositories in multi-repo environments. Use when deploy keys collide, a machine manages multiple private repos, automation or backup scripts push to GitHub, or errors like "Permission denied (publickey)" / "Repository not found" appear despite the repo existing.
---

# GitHub Deploy Key Routing

Treat GitHub private repo access as a routing problem, not just a Git problem.

## Core rules

- Use one deploy key per private repository unless a machine user is intentionally chosen.
- Use one SSH host alias per key.
- Point each repo remote at the correct alias explicitly.
- Do not rely on a catch-all `Host github.com` when multiple deploy keys exist.
- Verify SSH first, then Git, then push.
- If automation is involved, fix both the live repo remote and the config/script source that writes it.

## Canonical pattern

```ssh
Host github.com-backup
    HostName github.com
    User git
    IdentityFile ~/.ssh/openclaw_backup_ed25519
    IdentitiesOnly yes
```

```bash
git remote set-url origin git@github.com-backup:OWNER/REPO.git
```

Use this skill when the machine has more than one private GitHub repo, more than one SSH key, or any recurring GitHub automation.

## Quick triage

If you need the fastest route:

1. Read `references/symptoms.md` and match the exact error.
2. Read `references/patterns.md` and compare the current alias + remote layout.
3. Read `references/decision-guide.md` only if the identity model itself is still undecided.
4. Read `references/openclaw-automation.md` only when a script, backup flow, or config value may be rewriting the remote.

## Workflow

### 1. Identify the repo + remote actually in use

Check the local repo path, current remotes, and whether the failing action came from:

- an interactive repo command
- a backup/sync script
- a config file that stores the repo URL
- a cron/automation job

If the repo path and the config source differ, do not treat them as the same fix.

### 2. Identify the key-routing layer

Read `references/patterns.md` for the standard alias layout.
Read `references/key-storage-by-system.md` when OS-specific key locations or mixed Windows/WSL/macOS behavior may matter.

Ask:

- Which SSH alias is the repo using now?
- Which key does that alias select?
- Is that key actually authorized for this repo?
- Is a broad `Host github.com` rule hijacking traffic?

### 3. Diagnose by symptom

Read `references/symptoms.md` and match the exact failure string before changing anything.

### 4. Choose the right identity model

Read `references/decision-guide.md` when the user is deciding between:

- deploy key
- personal SSH key
- machine user

Read `references/identity-model-boundaries.md` when the question is really about where SSH routing ends and GitHub API authority begins — especially for PR merge automation, release creation, or fine-grained PAT vs deploy key decisions.

### 5. Check automation-specific drift

Read `references/openclaw-automation.md` when the repo is used by OpenClaw backup/restore, plugins, cron jobs, or config-driven workflows.

### 6. Fix in the safe order

1. Fix or add the SSH alias.
2. Verify with `ssh -G <alias>`.
3. Test with `ssh -T git@<alias>`.
4. Update the repo remote URL.
5. Update any config/script source that still writes the old remote.
6. Verify with `git ls-remote origin`.
7. Only then push or pull.

## Minimal command set

```bash
ls -la ~/.ssh
sed -n '1,200p' ~/.ssh/config
git remote -v
ssh -G <host-alias> | sed -n '1,40p'
ssh -T git@<host-alias>
git ls-remote origin
```

## Bundled script

For a read-only audit of one local repo, run:

```bash
scripts/audit-routing.sh /path/to/repo
```

The script summarizes:

- repo remotes
- inferred SSH alias from `origin`
- `~/.ssh` files and permissions
- `~/.ssh/config` preview
- `ssh -G` summary for the detected alias

Use the script to inspect before editing.

## What to report

- Root cause in one sentence
- Whether the failure is local config, GitHub permission, or both
- The minimal fix
- Exactly what changed
