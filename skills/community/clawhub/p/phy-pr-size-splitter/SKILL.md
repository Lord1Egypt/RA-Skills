---
name: PR Size Splitter
description: Pull request size analyzer and split planner. Measures diff stats for any open or local PR using the gh CLI, classifies it as atomic / reviewable / oversized / unmergeable against configurable line thresholds, detects independent logical chunks (schema migrations, business logic, test additions, config changes, refactors), and proposes a named split plan with branch names and dependency order. Generates a ready-to-post PR comment with the split checklist. Works on open GitHub PRs, local git branches, or raw diff files. Zero external API — uses only the local gh CLI and git diff. Triggers on "PR too large", "split this PR", "pr size", "review this diff", "break up this PR", "atomic commits", "/pr-size".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - git
    - pull-request
    - code-review
    - developer-tools
    - workflow
    - github
    - atomic-commits
    - pr-hygiene
---

# PR Size Splitter

A PR with 800 lines changed catches half as many bugs as four 200-line PRs — and takes four times as long to review.

This skill measures your PR, identifies independent logical units in the diff, and gives you a concrete split plan with branch names, PR titles, and dependency order. Copy the output directly into a PR comment.

**Works on open GitHub PRs, local branches, or raw diff files. Zero external API.**

---

## Trigger Phrases

- "PR too large", "this PR is too big", "split this PR"
- "pr size", "review this diff", "break up this PR"
- "atomic commits", "atomic PR", "pr hygiene"
- "how do I split this", "reviewable PR"
- "/pr-size"

---

## How to Provide Input

```bash
# Option 1: Analyze an open GitHub PR
/pr-size 1234
/pr-size https://github.com/org/repo/pull/1234

# Option 2: Analyze current branch vs main
/pr-size

# Option 3: Analyze a specific branch
/pr-size feature/my-big-feature

# Option 4: Analyze against a specific base
/pr-size --base main --head feature/my-big-feature

# Option 5: Set custom size thresholds
/pr-size --atomic 150 --reviewable 400 --oversized 800

# Option 6: Output split plan as GitHub PR comment
/pr-size 1234 --post-comment

# Option 7: Just get the size classification (no split plan)
/pr-size --classify-only
```

---

## Step 1: Measure Diff Stats

```bash
# For a GitHub PR number
PR_NUMBER=1234

# Get diff stats via gh CLI
gh pr diff $PR_NUMBER --stat 2>/dev/null || \
  gh pr view $PR_NUMBER --json files --jq '.files[] | "\(.additions) \(.deletions) \(.path)"'

# Get summary numbers
gh pr view $PR_NUMBER --json additions,deletions,changedFiles \
  --jq '"Files: \(.changedFiles) | +\(.additions) -\(.deletions) | Total: \(.additions + .deletions)"'

# For a local branch (vs main)
git diff main...HEAD --stat
git diff main...HEAD --shortstat
```

**For raw diff from stdin or file:**
```bash
# Count lines from a saved diff
git diff main...HEAD | python3 -c "
import sys
added = deleted = files = 0
for line in sys.stdin:
    if line.startswith('+++') or line.startswith('---'):
        if line[4:] != '/dev/null\n': files += 1 if line.startswith('+++') else 0
    elif line.startswith('+'): added += 1
    elif line.startswith('-'): deleted += 1
print(f'Files: {files//2 or 1}  +{added} -{deleted}  Total: {added+deleted}')
"
```

---

## Step 2: Classify PR Size

```python
def classify_pr_size(files: int, additions: int, deletions: int,
                     thresholds=None) -> dict:
    """Classify PR size and predict review quality impact."""

    thresholds = thresholds or {
        'atomic':    {'lines': 150,  'files': 10},
        'reviewable':{'lines': 400,  'files': 25},
        'oversized': {'lines': 800,  'files': 50},
        # above oversized = unmergeable
    }

    total = additions + deletions

    if total <= thresholds['atomic']['lines'] and files <= thresholds['atomic']['files']:
        tier = 'ATOMIC'
        emoji = '✅'
        review_time = '< 15 min'
        bug_catch_rate = '~90%'
        recommendation = 'Good to go — this PR is easy to review.'
    elif total <= thresholds['reviewable']['lines'] and files <= thresholds['reviewable']['files']:
        tier = 'REVIEWABLE'
        emoji = '🟡'
        review_time = '15–45 min'
        bug_catch_rate = '~70%'
        recommendation = 'Acceptable size. Consider splitting if changes are logically independent.'
    elif total <= thresholds['oversized']['lines'] and files <= thresholds['oversized']['files']:
        tier = 'OVERSIZED'
        emoji = '🟠'
        review_time = '1–2 hours'
        bug_catch_rate = '~50%'
        recommendation = 'Split recommended. Reviewers will miss issues at this size.'
    else:
        tier = 'UNMERGEABLE'
        emoji = '🔴'
        review_time = '4+ hours (often skipped)'
        bug_catch_rate = '~30%'
        recommendation = 'Split required. PRs this large rarely get meaningful review.'

    return {
        'tier': tier,
        'emoji': emoji,
        'total_lines': total,
        'files': files,
        'review_time': review_time,
        'bug_catch_rate': bug_catch_rate,
        'recommendation': recommendation,
    }
```

---

## Step 3: Detect Independent Logical Chunks

```python
import subprocess
import re
from collections import defaultdict

# File patterns → logical chunk types
CHUNK_PATTERNS = [
    ('SCHEMA_MIGRATION', [
        r'migrations?/', r'db/migrate/', r'alembic/', r'\.sql$',
        r'schema\.prisma$', r'flyway/',
    ]),
    ('TESTS', [
        r'\.test\.[jt]sx?$', r'\.spec\.[jt]sx?$', r'_test\.py$',
        r'test_.*\.py$', r'__tests__/', r'spec/', r'/tests?/',
    ]),
    ('DEPENDENCIES', [
        r'package\.json$', r'package-lock\.json$', r'yarn\.lock$',
        r'pnpm-lock\.yaml$', r'requirements.*\.txt$', r'Pipfile',
        r'Cargo\.toml$', r'Cargo\.lock$', r'go\.mod$', r'go\.sum$',
    ]),
    ('CONFIG', [
        r'\.(yaml|yml|toml|ini|env|conf)$', r'docker', r'Dockerfile',
        r'\.github/', r'\.circleci/', r'\.gitlab-ci',
        r'webpack\.', r'vite\.', r'tsconfig\.', r'eslint',
    ]),
    ('DOCS', [
        r'\.md$', r'\.rst$', r'docs?/', r'README', r'CHANGELOG',
        r'CONTRIBUTING', r'\.txt$',
    ]),
    ('REFACTOR', [
        # Heuristic: many renames, moves, or files with high churn but same logic
    ]),
    ('FEATURE', []),  # Catch-all for business logic
]


def classify_files_to_chunks(pr_number_or_branch: str) -> dict:
    """Group changed files into logical chunks."""

    # Get changed files
    if pr_number_or_branch.isdigit():
        result = subprocess.run(
            ['gh', 'pr', 'diff', pr_number_or_branch, '--name-only'],
            capture_output=True, text=True
        )
    else:
        result = subprocess.run(
            ['git', 'diff', f'main...{pr_number_or_branch}', '--name-only'],
            capture_output=True, text=True
        )

    files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]

    chunks = defaultdict(list)
    for fpath in files:
        assigned = False
        for chunk_type, patterns in CHUNK_PATTERNS[:-1]:  # all except FEATURE
            if any(re.search(p, fpath, re.IGNORECASE) for p in patterns):
                chunks[chunk_type].append(fpath)
                assigned = True
                break
        if not assigned:
            chunks['FEATURE'].append(fpath)

    # Further split FEATURE files by top-level directory (module)
    feature_by_module = defaultdict(list)
    for fpath in chunks.get('FEATURE', []):
        parts = fpath.split('/')
        module = parts[0] if len(parts) > 1 else 'root'
        feature_by_module[module].append(fpath)

    # If multiple modules, split FEATURE by module
    if len(feature_by_module) > 1:
        del chunks['FEATURE']
        for module, module_files in feature_by_module.items():
            chunks[f'FEATURE:{module}'] = module_files

    return dict(chunks)


def suggest_split_plan(chunks: dict, pr_title: str = '') -> list[dict]:
    """Generate a concrete PR split plan from chunks."""
    plan = []

    # Priority order for split sequencing
    DEPENDENCY_ORDER = [
        'SCHEMA_MIGRATION', 'DEPENDENCIES', 'CONFIG',
        # FEATURE modules sorted alphabetically
        'REFACTOR', 'DOCS', 'TESTS',
    ]

    # Sort chunks by dependency order
    def chunk_sort_key(chunk_name):
        base = chunk_name.split(':')[0]
        try:
            return DEPENDENCY_ORDER.index(base)
        except ValueError:
            return 5  # FEATURE modules go in the middle

    sorted_chunks = sorted(chunks.items(), key=lambda x: chunk_sort_key(x[0]))

    for i, (chunk_type, files) in enumerate(sorted_chunks):
        base_type = chunk_type.split(':')[0]
        module = chunk_type.split(':')[1] if ':' in chunk_type else None

        # Generate suggested branch name and PR title
        if base_type == 'SCHEMA_MIGRATION':
            suggested_branch = f'feat/db-migration'
            suggested_title = f'[1/{len(sorted_chunks)}] Add database migration'
            note = 'Merge first — code changes should be backward-compatible with old schema'
        elif base_type == 'DEPENDENCIES':
            suggested_branch = f'chore/deps-update'
            suggested_title = f'[1/{len(sorted_chunks)}] Update dependencies'
            note = 'Can be reviewed and merged independently'
        elif base_type == 'CONFIG':
            suggested_branch = f'chore/config-updates'
            suggested_title = f'[{i+1}/{len(sorted_chunks)}] Update configuration'
            note = 'Low risk, easy to review'
        elif base_type == 'TESTS':
            suggested_branch = f'test/add-tests'
            suggested_title = f'[{i+1}/{len(sorted_chunks)}] Add tests'
            note = 'Merge after the feature PRs it tests'
        elif base_type == 'DOCS':
            suggested_branch = f'docs/update-docs'
            suggested_title = f'[{i+1}/{len(sorted_chunks)}] Update documentation'
            note = 'Can be merged any time'
        else:
            slug = (module or 'feature').lower().replace('/', '-').replace('_', '-')
            suggested_branch = f'feat/{slug}'
            suggested_title = f'[{i+1}/{len(sorted_chunks)}] {module or "Feature"}: {pr_title[:40]}'
            note = 'Core feature changes'

        plan.append({
            'order': i + 1,
            'chunk_type': chunk_type,
            'suggested_branch': suggested_branch,
            'suggested_title': suggested_title,
            'files': files,
            'file_count': len(files),
            'note': note,
        })

    return plan
```

---

## Step 4: Output Report

```markdown
## PR Size Analysis
PR #1234: "Add user preferences system and refactor auth middleware"
Branch: `feature/user-preferences` → `main`

---

### Size Classification: 🔴 UNMERGEABLE

| Metric | This PR | Atomic | Reviewable | Oversized |
|--------|---------|--------|------------|-----------|
| Lines changed | **1,247** | ≤150 | ≤400 | ≤800 |
| Files changed | **67** | ≤10 | ≤25 | ≤50 |
| Est. review time | **4+ hours** | <15 min | 15–45 min | 1–2 hrs |
| Est. bug catch rate | **~30%** | ~90% | ~70% | ~50% |

**This PR will not receive meaningful review.** Split into atomic units.

---

### Detected Logical Chunks (5 independent units)

```
1. SCHEMA_MIGRATION (2 files)
   db/migrate/20260319_add_preferences_table.rb
   db/migrate/20260319_add_user_settings_column.rb
   → Branch: feat/db-migration | Merge FIRST

2. FEATURE:auth (11 files)
   src/auth/middleware.ts
   src/auth/session.ts
   src/auth/token-validator.ts
   ... 8 more
   → Branch: feat/auth-refactor | Independent

3. FEATURE:preferences (24 files)
   src/preferences/model.ts
   src/preferences/api.ts
   src/preferences/components/PreferencesPage.tsx
   ... 21 more
   → Branch: feat/user-preferences | Depends on migration

4. CONFIG (5 files)
   .env.example
   docker-compose.yml
   src/config/app.ts
   tsconfig.json
   .eslintrc.js
   → Branch: chore/config-updates | Independent, merge any time

5. TESTS (25 files)
   src/auth/__tests__/middleware.test.ts
   src/preferences/__tests__/api.test.ts
   ... 23 more
   → Branch: test/add-tests | Merge LAST
```

---

### Suggested Split Plan

```
PR 1/5 — feat/db-migration (2 files, ~45 lines)
  Title: "[1/5] Add preferences table migration"
  Note: Merge first. New columns are nullable — safe for old app code.
  Depends on: nothing

PR 2/5 — feat/auth-refactor (11 files, ~280 lines)
  Title: "[2/5] Refactor auth middleware"
  Note: Pure refactor — no behavior change. Easy to review in isolation.
  Depends on: nothing

PR 3/5 — feat/user-preferences (24 files, ~580 lines)
  Title: "[3/5] Add user preferences system"
  Note: Core feature. Still large — consider splitting by layer (API / components / model).
  Depends on: PR 1/5 (migration)

PR 4/5 — chore/config-updates (5 files, ~90 lines)
  Title: "[4/5] Update config for preferences feature"
  Note: Trivial changes. Can be merged any time.
  Depends on: nothing

PR 5/5 — test/add-tests (25 files, ~252 lines)
  Title: "[5/5] Add tests for preferences and auth"
  Note: Merge after PRs 2 and 3 are in.
  Depends on: PR 2/5, PR 3/5
```

---

### How to Execute the Split

```bash
# Step 1: Create the migration branch
git checkout main
git checkout -b feat/db-migration
git checkout feature/user-preferences -- db/migrate/20260319_add_preferences_table.rb
git checkout feature/user-preferences -- db/migrate/20260319_add_user_settings_column.rb
git commit -m "Add preferences table migration"
gh pr create --title "[1/5] Add preferences table migration" --base main

# Step 2: Auth refactor branch
git checkout main
git checkout -b feat/auth-refactor
git checkout feature/user-preferences -- src/auth/
git commit -m "Refactor auth middleware"
gh pr create --title "[2/5] Refactor auth middleware" --base main

# Repeat for each chunk...
```

---

### PR Comment (ready to post)

```
⚠️ **This PR is 1,247 lines across 67 files — too large for meaningful review.**

I've identified 5 independent logical units. Suggested split:

| # | Title | Size | Depends On |
|---|-------|------|------------|
| 1 | feat/db-migration — Add migration | ~45 lines | — |
| 2 | feat/auth-refactor — Refactor auth | ~280 lines | — |
| 3 | feat/user-preferences — Core feature | ~580 lines | #1 |
| 4 | chore/config-updates — Config | ~90 lines | — |
| 5 | test/add-tests — Tests | ~252 lines | #2, #3 |

Run `/pr-size 1234` for full split instructions with git commands.
```

---

## Quick Mode Output

```
PR #1234 Size: 🔴 UNMERGEABLE (1,247 lines, 67 files)

5 logical chunks detected:
  1. SCHEMA_MIGRATION (2 files) — merge first
  2. FEATURE:auth (11 files) — independent
  3. FEATURE:preferences (24 files) — depends on migration
  4. CONFIG (5 files) — independent
  5. TESTS (25 files) — merge last

Run /pr-size 1234 --split for git commands to execute the split.
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
