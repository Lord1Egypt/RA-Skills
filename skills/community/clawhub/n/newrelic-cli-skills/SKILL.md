---
name: newrelic-cli-skills
version: 1.0.3
description: >
  Monitor, query, and manage New Relic observability data via the newrelic CLI.
  Covers NRQL queries, APM performance triage, deployment markers, alert policy and
  condition management, notification channel setup, infrastructure monitoring, and
  agent diagnostics. Use when user asks about application performance, error rates,
  slow transactions, deployment tracking, alert configuration, or New Relic setup.
metadata:
  openclaw:
    purpose: >
      New Relic observability skill for both read and targeted write workflows.
      Reads APM metrics, NRQL query results, alert policies/conditions, incidents,
      and infrastructure host data from the New Relic API. Write operations in this
      repo include deployment marker creation plus alert policy, condition, and
      notification channel creation; the alerts sub-skill also documents alert
      condition deletion. Helper scripts execute newrelic CLI commands only and
      should validate untrusted inputs before embedding them in NRQL.
    requires:
      env:
        - NEW_RELIC_API_KEY
        - NEW_RELIC_ACCOUNT_ID
      binaries:
        - newrelic
      notes: |
        NEW_RELIC_API_KEY must be a User Key (starts with NRAK-).
        NEW_RELIC_ACCOUNT_ID is the numeric account ID from the NR UI.
        See README.md for CLI installation instructions.
        Use an API key scoped to the minimum required accounts.
tags:
  - newrelic
  - observability
  - apm
  - monitoring
  - performance
  - nrql
---

# New Relic CLI Skills

## Quick Decision Tree

**Performance issue reported?** → [`apm/SKILL.md`](apm/SKILL.md)
**Need to query data with NRQL?** → [`nrql/SKILL.md`](nrql/SKILL.md)
**Recording a deployment?** → [`deployments/SKILL.md`](deployments/SKILL.md)
**Alert management?** → [`alerts/SKILL.md`](alerts/SKILL.md)
**Infrastructure/host issues?** → [`infrastructure/SKILL.md`](infrastructure/SKILL.md)
**Agent not reporting?** → [`diagnostics/SKILL.md`](diagnostics/SKILL.md)

---

## Setup & Auth

```bash
# Install (manual or package manager)
# macOS (Homebrew)
brew install newrelic-cli

# Or manually download a release archive from:
# https://github.com/newrelic/newrelic-cli/releases
# Extract it, place the `newrelic` binary on your PATH, then verify with:
newrelic --version

# Configure profile
newrelic profile add \
  --profile default \
  --apiKey $NEW_RELIC_API_KEY \
  --accountId $NEW_RELIC_ACCOUNT_ID \
  --region US   # or EU

newrelic profile default --profile default

# Verify
newrelic profile list
```

---

## Common One-Liners

```bash
# Search for an entity by name
newrelic entity search --name "my-app"

# Run a NRQL query
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "SELECT average(duration) FROM Transaction WHERE appName='my-app' SINCE 1 hour ago"

# Record a deployment
newrelic apm deployment create \
  --applicationId <APP_ID> \
  --revision "v1.2.3" \
  --description "Feature: user auth"

# Run diagnostics
newrelic diagnose run
```

---

## Entity Reference

Find entity GUIDs (needed for API calls and deployment markers):

```bash
# List all APM apps
newrelic entity search --name "" --type APPLICATION --domain APM

# Get specific entity details
newrelic entity get --guid <GUID>

# List all hosts
newrelic entity search --name "" --type HOST
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `NEW_RELIC_API_KEY` | User key (NRAK-...) |
| `NEW_RELIC_ACCOUNT_ID` | Numeric account ID |
| `NEW_RELIC_REGION` | `US` or `EU` |

---

## Sub-Skills

| Sub-skill | When to use |
|---|---|
| [`apm/`](apm/SKILL.md) | Performance triage, slow transactions, error analysis |
| [`nrql/`](nrql/SKILL.md) | Custom queries, dashboards, ad-hoc data exploration |
| [`deployments/`](deployments/SKILL.md) | Mark releases, correlate deploys with performance |
| [`alerts/`](alerts/SKILL.md) | Alert policies, conditions, notification channels |
| [`infrastructure/`](infrastructure/SKILL.md) | Host metrics, CPU/memory, process monitoring |
| [`diagnostics/`](diagnostics/SKILL.md) | Agent health, config validation, connectivity |

## Scripts

| Script | Purpose |
|---|---|
| [`scripts/check-performance.sh`](scripts/check-performance.sh) | Quick health check across all apps |
| [`scripts/deployment-marker.sh`](scripts/deployment-marker.sh) | Record a deployment event |
| [`scripts/top-slow-transactions.sh`](scripts/top-slow-transactions.sh) | Find the 10 slowest transactions |
| [`scripts/error-report.sh`](scripts/error-report.sh) | Recent errors with stack traces |

## References

- [`references/nrql-patterns.md`](references/nrql-patterns.md) — Common NRQL query patterns
- [`references/performance-triage.md`](references/performance-triage.md) — Step-by-step triage guide
