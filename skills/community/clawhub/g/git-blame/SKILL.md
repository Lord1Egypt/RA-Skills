---
name: Git Blame Auditor
description: Production code audit via git blame. Natural language risk analysis — overtime commits, scattered changes, no-PR-review merges, and impact domain tracing for every suspicious line.
license: MIT-0
homepage: https://github.com/harry
metadata:
  author: Harry Jiang
  version: "1.0.0"
  tags:
    - git
    - blame
    - audit
    - security
    - code-review
    - risk-analysis
    - developer-tools
---

# Git Blame Auditor

> **Audit perspective git blame.** Not "why does this code exist?" — but "**is this code safe?**"

You're in a security review. A line catches your eye — `exec("rm -rf " + userInput)`. `git blame` shows it was pushed on a Saturday at 2 AM by a junior dev, in a 47-file mega-commit with no PR review. Is this an accident? A backdoor? Or just a bad week?

**Git Blame Auditor** reads the same raw git data as any blame tool, but interprets it through an *audit and risk lens*. It flags risk signals (`⏰` overtime, `📦` scattered change, `🚫` no review, `🔍` indirect invocation), maps impact domains (which tests, services, or endpoints touch this code), and outputs a structured risk verdict.

This skill is **explicitly not** a history archaeology tool. Use `phy-git-blame-archaeologist` if you want to reconstruct the narrative timeline and original decision rationale behind a line. Use this skill when you need to **assess code safety, risk posture, and author patterns** for audits, security reviews, or on-call incident triage.

---

## What This Skill IS (vs IS NOT)

| Criterion | Git Blame Auditor (this skill) | phy-git-blame-archaeologist (competitor) |
|---|---|---|
| **Primary lens** | Security & code audit | History archaeology |
| **Question answered** | "Is this change risky?" | "Why does this code exist?" |
| **Output** | Risk score + author pattern + impact domain | Narrative timeline + decision rationale |
| **Risk signals** | ⏰ Overtime, 📦 Scattered, 🚫 No review, 🔍 Indirect use | Mystery blocks (terse messages), rename history |
| **Impact analysis** | Cross-file call graph / dependency trace | Rename trail |
| **Author profiling** | Commit-time patterns, file affinity, area expertise | Basic author attribution |
| **Review signal** | Extract PR/commit review status | Message quality classification |
| **Target user** | Security auditor, tech lead, on-call engineer | Developer onboarding, code historian |
| **Model** | DeepSeek (recommended) | GPT-5.5 |

---

## Trigger Phrases

- "audit this line" / "risk check this change"
- "who last touched this and is it safe"
- "is this code risky"
- "blame audit on" / "git blame audit"
- "find suspicious commits in"
- "show risky changes by this author"
- "/git-blame-audit"

---

## How to Provide Input

```bash
# Option 1: Audit a specific line (risk-focused blame)
/git-blame-audit src/payment/gateway.ts:142

# Option 2: Audit a range
/git-blame-audit src/payment/gateway.ts:140-155

# Option 3: Audit a symbol (function / class / constant)
/git-blame-audit --symbol processRefund src/

# Option 4: Full file audit — get risk summary of every line
/git-blame-audit src/payment/gateway.ts

# Option 5: Author risk profile — all risky commits by one person
/git-blame-audit --author "alice@company.com" --since 2026-01-01

# Option 6: Time-window scan — all commits in last 7 days with risk markers
/git-blame-audit --since "7 days ago"
```

---

## Step 1: Run git blame and collect raw signals

```bash
# Get blame for a specific line with full porcelain
git blame -L 142,142 src/payment/gateway.ts --porcelain

# For a range
git blame -L 140,155 src/payment/gateway.ts --porcelain

# For an entire file (condensed)
git blame --date=short src/payment/gateway.ts
```

**Read and extract these fields from porcelain output:**

```
abc1234def5678... 142 142
author Alice Chen
author-mail <alice@company.com>
author-time 1825027200     ← Unix timestamp
author-tz +0800
committer Alice Chen
committer-time 1825027200
summary fix: validate amount
previous e1234567 src/payment/gateway.ts
filename src/payment/gateway.ts
        const MAX_AMOUNT = 100000
```

Extract for risk assessment:
- `author-time` → convert to local time → flag if outside 09:00-18:00 Mon-Fri
- `summary` → check for PR/issue references in message
- `previous` → know the exact previous commit on this line
- Commit hash → use for Step 2 (review status check)

---

## Step 2: Assess review status and commit size

```bash
# Get full commit details
COMMIT="abc1234def5678"
git show $COMMIT --stat               # How many files changed?
git log --format="%H%n%an%n%ae%n%ai%n%s%n%b" $COMMIT -1

# Check if it's a merge commit (may indicate no individual review)
git cat-file -p $COMMIT | head -5
# If it shows two parents (Merge: xxx yyy), it's a merge commit

# Count total files changed (scatter metric)
git diff-tree --no-commit-id -r --name-only $COMMIT | wc -l

# Count total lines changed (churn metric)
git diff --stat $COMMIT | tail -1 | grep -oP '\d+ insertions?'
git diff --stat $COMMIT | tail -1 | grep -oP '\d+ deletions?'
```

**Risk thresholds (configurable):**
- `🔴 High scatter`: > 15 files changed in one commit
- `🟡 Medium scatter`: 8-15 files changed
- `⏰ Overtime`: commit timestamp outside standard working hours (configurable: default Mon-Fri 09:00-18:00)
- `🚫 No PR reference`: commit message lacks PR/issue pattern (`#\d+`, `PR-\d+`, `JIRA-\d+`)
- `📏 Large churn`: > 500 lines added or deleted

---

## Step 3: Impact domain analysis — what depends on this code?

```bash
# Find functions / classes that reference this symbol
# If the blamed line defines a symbol:
git grep -n "processRefund\|MAX_AMOUNT" -- src/ -- ':!*.test.*'

# Find all callers within the codebase
# (Use grep to find function invocations)
git grep -n "processRefund(" -- src/ -- ':!*.test.*'

# Find ALL files touched by this commit (not just the blamed line)
git diff-tree --no-commit-id -r --name-only $COMMIT | sort
```

**Classify impact domains:**
- Database / migrations
- Payment / billing
- Authentication / authorization
- Public API endpoints
- Internal utilities
- Configuration / constants
- Build / CI
- Test files (lower risk per line but may indicate testing gaps)

---

## Step 4: Author pattern analysis

```bash
# Author's recent commit count
git shortlog -sn --since="2026-01-01" --until="now" | grep "Alice Chen"

# Author's file affinity — what areas does this author normally touch?
git log --author="alice@company.com" --oneline --name-only --since="2026-01-01" \
  | grep -E "\.(ts|js|py|go|java|rb)$" | sort | uniq -c | sort -rn | head -10

# Author's commit time distribution
git log --author="alice@company.com" --format="%ai" --since="2026-01-01" \
  | cut -d' ' -f2 | cut -d: -f1 | sort | uniq -c | sort -rn

# Does the author normally work in this area?
# If their top 10 files never include this module → ⚠️ out-of-area change
```

**Author risk signals:**
- `🔄 Out-of-area`: Author normally works in frontend, but this change is in database migrations
- `🌙 Night pattern`: > 40% of commits outside 09:00-18:00
- `🆕 New contributor`: Author has < 10 commits in this repository
- `📈 Churn spike`: This month's commit count is > 3× their monthly average
- `🗂️ Wide scatter`: Author's last commit touched files across 5+ unrelated modules

---

## Step 5: Composite risk scoring

Combine risk signals into a weighted score (0-100):

| Signal | Weight | Detection |
|---|---|---|
| Overtime commit | +15 | timestamp outside working hours |
| Scattered commit (15+ files) | +20 | git diff-tree wide footprint |
| No PR/issue reference | +15 | commit message lacks `#\d+`, `PR-` |
| Out-of-area change | +15 | author's file affinity doesn't include this module |
| Large churn (500+ lines) | +10 | diff stat large |
| Merge commit (no individual review) | +10 | commit has 2+ parents |
| Night owl author pattern | +10 | >40% commits at night |
| New contributor (<10 commits) | +10 | shortlog count low |
| Indirect/high-risk function | +15 | calls `exec`, `eval`, `fs.write`, SQL raw, crypto |
| Delicate domain | +15 | touches payment, auth, data migration |

**Risk bands:**
- `🟢 LOW (0-20)`: Routine change, reviewed, in-area, normal hours
- `🟡 MEDIUM (21-50)`: Some flags — worth a second look during review
- `🟠 HIGH (51-75)`: Multiple risk signals — audit before deployment
- `🔴 CRITICAL (76-100)`: Strong risk pattern — immediate investigation

---

## Step 6: Output structured risk report

```markdown
## Git Blame Audit Report
**Target**: `src/payment/gateway.ts:142` — `const MAX_AMOUNT = 100000`

---

### 🔴 Risk Score: 72 / 100 (HIGH)

| Risk Factor | Weight | Details |
|---|---|---|
| ⏰ Overtime | +15 | Sat 2026-06-13 02:15 CST |
| 📦 Scattered | +20 | 47 files changed |
| 🚫 No review | +15 | Merge commit, no PR/issue reference |
| 🔍 Out-of-area | +10 | Author's main area: frontend/src |
| 🆕 New contributor | +10 | Only 4 total commits |
| ⚠️ Delicate domain | +15 | Payment code — affects billing |

---

### 🧑‍💻 Author Profile

**Alice Chen** `<alice@company.com>` (active since 2026-05-20)

- **Total commits in repo**: 4 (all in last 3 weeks)
- **File affinity**: `frontend/src/components/`, `frontend/src/api/`
- **This commit area**: `src/payment/` (first time → out-of-area)
- **Commit time pattern**: 3 of 4 commits after 22:00
- **Typical reviewer**: No review found for any commit

---

### 🌐 Impact Domain

`MAX_AMOUNT = 100000` is used in:

```
src/payment/processor.ts:47     ← amount check logic
src/payment/validation.ts:88    ← input validation
src/api/checkout.ts:23          ← POST /checkout endpoint
```

**Upstream callers** (files calling into these 3 files):

```
src/controllers/OrderController.ts:15
src/workers/paymentWorker.ts:33
```

**This change affects**: payment processing, checkout flow, order controller.

---

### 📋 Risk Detail

**The commit `a1b2c3d4` changed 47 files across 6 modules:**

| Module | Files Changed |
|---|---|
| frontend/src/components | 14 |
| frontend/src/api | 8 |
| src/payment | 7 ← new area for author |
| src/db/migrations | 5 ← extremely sensitive |
| src/config | 4 ← production config |
| tests | 9 |

**3 files contain high-risk operations:**
- `src/payment/executeRefund.ts:22` — `eval()` used with dynamic input
- `src/db/migrations/20260613_add_columns.sql` — raw SQL (migration)
- `src/payment/gateway.ts:142` — MAX_AMOUNT cap changed from 50000 → 100000

---

### ✅ Recommendation

1. 🔴 **Hold deployment** — this commit requires manual review
2. 👥 Assign reviewer with payment domain expertise
3. 🔄 Request author to split into focused commits (one concern per commit)
4. 📝 Add issue reference linking to the business requirement for the 2× amount increase
5. 🧪 Verify test coverage for the new MAX_AMOUNT boundary

---

### 📊 Quick Verdict

```
Git Blame Audit: src/payment/gateway.ts:142
──────────────────────────────────────────────────
Risk:   🔴 HIGH (72/100)
Author: Alice Chen (new, out-of-area, night pattern)
When:   Sat 02:15 — 47 files, 6 modules, no review
What:   MAX_AMOUNT doubled (50000 → 100000)
Impact: Payment processing, checkout, order controller
Action: 🛑 Hold. Requires domain expert review.
```

---

## Quick Mode Output

```
/git-blame-audit src/config.prod.ts:23

🟠 RISK: 62/100
   ⏰ Overtime (Sun 23:47) +10
   📦 23 files +15
   🚫 No PR ref +15
   🔍 Env config +10
   🆕 New contributor +12
Author: Bob (2 total commits, no reviews)
Change: API_ENDPOINT changed to https://staging.example.com
Action: 🛑 Investigate — staging URL in production config
```

---

## First Success Path

For first-time users, here's the fastest path to a valuable result:

1. **Navigate** to any git repository on your machine
2. **Run**: `/git-blame-audit any-file.ts:10` (pick any file with at least 10 lines)
3. **Verify** you see:
   - A risk score (0-100)
   - At least one risk marker (overtime, scattered, etc.)
   - The author and commit context
4. **Optionally drill deeper**: `/git-blame-audit --author "$(git log --format='%ae' -1)" --since 2026-01-01`

Expected time: < 30 seconds from trigger to first report.

---

## Sample Prompts

- "Audit `src/api/users.ts:88` — is this change safe?"
- "Show me all risky commits from Alice in the last 30 days"
- "Flag every line in `src/payment/` that was committed outside business hours"
- "Risk check the last 10 commits on the `main` branch"
- "Who changed `MAX_RETRIES` and is it a concern?"
- "Find all lines in `src/db/` that lack a PR reference in blame"
- "This PR touches 4 unrelated modules — audit the risk score"
- "Compare risk patterns between Alice and Bob's commits this sprint"

---

## Notes

- **Works fully offline** — only requires local git binary and the repository
- **No external API calls** — all analysis is local
- **Model**: DeepSeek recommended for the natural language risk interpretation
- **Configurable thresholds**: Risk thresholds can be adjusted per team policy
- **Not a replacement for code review** — it's a triage tool to focus reviewer attention
- **PR reference patterns** are currently tuned for GitHub (`#\d+`) and Jira (`[A-Z]+-\d+`); extendable in config
