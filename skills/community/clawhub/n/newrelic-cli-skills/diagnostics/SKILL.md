# CLI and Agent Diagnostics

Check CLI configuration/connectivity and agent reporting; run the separate nrdiag
troubleshooting suite only with explicit approval. `diagnose validate` does not
validate agent configuration files.

---

## Run Approved, Targeted Diagnostics

`diagnose run` downloads the platform-specific **nrdiag executable** into
`~/.newrelic/bin` when absent, then executes it. This is not a read-only CLI/API
preflight. Obtain explicit approval for download/execution and the intended
diagnostic scope before any invocation, including `--list-suites`: listing also
uses the executable and can trigger its download. Use `diagnose run --help` for
CLI flag discovery without launching nrdiag.

```bash
# Only after explicit download/execution approval
newrelic diagnose run --list-suites
# After reviewing the list and approving these specific suites
newrelic diagnose run --suites java,infra
```

Checks depend on the selected nrdiag suites, not on a fixed set of CLI checks.
Treat collected configuration, logs, and results as potentially sensitive. Never
pass `--attachment-key` or upload results to a support ticket without separate
authorization for the destination and reviewed data. The flag is advertised for
upload, but this CLI's runner does not forward it to nrdiag; do not assume it
uploads anything or work around that limitation with an unapproved upload.

---

## Validate CLI Configuration and Connectivity

This is a **live telemetry write**, not a local agent-configuration-file check.
Obtain explicit approval before running it. Confirm the intended account, region,
profile, and effective environment overrides without printing credentials; the
tracer includes the machine hostname. The command validates the configured LICENSE
ingest key, sends a tracer event, then queries New Relic to confirm receipt.

```bash
# Stored-profile mode: verify this profile's account/region and required keys first.
# Only after explicit approval for that target and hostname disclosure.
# Remove overrides for this invocation only; do not alter the parent environment.
env -u NEW_RELIC_API_KEY -u NEW_RELIC_ACCOUNT_ID \
  -u NEW_RELIC_REGION -u NEW_RELIC_LICENSE_KEY \
  newrelic diagnose validate --profile "staging.us"
```

Use this example only with a complete, verified stored profile; stop if it lacks
the intended API key, LICENSE ingest key, or account. A profile name alone does
not establish its target. For environment-driven credentials instead, verify and
approve the effective account/region and key pairing; `--profile` alone does not
override them. Do not dump credentials during preflight. Allow a long-running
tracked execution (for example, a 15-minute tool timeout, not a CLI flag); see the
reference for retry timing. If interrupted, treat the write as uncertain and do
not blindly re-run it; inspect the approved target read-only and obtain renewed
approval before another invocation.

There is no `diagnose validate --config` flag. Do not pass an agent YAML/XML file
to this command or use it as an offline lint. A successful run confirms tracer
ingestion, not that every application agent is healthy. Read
[configuration-validation safeguards and compatibility](references/config-validation.md)
before using this workflow, especially for accounts with many ingest keys. If it
fails, report the failure; do not rotate keys, run installers, or bypass validation
without separate authorization.

---

## Check Agent is Reporting

```bash
# Verify an app is actively sending data
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT count(*)
  FROM Transaction
  WHERE appName = 'my-app'
  SINCE 10 minutes ago
"
# count = 0 means agent is not reporting

# Check entity reporting status
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, reporting}'
```

---

## Check Agent Version

```bash
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, tags: (.tags[] | select(.key == "agentVersion"))}'
```

---

## Connectivity Test

```bash
# Inventory stored profiles (not a connectivity test)
newrelic profile list --format JSON
# Query access and integration-error triage, excluding intentional CLI tracers
newrelic nrql query --accountId "$NEW_RELIC_ACCOUNT_ID" \
  --query "SELECT count(*) FROM NrIntegrationError WHERE purpose IS NULL OR purpose != 'New Relic CLI configuration validation' SINCE 1 hour ago"
# Inspect details before assigning a cause; no FACET that could hide missing fields
newrelic nrql query --accountId "$NEW_RELIC_ACCOUNT_ID" \
  --query "SELECT category, message, newRelicFeature, purpose FROM NrIntegrationError WHERE purpose IS NULL OR purpose != 'New Relic CLI configuration validation' SINCE 1 hour ago LIMIT 20"
```

Inspect event details and purpose before diagnosing an ingestion issue. CLI
configuration validation intentionally emits an `NrIntegrationError` tracer with
purpose `New Relic CLI configuration validation`; a nonzero count alone is not
proof of an application ingestion failure.

---

## Common Issues

| Symptom | Likely Cause | Fix |
|---|---|---|
| App shows `reporting: false` | Agent stopped or config missing | Restart app pool / check agent logs |
| Transaction count = 0 | IIS app pool recycled without agent init | Ensure agent auto-instruments on startup |
| High `NrIntegrationError` after excluding CLI validation tracers | Cause depends on event details; not necessarily malformed data | Exclude purpose `New Relic CLI configuration validation`, retain events with no purpose, and inspect `category`/`message` before selecting a fix |
| `alertSeverity: NOT_CONFIGURED` | No alert conditions on the entity | Add NRQL or APM metric conditions |

---

## .NET Agent Specific (Windows/IIS)

```bash
# Check which apps are instrumented on a host
newrelic entity search --name "my-host" --type HOST | \
  jq '.[] | .tags[] | select(.key == "apmApplicationNames")'

# Agent logs location (Windows)
# C:\ProgramData\New Relic\.NET Agent\Logs\
```

---

## Profile Management

```bash
# Machine-readable profile inventory; do not parse decorated table text
newrelic profile list --format JSON

# Print the persisted default profile name (the JSON key is capitalized `Name`)
newrelic profile list --format JSON | jq -r '.[] | select(.isDefault) | .Name'

# Switch profile; shell-quote the exact profile name
newrelic profile default --profile "production.us"

# Add a new profile
newrelic profile add \
  --profile "staging.us" \
  --apiKey $NEW_RELIC_API_KEY \
  --accountId $NEW_RELIC_ACCOUNT_ID \
  --region US  # US, EU, JP, GOV, or FEDRAMP (alias for GOV)

# Confirm an exact profile name before deleting it
PROFILE_NAME='production.us'
if newrelic profile list --format JSON | \
  jq -e --arg p "$PROFILE_NAME" 'any(.[]; .Name == $p)' >/dev/null; then
  newrelic profile delete --profile "$PROFILE_NAME"
else
  printf 'Profile %s not found; refusing to delete.\n' "$PROFILE_NAME" >&2
fi
```

Profile names may contain dots and other punctuation. Preserve the exact identifier
and always shell-quote it for `add`, `default`, and `delete`. If the exact-name lookup
fails, stop without deleting a profile.
