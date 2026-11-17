# Secret Remediation Playbook

When to read: when secret-scan.sh exits 1.

### Remediation
- **Working tree:** redact/remove the secret, commit the fix.
- **Token in remote URL (`.git/config`):** strip it — git authenticates via the `gh` credential helper, so `<GITHUB_URL_WITH_TOKEN>` is redundant AND a leak. `git remote set-url origin https://github.com/owner/repo.git`.
- **Secret in history:** rewrite. `git-filter-repo` is broken on this host (missing module) — use `git filter-branch`:
  ```bash
  git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch <path>' --prune-empty -- --all
  git for-each-ref --format='%(refname)' refs/original/ | xargs -n1 git update-ref -d
  git reflog expire --expire=now --all && git gc --prune=now
  git push --force
  ```
  Verify: `git log --all -p | grep -c '<secret>'` → 0.
- **Live credential still valid (PAT/API key):** scrubbing history does NOT invalidate it. Rotate/revoke at the provider (GitHub PATs: Settings → Developer settings → PATs; classic PATs can't be API-revoked).

