---
name: lingxi-webhook-dispatcher
category: automation
description: "Intelligent webhook dispatcher with GitHub API fallback. Automatically handles git push failures by routing to GitHub Contents API. Supports retry logic, delivery receipts, and multi-endpoint fan-out."
version: 1.0
---

# lingxi-webhook-dispatcher

An intelligent webhook routing system with automatic GitHub API fallback when standard push fails.

## Problem It Solves

Git push can fail due to:
- Port 443 blocked by firewall/network
- DNS resolution issues
- SSL certificate problems
- Rate limiting on git protocol

This skill provides a robust fallback: when `git push` fails, automatically route to GitHub Contents API (`PUT /repos/{owner}/{repo}/contents/{path}`) to upload files directly.

## Architecture

```
git push → [fails] → Webhook Dispatcher
  → GitHub Contents API (fallback upload)
  → Retry logic (exponential backoff)
  → Delivery receipt (JSON log)
  → Alert notification (if still failing)
```

## Usage

### Trigger: Automatic on git push failure

```
When: git push fails in any workflow
Action: Dispatcher intercepts → GitHub API fallback → Upload files
Output: Delivery receipt at ~/webhook-dispatch/logs/YYYY-MM-DD.json
```

### Manual Dispatch

```
Trigger: "Dispatch files to GitHub via API"
Action: Uploads specified files to GitHub using Contents API
```

### Fan-out Dispatch

```
Trigger: "Push this update to repos: [repo1, repo2, repo3]"
Action: Parallel upload to all specified repos
Output: Summary report of success/failure per repo
```

## Configuration

```json
{
  "github_token": "ghp_xxx",
  "default_owner": "nima54851",
  "retry_attempts": 3,
  "retry_backoff_ms": 1000,
  "log_path": "~/webhook-dispatch/logs/",
  "alert_webhook": "https://your-alert-channel.com/webhook"
}
```

## GitHub Contents API Upload Flow

```bash
# 1. Get current file SHA (if exists)
gh api repos/{owner}/{repo}/contents/{path} --jq '.sha'

# 2. Upload with SHA for update (or no SHA for new files)
gh api -X PUT repos/{owner}/{repo}/contents/{path} \
  -f message="Automated dispatch: {timestamp}" \
  -f content=$(base64 -w 0 file.txt) \
  -f sha={sha}
```

## Retry Logic

| Attempt | Delay | Strategy |
|---------|-------|----------|
| 1 | Immediate | Direct API call |
| 2 | 1 second | Exponential backoff |
| 3 | 3 seconds | Exponential backoff |
| 4 | 10 seconds | Alert + final attempt |

## Installation

```bash
clawhub install lingxi-webhook-dispatcher
```

## Integration with GitHub Actions

Add to your workflow as a fallback step:

```yaml
- name: GitHub API Fallback Dispatch
  if: failure()
  run: |
    curl -X POST https://your-dispatcher-endpoint.com/dispatch \
      -H "Authorization: Bearer ${{ secrets.DISPATCH_TOKEN }}" \
      -d '{"event": "push_failure", "repo": "${{ github.repository }}"}'
```

## Use Cases

1. **CI/CD Pipeline Fallback**: When git push fails in CI, use API to push artifacts
2. **Automated Reports**: Daily/weekly reports uploaded via API instead of git
3. **Multi-repo Sync**: Push same content to multiple repos simultaneously
4. **Offline-to-Online Sync**: Store changes locally, sync via API when network is available
