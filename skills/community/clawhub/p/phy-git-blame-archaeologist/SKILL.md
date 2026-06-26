---
name: Git Blame Archaeologist
description: Git history archaeology tool that answers "why does this code exist?" for any file, line, or suspicious block. Chains git blame → git log --follow → commit message / PR body to surface the original decision rationale, linked issue or ticket reference, and narrative timeline behind any line of code. Detects rename/move history across refactors so the chain is never broken by file renames. Flags "mystery blocks" — code with no explanatory commit context, terse messages like "fix" or "wip", or commits that post-date the feature they implement. Works fully offline with only the local git binary. Triggers on "why does this code exist", "git archaeology", "code history", "blame chain", "why was this added", "who wrote this and why", "/git-blame-archaeologist".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - git
    - archaeology
    - code-history
    - blame
    - developer-tools
    - onboarding
    - debugging
    - documentation
---

# Git Blame Archaeologist

You're staring at a magic number. `const TIMEOUT = 47000`. Why 47? Not 45, not 60 — 47.

`git blame` tells you Alice changed it on March 3rd. The commit message says "fix timeout". The PR is closed. The linked issue is closed. The ticket is gone.

This skill chains blame → log → follow → context to reconstruct *why* the code is the way it is — not just who and when.

**Works fully offline. Zero external API. Only requires a git repo.**

---

## Trigger Phrases

- "why does this code exist", "why was this added"
- "what's the history of this", "git archaeology"
- "trace this line", "blame chain"
- "why is this magic number here", "who added this and why"
- "explain the history of this file"
- "mystery code", "unexplained block"
- "/git-blame-archaeologist"

---

## How to Provide Input

```bash
# Option 1: Investigate a specific line
/git-blame-archaeologist src/auth/middleware.ts:47

# Option 2: Investigate a line range
/git-blame-archaeologist src/config.py:120-135

# Option 3: Investigate a named symbol (function, constant)
/git-blame-archaeologist --symbol TIMEOUT_MS src/

# Option 4: Investigate the entire recent history of a file
/git-blame-archaeologist src/api/users.ts

# Option 5: Find all "mystery blocks" in a file (terse commit messages)
/git-blame-archaeologist --find-mysteries src/

# Option 6: Start from a specific commit and trace back
/git-blame-archaeologist src/utils.js:88 --since abc1234
```

---

## Step 1: Run git blame

```bash
# Get blame for a specific line or file
git blame -L 47,47 src/auth/middleware.ts --porcelain
# -L: line range
# --porcelain: machine-readable output with full commit hashes

# For a range of lines
git blame -L 120,135 src/config.py --porcelain

# For an entire file (condensed)
git blame --date=short src/api/users.ts
```

**Read the blame output:**
```
# porcelain format:
abc1234def5678... 47 47
author Alice Chen
author-mail <alice@company.com>
author-time 1741824000
author-tz +0800
committer Alice Chen
committer-time 1741824000
summary fix timeout issue
filename src/auth/middleware.ts
        const TIMEOUT = 47000
```

Key fields to extract:
- `summary` — the commit message (often terse)
- The commit hash (`abc1234...`) — use this to get full context
- `author-time` — when the change was made

---

## Step 2: Get Full Commit Context

```bash
# Get the full commit message and diff for the blamed commit
COMMIT_HASH="abc1234def5678"

# Full commit with diff context around the changed line
git show $COMMIT_HASH --stat

# The specific change to this file
git show $COMMIT_HASH -- src/auth/middleware.ts

# Check if this commit references a PR, issue, or ticket
git log --format="%H %s %b" $COMMIT_HASH -1
# Look for: "fixes #123", "closes #456", "JIRA-789", "PR #234"
```

---

## Step 3: Trace Rename/Move History

Files get renamed, moved, and split. `git blame` on the current path only shows history *after* the last rename.

```bash
# Follow file across renames
git log --follow --all --oneline -- src/auth/middleware.ts
# --follow: traces through renames
# --all: includes all branches

# Find the original filename
git log --follow --diff-filter=R --summary -- src/auth/middleware.ts | grep "rename"
# Shows: "rename old/path/auth.js => src/auth/middleware.ts (95%)"

# If renamed, also blame the old path for full history
git log --follow -p -- src/auth/middleware.ts | grep -A5 "TIMEOUT = "
```

---

## Step 4: Reconstruct the Decision Timeline

```python
import subprocess
import re
from datetime import datetime

def get_blame_for_line(filepath, line_num):
    """Get git blame data for a specific line."""
    result = subprocess.run(
        ['git', 'blame', '-L', f'{line_num},{line_num}', '--porcelain', filepath],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None

    output = result.stdout
    commit_hash = output.split('\n')[0].split(' ')[0]

    fields = {}
    for line in output.split('\n'):
        if line.startswith('author '):
            fields['author'] = line[7:]
        elif line.startswith('author-time '):
            ts = int(line[12:])
            fields['date'] = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        elif line.startswith('summary '):
            fields['summary'] = line[8:]
        elif line.startswith('filename '):
            fields['filename'] = line[9:]

    return {'hash': commit_hash[:8], **fields}


def get_full_commit_context(commit_hash, filepath):
    """Get the full commit message and linked references."""
    result = subprocess.run(
        ['git', 'log', '--format=%H%n%s%n%b', '-1', commit_hash],
        capture_output=True, text=True
    )
    full_message = result.stdout

    # Extract ticket/issue references
    refs = []
    patterns = [
        (r'#(\d+)', 'GitHub Issue/PR'),
        (r'[A-Z]+-\d+', 'Jira/Linear ticket'),
        (r'fixes?\s+#(\d+)', 'Fixes issue'),
        (r'closes?\s+#(\d+)', 'Closes issue'),
        (r'https?://[^\s]+/(?:issues?|pull)s?/(\d+)', 'Linked URL'),
    ]
    for pattern, label in patterns:
        for m in re.finditer(pattern, full_message, re.IGNORECASE):
            refs.append({'ref': m.group(0), 'type': label})

    # Get files changed in this commit
    stat_result = subprocess.run(
        ['git', 'show', '--stat', '--format=', commit_hash],
        capture_output=True, text=True
    )

    return {
        'full_message': full_message.strip(),
        'refs': refs,
        'files_changed': stat_result.stdout.strip(),
    }


def follow_file_history(filepath):
    """Trace file through renames."""
    result = subprocess.run(
        ['git', 'log', '--follow', '--all', '--oneline', '--', filepath],
        capture_output=True, text=True
    )
    commits = result.stdout.strip().split('\n')

    # Find renames
    rename_result = subprocess.run(
        ['git', 'log', '--follow', '--diff-filter=R', '--summary', '--', filepath],
        capture_output=True, text=True
    )

    renames = re.findall(r'rename (.+?) => (.+?) \(\d+%\)', rename_result.stdout)

    return commits[:10], renames  # Last 10 commits + rename history


def classify_commit_quality(summary, body=''):
    """Classify whether a commit message explains the WHY."""
    terse_patterns = [
        r'^(fix|wip|update|change|edit|stuff|misc|temp|hack|todo)\.?$',
        r'^(fix\s+\w+|update\s+\w+)$',
        r'^[a-z]{1,8}$',
    ]

    for pattern in terse_patterns:
        if re.match(pattern, summary.strip().lower()):
            return 'MYSTERY', 'Terse commit message — no context about why'

    if len(summary) < 10:
        return 'MYSTERY', 'Commit message too short to be informative'

    if any(keyword in summary.lower() for keyword in ['fix', 'patch', 'hotfix']):
        if body:
            return 'PARTIAL', 'Fix commit — body may have context'
        return 'PARTIAL', 'Fix commit with no body explanation'

    return 'GOOD', 'Commit message describes intent'
```

---

## Step 5: Search Related Context

```bash
# Search all commits that ever touched this symbol or value
git log --all -S "47000" --oneline -- src/
# -S: pickaxe search — commits where this string was added or removed

git log --all -S "TIMEOUT" --oneline -- src/
# Find when the constant was first introduced

# Find the PR or issue discussion (if remote is GitHub)
git log --all --format="%H %s" | grep -i "timeout\|TIMEOUT"

# Check if value is documented in comments, README, or docs
grep -r "47000\|TIMEOUT_MS\|47 seconds" . --include="*.md" --include="*.txt" -l

# Check if it appears in test files (often tests document the reason)
grep -r "47000\|TIMEOUT_MS" . --include="*.test.*" --include="*spec*" -A5
```

---

## Step 6: Output Report

```markdown
## Git Archaeology Report
Target: `src/auth/middleware.ts:47` — `const TIMEOUT = 47000`

---

### Timeline

**Current state** (2026-01-15, Alice Chen)
```
Commit: abc1234
Message: "fix timeout issue"
Classification: ⚠️ MYSTERY — terse message, no context
```

**Tracing back...**

```bash
git log --all -S "47000" --oneline -- src/
→ abc1234 fix timeout issue         ← current
→ def5678 add auth middleware        ← original introduction
→ (no earlier matches — first added in def5678)
```

**Original introduction** (2025-09-03, Bob Martinez)
```
Commit: def5678
Message: "add auth middleware with session timeout"
Body: "Adds request timeout for auth endpoints.
      47s chosen to match our upstream vendor API timeout (46s)
      plus 1s buffer. See issue #234 for vendor SLA discussion."

Linked issues: #234 ("Upstream API timeout SLA")
Files changed: src/auth/middleware.ts (+1), README.md (+3 lines)
```

**Why the change to abc1234?** (2026-01-15)
```
The value was unchanged — Alice's "fix" commit appears to have touched a
different part of the same file (formatting only). The TIMEOUT value itself
hasn't changed since original introduction.
```

---

### Answer

**Why is TIMEOUT = 47000?**

The value was set on 2025-09-03 by Bob Martinez in commit `def5678`.

The commit body explains: "47s chosen to match our upstream vendor API timeout (46s) plus 1s buffer."

The original issue #234 ("Upstream API timeout SLA") contains the full discussion about the vendor SLA.

**Key finding:** The magic number exists because of a vendor-imposed constraint. If the vendor changes their SLA, this value needs to change too.

**Recommendation:** Add a comment to make this self-documenting:
```ts
// 47s = upstream vendor API timeout (46s) + 1s buffer. See issue #234.
const TIMEOUT = 47000
```

---

### File History

```
src/auth/middleware.ts was previously: src/middleware/auth.js
Renamed in commit bcd9012 on 2025-11-20 ("restructure middleware directory")

Full history (10 commits across both paths):
  abc1234 (2026-01-15) fix timeout issue
  xyz7890 (2025-12-01) add unit tests for middleware
  bcd9012 (2025-11-20) restructure middleware directory [RENAME]
  mno3456 (2025-10-14) add error handling to auth middleware
  def5678 (2025-09-03) add auth middleware with session timeout ← ORIGIN
```

---

### Mystery Blocks Detected

```
src/auth/middleware.ts contains 2 other mystery blocks:

Line 23: const MAX_RETRIES = 3
  → Commit: "update" (abc3333, 2025-10-01) — terse, no body, no linked issues
  → No earlier commits touch this value
  → Recommend: investigate why 3 and not 2 or 5

Line 89: if (user.role === 'legacy_admin') {
  → Commit: "fix" (abc4444, 2026-01-10) — terse, no body
  → git log -S "legacy_admin": first introduced in abc9999 (2024-06-15) "add legacy admin support"
  → Original commit body: "Temporary backward compat for users migrated from v1. Remove after 2025-Q1."
  → 🚨 This is overdue for removal — the comment said "remove after 2025-Q1"
```
```

---

## Quick Mode Output

```
Git Archaeology: src/auth/middleware.ts:47 (TIMEOUT = 47000)

Origin: def5678 (2025-09-03, Bob Martinez) — "add auth middleware with session timeout"
Reason: "47s = upstream vendor API timeout (46s) + 1s buffer. See issue #234."
Current: abc1234 (2026-01-15) — formatting-only change, value unchanged since origin

File was renamed from: src/middleware/auth.js → src/auth/middleware.ts (2025-11-20)

🚨 Mystery found: line 89 `if (user.role === 'legacy_admin')` was marked for
   removal "after 2025-Q1" in its origin commit — still present, 12 months overdue.

Run /git-blame-archaeologist --find-mysteries src/ to scan entire directory.
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
