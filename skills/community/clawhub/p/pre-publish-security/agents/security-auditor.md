# Security Auditor Agent Task

**Target:** {{TARGET}}

## Mission
Scan for leaked credentials, secrets, API keys, and sensitive data.

## Checks

1. **Secret Patterns:**
   - GitHub PATs (`github_pat_`, `ghp_`)
   - AWS keys (`AKIA`, `aws_access_key`)
   - API keys (`api_key`, `apikey`, Bearer tokens)
   - Private keys (PEM, SSH keys)
   - Passwords (`password=`, `pwd=`)
   - Email addresses in code/config

2. **Git History:**
   - Scan all commits for secrets (not just current state)
   - Check for removed-but-still-in-history credentials

3. **Config Files:**
   - `.env`, `.env.local`, `config.json`
   - Git config files (`.git/config`)
   - Credential stores (`~/.git-credentials`)

4. **Environment Variables:**
   - Hardcoded secrets in scripts
   - Exported tokens in shell scripts

## Commands to Run

```bash
cd {{TARGET}}

# Pattern scan
grep -r -E "(github_pat_|ghp_|AKIA|api_key|apikey|Bearer|password=|pwd=)" . \
  --exclude-dir=node_modules \
  --exclude-dir=.git \
  2>/dev/null || true

# Git history scan (last 10 commits)
git log -p -10 | grep -E "(github_pat_|ghp_|AKIA|api_key|Bearer)" || true

# Check for credential files
find . -name ".env*" -o -name "*credentials*" -o -name "*.pem" | head -20
```

## Output Format

**CRITICAL:** Found GitHub PAT in file X, line Y
**HIGH:** API key pattern detected in Z
**MEDIUM:** Email address in source code
**LOW:** Potential credential file found

If no issues: **✅ No secrets detected**
