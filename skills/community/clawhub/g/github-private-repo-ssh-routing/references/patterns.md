# Patterns

## Good pattern: one alias per repo key

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

## Good pattern: multiple private repos on one machine

```ssh
Host github.com-backup
    HostName github.com
    User git
    IdentityFile ~/.ssh/openclaw_backup_ed25519
    IdentitiesOnly yes

Host github.com-memory-bridge
    HostName github.com
    User git
    IdentityFile ~/.ssh/openclaw_memory_bridge_ed25519
    IdentitiesOnly yes
```

Each repo remote must point at its matching alias.

## Acceptable pattern: single personal key on a workstation

Only acceptable when there is a single broad user identity by design.

```ssh
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Do not use this pattern when multiple deploy keys exist.

## Risky pattern: broad `Host github.com` in a multi-key environment

```ssh
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/some_repo_key
```

Why risky:

- every `git@github.com:...` repo will try that key
- private repos start failing in confusing ways
- users blame Git when the real problem is SSH routing

For cross-system storage differences, read `key-storage-by-system.md`.

## Storage rules

- Keep private keys in `~/.ssh/`
- Do not put private keys in repos, sync folders, downloads, or `.txt` backups
- Name keys by purpose or machine
- Keep file permissions tight
- Prefer `~/.ssh` = `700`, private keys = `600`, `config` = `600`, public keys = `644`

## Read-only audit checklist

```bash
ls -la ~/.ssh
stat -c '%a %U:%G %n' ~/.ssh ~/.ssh/* 2>/dev/null
sed -n '1,200p' ~/.ssh/config
git remote -v
```

Use the audit first; do not edit until you know which alias, key, and repo are actually involved.
