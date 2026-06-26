---
name: github-actions-optimizer
description: Optimize GitHub Actions workflows for speed, cost, security, and reliability — analyze run times, cache strategies, job parallelism, and runner selection.
metadata:
  tags: ["github-actions", "ci-cd", "optimization", "devops", "automation"]
---

# GitHub Actions Optimizer

Analyze and optimize GitHub Actions workflows for faster builds, lower costs, better security, and higher reliability. Reviews workflow files, run history, cache usage, and runner configurations. Use when CI is slow, expensive, or unreliable.

## Usage

```
"Optimize my GitHub Actions workflows"
"Why are my CI builds so slow?"
"Audit my workflows for security issues"
"Reduce GitHub Actions costs"
"Find flaky steps in my CI pipeline"
```

## How It Works

### 1. Workflow Discovery

```bash
# Find all workflow files
find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null

# Check recent run durations
gh run list --limit 20 --json name,status,conclusion,startedAt,updatedAt,databaseId | python3 -c "
import json, sys
from datetime import datetime
runs = json.load(sys.stdin)
for r in runs:
    start = datetime.fromisoformat(r['startedAt'].rstrip('Z'))
    end = datetime.fromisoformat(r['updatedAt'].rstrip('Z'))
    duration = (end - start).total_seconds() / 60
    print(f'{r[\"name\"]:30s} {r[\"conclusion\"]:10s} {duration:.1f}min')
"
```

### 2. Speed Optimization

**Caching analysis:**
- Are dependencies cached? (`actions/cache` or `actions/setup-node` with cache)
- Cache hit rate from recent runs
- Missing cache keys for build artifacts, Docker layers, compiled assets
- Cache size approaching 10GB limit?
- Stale cache keys never cleaned up

**Job parallelism:**
- Sequential jobs that could run in parallel
- Large matrix builds that could be split
- Test suites that could be sharded
- Independent steps within a single job

**Runner optimization:**
- Self-hosted vs GitHub-hosted: cost/speed tradeoff
- Larger runners available? (`ubuntu-latest-xl`, `ubuntu-latest-16-cores`)
- ARM runners for compatible workloads (30% cheaper)
- Container jobs vs VM jobs

**Build optimization:**
- Unnecessary checkout of full git history (`fetch-depth: 0`)
- Redundant install steps across jobs
- Tests running on every push instead of just PRs
- Docker builds without layer caching
- Missing path filters (trigger on irrelevant file changes)

### 3. Cost Reduction

**Minute savings:**
- Identify most expensive workflows (minutes × frequency)
- Timeout missing on long-running jobs (default: 6 hours!)
- Concurrency groups to cancel redundant runs
- Path filtering to skip irrelevant triggers
- PR-only vs push+PR triggers

**Storage savings:**
- Artifact retention too long (default: 90 days)
- Large artifacts uploaded unnecessarily
- Cache entries never evicted

### 4. Security Audit

- **Pinned actions**: Using `@v3` instead of SHA pinning
- **Secrets exposure**: Secrets passed to untrusted steps
- **GITHUB_TOKEN permissions**: Overly broad default permissions
- **Pull request target**: Workflow runs on `pull_request_target` with checkout of PR head
- **Script injection**: Untrusted input in `run:` blocks (`${{ github.event.issue.title }}`)
- **Third-party actions**: Unverified marketplace actions with broad permissions
- **Environment protection**: Missing required reviewers on production deployments

### 5. Reliability

- **Retry strategy**: Flaky steps without retry configuration
- **Timeout values**: Missing or too generous timeouts
- **Error handling**: `continue-on-error` hiding real failures
- **Status checks**: Required checks that aren't actually running
- **Concurrency**: Race conditions between parallel workflow runs

### 6. Modern Patterns

Recommend modern GitHub Actions features:
- Reusable workflows for DRY CI
- Composite actions for shared steps
- Environments with deployment protection rules
- OIDC for cloud authentication (no long-lived secrets)
- Merge queues for safe main branch

## Output

```
## GitHub Actions Optimization Report

**Workflows:** 5 | **Avg monthly minutes:** 12,400 | **Monthly cost:** ~$99

### ⚡ Speed Improvements

1. **Add dependency caching** — ci.yml
   Current: `npm ci` runs fresh every time (2m 15s)
   Fix: Add `cache: 'npm'` to `actions/setup-node`
   Savings: ~1m 45s per run × 180 runs/mo = 315 min/mo

2. **Parallelize test suites** — ci.yml
   Current: Unit + integration + e2e run sequentially (18 min)
   Fix: Split into 3 parallel jobs
   Savings: ~12 min per run (runs in 6 min instead of 18)

3. **Add path filters** — ci.yml
   Current: Triggers on all pushes including docs changes
   Fix: `paths-ignore: ['docs/**', '*.md', 'LICENSE']`
   Savings: ~40 unnecessary runs/mo × 18 min = 720 min/mo

### 🔐 Security Issues

4. **Unpinned action** — deploy.yml:12
   `uses: actions/checkout@v4` → pin to SHA
   
5. **Script injection risk** — pr-comment.yml:8
   `run: echo "${{ github.event.comment.body }}"` 
   → Use environment variable instead

6. **Broad GITHUB_TOKEN** — all workflows
   No `permissions:` block = read-write to everything
   → Add explicit `permissions: { contents: read }`

### 💰 Cost Savings
| Optimization | Minutes Saved/mo | $ Saved/mo |
|-------------|------------------|------------|
| Dependency cache | 315 | $2.52 |
| Path filters | 720 | $5.76 |
| Concurrency cancel | 200 | $1.60 |
| Timeout (6h → 30m) | ~0 (prevents surprise) | — |
| **Total** | **1,235** | **$9.88** |

Projected monthly: 12,400 → 11,165 min (-10%)
```
