---
name: password-policy-auditor
description: Audit password policies and authentication configurations for security compliance. Check password complexity, storage (hashing algorithms), rotation policies, MFA coverage, account lockout, and compliance with NIST 800-63, OWASP, and PCI-DSS guidelines.
---

# Password Policy Auditor

Audit your authentication system against modern security standards. Check password complexity rules, storage practices (bcrypt vs MD5), MFA adoption, account lockout policies, and compliance with NIST 800-63B, OWASP ASVS, and PCI-DSS — then generate a remediation plan.

Use when: "audit password policy", "is our auth secure", "password security review", "NIST compliance", "MFA audit", "authentication hardening", "are we storing passwords safely", or before security assessments.

## Commands

### 1. `audit` — Full Authentication Audit

#### Step 1: Check Password Hashing

```bash
# Find password hashing in code
rg "bcrypt|argon2|scrypt|pbkdf2|sha256|sha512|md5|hashlib" \
  --type-not binary -g '!node_modules' -g '!vendor' -g '!*.test.*' 2>/dev/null

# Check for plaintext password storage
rg -i "password.*=.*['\"]|password.*store|INSERT.*password" \
  --type-not binary -g '!node_modules' -g '!vendor' -g '!*.test.*' 2>/dev/null
```

Rate the hashing algorithm:
| Algorithm | Rating | Notes |
|-----------|--------|-------|
| Argon2id | 🟢 Best | Memory-hard, recommended by OWASP |
| bcrypt | 🟢 Good | Time-tested, work factor ≥ 12 |
| scrypt | 🟢 Good | Memory-hard alternative |
| PBKDF2 | 🟡 Acceptable | Needs ≥ 600K iterations (OWASP 2023) |
| SHA-256/512 + salt | 🔴 Weak | Too fast for password hashing |
| MD5 | 🔴 Critical | Broken, must migrate immediately |
| Plaintext | 🔴 Critical | Unacceptable in any context |

#### Step 2: Check Password Policy Configuration

```bash
# Find password validation rules
rg "password.*length|min.*password|password.*policy|password.*validation|password.*strength" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null

# Check for complexity requirements
rg "uppercase|lowercase|digit|special.*char|complexity" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null
```

Evaluate against NIST SP 800-63B (2024):

| Requirement | NIST Recommendation | Status |
|-------------|-------------------|--------|
| Minimum length | ≥ 8 characters (15+ recommended) | Check |
| Maximum length | ≥ 64 characters | Check |
| Complexity rules | NOT required (users pick bad passwords with forced complexity) | Check |
| Breached password check | REQUIRED — check against known breach lists | Check |
| Password rotation | NOT required (only on evidence of compromise) | Check |
| Password hints | NOT allowed | Check |
| Knowledge-based auth | NOT recommended (mother's maiden name, etc.) | Check |

#### Step 3: Check Account Security Features

```bash
# MFA implementation
rg "totp|2fa|mfa|authenticator|otp|two.factor" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null

# Account lockout
rg "lockout|lock.*account|failed.*attempt|max.*attempt|brute.force" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null

# Rate limiting on auth endpoints
rg "rate.limit|throttle|login.*limit" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null

# Session management
rg "session.*timeout|session.*expire|max.*session|concurrent.*session" \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null
```

#### Step 4: Check for Breached Passwords

```bash
# HaveIBeenPwned k-Anonymity API (safe, only sends hash prefix)
python3 -c "
import hashlib, requests
password = 'password123'
sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
prefix, suffix = sha1[:5], sha1[5:]
resp = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
for line in resp.text.splitlines():
    h, count = line.split(':')
    if h == suffix:
        print(f'🔴 Password found in {count} breaches!')
        break
else:
    print('✅ Password not found in known breaches')
"
```

#### Step 5: Generate Report

```markdown
# Password Policy Audit Report

## Overall Score: 62/100 (⚠️ Needs Improvement)

## Password Storage
- Algorithm: bcrypt ✅
- Work factor: 10 (🟡 recommend ≥ 12)
- Salt: automatic (bcrypt built-in) ✅
- No plaintext storage found ✅

## Password Policy
| Rule | Current | NIST 800-63B | OWASP | Status |
|------|---------|-------------|--------|--------|
| Min length | 8 | ≥ 8 (15+ recommended) | ≥ 8 | 🟡 |
| Max length | 50 | ≥ 64 | ≥ 128 | ❌ Increase to 128 |
| Complexity | Required | Not required | Not required | 🟡 Remove |
| Breach check | ❌ None | Required | Required | ❌ Add HIBP check |
| Rotation | 90 days | Not required | Not required | 🟡 Remove forced rotation |

## Account Security
- MFA: Available but not enforced (23% adoption) ⚠️
- Account lockout: After 5 failures, 30 min lock ✅
- Rate limiting on /login: 10 req/min/IP ✅
- Session timeout: 24 hours (🟡 consider 8h for sensitive apps)
- Concurrent sessions: Unlimited (🟡 consider limiting)

## Critical Issues
1. 🔴 No breached password checking — users can set `password123`
2. 🔴 Max password length only 50 chars — blocks passphrase users
3. 🟡 bcrypt work factor 10 — increase to 12 (rehash on login)
4. 🟡 MFA not enforced for admin accounts

## Remediation Plan
1. Implement HIBP breach check on registration and password change
2. Increase max password length to 128
3. Remove complexity requirements (per NIST)
4. Remove forced 90-day rotation (per NIST)
5. Enforce MFA for all admin/privileged accounts
6. Increase bcrypt rounds to 12 (transparent rehash on next login)
```

### 2. `compliance` — Map to Specific Standard

Generate compliance checklist for:
- **NIST SP 800-63B** — Digital Identity Guidelines
- **OWASP ASVS v4** — Application Security Verification
- **PCI-DSS v4** — Payment Card Industry
- **SOC 2** — Service Organization Controls
- **ISO 27001** — Information Security Management

### 3. `migrate` — Plan Password Hash Migration

If using weak hashing (MD5, SHA-256), generate migration plan:
- Wrap existing hash with bcrypt (dual-hash during transition)
- Rehash on next successful login
- Force password reset for accounts not logged in within N months
- Preserve audit trail of migration status
