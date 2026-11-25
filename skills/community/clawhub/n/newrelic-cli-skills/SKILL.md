---
name: newrelic-cli-skills
version: 1.0.13
description: >
  Monitor, query, and manage New Relic observability data via the newrelic CLI.
  Covers NRQL queries and organization-scoped macros, AI Monitoring telemetry and datasets, APM performance triage, deployment
  markers, read-only alert and incident inspection,
  infrastructure monitoring, agent diagnostics, and identity/access administration.
  Use when user asks about LLM token usage, AI application telemetry or datasets, application
  performance, error rates, slow transactions, deployment tracking, incident inspection,
  New Relic setup, users, groups, roles, permissions, or access grants.
metadata:
  openclaw:
    purpose: >
      New Relic observability skill for both read and targeted write workflows.
      Reads APM metrics, NRQL query results, AI Monitoring events (including potentially
      sensitive prompt/response content and tool inputs), incidents, entity alert severity,
      and infrastructure host data from the New Relic API. The documented New Relic CLI
      has no alerts command tree, so alert and incident workflows in this repo are read-only.
      Write operations include deployment marker creation and organization-scoped NRQL
      macro creation/update/deletion, plus irreversible AI Monitoring dataset/version deletion.
      Dataset deletion cascades to all versions; last-version deletion also deletes its dataset.
      Require explicit approval of exact dataset/version IDs and cascade scope, fresh
      read-back before deletion, and exact-result verification afterward; do not bypass
      confirmation for automation. See aimonitoring/references/datasets.md. Require explicit approval before macro writes,
      inspect downstream query/dashboard impact with coverage gaps disclosed, and read
      the exact target back. Macros are not supported in alert conditions; cached query
      execution may lag behind stored-state read-back.
      Diagnostics validate writes hostname-bearing NrIntegrationError tracer telemetry;
      require explicit approval for the verified effective target and hostname disclosure,
      and do not blindly retry interrupted writes. Diagnostics run can download and
      execute nrdiag, including when listing suites; require explicit download/execution
      approval and separate authorization for any diagnostic-data upload. The advertised
      attachment-key flag is not forwarded by this CLI runner; do not assume upload.
      IAM workflows add user/group
      CRUD, membership changes, and access-grant creation/revocation; require explicit
      confirmation before IAM writes and verify each
      write by reading the target back. Helper scripts execute newrelic CLI commands only
      and should validate untrusted inputs before embedding them in NRQL.
    requires:
      env:
        - NEW_RELIC_API_KEY
        - NEW_RELIC_ACCOUNT_ID
      binaries:
        - newrelic
      notes: |
        NEW_RELIC_API_KEY must be a User Key (starts with NRAK-).
        NEW_RELIC_ACCOUNT_ID is the numeric account ID from the NR UI.
        AI Monitoring dataset and dataset-version commands require CLI >=v0.117.0;
        check newrelic --version before using them. This floor applies only to those commands.
        See references/installation.md for CLI installation instructions.
        Use an API key scoped to the minimum required accounts.
        Macro writes require Organization product admin or Organization manager access;
        Organization read only grants macro reads. Confirm the effective organization
        and its primary region before macro operations; environment credentials can
        override the selected profile. See nrql/SKILL.md for preflight and write gates.
        IAM writes also require organization-level authorization for the user associated
        with the key: Authentication domain manager or Organization manager for
        usermanagement, and Organization manager for accessmanagement grant writes.
        Administrative user-management access requires a core or full platform user.
tags:
  - newrelic
  - observability
  - apm
  - monitoring
  - performance
  - nrql
  - ai-monitoring
  - iam
---

# New Relic CLI Skills

## Quick Decision Tree

**Performance issue reported?** → [`apm/SKILL.md`](apm/SKILL.md)
**Need to query data or manage organization-scoped NRQL macros?** → [`nrql/SKILL.md`](nrql/SKILL.md)
**AI/LLM telemetry, datasets, or dataset versions?** → [`aimonitoring/SKILL.md`](aimonitoring/SKILL.md)
**Recording a deployment?** → [`deployments/SKILL.md`](deployments/SKILL.md)
**Inspecting alerts or incidents?** → [`alerts/SKILL.md`](alerts/SKILL.md)
**Infrastructure/host issues?** → [`infrastructure/SKILL.md`](infrastructure/SKILL.md)
**Agent not reporting?** → [`diagnostics/SKILL.md`](diagnostics/SKILL.md)
**Users, groups, roles, permissions, or access grants?** → [`iam/SKILL.md`](iam/SKILL.md)

---

## Setup & Auth

For installation, use Homebrew on macOS or an official release archive. The Scoop
route remains blocked by manifest/archive checksum mismatches, including the checked
default-branch manifest; do not skip or disable checksum checks. Follow the
[installation reference](references/installation.md) for immutable evidence and the
manual path: verify the exact archive against its release's official SHA-256 manifest
(case-insensitive hex comparison) before extraction. This checks integrity, not
release authenticity. Confirm the selected version with `newrelic --version` before
configuring credentials.

```bash
# macOS (Homebrew)
brew install newrelic-cli
newrelic --version

# Configure profile
newrelic profile add \
  --profile "default" \
  --apiKey $NEW_RELIC_API_KEY \
  --accountId $NEW_RELIC_ACCOUNT_ID \
  --region US   # US, EU, JP, GOV, or FEDRAMP (alias for GOV)

newrelic profile default --profile "default"

# Verify
newrelic profile list --format JSON
```

For structured profile discovery, pass `--format JSON` explicitly. The `isDefault`
field identifies the persisted default profile, and profile names are emitted without
terminal decoration. It does not necessarily identify the effective credentials: the
global `--profile` flag can select another profile, while `NEW_RELIC_API_KEY`,
`NEW_RELIC_ACCOUNT_ID`, `NEW_RELIC_REGION`, and `NEW_RELIC_LICENSE_KEY` override the
corresponding stored profile fields.

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

# Discover diagnostic CLI flags without launching nrdiag.
# Before any diagnose run (even --list-suites), follow diagnostics/SKILL.md:
# explicit download/execution approval; separate authorization for data upload.
newrelic diagnose run --help

# Find applications reporting AI Monitoring telemetry
newrelic aimonitoring application search
```

---

## Entity Reference

Find entity GUIDs (needed for API calls and deployment markers):

```bash
# List all APM apps
newrelic entity search --name "" --type APPLICATION --domain APM

# Get APM application details
newrelic apm application get --guid <GUID>

# List all hosts
newrelic entity search --name "" --type HOST
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `NEW_RELIC_API_KEY` | User key (NRAK-...) |
| `NEW_RELIC_ACCOUNT_ID` | Numeric account ID |
| `NEW_RELIC_REGION` | `US`, `EU`, `JP`, `GOV`, or `FEDRAMP` (`FEDRAMP` is an alias for `GOV`) |

---

## Sub-Skills

| Sub-skill | When to use |
|---|---|
| [`apm/`](apm/SKILL.md) | Performance triage, slow transactions, error analysis |
| [`nrql/`](nrql/SKILL.md) | Custom queries, dashboards, ad-hoc exploration, and approval-gated organization macros |
| [`aimonitoring/`](aimonitoring/SKILL.md) | AI/LLM telemetry, dataset discovery/version inventory, and approval-gated deletion |
| [`deployments/`](deployments/SKILL.md) | Mark releases, correlate deploys with performance |
| [`alerts/`](alerts/SKILL.md) | Read-only incident telemetry and entity alert severity |
| [`infrastructure/`](infrastructure/SKILL.md) | Host metrics, CPU/memory, process monitoring |
| [`diagnostics/`](diagnostics/SKILL.md) | CLI profile/connectivity validation, agent reporting, and approval-gated nrdiag suites |
| [`iam/`](iam/SKILL.md) | Users, groups, memberships, roles, permissions, and access grants |

## Scripts

| Script | Purpose |
|---|---|
| [`scripts/check-performance.sh`](scripts/check-performance.sh) | Quick health check across all apps |
| [`scripts/deployment-marker.sh`](scripts/deployment-marker.sh) | Record a deployment event |
| [`scripts/top-slow-transactions.sh`](scripts/top-slow-transactions.sh) | Find the 10 slowest transactions |
| [`scripts/error-report.sh`](scripts/error-report.sh) | Recent errors with stack traces |

## References

- [`references/installation.md`](references/installation.md) — CLI installation, checksum checks, and Scoop mismatch evidence
- [`references/nrql-patterns.md`](references/nrql-patterns.md) — Common NRQL query patterns
- [`references/performance-triage.md`](references/performance-triage.md) — Step-by-step triage guide
