# Example: Full Security Audit

This example shows a complete three-council security audit triggered by a user request.

---

**User:** Run a security scan

**Agent (thinking):**
> Loading config from `config/security-config.json`. Scan directories: `nollio-dashboard`, `normieclaw`. Domains: `https://nolliolabs.com`, `https://normieclaw.ai`. Services: Ollama (11434), Qdrant (6333). Memory checks: memory_md, daily_notes, qmd.

> Running `scripts/security-scan.sh`... parsing JSON output.
> Running `scripts/platform-health.sh`... parsing JSON output.
> Running memory health checks inline.

> Security scan found 3 findings. Checking against state.json — 1 is an accepted risk (CORS on localhost). 2 remain.
> Platform health found 1 finding.
> Memory checks: all clear.

> Calculating scores: Security 6.5, Platform 8.0, Memory 9.5. Overall: 7.4.

**Agent:**

🛡️ **Security Team: Audit Complete**
Overall Score: 🟡 7.4/10

🛡️ **Security Council — 6.5/10** [2 issues]
🔴 CRITICAL: Possible hardcoded secret (sk-pro***) in `nollio-dashboard/scripts/test-api.js` (line 22)
→ Move to environment variable. If committed to git, rotate the key immediately.

🟡 MEDIUM: npm audit: 4 moderate vulnerabilities in `normieclaw`
→ Run `npm audit fix` or review with `npm audit`.

⚙️ **Platform Council — 8.0/10** [1 issue]
🟡 MEDIUM: Uncommitted changes in `normieclaw` (5 files modified)
→ Review and commit or stash your changes.

🟢 https://nolliolabs.com — UP (200)
🟢 https://normieclaw.ai — UP (200)
🟢 Ollama — UP
🟢 Qdrant — UP
🟢 Disk usage: 62%

🧠 **Memory Monitor — 9.5/10** [All Clear]
🟢 MEMORY.md healthy (14KB)
🟢 Today's daily note exists
🟢 QMD index fresh (1h 20m ago)

Reply: "Accept risk [issue]" to mute · "Fix [issue]" for remediation steps

---

**User:** Accept risk the npm vulnerabilities in normieclaw — we're rewriting that module next week

**Agent (thinking):**
> Finding the npm audit finding in state.json by matching description substring "npm audit" + "normieclaw".
> Moving hash `npm-audit-normieclaw-moderate-4` from known_issues to accepted_risks with reason and timestamp.

**Agent:**

✅ Accepted risk: "npm audit: 4 moderate vulnerabilities in normieclaw"
Reason: Rewriting module next week.
I won't flag this again unless the vulnerability count changes.

---

**User:** Fix the hardcoded secret

**Agent:**

Got it. Here's what to do:

1. **Open** `nollio-dashboard/scripts/test-api.js` line 22
2. **Replace** the hardcoded key with `process.env.OPENAI_API_KEY`
3. **Rotate** the exposed key — it's been in your source code, so generate a new one from your OpenAI dashboard
4. **Check git history** — if this was ever committed, consider using BFG Repo-Cleaner to purge it

Want me to note this for a coding agent to handle, or are you fixing it manually?
