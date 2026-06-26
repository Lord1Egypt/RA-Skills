---
name: vibe-safe
description: Security pre-flight for AI coding agents — plan libs, audit CVEs, certify, then code. Non-blocking in autonomous mode (ex-post report).
trigger: Before writing any code that installs or uses external packages/libraries
version: 1.1.0
compatible: claude-code, kimi, hermes, openclaw, copilot, cursor
---

# VibeSafe — Security Pre-Flight Protocol

> **Vibe coding fast is fine. Vibe coding blind is debt.**
> Run this BEFORE committing to any library. Redesign is free before you write line 1. It's not free on line 1000.

---

## WHEN TO INVOKE

**Always invoke when:**
- Starting a new project or feature that adds dependencies
- User says "use X library" or "install Y"
- You are about to write a `package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`

**Safe to skip:** Pure logic code, refactoring existing code, documentation, config changes with no new deps.

**Autonomous mode:** Run phases 1-3 AFTER coding (ex-post), append `risk-report.md` to session output. Never block the user mid-flow.

**Interactive mode:** Run phases 1-3 BEFORE coding. User can type `/skip-audit` to proceed anyway (decision logged in stay_safe.md as "user-waived").

---

## PHASE 1: PLAN

Before touching any code, produce this exact table in your response:

```markdown
## VibeSafe Pre-Flight — Planning

### Proposed Libraries
| Library | Version (target) | Ecosystem | Purpose | Alternatives considered | Why this one |
|---------|-----------------|-----------|---------|------------------------|--------------|
| express | ^4.18           | npm       | HTTP server | fastify, hono, koa | ecosystem size |
| ...     | ...             | ...       | ...     | ...                    | ...          |

### Threat Model
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Supply chain attack via malicious package | Low | Critical | Pin exact versions, use lockfile |
| CVE in outdated dep | Medium | High | Audit before code |
| Secrets leaked to git | Medium | Critical | .env + .gitignore policy |
| Unmaintained lib breaks in 6 months | Medium | Medium | Check last commit < 12 months |
```

**Secrets policy declaration (MANDATORY):**
Confirm in your plan:
- API keys go into `.env` file only, never in source code
- `.env` is always in `.gitignore`
- Credentials are accessed via environment variables or a secret manager
- `.env.example` with dummy values is committed to the repo

If any library requires embedding secrets in source code: REDESIGN, find alternative.

---

## PHASE 2: AUDIT

Run these checks. Use real tools when available. Always run at least the OSV API check (no tools required).

### Node.js / npm
```bash
# If package.json exists or you are about to create one:
npm audit --json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
vulns = d.get('vulnerabilities', {})
critical = sum(1 for v in vulns.values() if v.get('severity') == 'critical')
high = sum(1 for v in vulns.values() if v.get('severity') == 'high')
medium = sum(1 for v in vulns.values() if v.get('severity') == 'moderate')
print(f'Critical: {critical}, High: {high}, Medium: {medium}, Total: {len(vulns)}')
" 2>/dev/null || echo "npm audit not available — use OSV API check instead"
```

### Python / pip
```bash
# Install pip-audit if missing, then run:
pip show pip-audit > /dev/null 2>&1 || pip install pip-audit --quiet
pip-audit --format=json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
deps = d.get('dependencies', [])
critical = [v for dep in deps for v in dep.get('vulns', []) if v.get('severity', '').lower() == 'critical']
high = [v for dep in deps for v in dep.get('vulns', []) if v.get('severity', '').lower() == 'high']
print(f'Critical: {len(critical)}, High: {len(high)}, Packages checked: {len(deps)}')
" 2>/dev/null || echo "pip-audit not available — install: pip install pip-audit"
```

### OSV.dev API (any ecosystem, no local tools required)
For each planned library, query the open vulnerability database:
```bash
# Replace LIBRARY_NAME and ECOSYSTEM (npm, PyPI, Go, crates.io, RubyGems, Maven, NuGet)
curl -s -X POST https://api.osv.dev/v1/query \
  -H "Content-Type: application/json" \
  -d '{"package":{"name":"LIBRARY_NAME","ecosystem":"npm"}}' \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
vulns = d.get('vulns', [])
for v in vulns:
    sev = v.get('database_specific', {}).get('severity', 'unknown')
    print(f\"{v['id']}: {sev} — {v.get('summary','')[:80]}\")
if not vulns:
    print('No known vulnerabilities')
"
```

### Maintenance check (GitHub API)
```bash
# For open-source libs, check recency of last commit:
# Replace OWNER/REPO with the package source repository
curl -s "https://api.github.com/repos/OWNER/REPO/commits?per_page=1" \
  -H "Accept: application/vnd.github.v3+json" \
  | python3 -c "
import json, sys
from datetime import datetime, timezone
d = json.load(sys.stdin)
if d and isinstance(d, list):
    date_str = d[0]['commit']['author']['date']
    last = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    age = (datetime.now(timezone.utc) - last).days
    print(f'Last commit: {date_str} ({age} days ago)')
    if age > 365:
        print('WARNING: Unmaintained (>12 months without commits)')
    if age > 730:
        print('CRITICAL: Abandoned (>24 months without commits)')
else:
    print('Could not fetch commit data')
"
```

### deps.dev API (Google — maintenance, licensing, advisories)
```bash
# For npm packages (URL-encode as needed)
PKGNAME="express"
curl -s "https://api.deps.dev/v3alpha/packages/npm/${PKGNAME}" \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('Advisories:', d.get('advisoryKeys', []))
versions = d.get('versions', [])
if versions:
    latest = sorted(versions, key=lambda v: v.get('publishedAt',''), reverse=True)[0]
    print('Latest version:', latest.get('versionKey', {}).get('version'))
    print('Published:', latest.get('publishedAt'))
"
```

### Decision thresholds

**Auto-BLOCK (agent cannot proceed without redesign):**
- Critical CVE with no fix available
- Package requires embedding credentials in source code
- Package has no license in a licensed project
- Package has 0 downloads and no commits in 24+ months (likely abandoned/typosquat)
- Package name matches a known typosquat pattern (e.g., `reacts`, `lodahs`)

**CONDITIONAL (user decision required, proceed with acknowledgment):**
- High CVE with an available fix (fix it first, then downgrade to CERTIFIED)
- Last commit 12-24 months ago
- Package has <100 weekly downloads (bus factor risk)
- Dependency chain is unusually deep (>15 levels for npm)

**CERTIFIED (proceed):**
- No critical or high CVEs
- Last commit within 12 months
- Active maintainer community
- License is compatible with project

---

## PHASE 3: CERTIFY

After running audits, generate `stay_safe.md` in the project root by calling:

```bash
./tools/stay-safe-gen.sh .vibesafe/summary.json
# OR
python3 ./tools/audit.py --generate-cert
```

**Certification rules:**

| Audit Result | Certificate Status | Can proceed? |
|---|---|---|
| No critical/high CVEs, all maintained | CERTIFIED | Yes, immediately |
| High CVE with available patch | CONDITIONAL | Yes, after user acknowledges |
| Medium CVEs or unmaintained packages | CONDITIONAL | Yes, after user acknowledges |
| Critical CVE with no fix | BLOCKED | No — redesign required |
| Abandoned package (24+ months) | BLOCKED | No — replace package |

When BLOCKED: go back to PHASE 1, replace the flagged library, re-run audit.
Maximum 3 redesign iterations. After 3 failures: "I cannot find a safe dependency for this purpose. Please advise."

---

## PHASE 4: CODE

Only after `stay_safe.md` shows CERTIFIED or CONDITIONAL (with explicit user approval in interactive mode):

1. Implement the solution using ONLY audited libraries
2. Apply secrets policy: all credentials via `process.env.X` or `os.environ["X"]`
3. Create `.env.example` with dummy/placeholder values for all required env vars
4. Verify `.gitignore` covers `.env`, `.env.*`, `*.key`, `*.pem`, `secrets.*`, `credentials.*`, `.vibesafe/`
5. If a new dependency is discovered mid-coding that was NOT in the Phase 1 plan:
   - Stop
   - Add the package to plan
   - Run OSV API check for that package (minimum)
   - Continue only if clean

---

## PHASE 5: POST-CODING REPORT (Autonomous mode)

After coding is complete, run a final scan on actually-installed packages and produce `risk-report.md`:

```bash
./tools/audit.sh --mode=installed > .vibesafe/post-summary.json
./tools/stay-safe-gen.sh .vibesafe/post-summary.json --template=risk-report
```

If post-scan finds new critical/high CVEs (introduced by transitive dependencies during install),
prepend this block to the final response:

```
WARNING — VibeSafe Post-Coding Scan Found New Issues
=====================================================
Critical CVEs found in installed packages: N
High CVEs found in installed packages: N
These were not present in the pre-flight plan (likely transitive dependencies).
See risk-report.md for full details.
Action required before deploying to production.
```

---

## REDESIGN LOOP

```
BLOCKED package detected
        |
        v
Remove from plan
        |
        v
Check "Alternatives considered" column from Phase 1
        |
        v
Evaluate alternative with Phase 2 audit
        |
   _____|_____
  |           |
CLEAN      BLOCKED
  |           |
Proceed    Attempt #2 alternative
           If no more alternatives:
           "Can this feature be implemented without any external library?"
           If no: escalate to user
```

---

## SKIP MECHANISM

User can type `/skip-audit` or `skip preflight` at any point in interactive mode.

When skipped:
- Log in stay_safe.md: `Status: USER-WAIVED — audit skipped by user at {ISO_TIMESTAMP}`
- Continue coding normally
- STILL run post-coding report (Phase 5) — skip does not disable ex-post scan
- Note in final output: "Security pre-flight was skipped. Run ./tools/audit.sh before production deploy."

---

## SECRETS POLICY — MANDATORY FOR ALL CODE WRITTEN

The agent MUST enforce these rules in every file it writes during Phase 4:

| Rule | Implementation |
|---|---|
| No secrets in source | Never write API keys, passwords, tokens, connection strings in .js/.py/.ts/.go/.rs/.rb |
| Use env vars | `process.env.MY_SECRET` (Node) / `os.environ["MY_SECRET"]` (Python) / `os.Getenv("MY_SECRET")` (Go) |
| Document secrets | Always create `.env.example` with placeholder values |
| Protect .env | Always ensure `.gitignore` includes `.env` and `.env.*` |
| Recommend hooks | Suggest `detect-secrets` or `git-secrets` as pre-commit hook |

---

## AGENT INVOCATION REFERENCE

| Agent | How to invoke |
|---|---|
| Claude Code | `Skill("vibe-safe")` or prefix task: "Run vibe-safe pre-flight first" |
| Kimi CLI / Hermes | Read this file from known path, execute phases via tool calls |
| OpenClaw (port 18789) | Configure webhook trigger on package install pattern |
| VS Code Continue/Copilot | Run "VibeSafe: Audit Project" task from `.vscode/tasks.json` |
| CI/CD | `.github/workflows/security-gate.yml` on push/PR |

---

## QUICK REFERENCE

```
/vibe-safe          — run full pre-flight (interactive)
/vibe-safe skip     — skip to coding, run post-scan only
/vibe-safe report   — run phase 5 post-scan on current project
/vibe-safe cert     — show current stay_safe.md status
```

## SCOPE — WHAT VIBESAFE DOES NOT DO

- VibeSafe does not run SAST on your own code (use Semgrep, CodeQL, Bandit)
- VibeSafe does not scan container images (use Trivy, Grype)
- VibeSafe does not manage secret rotation (use Vault, AWS Secrets Manager)
- VibeSafe audits external dependencies only — not your business logic
