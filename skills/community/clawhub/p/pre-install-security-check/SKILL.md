---
name: security-check
description: 🔒 Pre-installation security verification for external code and dependencies. Automated risk analysis for GitHub repos, npm packages, PyPI libraries, and shell scripts. Integrates CVE databases (Snyk, Safety DB) to detect vulnerabilities before you install. Shows risk level (✅ safe / ⚠️ review / ❌ dangerous) with actionable recommendations. First comprehensive security skill for OpenClaw — protect your system before downloading untrusted code.
tags: security, dependencies, vulnerability, safety, audit, npm, pypi, github, cve, snyk, supply-chain, pre-install
license: MIT
---

# Security Check

Pre-installation security verification for external code and dependencies.

## Core Principle

**Always verify before you download.** External code (GitHub repos, npm packages, PyPI libraries, scripts) can contain malicious code, vulnerabilities, or supply chain attacks. This skill automates security checks **before** executing potentially dangerous commands.

## When to Use

Automatically trigger security check **before**:

- `git clone <url>` — GitHub/GitLab repositories
- `pip install <package>` — Python packages
- `npm install <package>` — Node packages
- `curl <url> | bash` — Shell scripts
- Downloading any external code for execution

## How It Works

### 1. Detect Source Type

Identify what's being installed:
- GitHub URL → Repository check
- PyPI package name → Package check
- npm package name → Package check
- Direct URL → Script/file check

### 2. Gather Security Metrics

Based on source type, collect:

**For GitHub repos:**
- Stars, forks, watchers
- Last commit date
- Open issues (especially `security` labels)
- Contributors count
- License type
- Code of Conduct presence

**For PyPI packages:**
- Downloads per month
- Release frequency
- Maintainer info
- Known CVEs (via safety DB)
- Dependencies count

**For npm packages:**
- Weekly downloads
- Dependencies count (fewer is better)
- Link to source code
- License
- Known vulnerabilities (Snyk)

### 3. Calculate Risk Score

Use threshold-based scoring (inspired by Skantek):

```
Risk Score = 0

# Positive signals (reduce risk):
- High stars/downloads: -10
- Recent activity (< 30 days): -5
- Well-known maintainer: -5
- Clear license: -3
- Few dependencies: -5

# Negative signals (increase risk):
- No activity (> 1 year): +15
- No license: +10
- Many dependencies: +5 per 10 deps
- Known CVEs: +20 per CVE
- Suspicious patterns: +25
```

**Risk Levels:**
- `Score < 0` → ✅ **Safe** (proceed automatically)
- `0 <= Score < 15` → ⚠️ **Review** (show summary, ask confirmation)
- `Score >= 15` → ❌ **Dangerous** (strong warning, manual approval required)

### 4. Show Summary

Present findings:

```
🔒 Security Check: <package/repo>

Risk Level: ⚠️ REVIEW

Metrics:
  ✅ Stars: 15.2k | Forks: 3.1k
  ⚠️  Last commit: 8 months ago
  ✅ License: MIT
  ⚠️  Open security issues: 2
  ✅ Dependencies: 5

Known Issues:
  - CVE-2024-12345 (Medium severity, patched in v1.2.3)

Recommendation: Update to v1.2.3+ before installing.

Proceed? [Y/n]
```

### 5. Request Confirmation

Based on risk level:
- ✅ Safe → Inform user, proceed automatically (unless user explicitly wants review)
- ⚠️ Review → Show summary, ask confirmation
- ❌ Dangerous → Strong warning, require explicit approval

## Implementation Pattern

```python
# Before: git clone https://github.com/user/repo
# After:
1. Detect: GitHub repo
2. Fetch metrics via GitHub API
3. Calculate risk score
4. Show summary
5. Ask confirmation if needed
6. Proceed or abort
```

## Integration Points

### GitHub API
```bash
curl -s "https://api.github.com/repos/{owner}/{repo}"
```

Returns: stars, forks, updated_at, open_issues_count, license

### PyPI JSON API
```bash
curl -s "https://pypi.org/pypi/{package}/json"
```

Returns: downloads, releases, maintainers

### npm Registry
```bash
curl -s "https://registry.npmjs.org/{package}"
```

Returns: downloads (via npm-stat), dependencies, license

### Vulnerability Databases
- **Snyk** (npm): https://security.snyk.io
- **Safety DB** (Python): https://github.com/pyupio/safety-db
- **GitHub Advisory**: https://github.com/advisories

## Best Practices from Research

Based on Adyen's Skantek and GitHub's Dependabot:

1. **Use fewer dependencies** — Each dependency multiplies risk
2. **Regular rescanning** — Zero-day exploits need monitoring
3. **Private registry** — For approved packages (optional)
4. **Threshold-based** — Not binary safe/unsafe, but risk spectrum
5. **Compatibility scores** — Check if update breaks CI tests

## Guardrails

- **Never bypass without user knowledge** — Always inform about security checks
- **Never auto-install flagged packages** — Require manual approval for high-risk
- **Log all decisions** — Track what was installed and why
- **Rate limit API calls** — GitHub/npm/PyPI have rate limits

## Example Workflows

### Example 1: Safe Package

```
User: pip install requests

Security Check:
✅ SAFE: requests (PyPI)
  - Downloads: 50M/month
  - Last release: 2 weeks ago
  - License: Apache 2.0
  - Dependencies: 5
  - Known CVEs: 0

Proceeding with installation...
```

### Example 2: Risky Repo

```
User: git clone https://github.com/suspicious/tool

Security Check:
❌ DANGEROUS: suspicious/tool
  - Stars: 12
  - Last commit: 3 years ago
  - Open issues: 45 (3 security labels)
  - No license
  - Risk score: 35

⚠️  This repository shows multiple red flags.
   Consider alternatives or manual code review.

Proceed anyway? [y/N]
```

### Example 3: Update Needed

```
User: npm install left-pad

Security Check:
⚠️  REVIEW: left-pad@1.0.0
  - Downloads: 2M/week
  - CVE-2024-xxxxx: Prototype pollution (High)
  - Fixed in: v1.0.1

Recommendation: Install v1.0.1 instead.

Use latest version? [Y/n]
```

## Future Enhancements

When skill matures:

1. **Local cache** — Cache risk scores for 24h to reduce API calls
2. **Pattern detection** — Scan code for suspicious patterns (eval, exec, shell commands)
3. **CI/CD integration** — Block deployments with vulnerable dependencies
4. **Custom rules** — User-defined thresholds and blocklists
5. **Reports** — Generate security audit logs

## References

For detailed implementation guidance:
- See `references/skantek-approach.md` — Adyen's methodology
- See `references/vulnerability-databases.md` — How to query CVE databases
