# Symptoms

Use this file when you already have the error text.

## `Permission denied (publickey)`

Most likely causes, in order:

1. The repo remote points at the wrong SSH alias.
2. The alias exists but is missing `User git`.
3. The alias exists but is missing `IdentitiesOnly yes`.
4. The key selected by the alias is not attached to the target repo.
5. A broad `Host github.com` rule is hijacking traffic.
6. File permissions or agent state are interfering.

Minimal checks:

```bash
git remote -v
ssh -G <alias> | sed -n '1,40p'
ssh -T git@<alias>
```

## `Repository not found`

On a private GitHub repo, this often means auth reached GitHub but the current key/user does not have access to that specific repo. It is often a permissions problem disguised as a path problem.

Check:

1. Repo owner/name is correct.
2. The repo really exists.
3. The current key is attached to the right repo.
4. The remote URL is SSH when you think it is SSH.
5. The alias is routing to the intended key.

Minimal checks:

```bash
git remote -v
ssh -T git@<alias>
git ls-remote origin
```

## Push rejected / `fetch first`

Common causes:

1. The remote branch moved.
2. An automation job pushed before you did.
3. Another local clone force-pushed.
4. Your backup/sync repo needs `fetch` + `rebase` before push.

Minimal checks:

```bash
git fetch origin
git status -sb
git log --oneline --decorate --graph --max-count=10 --all
```

## "It works in one repo but not another"

This usually means routing, not Git itself.

Check:

1. Does each repo use a different host alias?
2. Does each alias use a different key?
3. Did one repo keep `git@github.com:` while another uses an alias?
4. Did a script or config reintroduce the old remote?

## "I fixed the repo remote but it broke again later"

Likely cause: the real source of truth is a script, config value, or automation job that keeps rewriting the remote.

Check:

- backup script env/config
- cron jobs
- bootstrap scripts
- repo initialization scripts
- app config storing repo URLs
