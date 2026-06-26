---
name: key-rotation-planner
description: Plan and track cryptographic key rotations for API keys, encryption keys, signing keys, and service credentials. Inventory all keys, assess rotation urgency, generate rotation runbooks, and verify post-rotation health.
---

# Key Rotation Planner

Manage cryptographic key rotations without breaking production. Inventory all keys and credentials, assess rotation urgency based on age, exposure risk, and compliance requirements, generate step-by-step rotation runbooks, and verify nothing breaks after rotation.

Use when: "rotate keys", "key rotation plan", "API key rotation", "credential rotation", "how old are our keys", "key management audit", "secret hygiene", or before compliance audits requiring key rotation evidence.

## Commands

### 1. `inventory` — Catalog All Keys and Credentials

#### Step 1: Discover Keys in Code and Config

```bash
# Find hardcoded secrets (should be 0)
rg -i "(api_key|apikey|secret_key|access_key|private_key|token)\s*[=:]\s*['\"][a-zA-Z0-9+/=_-]{16,}" \
  --type-not binary -g '!node_modules' -g '!vendor' -g '!*.test.*' -g '!*.example*' 2>/dev/null

# Find environment variable references for secrets
rg -i "(API_KEY|SECRET|TOKEN|PASSWORD|PRIVATE_KEY|ACCESS_KEY|CLIENT_SECRET)" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null | \
  grep -v "test\|example\|mock\|fake\|dummy" | head -30

# Check secrets manager
aws secretsmanager list-secrets 2>/dev/null | python3 -c "
import json, sys
secrets = json.load(sys.stdin)['SecretList']
for s in secrets:
    last_rotated = s.get('LastRotatedDate', 'NEVER')
    last_changed = s.get('LastChangedDate', 'Unknown')
    print(f'{s[\"Name\"]}: last_rotated={last_rotated}, last_changed={last_changed}')
"

# Vault secrets
vault secrets list 2>/dev/null
vault list secret/ 2>/dev/null
```

#### Step 2: Assess Rotation Urgency

For each key/credential:

| Factor | Score | Criteria |
|--------|-------|---------|
| Age | 🔴 5 | Never rotated or > 1 year |
| Age | 🟡 3 | 6-12 months |
| Age | 🟢 1 | < 6 months |
| Exposure | 🔴 5 | In code/git history |
| Exposure | 🟡 3 | In env file on server |
| Exposure | 🟢 1 | In secrets manager |
| Scope | 🔴 5 | Admin/root access |
| Scope | 🟡 3 | Write access |
| Scope | 🟢 1 | Read-only |
| Compliance | 🔴 5 | Required by PCI/SOC2 |
| Compliance | 🟢 1 | No compliance requirement |

Priority = sum of scores. Rotate highest priority first.

#### Step 3: Generate Inventory Report

```markdown
# Key and Credential Inventory

## Summary
- Total keys/credentials: 34
- Overdue for rotation: 12 (🔴)
- Due soon (30 days): 5 (🟡)
- Healthy: 17 (🟢)

## Critical (rotate immediately)
| Key | Type | Age | Last Rotated | Location | Priority |
|-----|------|-----|-------------|----------|----------|
| STRIPE_SECRET_KEY | API key | 14 months | Never | .env (server) | 18/20 🔴 |
| DB_PASSWORD (prod) | Password | 11 months | 2025-05-15 | Vault | 15/20 🔴 |
| JWT_SIGNING_KEY | Signing key | 8 months | 2025-08-01 | env var | 14/20 🔴 |

## Rotation Schedule
| Key | Next Rotation | Responsible | Runbook |
|-----|--------------|-------------|---------|
| STRIPE_SECRET_KEY | ASAP | @payments-team | See below |
| DB_PASSWORD | May 2026 | @infra | DB password rotation runbook |
```

### 2. `rotate` — Generate Rotation Runbook

For each key type, generate a step-by-step rotation runbook:

**API Key Rotation (zero-downtime):**
1. Generate new key in provider dashboard
2. Add new key to secrets manager alongside old key
3. Deploy application update to use new key
4. Verify new key works (test API call)
5. Wait for old key to drain from all instances
6. Revoke old key in provider dashboard
7. Remove old key from secrets manager
8. Update inventory with rotation date

**Database Password Rotation:**
1. Generate new password
2. Create temp user with new password in database
3. Update secrets manager with new password
4. Rolling restart of application instances
5. Verify connections using new password
6. Drop old user / change password on existing user
7. Update inventory

**JWT Signing Key Rotation (asymmetric):**
1. Generate new key pair
2. Add new public key to JWKS endpoint (both keys listed)
3. Switch signing to new private key
4. Wait for all old tokens to expire (max TTL)
5. Remove old public key from JWKS endpoint
6. Archive old key pair

### 3. `verify` — Post-Rotation Health Check

After rotation, verify:
- Application starts without errors
- API calls succeed with new key
- No auth failures in logs
- Old key is actually revoked (test that it fails)
- Monitoring shows normal error rates
- No services still using old key (grep for old key hash)

### 4. `schedule` — Set Up Rotation Reminders

Generate calendar events or ticketing system reminders:
- API keys: every 90 days
- Database passwords: every 180 days
- Signing keys: every 365 days
- SSL certificates: 30 days before expiry
- SSH keys: every 365 days
