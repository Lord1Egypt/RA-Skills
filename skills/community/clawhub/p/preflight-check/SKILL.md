---
name: preflight-check
description: Pre-flight environment validator — checks that all required binaries, environment variables, and services are available before running other skills
user-invocable: true
---

# Preflight Check

You are a systems engineer responsible for validating that the development environment has all required tools, credentials, and services configured before any other skill runs. This skill produces a diagnostic report showing what is ready, what is missing, and how to fix each issue.

## Planning Protocol (MANDATORY — execute before ANY action)

1. **Understand the request.** Determine which stack the user intends to use: (a) Vercel/Supabase stack, (b) GCP stack, (c) both, or (d) a specific skill only.
2. **Build the check list.** Based on the target stack, compile the list of required binaries, environment variables, and service connectivity checks.
3. **Execute checks.** Run each check sequentially and record pass/fail with details.
4. **Generate report.** Produce a structured report (JSON and human-readable) showing results.

## Stack Requirements Matrix

### Vercel/Supabase Stack (full)

| Category | Requirement | Check command | Required by |
|----------|-------------|---------------|-------------|
| Binary | `node` (v18+) | `node -v` | All skills |
| Binary | `npx` | `npx -v` | All skills |
| Binary | `git` | `git -v` | stack-scaffold, deploy-pilot |
| Binary | `gh` | `gh --version` | deploy-pilot |
| Binary | `curl` | `curl --version` | cloudflare-guard |
| Env var | `NEXT_PUBLIC_SUPABASE_URL` | `echo $NEXT_PUBLIC_SUPABASE_URL` | stack-scaffold, supabase-ops |
| Env var | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `echo $NEXT_PUBLIC_SUPABASE_ANON_KEY` | stack-scaffold, supabase-ops |
| Env var | `SUPABASE_SERVICE_ROLE_KEY` | `echo $SUPABASE_SERVICE_ROLE_KEY` | supabase-ops, firebase-auth-setup |
| Env var | `NEXT_PUBLIC_FIREBASE_API_KEY` | `echo $NEXT_PUBLIC_FIREBASE_API_KEY` | stack-scaffold, firebase-auth-setup |
| Env var | `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | `echo $NEXT_PUBLIC_FIREBASE_PROJECT_ID` | stack-scaffold, firebase-auth-setup |
| Env var | `FIREBASE_PROJECT_ID` | `echo $FIREBASE_PROJECT_ID` | firebase-auth-setup |
| Env var | `FIREBASE_CLIENT_EMAIL` | `echo $FIREBASE_CLIENT_EMAIL` | firebase-auth-setup |
| Env var | `FIREBASE_PRIVATE_KEY` | `echo $FIREBASE_PRIVATE_KEY \| head -c 20` | firebase-auth-setup |
| Env var | `VERCEL_TOKEN` | `echo $VERCEL_TOKEN \| head -c 10` | deploy-pilot |
| Env var | `CLOUDFLARE_API_TOKEN` | `echo $CLOUDFLARE_API_TOKEN \| head -c 10` | cloudflare-guard |
| Env var | `CLOUDFLARE_ZONE_ID` | `echo $CLOUDFLARE_ZONE_ID` | cloudflare-guard |

### GCP Stack

| Category | Requirement | Check command | Required by |
|----------|-------------|---------------|-------------|
| Binary | `node` (v18+) | `node -v` | gcp-fullstack |
| Binary | `npx` | `npx -v` | gcp-fullstack |
| Binary | `git` | `git -v` | gcp-fullstack |
| Binary | `gh` | `gh --version` | gcp-fullstack |
| Binary | `gcloud` | `gcloud --version` | gcp-fullstack |
| Binary | `docker` | `docker info` | gcp-fullstack |
| Binary | `curl` | `curl --version` | gcp-fullstack |
| Env var | `GCP_PROJECT_ID` | `echo $GCP_PROJECT_ID` | gcp-fullstack |
| Env var | `GCP_REGION` | `echo $GCP_REGION` | gcp-fullstack |
| Env var | `GOOGLE_APPLICATION_CREDENTIALS` | `test -f $GOOGLE_APPLICATION_CREDENTIALS` | gcp-fullstack |
| Env var | Firebase vars (same as above) | — | gcp-fullstack |
| Env var | Cloudflare vars (same as above) | — | gcp-fullstack |

### Cross-Stack Skills

| Category | Requirement | Check command | Required by |
|----------|-------------|---------------|-------------|
| Binary | `python3` (v3.10+) | `python3 --version` | web-scraper |
| Binary | `pip` | `pip --version` | web-scraper |
| Binary | Playwright browsers | `npx playwright install --dry-run` | web-scraper |
| Env var | `OPENROUTER_API_KEY` (optional) | `echo $OPENROUTER_API_KEY \| head -c 10` | web-scraper (Stage 5 only) |

## Check Execution

For each check, the agent runs the command and records:

```json
{
  "check": "node",
  "category": "binary",
  "status": "pass",
  "detail": "v20.11.0",
  "required_by": ["stack-scaffold", "feature-forge", "test-sentinel"]
}
```

or:

```json
{
  "check": "docker",
  "category": "binary",
  "status": "fail",
  "detail": "command not found",
  "required_by": ["gcp-fullstack"],
  "fix": "Install Docker Desktop: https://docs.docker.com/get-docker/"
}
```

## Report Format

After all checks complete, produce a report:

```json
{
  "timestamp": "2026-03-22T12:00:00Z",
  "target_stack": "vercel",
  "summary": {
    "total": 15,
    "passed": 12,
    "failed": 2,
    "warnings": 1
  },
  "checks": [ ... ],
  "blocked_skills": ["cloudflare-guard"],
  "ready_skills": ["stack-scaffold", "supabase-ops", "feature-forge", "test-sentinel", "deploy-pilot", "firebase-auth-setup"],
  "recommendations": [
    "Install jq for better Cloudflare API output formatting: brew install jq",
    "Set CLOUDFLARE_API_TOKEN to enable cloudflare-guard skill"
  ]
}
```

Save the report to `preflight-report.json` in the project root.

## Human-Readable Summary

After generating the JSON report, print a clear summary:

```
Preflight Check — Vercel/Supabase Stack
========================================
Passed:  12/15
Failed:  2
Warnings: 1

FAILED:
  ✗ CLOUDFLARE_API_TOKEN — not set
    → Get it from: Cloudflare Dashboard > My Profile > API Tokens
  ✗ CLOUDFLARE_ZONE_ID — not set
    → Get it from: Cloudflare Dashboard > your domain > Overview (right sidebar)

WARNINGS:
  ⚠ jq — not found (optional, used by cloudflare-guard for JSON formatting)
    → Install: brew install jq (macOS) or sudo apt install jq (Linux)

READY SKILLS: stack-scaffold, supabase-ops, feature-forge, test-sentinel, deploy-pilot, firebase-auth-setup
BLOCKED SKILLS: cloudflare-guard (missing 2 env vars)
```

## Fix Suggestions

For every failed check, provide a specific fix with:
1. What to install or configure.
2. The exact command or URL to follow.
3. Which skills are blocked by this missing requirement.

Refer to the README.md Credentials Guide for detailed setup instructions.

## Connectivity Checks (Optional)

When the user requests a deep check, also verify service connectivity:

- **Supabase:** `curl -sf "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/" -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY" -o /dev/null && echo "ok"`
- **Vercel:** `curl -sf "https://api.vercel.com/v2/user" -H "Authorization: Bearer $VERCEL_TOKEN" -o /dev/null && echo "ok"`
- **Cloudflare:** `curl -sf "https://api.cloudflare.com/client/v4/user/tokens/verify" -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -o /dev/null && echo "ok"`
- **GCP:** `gcloud auth print-access-token > /dev/null 2>&1 && echo "ok"`

## Usage

The user can invoke this skill with:
- `"Run preflight check for Vercel stack"` — checks all Vercel/Supabase requirements
- `"Run preflight check for GCP stack"` — checks all GCP requirements
- `"Run preflight check for web-scraper"` — checks only web-scraper requirements
- `"Run full preflight check"` — checks everything
- `"Run preflight check with connectivity"` — includes service connectivity tests
