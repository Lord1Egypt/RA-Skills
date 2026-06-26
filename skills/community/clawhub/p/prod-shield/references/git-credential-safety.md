# Git & GitHub Credential Safety Reference

Quick-reference for credential patterns, .gitignore templates, scanning tools,
and emergency remediation. See SKILL.md Section 17 for full rules.

---

## The Golden Rule

> **NEVER commit credentials to Git. Never. Not to private repos. Not "just temporarily".
> Once pushed, the credential is compromised — full stop. Git history is permanent.**

---

## Credential Regex Detection Patterns

Use these with `grep -rE` or in your scanner configuration to detect secrets before committing.

```
# AWS
AKIA[0-9A-Z]{16}                              AWS Access Key ID
(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+]{40}['\"]  AWS Secret Access Key

# Google / GCP
AIza[0-9A-Za-z\-_]{35}                        Google API key
ya29\.[0-9A-Za-z\-_]+                         Google OAuth2 access token
"private_key":\s*"-----BEGIN                  GCP service account private key in JSON

# GitHub
ghp_[a-zA-Z0-9]{36}                           GitHub Personal Access Token (classic)
github_pat_[a-zA-Z0-9_]{82}                   GitHub fine-grained PAT
ghs_[a-zA-Z0-9]{36}                           GitHub Actions token
ghr_[a-zA-Z0-9]{36}                           GitHub refresh token

# Slack
xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+              Slack bot token
xoxp-[0-9]+-[0-9]+-[0-9]+-[a-zA-Z0-9]+       Slack user token
xoxs-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+ Slack session token

# Stripe
sk_live_[a-zA-Z0-9]{24,}                      Stripe live secret key
sk_test_[a-zA-Z0-9]{24,}                      Stripe test secret key (flag, still a risk)
rk_live_[a-zA-Z0-9]{24,}                      Stripe restricted key

# SendGrid
SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}     SendGrid API key

# Twilio
AC[a-zA-Z0-9]{32}                             Twilio Account SID
SK[a-zA-Z0-9]{32}                             Twilio API key SID

# OpenAI
sk-[a-zA-Z0-9]{48}                            OpenAI API key

# Azure
AccountKey=[a-zA-Z0-9+/=]{88}                 Azure Storage Account key
[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}  Azure client secret GUID context

# Private keys (any type)
-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----

# Generic high-risk patterns
(?i)(password|passwd|pwd|secret|token|api.?key)\s*[=:]\s*[^\s${\'"\\]{6,}
(?i)db.?(pass|password|passwd)\s*[=:]\s*\S+
(?i)(auth|bearer)\s+[a-zA-Z0-9_\-\.]{20,}
```

---

## Quick .gitignore Template

Copy this block into any project's `.gitignore`:

```gitignore
# ── Credentials & secrets — NEVER commit ──────────────────────
.env
.env.*
!.env.example
!.env.template
*.env
secrets.*
*secret*
*secrets*
*credential*
*credentials*

# Private keys & certificates
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
*.crt
*.cer

# Cloud credentials
.aws/
application_default_credentials.json
*service-account*.json
firebase-adminsdk*.json
gcloud-key.json
kubeconfig
*.kubeconfig
*kubeconfig*

# Terraform
*.tfvars
!*.tfvars.example
terraform.tfstate
terraform.tfstate.backup
.terraform/
crash.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Tool auth files
.netrc
.npmrc
.pypirc
.docker/config.json
```

---

## Secrets Scanning Tools — Quick Reference

| Tool | Install | Scan Command | Best For |
|---|---|---|---|
| **gitleaks** | `brew install gitleaks` | `gitleaks detect --source .` | Fast, CI-friendly, wide pattern coverage |
| **detect-secrets** | `pip install detect-secrets` | `detect-secrets scan .` | Baseline-based, reduces noise over time |
| **truffleHog** | `pip install trufflehog` | `trufflehog filesystem .` | High-entropy detection + git history scan |
| **git-secrets** | `brew install git-secrets` | `git secrets --scan` | AWS-focused, pre-commit hooks |
| **semgrep** | `pip install semgrep` | `semgrep --config=p/secrets .` | SAST + secrets, highly configurable |

### Scan git history (finds secrets in past commits):
```bash
trufflehog git file://. --since-commit HEAD~50 --only-verified
gitleaks detect --source . --log-opts="--all"
```

---

## Pre-Commit Hook Setup (Recommended for Every Repo)

```yaml
# .pre-commit-config.yaml
repos:
  # Gitleaks — secret scanning
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.2
    hooks:
      - id: gitleaks

  # detect-secrets — baseline approach
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  # General hygiene
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files    # Catches binary credential files
      - id: check-merge-conflict
      - id: detect-private-key          # Built-in private key detector
```

```bash
pip install pre-commit
pre-commit install           # Now runs automatically on every git commit
pre-commit run --all-files   # One-time scan of everything right now
```

---

## GitHub Native Protection

### Enable in repository settings:
```
Settings → Security → Code security and analysis:
  ✅ Dependency graph
  ✅ Dependabot alerts
  ✅ Dependabot security updates
  ✅ Secret scanning          ← detects known secret patterns in code
  ✅ Push protection          ← BLOCKS pushes containing secrets before they land
```

### Push Protection
When Push Protection is enabled, GitHub will **block the push** if it detects any of 200+
known secret patterns (AWS keys, GitHub tokens, Stripe keys, etc.) and prompt the user to
remove the secret before the push is accepted.

This is the strongest available defense — enable it on every repository.

---

## Emergency Remediation Checklist

If credentials were accidentally committed and pushed:

```
[ ] 1. ROTATE the credential immediately at the source (before touching git)
[ ] 2. Identify all branches and tags that contain the leaked commit
[ ] 3. Scrub git history using git-filter-repo or BFG Repo Cleaner
[ ] 4. Force push all branches: git push origin --force --all
[ ] 5. Force push all tags:     git push origin --force --tags
[ ] 6. Notify all collaborators to delete local clones and re-clone
[ ] 7. Check cloud provider audit logs for unauthorized use
[ ] 8. Check SIEM / access logs for the credential being used
[ ] 9. If a GitHub PAT: check org audit log for activity
[ ] 10. Enable GitHub Push Protection to prevent recurrence
[ ] 11. Add pre-commit hooks (above) to the repository
[ ] 12. Conduct a brief post-mortem — document and share with the team
```

---

## Correct Credential Patterns by Stack

### Node.js
```js
// ✅ Load from environment — never hardcode
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const db = new Pool({ connectionString: process.env.DATABASE_URL });

// 🔴 NEVER
const stripe = new Stripe('<EXAMPLE-STRIPE-LIVE-KEY>');
```

### Python
```python
# ✅ Use environment variables
import os
api_key = os.environ['OPENAI_API_KEY']

# ✅ Use python-dotenv for local development (.env in .gitignore)
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# 🔴 NEVER
api_key = '<EXAMPLE-SECRET-KEY>'
```

### Docker
```dockerfile
# ✅ No credentials in Dockerfile — inject at runtime
ENV APP_PORT=8080

# 🔴 NEVER — visible in image layers and docker history
ENV DB_PASSWORD=<EXAMPLE-PASSWORD>
ARG API_KEY=<EXAMPLE-SECRET-KEY>
```

```bash
# ✅ Inject at runtime
docker run --env-file .env myimage         # .env is in .gitignore
docker run -e API_KEY="$API_KEY" myimage   # From shell environment

# 🔴 NEVER bake credentials into the image
docker build --build-arg API_KEY=<EXAMPLE-SECRET-KEY> .
```

### Terraform
```hcl
# ✅ Use environment variables — no credentials in .tf or .tfvars files
# export TF_VAR_db_password="$(vault kv get -field=password secret/db)"

variable "db_password" {
  type      = string
  sensitive = true
  # Value comes from TF_VAR_db_password env var, never from a committed file
}

# 🔴 NEVER in terraform.tfvars (which should not be committed):
# db_password = "mypassword"
```

### GitHub Actions
```yaml
# ✅ Use repository or environment secrets
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh

# ✅ Best: OIDC — no secrets stored at all
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
    aws-region: ap-southeast-1

# 🔴 NEVER
- run: ./deploy.sh --api-key <EXAMPLE-SECRET-KEY>
```

---

## Credential Rotation Schedule (Recommended)

| Credential Type | Rotation Frequency | Notes |
|---|---|---|
| Long-lived IAM access keys | Every 90 days (better: replace with OIDC) | Audit unused keys monthly |
| Database passwords | Every 90 days or after any staff departure | Use Secrets Manager rotation |
| API keys (third-party) | Every 180 days or after any suspected exposure | Keep previous key active for 24h during rotation |
| GitHub PATs | Every 90 days; use fine-grained PATs with minimal scope | Set expiry when creating |
| Service account keys | Every 90 days (better: use Workload Identity) | Delete old keys immediately after rotation |
| JWT / session secrets | Every 30–90 days | Requires re-login for all active sessions |
| Webhook secrets | After any incident; otherwise annually | |
| SSH keys | Annually or after team member offboarding | |
