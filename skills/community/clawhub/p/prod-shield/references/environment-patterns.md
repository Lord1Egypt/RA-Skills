# Environment Detection Patterns

Patterns Claude uses to identify whether a target is production.
When in doubt, default to treating as production.

---

## Regex Patterns — Production Indicators

```regex
# Exact match (case-insensitive)
^prod$
^production$
^live$
^main$
^master$
^release$
^stable$
^public$

# Prefix patterns
^prod[-_.]
^prd[-_.]
^production[-_.]
^live[-_.]

# Suffix patterns
[-_.]prod$
[-_.]prd$
[-_.]production$
[-_.]live$
[-_.]release$
[-_.]stable$

# Contains patterns (use with context)
.*prod.*
.*production.*
.*live.*

# Obfuscated / typo-variants (treat as production)
^pr0d
^p0d
^pr[0o]d
```

---

## Environment Name Examples

### Treat as PRODUCTION 🔴
```
prod
production
live
main
master
release
stable
public
prd
prod-us-east-1
us-prod
eu-production
prod-db
prod-cluster
prod-api
prod-web
production-database
live-server
main-branch
release-v2
stable-channel
```

### Treat as SAFE (Non-Production) ✅
```
dev
development
local
localhost
test
testing
staging
sandbox
qa
uat
demo
preview
experimental
feature-xyz
hotfix-branch
```

### Ambiguous — Ask Before Proceeding ⚠️
```
# These could be prod or non-prod — always confirm
app
default
primary
core
base
current
latest
new
v2
blue
green
canary
```

---

## Cloud Resource Tags — Production Indicators

### AWS
```
Environment = prod | production | live
Stage = prod | production
Tier = production
Name contains "prod" or "production"
```

### GCP
```
env=prod
environment=production
goog-managed-by with prod context
```

### Azure
```
environment: prod
env: production
```

---

## URL / Endpoint Patterns — Production Indicators

```
api.company.com           (no environment prefix = likely prod)
app.company.com
www.company.com
company.com/api
*.company.com (root domain, no dev/test prefix)

vs. SAFE:
dev.api.company.com
api.dev.company.com
staging-api.company.com
test.company.com
localhost:*
127.0.0.1:*
*.ngrok.io            (local tunnels = dev)
*.vercel.app          (preview deployments — but confirm; see below)
```

---

## Database Connection String Patterns

### Production Indicators in Connection Strings
```
Host: db.company.com                (root domain)
Host: prod-db.company.com
Host: rds.amazonaws.com             (could be prod — check name)
Database name: prod_*, *_prod, production_*
Port: standard (5432, 3306, 27017) on non-localhost = possible prod
SSL required = likely production
```

### Safe Indicators in Connection Strings
```
Host: localhost
Host: 127.0.0.1
Host: dev-db.*, staging-db.*
Database name: dev_*, test_*, staging_*, local_*
Port: non-standard (e.g., 5433 local replica)
```

---

## File Path / Config Patterns

```
# Production config indicators
config/production.yml
config/prod.env
.env.production
.env.prod
settings/prod.py
prod.config.js
production.json

# Safe config indicators
config/development.yml
.env.local
.env.dev
settings/test.py
local.config.js
```

---

## GitHub Actions Environment Detection 🆕

GitHub Actions workflows can target production environments explicitly or implicitly.
Claude must detect these patterns and apply production guards.

### Production Indicators in Workflow Files

```yaml
# Explicit environment declaration
environment: production
environment: prod
environment: live

# Branch triggers targeting protected branches
on:
  push:
    branches:
      - main       # ← PRODUCTION
      - master     # ← PRODUCTION
      - release/*  # ← PRODUCTION
      - stable     # ← PRODUCTION

# Deploy job names (semantic indicators)
jobs:
  deploy-production:
  release:
  publish:
  push-to-prod:

# Secrets referencing production credentials
env:
  AWS_ACCOUNT_ID: ${{ secrets.PROD_AWS_ACCOUNT_ID }}
  KUBE_CONFIG: ${{ secrets.PROD_KUBECONFIG }}
```

### Safe Workflow Patterns
```yaml
on:
  push:
    branches:
      - develop
      - staging
      - feature/*
      - hotfix/*

environment: staging
environment: dev
environment: preview
```

### Ambiguous — Confirm Before Proceeding
```yaml
# workflow_dispatch (manual trigger) — ask user which environment
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'

# pull_request_target — runs with write access to the base repo; treat as sensitive
on:
  pull_request_target:
```

---

## AWS ECS / Lambda / Fargate Environment Detection 🆕

### ECS Task Definition Indicators
```json
{
  "family": "prod-api-task",          // "prod" in family name → production
  "environment": [
    { "name": "ENVIRONMENT", "value": "production" },   // explicit env var
    { "name": "APP_ENV", "value": "prod" }
  ],
  "logConfiguration": {
    "logDriver": "awslogs",
    "options": {
      "awslogs-group": "/ecs/prod-api"   // "prod" in log group → production
    }
  }
}
```

### Lambda Function Name / Environment Patterns
```
# Production indicators in function names
prod-*
*-prod
*_production
*-live

# Environment variables inside Lambda
ENVIRONMENT=production
APP_ENV=prod
STAGE=prod

# Lambda aliases indicating production
alias: prod
alias: production
alias: live
alias: stable

# Safe aliases
alias: dev
alias: staging
alias: $LATEST  (always dev/test context)
```

### CloudFormation / CDK Stack Names
```
# Production indicators
ProdStack
ProductionStack
*-prod-*
*-production-*

# Safe
DevStack
StagingStack
TestStack
```

---

## Vercel / Netlify Production Detection 🆕

### Vercel
```
# Production deployments
Domain: app.company.com (custom domain, no branch prefix)
VERCEL_ENV=production
Branch: main, master

# Preview deployments (treat as staging)
Domain: *.vercel.app
VERCEL_ENV=preview
Branch: feature/*, develop, staging

# Development (safe)
VERCEL_ENV=development
localhost:3000
```

### Netlify
```
# Production deployments
Domain: app.company.com (custom production domain)
CONTEXT=production
Branch: main, master, production

# Deploy previews (staging)
Domain: deploy-preview-*.netlify.app
CONTEXT=deploy-preview

# Branch deploys (staging)
Domain: <branch-name>--<site>.netlify.app
CONTEXT=branch-deploy

# Development (safe)
CONTEXT=dev
netlify dev (local)
```

---

## Container Registry Patterns 🆕

### Production Image Indicators
```
# ECR production repositories
<account>.dkr.ecr.<region>.amazonaws.com/prod/*
<account>.dkr.ecr.<region>.amazonaws.com/*-prod*

# GCR / Artifact Registry production
gcr.io/<project>/prod-*
<region>-docker.pkg.dev/<project>/prod/*

# Docker Hub (treat ALL as potentially untrusted unless official/verified)
docker.io/library/*   (official images — trusted)
docker.io/<org>/*     (verify publisher before pulling)

# Tags
:latest              → AMBIGUOUS — confirm which environment
:prod, :production   → PRODUCTION
:stable, :release    → PRODUCTION
:v1.2.3              → Acceptable (pinned version)
:sha-<hash>          → Preferred (immutable)
:dev, :staging       → SAFE
```

---

## Decision Tree

```
Is the environment name in the PRODUCTION list?
  └─ YES → Apply full production guards
  └─ NO → Is it in the SAFE list?
             └─ YES → Apply standard caution
             └─ NO → Is it AMBIGUOUS or UNKNOWN?
                        └─ YES → TREAT AS PRODUCTION, ask user to confirm
                        └─ NO → Apply standard caution
```

### Extended Decision Tree (Cloud-Native) 🆕

```
Is this a GitHub Actions workflow?
  └─ Check branch triggers and environment: declarations
  └─ Treat main/master/release branches as PRODUCTION

Is this an ECS task / Lambda function?
  └─ Check family name, function name, and ENVIRONMENT env var
  └─ If name contains "prod" → PRODUCTION

Is this a Vercel / Netlify deployment?
  └─ Check VERCEL_ENV / CONTEXT variable
  └─ Check domain (custom domain = likely production)
  └─ Check branch (main/master = production)

Is this a container image?
  └─ Check registry path for "prod" prefix
  └─ :latest tag → ambiguous, ask user
  └─ :prod / :stable tag → PRODUCTION
```
