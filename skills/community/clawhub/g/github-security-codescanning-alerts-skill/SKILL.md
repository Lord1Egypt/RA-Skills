---
name: github-manage-security-alerts
description: Use when the user asks to inspect, triage, summarize, export, or safely update GitHub security alerts for code scanning, Dependabot, malware, or secret scanning.
license: "Unlicense"
metadata: { "short-description": "Inspect and triage GitHub security alerts" }
---

# GitHub Security Alerts Management

## Overview

Use this skill when a user asks to inspect or manage GitHub repository security alerts, including:

- code scanning alerts
- Dependabot alerts
- Dependabot malware alerts
- secret scanning alerts
- secret scanning alert locations
- secret scanning scan history
- repository security settings overview
- raw GitHub security API inspection across repositories
- bulk alert export for offline triage or reporting workflows
- bulk alert mutation for high-volume cleanup workflows

The bundled helper is repository-agnostic:

- point `--repo` at any local checkout
- let it auto-detect `owner/repo` and the GitHub host from the git remote
- or pass `--repository owner/repo` explicitly
- authenticate via environment variable instead of putting a token on the command line
- optionally override the API or web base URL for custom environments

## Compatibility

Requires Python 3.
Uses the GitHub REST API directly with a token supplied through an environment variable such as `GITHUB_TOKEN` or `GH_TOKEN`.
Supports GitHub.com and standard GHES API base URL derivation from git remotes, with a raw API fallback for anything not wrapped yet.

## Invocation hints

Use `repo` when the target is a local checkout, defaulting to `.`.
Use optional `repository`, `api_base_url`, `web_base_url`, and `token_env` values when auto-detection is not enough.
Common commands include `summary`, `export-alerts`, `bulk-update-alerts`, `repo-security-overview`, `list-code-scanning`, `show-code-scanning`, `update-code-scanning`, `list-dependabot`, `show-dependabot`, `update-dependabot`, `list-malware`, `show-malware`, `update-malware`, `list-secret-scanning`, `show-secret-scanning`, `update-secret-scanning`, `list-secret-locations`, `secret-scan-history`, and `api-call`.

## Security model

Do not paste GitHub tokens into command arguments.
Do not use `--show-secret-values` unless the user explicitly asks for unredacted secret values and confirms the exposure risk. Prefer redacted alert metadata, secret locations, validity, and resolution state. If unredacted output is required for remediation, do not paste secret material into chat, issue comments, PRs, commits, logs, or saved reports.

Preferred pattern:

```powershell
$env:GITHUB_TOKEN = Get-Secret GITHUB_TOKEN -AsPlainText
```

If a repository uses a different environment variable name, either export that variable first or pass the variable name with `--token-env`.

Examples:

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" summary --repo "."
python "<path-to-skill>/scripts/manage_github_security_alerts.py" summary --repo "." --token-env GITHUB_TOKEN
```

## Inputs

- `repo`: path inside the target repository checkout (default `.`)
- `repository`: optional explicit `owner/repo` override
- `api_base_url`: optional explicit API base URL override
- `web_base_url`: optional explicit web base URL override for rendered links
- `token_env`: optional environment variable name containing the token; repeatable for fallbacks
- `json`: optional machine-readable output flag

## Important note about malware alerts

GitHub surfaces malware findings as **Dependabot malware alerts**.

GitHub does not provide a separate repository alert family with its own dedicated REST surface. The bundled helper therefore treats malware as a filtered subset of Dependabot alerts and cross-references each alert's advisory GHSA against the GitHub Advisory Database to identify advisories whose type is `malware`.

That means:

- `list-malware`, `show-malware`, and `update-malware` are backed by Dependabot alert APIs
- malware classification is strongest on GitHub.com, where the advisory database endpoint is available
- if advisory type lookup is unavailable on the target host, the helper reports that state instead of silently guessing

## Quick start

### 1. Inspect the current security state

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" summary --repo "."
```

### 2. View repository security settings overview

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" repo-security-overview --repo "."
```

### 2.5 Export the full alert sets for bulk triage

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" export-alerts --repo "." --json
```

### 3. List code scanning alerts

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-code-scanning --repo "." --state open --severity high,error
```

### 3.5 Bulk-dismiss or bulk-reopen alerts

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" bulk-update-alerts --repo "." --surface code-scanning --select-state open --target-state dismissed --dismissed-reason "false positive" --comment "Reviewed and intentionally dismissed." --limit 10 --dry-run --json

python "<path-to-skill>/scripts/manage_github_security_alerts.py" bulk-update-alerts --repo "." --surface dependabot --select-state open --target-state dismissed --dismissed-reason tolerable_risk --comment "Accepted until the next dependency refresh." --limit 25 --dry-run --json

python "<path-to-skill>/scripts/manage_github_security_alerts.py" bulk-update-alerts --repo "." --surface secret-scanning --select-state open --target-state resolved --resolution used_in_tests --limit 25 --dry-run --json
```

### 4. Dismiss or reopen a code scanning alert

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-code-scanning --repo "." --alert 42 --state dismissed --dismissed-reason false_positive --comment "False positive after manual review." --dry-run
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-code-scanning --repo "." --alert 42 --state open
```

### 5. List Dependabot alerts

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-dependabot --repo "." --state open --ecosystem npm --has patch
```

### 6. Dismiss or reopen a Dependabot alert

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-dependabot --repo "." --alert 7 --state dismissed --dismissed-reason tolerable_risk --comment "Accepted until next quarterly upgrade." --dry-run
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-dependabot --repo "." --alert 7 --state open
```

### 7. List malware alerts

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-malware --repo "." --state open
```

### 8. List secret scanning alerts safely

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-secret-scanning --repo "." --state open
```

Secret values are hidden by default. Keep that default unless the user explicitly confirms that unredacted secret output is necessary.

### 9. Resolve or reopen a secret scanning alert

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-secret-scanning --repo "." --alert 11 --state resolved --resolution revoked --comment "Token revoked and rotated." --dry-run
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-secret-scanning --repo "." --alert 11 --state open
```

### 10. Show secret locations and scan history

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-secret-locations --repo "." --alert 11
python "<path-to-skill>/scripts/manage_github_security_alerts.py" secret-scan-history --repo "."
```

### 11. Use the raw API fallback for anything not wrapped yet

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" api-call --repo "." --endpoint /repos/OWNER/REPO/code-scanning/default-setup
```

## Workflow

1. Resolve authentication securely.
   - Prefer an environment variable like `GITHUB_TOKEN`.
   - If needed, load it from a secret manager into an environment variable first.
   - Never print the token in logs or chat output.
2. Resolve the target repository.
   - Prefer `--repo` and auto-detection from git remote.
   - Fall back to `--repository owner/repo` when the local checkout is unavailable or nonstandard.
3. Inspect current findings.
   - Run `summary` first.
   - Use `export-alerts` when you need a fuller multi-surface JSON snapshot for bulk triage or external reporting.
   - Use the list/show commands for the alert family you care about.
   - Use `repo-security-overview` when the question is about enablement or available security settings.
4. Classify findings.
   - Fix real defects in code or dependency configuration when appropriate.
   - Dismiss only when you have a clear justification.
   - Reopen alerts when the earlier dismissal or resolution is no longer valid.
   - Use `bulk-update-alerts` when a repository has dozens or hundreds of already-reviewed, mis-triaged alerts that need the same action.
5. Apply mutations carefully.
   - Prefer `--dry-run` first for risky changes.
   - Add a short, actionable dismissal or resolution comment.
   - Remember that write operations need the corresponding GitHub permissions.
6. Verify the post-change state.
   - Re-run the relevant list/show command.
   - For code or dependency fixes, wait for the next GitHub analysis cycle if you expect the alert to disappear naturally.

## Bundled resources

### scripts/manage_github_security_alerts.py

Repository-agnostic helper for GitHub repository security alerts.

Supported commands:

- `summary`
- `export-alerts`
- `bulk-update-alerts`
- `repo-security-overview`
- `list-code-scanning`
- `show-code-scanning`
- `update-code-scanning`
- `list-dependabot`
- `show-dependabot`
- `update-dependabot`
- `list-malware`
- `show-malware`
- `update-malware`
- `list-secret-scanning`
- `show-secret-scanning`
- `update-secret-scanning`
- `list-secret-locations`
- `secret-scan-history`
- `api-call`

Implementation modules:

- `github_security_api.py`
- `github_security_cli.py`
- `github_security_common.py`
- `github_security_operations.py`
- `github_security_render.py`

Examples:

```powershell
python "<path-to-skill>/scripts/manage_github_security_alerts.py" summary --repo "." --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" export-alerts --repo "." --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" bulk-update-alerts --repo "." --surface code-scanning --select-state open --target-state dismissed --dismissed-reason "false positive" --comment "Reviewed and intentionally dismissed." --limit 10 --dry-run --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-code-scanning --repo "." --state open --per-page 100 --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-code-scanning --repo "." --alert 42 --state dismissed --dismissed-reason false_positive --comment "False positive after review." --dry-run
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-dependabot --repo "." --state open --ecosystem npm --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-malware --repo "." --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-dependabot --repo "." --alert 7 --state dismissed --dismissed-reason tolerable_risk --comment "Accepted temporarily." --dry-run
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-secret-scanning --repo "." --state open --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" update-secret-scanning --repo "." --alert 11 --state resolved --resolution revoked --comment "Revoked and rotated." --dry-run
python "<path-to-skill>/scripts/manage_github_security_alerts.py" list-secret-locations --repo "." --alert 11 --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" secret-scan-history --repo "." --json
python "<path-to-skill>/scripts/manage_github_security_alerts.py" api-call --repo "." --endpoint /repos/OWNER/REPO/dependabot/alerts --query-param state=open --json
```
