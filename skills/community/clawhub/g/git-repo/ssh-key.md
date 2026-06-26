# SSH Key

Configure per-repo `core.sshCommand` to map SSH keys for multi-account GitHub access.

## When to Use

- Multiple GitHub accounts with different SSH keys (e.g., one for personal, one for work)
- SSH agent loads keys in wrong order — `git@github.com` authenticates as the wrong account
- `Repository not found` errors despite correct SSH key existing

## Problem

When multiple SSH keys are loaded in the SSH agent, Git uses the **first matching key** regardless of `IdentitiesOnly=yes` or `-i` flag. This causes:

```
$ ssh -i ~/.ssh/<account>/<key> -o IdentitiesOnly=yes -T git@github.com
Hi other-account!  ← Wrong account! Agent key takes priority
```

## Solution

Use `core.sshCommand` with `IdentityAgent=none` to bypass the SSH agent entirely:

```bash
git config core.sshCommand "ssh -o IdentityAgent=none -i ~/.ssh/<account>/<key> -o IdentitiesOnly=yes"
```

- `IdentityAgent=none` — disables SSH agent, forces file-based key only
- `-i <key>` — specifies the exact key file
- `IdentitiesOnly=yes` — prevents SSH from trying other keys

## Procedure

### 1. Identify the SSH key mapping

Check `~/.ssh/config` for host aliases and their associated keys:

```bash
grep -A3 "Host " ~/.ssh/config | grep -E "Host |IdentityFile"
```

### 2. Verify key-to-account mapping

```bash
# Test which GitHub account each key authenticates as
ssh -o IdentityAgent=none -i <key_path> -o IdentitiesOnly=yes -T git@github.com
```

### 3. Apply to repositories

For all repos under an org directory:

```bash
for dir in ~/ghq/github.com/<org>/*/; do
  if [ -d "$dir/.git" ] || [ -f "$dir/.git" ]; then
    cd "$dir"
    git config core.sshCommand "ssh -o IdentityAgent=none -i <key_path> -o IdentitiesOnly=yes"
    echo "✅ $(basename $dir)"
  fi
done
```

### 4. Verify push works

```bash
git push --dry-run origin <branch> 2>&1 | head -3
```

Expected: `Everything up-to-date` or `rejected` (auth OK, needs fetch) — NOT `Repository not found`.

## GUI Client Compatibility Matrix (HARD STOP — verify before relying on any method)

**Different GUI clients use different SSH invocation paths.** Neither `core.sshCommand` nor URL host aliases work universally. Verify with the actual GUI client before declaring a method as "compatible".

| Method | git CLI | SourceTree | SourceGit | GitHub Desktop | Notes |
|--------|---------|------------|-----------|----------------|-------|
| Per-repo `core.sshCommand` | ✅ | Usually ✅ (spawns git CLI) | ❌ **Not honored** | Unknown | SourceGit uses bundled/embedded SSH client → ignores git CLI's `core.sshCommand` |
| URL host alias (`git@host-alias:org/repo`) | ✅ (reads `~/.ssh/config`) | Usually ✅ | ❌ **`Could not resolve hostname`** | Unknown | SourceGit's bundled SSH does not read `~/.ssh/config` |
| SSH agent + key ordering | Unreliable | Unreliable | Depends on agent | Unknown | Agent loads first matching key — wrong account possible |
| Per-repo `remote.origin.sshkey` (GUI-specific) | Ignored | SourceTree honors | **SourceGit honors** | Unknown | GUI clients may set this themselves after Settings → "Update SSH key for origin" |

**Conclusion**:
- CLI-only environments → `core.sshCommand` works (this skill's original recommendation)
- **SourceGit users** → must verify per-GUI; common solutions in priority order:
  1. **Switch remote URL to HTTPS** + configure path-based credential helper in `~/.gitconfig` (`[credential "https://github.com/<org>"] helper = !sh -c '...gh auth token --user <account>...'`). SourceGit calls git's HTTPS credential pipeline directly — works without any SSH config / agent / `core.sshCommand` dependency. Most reliable when `~/.ssh/config` is not visible to SourceGit's git invocation
  2. Set `remote.origin.sshkey` in `.git/config` directly (some SourceGit versions honor this; verify per-version)
  3. Use SourceGit Settings → "Custom SSH Key" per repository (writes the same key)
  4. Grant SourceGit Full Disk Access (**macOS** — System Settings → Privacy & Security → Full Disk Access; on Windows / Linux the equivalent is reading `~/.ssh/config` directly without sandboxing, so this step is not required) so its spawned git can read `~/.ssh/config` — required on macOS for SSH alias / `core.sshCommand` paths to function reliably

## Verification Mandate (HARD STOP)

**CLI verification alone is insufficient.** After applying any of the methods above, verify the actual GUI client used by the user:

| Verification | Command / Action |
|--------------|------------------|
| CLI (per-repo `core.sshCommand`) | `git ls-remote --heads origin` from repo dir |
| SourceTree | Right-click repo → Pull → confirm no auth prompt |
| **SourceGit** | Open repo in SourceGit → Fetch → **must succeed without "Could not resolve hostname" / "Repository not found"** |
| GitHub Desktop | Repo → Fetch origin → confirm success |

**Do not declare "fix complete" until the user-reported GUI client succeeds.** CLI passing while GUI fails = same root issue still active.

## Notes

- This is a **per-repo** setting stored in `.git/config` — does not affect other repos
- If a repo is cloned fresh, the setting must be re-applied
- For `ghq get`, apply after clone using the patrol or clone topic
