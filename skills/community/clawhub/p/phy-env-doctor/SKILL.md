---
name: Env Doctor
description: Scans your codebase to auto-discover every environment variable referenced in source code, generates a fully-documented .env.example, detects missing vars in your current .env, and flags security risks (logged secrets, committed .env files, exposed keys). Works across Node.js, Python, Go, Ruby, and shell scripts. Zero config — just run it in your project directory. Triggers on "env doctor", "check env vars", "generate .env.example", "missing environment variables", "audit secrets", "/env-doctor".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - environment-variables
    - secrets
    - dotenv
    - security
    - developer-tools
    - configuration
    - node
    - python
    - go
---

# Env Doctor

Scan any codebase for environment variable usage, auto-generate a documented `.env.example`, find missing vars, and catch secret leaks — before they reach production.

**No config files. No API keys. Works entirely from your source code.**

---

## Trigger Phrases

- "env doctor", "check env vars", "audit my env"
- "generate .env.example", "what env vars does this project need"
- "missing environment variables", "undefined env vars"
- "audit secrets", "are any secrets exposed"
- "/env-doctor"

---

## Step 1: Scan Source Code for All Env References

Run language-specific grep patterns to extract every referenced environment variable:

```bash
# Node.js / TypeScript — process.env.VAR_NAME
grep -rn "process\.env\.\([A-Z_][A-Z0-9_]*\)" \
  --include="*.js" --include="*.ts" --include="*.mjs" --include="*.cjs" \
  --exclude-dir=node_modules --exclude-dir=.git \
  -h . | grep -oE "process\.env\.[A-Z_][A-Z0-9_]*" | sort -u

# Python — os.environ["VAR"] / os.getenv("VAR") / os.environ.get("VAR")
grep -rn \
  --include="*.py" --exclude-dir=.git --exclude-dir=venv --exclude-dir=__pycache__ \
  -hE 'os\.environ\[.([A-Z_][A-Z0-9_]*).|(os\.getenv|os\.environ\.get)\(.([A-Z_][A-Z0-9_]*).' \
  . | grep -oE '[A-Z_][A-Z0-9_]{2,}' | sort -u

# Go — os.Getenv("VAR")
grep -rn --include="*.go" --exclude-dir=.git \
  -hE 'os\.Getenv\("([A-Z_][A-Z0-9_]*)"\)' \
  . | grep -oE '"[A-Z_][A-Z0-9_]*"' | tr -d '"' | sort -u

# Ruby — ENV["VAR"] / ENV.fetch("VAR")
grep -rn --include="*.rb" --exclude-dir=.git \
  -hE 'ENV\[.([A-Z_][A-Z0-9_]*).|(ENV\.fetch)\(.([A-Z_][A-Z0-9_]*).' \
  . | grep -oE '[A-Z_][A-Z0-9_]{2,}' | sort -u

# Shell scripts
grep -rn --include="*.sh" --include="*.bash" --exclude-dir=.git \
  -hE '\$\{?([A-Z_][A-Z0-9_]*)\}?' \
  . | grep -oE '[A-Z_][A-Z0-9_]{2,}' | grep -v "^IFS$\|^PATH$\|^HOME$\|^USER$\|^PWD$\|^SHELL$" | sort -u
```

Combine all results into a **master list** of required env vars, with the file:line where each is used.

---

## Step 2: Compare Against Current .env

```bash
# Parse current .env (if exists)
if [ -f .env ]; then
  grep -v '^#' .env | grep '=' | cut -d= -f1 | sort -u > /tmp/env_defined.txt
  echo "Found $(wc -l < /tmp/env_defined.txt) defined vars"
else
  echo "No .env file found"
fi

# Check for .env.example
if [ -f .env.example ]; then
  grep -v '^#' .env.example | grep '=' | cut -d= -f1 | sort -u > /tmp/env_example.txt
  echo "Found $(wc -l < /tmp/env_example.txt) vars in .env.example"
fi
```

Cross-reference to find:
- **Missing**: In code but not in `.env` → will cause runtime errors
- **Undocumented**: In `.env` but not in `.env.example` → invisible to new team members
- **Orphaned**: In `.env.example` but not in code → stale, can be removed

---

## Step 3: Infer Documentation from Usage Context

For each env var found, read the surrounding code to infer what it does:

```bash
# Get 3 lines of context around each usage
grep -rn "PROCESS_ENV_VAR_NAME\|os.getenv.*VAR_NAME" . --include="*.py" --include="*.js" -A 1 -B 1
```

Use the context to generate a human-readable description:
- If used in a database connection → "PostgreSQL connection string"
- If used in an API client constructor → "API key for [service]"
- If used in `if (process.env.X === 'true')` → "Feature flag — set to 'true' to enable"
- If used as a URL → "Base URL for [service] API"
- If used in JWT signing → "Secret key for JWT signing — must be 32+ chars, random"

---

## Step 4: Security Scan

Check for dangerous patterns that could expose secrets:

```bash
# 1. Is .env committed to git?
git ls-files .env 2>/dev/null && echo "⚠️  .env IS TRACKED BY GIT"

# 2. Is .env in .gitignore?
grep -q "^\.env$\|^\.env\b" .gitignore 2>/dev/null && echo "✅ .env in .gitignore" || echo "⚠️  .env NOT in .gitignore"

# 3. Any env vars being logged/printed?
grep -rn --include="*.js" --include="*.ts" --include="*.py" \
  -E "(console\.log|print|logger\.(info|debug|warn))\(.*process\.env|os\.environ" \
  . | grep -v node_modules | head -10

# 4. Any hardcoded secrets (common patterns)?
grep -rn --include="*.js" --include="*.ts" --include="*.py" --include="*.go" \
  -E "(api_key|apikey|secret|password|token)\s*=\s*['\"][a-zA-Z0-9+/]{20,}['\"]" \
  . | grep -v "\.env\|test\|spec\|mock\|example" | grep -v node_modules | head -10

# 5. Any .env files other than root?
find . -name ".env*" -not -path "*/node_modules/*" -not -name ".env.example" -not -name ".env.sample"
```

---

## Step 5: Generate .env.example

Build a complete, documented `.env.example`:

```bash
cat > .env.example.generated << 'EOF'
# Generated by phy-env-doctor — $(date)
# This file documents all environment variables required by this project.
# Copy to .env and fill in real values. Never commit .env to version control.

# ─── DATABASE ───────────────────────────────────────────────
DATABASE_URL=          # PostgreSQL connection string. Format: postgresql://user:pass@host:5432/dbname

# ─── AUTHENTICATION ─────────────────────────────────────────
JWT_SECRET=            # Secret key for JWT signing. Must be 32+ random chars. Generate: openssl rand -base64 32
JWT_EXPIRY=7d          # Token expiry duration. Examples: 7d, 24h, 3600

# ─── EXTERNAL APIs ──────────────────────────────────────────
STRIPE_SECRET_KEY=     # Stripe secret key. Get from dashboard.stripe.com/apikeys
STRIPE_WEBHOOK_SECRET= # Stripe webhook signing secret. Get from Stripe CLI or dashboard.

# ─── APP CONFIG ─────────────────────────────────────────────
NODE_ENV=development   # Environment: development | staging | production
PORT=3000              # HTTP server port
LOG_LEVEL=info         # Logging level: debug | info | warn | error
EOF
```

Group vars by category (inferred from names and usage patterns):
- `DATABASE_*`, `DB_*`, `POSTGRES_*`, `MONGO_*`, `REDIS_*` → **Database**
- `JWT_*`, `AUTH_*`, `SESSION_*`, `COOKIE_*` → **Authentication**
- `STRIPE_*`, `PAYPAL_*`, `BRAINTREE_*` → **Payments**
- `SMTP_*`, `SENDGRID_*`, `MAILGUN_*`, `EMAIL_*` → **Email**
- `AWS_*`, `GCP_*`, `AZURE_*`, `S3_*` → **Cloud / Storage**
- `*_API_KEY`, `*_SECRET`, `*_TOKEN` → **API Keys**
- `NODE_ENV`, `PORT`, `LOG_*`, `DEBUG` → **App Config**

---

## Output Format

```markdown
## Env Doctor Report
Project: [name] | $(date) | Languages: Node.js, Python

### Summary
| Status | Count |
|--------|-------|
| ✅ Defined in .env | 12 |
| ❌ Missing (in code, not in .env) | 3 |
| 📋 Undocumented (in .env, not in .env.example) | 5 |
| 🗑️ Orphaned (in .env.example, not in code) | 1 |
| ⚠️ Security issues | 2 |

---

### ❌ Missing Variables — Will Cause Runtime Errors

| Variable | Used In | Type (inferred) |
|----------|---------|-----------------|
| `REDIS_URL` | src/cache.ts:14 | Redis connection string |
| `SENDGRID_API_KEY` | lib/email.js:8 | API key for SendGrid |
| `ENCRYPTION_KEY` | utils/crypto.py:22 | AES encryption key (32 chars) |

**Quick fix:**
\`\`\`bash
echo "REDIS_URL=" >> .env
echo "SENDGRID_API_KEY=" >> .env
echo "ENCRYPTION_KEY=" >> .env
\`\`\`

---

### ⚠️ Security Issues

**[CRITICAL]** `.env` is tracked by git
→ Run: `echo ".env" >> .gitignore && git rm --cached .env`

**[HIGH]** Secret potentially logged at `src/auth.js:42`:
→ `console.log('Auth config:', process.env.JWT_SECRET)` — remove this log

---

### 📋 Generated .env.example

[full generated content — ready to copy]

---

### 🗑️ Orphaned Variables (safe to remove from .env.example)

- `OLD_API_URL` — referenced nowhere in current codebase
```

---

## Quick Mode

If user just wants a fast check: `env doctor --quick`

```
Quick Env Check:
❌ 3 missing vars  ⚠️ 2 security issues  📋 5 undocumented

Missing: REDIS_URL, SENDGRID_API_KEY, ENCRYPTION_KEY
Run /env-doctor for full report + generated .env.example
```

---

## Why This Is Different

Existing tools like `bytesagain3/env-config` provide a **template manager** — you tell it what vars to create. This skill does the opposite: it **reads your code** to discover what vars you're already using, then builds documentation from reality, not from what you remember to document.

This solves the #1 env var pain: **undiscovered missing variables that only crash in production**.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
