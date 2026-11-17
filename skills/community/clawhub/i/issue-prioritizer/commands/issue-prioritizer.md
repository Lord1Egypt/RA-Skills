| allowed-tools | description |
|---|---|
| Bash(*fetch-issues.sh*), Bash(gh issue list *), Bash(gh issue view *), Bash(gh pr list *), Bash(gh pr view *), Bash(jq *), Bash(cat *manifest*), Read, Glob, Grep, Task | Read-only analysis of issues from an explicitly named GitHub repository |

# Issue Prioritizer Skill (Parallel Edition)

Analyze issues from a GitHub repository and rank them by **Adjusted Score** (ROI penalized by Tripping Scale).

**Performance:** Batch-size-based splitting + wave processing. Scales to 1000+ issues.

## Modes

This is a **read-only skill**. It analyzes and presents information. YOU make all decisions and implement changes.

## Instructions

### Step 1: Get Repository

If the user didn't specify a repository, ask which repository to analyze (format: `owner/repo`).

### Step 2: Fetch and Prepare Issues

Use the `fetch-issues.sh` script to fetch issues, detect linked PRs (via GitHub GraphQL closingIssuesReferences + regex fallback), and split into fixed-size batches — all without loading raw data into your context.

**Find the script:**
Use Glob to find `**/issue-prioritizer/**/fetch-issues.sh`.

**Run it:**
```bash
bash <path-to-script> {owner/repo} \
  --limit {limit} \
  --batch-size {batch_size} \
  --max-concurrency {concurrency} \
  [--truncate {chars}] \
  [--topic {topic}] [--search {query}] [--label {label}] \
  [--include-with-prs] [--full-body] \
  [--history-dir {path}] [--retain 20]

# Resume from existing run (no refetch)
bash <path-to-script> --resume {run_id_or_path} [--batch-size 20] [--truncate 500]

# Incremental mode: reuse cached scores for unchanged issues
bash <path-to-script> {owner/repo} --limit {limit} --diff-from latest
bash <path-to-script> {owner/repo} --limit {limit} --diff-from {run_id_or_path}
```

**Key parameters:**
- `--limit N` — Issues to fetch (default: 30)
- `--batch-size N` — Issues per batch file (default: 20). Keep at 15-25 for optimal agent quality.
- `--max-concurrency N` — Max parallel agents per wave (default: 30)
- `--truncate N` — Body truncation in chars (default: 500). Use `--full-body` for 2000 chars.
- `--topic`, `--search`, `--label` — Filtering (combinable)
- `--include-with-prs` — Skip PR exclusion
- `--history-dir <path>` — Persist runs (default: `${XDG_STATE_HOME:-~/.local/state}/issue-prioritizer/runs`)
- `--retain N` — Keep only latest N runs in history dir (default: 20, 0 = keep only current run)
- `--resume <run_id|path>` — Resume from prior run without fetching issues again
- `--diff-from <ref>` — Incremental mode: fetch fresh issues but reuse cached scores for unchanged ones. `<ref>` = `latest`, run_id, or full path. Mutually exclusive with `--resume`.

**Scale guidance:**
| Issues  | Batch Size | Batches | Waves (at concurrency 30) |
|---------|-----------|---------|---------------------------|
| 30      | 20        | 2       | 1                         |
| 100     | 20        | 5       | 1                         |
| 200     | 20        | 10      | 1                         |
| 500     | 20        | 25      | 1                         |
| 1000    | 20        | 50      | 2                         |

The script outputs a single JSON line to stdout with the summary:
```json
{"status":"ok","repo":"owner/repo","runId":"20260222-113000_owner_repo","filter":"latest","source":"list","linkingMode":"github_link","totalFetched":200,"excluded":48,"remaining":152,"batches":8,"waves":1,"batchSize":20,"concurrency":30,"workdir":"~/.local/state/issue-prioritizer/runs/20260222-113000_owner_repo"}
```

**Parse the summary** from stdout. Extract `workdir`, `batches`, `waves`.

**Read the manifest** for full details:
```bash
cat {workdir}/manifest.json
```

The manifest contains:
- `stats`: totalFetched, excludedWithPRs, remaining, batchSize, totalBatches, maxConcurrency, wavesNeeded, truncateChars, truncatedCount
- `source`: "list" or "search" (warns if search hit GitHub's 1000-result ceiling)
- `linkingMode`: "github_link" | "partial_github_link" | "regex_only" | "disabled" | "skipped"
- `runId`, `paths` (batches/results/summary locations)
- `generatedAt`, `ghVersion`
- `batches[]`: file name, issue count, first/last issue number per batch
- `excluded[]`: issues with linked PRs (issue number, title, PR number, title, URL, detection method: "github_link" or "regex_keyword")
- `diffMode`: true if `--diff-from` was used and baseline was valid
- `diffFrom`: baseline run path (or null)
- `diffStats`: `{ cached, new, modified, removed }` (or null)
- `paths.cachedScores`: "cached-scores.json" when in diff mode (or null)

**Error Handling:**
- `status: "error"` → display error and exit
- `status: "empty"` → "No open issues found" and exit
- `remaining: 0` → all issues have PRs; report that and exit
- `diffMode: true` AND `remaining: 0` → all issues unchanged; skip agent analysis entirely. Copy `{workdir}/cached-scores.json` to `{workdir}/results/merged.json` as the full result.
- If `source: "search"` and `totalFetched: 1000` → warn user about GitHub's 1000-result ceiling, suggest date-range slicing

### Step 3: Report Excluded Issues

Before analysis, report issues excluded by PR detection:

```
═══════════════════════════════════════════════════════════════
  ISSUES WITH EXISTING PRs (excluded from ranking)
═══════════════════════════════════════════════════════════════

  #123: Login crashes on empty password
        └─ 🔗 PR #456: "Fix login validation" (github_link)
           https://github.com/owner/repo/pull/456

  #789: Add email validation
        └─ 🔑 PR #101: "Add form validation" (regex_keyword: fixes #789)
           https://github.com/owner/repo/pull/101

  {N} issues excluded. Analyzing remaining {M} issues...
═══════════════════════════════════════════════════════════════
```

Detection method icons:
- 🔗 `github_link` — GitHub's own closingIssuesReferences (high fidelity)
- 🔑 `regex_keyword` — Regex fallback (fixes/closes/resolves #N)

The excluded data is in `manifest.excluded[]`.

### Step 4: Wave-Based Parallel Analysis

**CRITICAL: This is the parallel processing step. Each agent reads its batch from disk.**

Use the manifest to determine wave processing:

1. Read `stats.wavesNeeded` and `batches[]` from the manifest
2. For each wave, spawn up to `maxConcurrency` agents in parallel
3. Wait for all agents in a wave to complete before starting the next wave

**Wave Processing:**

```
Wave 1: Spawn agents for batches 1..min(maxConcurrency, totalBatches)
         → Wait for all to complete
Wave 2: Spawn agents for batches (maxConcurrency+1)..min(2*maxConcurrency, totalBatches)
         → Wait for all to complete
...repeat until all batches processed
```

**Report progress between waves:**
- "Processing Wave 1/3: batches 1-7 (140 issues)..."
- "Wave 1 complete. Processing Wave 2/3: batches 8-14 (140 issues)..."

**IMPORTANT:** Within each wave, launch ALL agents in a SINGLE message with multiple Task tool calls for maximum parallelism.

**Task Tool Parameters:**
```
Task tool call:
- description: "Analyze issues batch N"
- prompt: (see Agent Prompt Template below)
- subagent_type: "general-purpose"
- model: "sonnet"
```

**Agent Prompt Template:**

For each batch, create a Task with this prompt (fill in the placeholders):

```
You are an issue analysis agent. Read and analyze GitHub issues from a batch file.

REPOSITORY: {owner/repo}
BATCH: {batch_number} of {total_batches}

STEP 1: Read the batch file at {workdir}/batches/batch-{N}.json using the Read tool.
It contains a JSON array of GitHub issues (bodies truncated to {truncateChars} chars).

STEP 2: For EACH issue in the file, analyze and score:

## 1. Difficulty Score (1-10)
Base score: 5
Adjustments:
- Documentation only: -3
- Has proposed solution: -2
- Has reproduction steps: -1
- Clear error message: -1
- Unknown root cause: +3
- Architectural change: +3
- Race condition/concurrency: +2
- Security implications: +2
- Multiple systems involved: +2

## 2. Importance Score (1-10)
- Critical (8-10): crash, data loss, security vulnerability, service down
- High (6-7): broken functionality, errors, performance issues
- Medium (4-5): enhancements, feature requests, improvements
- Low (1-3): cosmetic, documentation, typos

## 3. Tripping Scale (1-5) - Solution Sanity
1 = Total Sanity (proven patterns, standard approach)
2 = Grounded with Flair (practical with creative touches)
3 = Dipping Toes (exploring new territory cautiously)
4 = Wild Adventure (bold, risky, unconventional)
5 = Tripping (questionable if it makes sense)

Red Flags (increase score): rewrite from scratch, blockchain/AI/ML buzzwords, experimental, breaking change, custom protocol
Green Flags (decrease score): standard, minimal change, backward compatible, well-documented, existing library

## 3.5. Architectural Impact (1-5) - How Much Does This Change Structure?

IMPORTANT: Always ask "Is there a simpler way?" before scoring.

1 = Surgical (isolated fix, touches 1-2 files, no new abstractions)
2 = Localized (small addition, follows existing patterns exactly, no new concepts)
3 = Moderate (new component BUT within existing architecture, respects boundaries)
4 = Significant (new subsystem, introduces new patterns, affects multiple modules)
5 = Transformational (restructures core, changes paradigms, migration required)

Red Flags (increase score):
- "rewrite", "refactor entire", "new architecture"
- Introduces new framework/library for existing capability
- Creates new abstraction layers
- Requires changes across >5 files
- Adds new configuration complexity
- Breaking changes to APIs/interfaces
- "we should also..." scope creep

Green Flags (decrease score):
- Bug fix in single file
- Uses existing utilities/helpers
- Follows established patterns in codebase
- Backward compatible
- No new dependencies
- Self-contained change
- Could be reverted easily

CRITICAL: If a simple solution exists, architectural changes are WRONG.
Example: Don't create a "validation framework" when a single if-check suffices.

## 4. Actionability Score (1-5) - Can it be PRed?
1 = Not Actionable (question, discussion, duplicate, support request)
2 = Needs Triage (missing info, unclear scope)
3 = Needs Investigation (unknown root cause, needs debugging)
4 = Ready to Work (clear scope, some design decisions needed)
5 = PR Ready (solution is clear, just implement)

Blockers (decrease): questions in title, "how do I?", duplicate label, wontfix label, missing repro
Ready signals (increase): "fix:", "add:" in title, proposed solution, repro steps, good-first-issue label, active maintainer interaction (recent comments/updates), issue not currently assigned

## 5. Derived Values
- issueType: "bug" | "feature" | "docs" | "other"
- suggestedLevel: "beginner" (diff 1-3) | "intermediate" (diff 4-6) | "advanced" (diff 7-10 or security/architecture)
- ROI = importance / difficulty (round to 2 decimals)
- TripMultiplier: use this table:
  | Trip Score | Multiplier |
  |------------|------------|
  | 1          | 1.00       |
  | 2          | 0.85       |
  | 3          | 0.70       |
  | 4          | 0.55       |
  | 5          | 0.40       |
- ArchMultiplier (Architectural Impact penalty): use this table:
  | Arch Score | Multiplier |
  |------------|------------|
  | 1          | 1.00       |
  | 2          | 0.90       |
  | 3          | 0.75       |
  | 4          | 0.50       |
  | 5          | 0.25       |
- ActionMultiplier: use this table:
  | Action Score | Multiplier |
  |--------------|------------|
  | 1            | 0.10       |
  | 2            | 0.40       |
  | 3            | 0.70       |
  | 4            | 0.90       |
  | 5            | 1.00       |
- AdjustedScore = ROI * TripMultiplier * ArchMultiplier * ActionMultiplier (round to 2 decimals)

## OUTPUT FORMAT

Return ONLY a valid JSON array. No markdown fences. No explanation. Just the array:

[
  {
    "number": 123,
    "title": "Issue title here",
    "url": "https://github.com/owner/repo/issues/123",
    "difficulty": 5,
    "difficultyReasoning": "base score; has reproduction (-1); unknown cause (+3)",
    "importance": 7,
    "importanceReasoning": "broken functionality affecting users",
    "tripScore": 2,
    "tripLabel": "Grounded with Flair",
    "tripRedFlags": [],
    "tripGreenFlags": ["minimal change", "standard approach"],
    "archScore": 2,
    "archLabel": "Localized",
    "archRedFlags": [],
    "archGreenFlags": ["uses existing patterns", "single file change"],
    "archSimplerAlternative": null,
    "actionScore": 4,
    "actionLabel": "Ready to Work",
    "actionBlockers": [],
    "actionReadySignals": ["has proposed solution"],
    "issueType": "bug",
    "suggestedLevel": "intermediate",
    "roi": 1.40,
    "tripMultiplier": 0.85,
    "archMultiplier": 0.90,
    "actionMultiplier": 0.90,
    "adjustedScore": 0.96,
    "deepReason": ["critical_bug", "top20_score"]
  }
]

IMPORTANT: Return ONLY the JSON array. No other text.
```

### Step 5: Collect and Merge Results

After each wave completes, collect results. For each agent response:

1. **Clean the response:**
   - If wrapped in markdown code fences (```json ... ```), extract the content
   - If wrapped in ```...```, extract the content
   - Trim whitespace

2. **Parse JSON:**
   - Attempt to parse as JSON array
   - If parsing fails, log which batch failed and continue with other results

3. **Merge results:**
   - Combine all successful arrays into a single array
   - Deduplicate by issue number (if same issue appears twice, keep first occurrence)
   - **If `diffMode: true`:** After merging agent results, also read `{workdir}/cached-scores.json` and combine: `agentResults + cachedScores`. Agent results take priority (dedup by number, keep agent result if both exist).

4. **Track failures:**
   - Note which batches failed to parse
   - Report: "Warning: Batch N failed to parse. Issues #X-#Y may be missing from results."

**If ALL agents fail:** Report error and suggest user retry with smaller --limit.

### Step 5.5: Deep Analysis Pass (Optional — for large repos)

For repos with 100+ issues, consider a 2-pass pipeline to maximize quality while controlling cost:

**Pass 1 (already done):** All issues analyzed with truncated bodies (default 500 chars). This gives preliminary scores.

**Pass 2 (optional deep dive):**
1. From the merged Pass 1 results, select the **top K issues** worth deeper analysis:
   - All Quick Wins (ROI ≥ 1.5, Difficulty ≤ 5, Trip ≤ 3, Arch ≤ 2, Action ≥ 4)
   - All Critical Bugs (type = "bug", Importance ≥ 8)
   - Top 20 by AdjustedScore that aren't in the above
   - Typical K: 50-80 issues
2. For each selected issue, read its full body from `{workdir}/issues.json` (untruncated)
3. Spawn a smaller set of agents (2-4) to re-analyze these issues with full context
4. For each selected issue, add `deepReason` (array of tags explaining why it entered Top K), e.g. `["critical_bug","quick_win","top20_score"]`
5. Merge Pass 2 results over Pass 1 results (Pass 2 overrides)

**When to use:** When `--limit` > 100 and accuracy matters. Skip for quick triage or small repos.

**When NOT to use:** When `--full-body` was already passed (bodies already at 2000 chars).

### Step 6: Categorize

From the merged results, categorize issues:

- **Quick Wins**: ROI ≥ 1.5 AND Difficulty ≤ 5 AND Trip ≤ 3 AND Arch ≤ 2 AND Actionability ≥ 4
- **Critical Bugs**: issueType = "bug" AND Importance ≥ 8
- **Tripping Issues**: Trip Score ≥ 4 (proceed with caution)
- **Over-Engineered**: Arch Score ≥ 4 (simpler solution likely exists)
- **Not Actionable**: Actionability ≤ 2 (questions/discussions/needs triage)

Sort all issues by AdjustedScore descending.

### Step 7: Present Results

Output a formatted report:

```
═══════════════════════════════════════════════════════════════
  ISSUE PRIORITIZATION REPORT
  Repository: {owner/repo}
  Filter: {filter} | Source: {source}
  Analyzed: {count} issues (via {N} agents, {W} wave(s))
  Excluded: {excluded} issues with existing PRs
  Batch size: {batchSize} | Truncation: {truncateChars} chars
  {IF diffMode: "Incremental: Reused {diffCached} cached scores | Re-analyzed {diffNew + diffModified} (new: {diffNew}, modified: {diffModified}) | Removed: {diffRemoved}"}
═══════════════════════════════════════════════════════════════

  Quick Wins: {n} | Critical Bugs: {n} | Tripping: {n} | Over-Engineered: {n} | Not Actionable: {n}

═══════════════════════════════════════════════════════════════
  TOP 10 BY ADJUSTED SCORE
═══════════════════════════════════════════════════════════════

  #123 [Adj: 3.50] ⭐ Quick Win
  Fix typo in README
  ├─ Difficulty: 1/10 | Importance: 4/10 | ROI: 4.00
  ├─ Trip: ✅ Total Sanity (1/5) | Arch: ✅ Surgical (1/5)
  ├─ Act: ✅ PR Ready (5/5) | Level: beginner
  └─ https://github.com/owner/repo/issues/123

  ...

═══════════════════════════════════════════════════════════════
  QUICK WINS (High Impact, Low Effort, Sane & Actionable)
═══════════════════════════════════════════════════════════════

  #123: Fix typo in README [Adj: 3.50]
        Difficulty: 1 | Importance: 4 | beginner

═══════════════════════════════════════════════════════════════
  RECOMMENDATIONS BY LEVEL
═══════════════════════════════════════════════════════════════

  BEGINNER (Difficulty 1-3, no security/architecture):
  - #123: Fix typo - Low risk, good first contribution

  INTERMEDIATE (Difficulty 4-6):
  - #456: Add validation - Medium complexity, clear requirements

  ADVANCED (Difficulty 7-10 or security/architecture):
  - #999: Refactor auth system - Architectural knowledge required

═══════════════════════════════════════════════════════════════
  CRITICAL BUGS (Importance ≥ 8)
═══════════════════════════════════════════════════════════════

  #111 [Adj: 1.67] 🔴 Critical
  App crashes on startup with large datasets
  ├─ Difficulty: 6/10 | Importance: 9/10 | ROI: 1.50
  ├─ Trip: ✅ (2/5) | Arch: ✅ (2/5) | Act: ⚠️ (3/5)
  └─ https://github.com/owner/repo/issues/111

═══════════════════════════════════════════════════════════════
  TRIPPING ISSUES (Trip ≥ 4 - Review Carefully)
═══════════════════════════════════════════════════════════════

  #999 [Trip: 🚨 5/5 - Tripping]
  Rewrite entire backend in Rust with blockchain storage
  ├─ Red Flags: "rewrite from scratch", "blockchain", over-engineering
  ├─ Adjusted Score: 0.12 (heavily penalized)
  └─ Consider: Is this complexity really needed?

═══════════════════════════════════════════════════════════════
  OVER-ENGINEERED (Arch ≥ 4 - Simpler Solution Likely Exists)
═══════════════════════════════════════════════════════════════

  #777 [Arch: 🏗️ 5/5 - Transformational]
  Add form validation
  ├─ Proposed: New validation framework with schema definitions
  ├─ Simpler Alternative: Single validation function, 20 lines
  └─ Ask: Why create a framework for one form?

  💡 TIP: Maintainers often reject PRs that change architecture
     unnecessarily. Always start with the simplest fix.

═══════════════════════════════════════════════════════════════
  NOT ACTIONABLE (Actionability ≤ 2)
═══════════════════════════════════════════════════════════════

  - #222: "How do I deploy to Kubernetes?" (Act: 1/5 - question)
  - #333: Duplicate of #111 (Act: 1/5 - duplicate)

═══════════════════════════════════════════════════════════════
  EXCLUDED - EXISTING PRs ({excluded} issues)
═══════════════════════════════════════════════════════════════

  #123: Login crashes on empty password
        └─ 🔗 PR #456: "Fix login validation" (github_link)
           https://github.com/owner/repo/pull/456

  #789: Add email validation
        └─ 🔑 PR #101: "Add form validation" (regex_keyword: fixes #789)
           https://github.com/owner/repo/pull/101

  Detection: 🔗 github_link | 🧩 partial_github_link | 🔑 regex_keyword

═══════════════════════════════════════════════════════════════
  SCALE LEGEND
═══════════════════════════════════════════════════════════════

  Trip (Solution Sanity):        Arch (Structural Impact):
  ✅ 1-2 = Sane                  ✅ 1-2 = Minimal change
  ⚠️  3  = Cautious              ⚠️  3  = Moderate
  🚨 4-5 = Risky                 🏗️ 4-5 = Over-engineered

  Actionability (PR-Ready):
  ✅ 4-5 = Ready for PR
  ⚠️  3  = Needs Investigation
  ❌ 1-2 = Not Actionable

  Adjusted Score = ROI × TripMultiplier × ArchMultiplier × ActionMultiplier
  Higher = Better (prioritize these first)

  🎯 SIMPLICITY PRINCIPLE: If a 10-line fix exists, a 200-line
     refactor is wrong. Always ask "is there a simpler way?"

═══════════════════════════════════════════════════════════════
  Performance: {N} agents, {W} wave(s), batch size {B}
  Mode: SKILL (read-only) - This shows info. YOU decide and act.
═══════════════════════════════════════════════════════════════
```

## Output Options

Command flags:
- `--json`: Output raw JSON data (merged from all agents)
- `--markdown` or `--md`: Output as markdown table
- `--quick-wins`: Show only quick wins section
- `--level beginner|intermediate|advanced`: Filter recommendations by level
- `--limit N`: Analyze N issues (default: 30)
- `--batch-size N`: Issues per batch (default: 20, keep 15-25 for quality)
- `--max-concurrency N`: Parallel agents per wave (default: 30)
- `--truncate N`: Body truncation in chars (default: 500)
- `--full-body`: Use 2000 char truncation for deeper analysis
- `--topic <keywords>`: Search issues by topic
- `--search <query>`: Raw GitHub search query
- `--label <name>`: Filter by GitHub label
- `--include-with-prs`: Include issues that already have open PRs
- `--history-dir <path>`: Persist runs in a stable location
- `--retain N`: Keep only latest N runs in history dir (0 = keep only current run)
- `--resume <run_id|path>`: Resume from an existing run without new fetch
- `--diff-from <ref>`: Incremental mode — fetch fresh issues, reuse cached scores for unchanged ones. `<ref>` = `latest`, run_id, or full path. Mutually exclusive with `--resume`.

## Important

- This is a **READ-ONLY** skill - never create PRs, write code, or modify repositories
- Present information objectively - let the user decide what to work on
- Flag "tripping" solutions but don't dismiss them outright - user has final say
- **Launch parallel agents in a SINGLE message** within each wave for maximum speed
- Each agent reads its batch file from disk — do NOT embed issue JSON in the agent prompt
- Always use **model: "sonnet"** for Task agents
- PR detection uses GitHub GraphQL `closingIssuesReferences` (primary) + regex fallback — no manual heuristics needed

## Example Usage

```
/issue-prioritizer anthropics/claude-code
/issue-prioritizer owner/repo --quick-wins
/issue-prioritizer owner/repo --level beginner
/issue-prioritizer owner/repo --limit 50
/issue-prioritizer owner/repo --limit 500 --batch-size 20
/issue-prioritizer owner/repo --limit 1000 --full-body
/issue-prioritizer owner/repo --json
/issue-prioritizer owner/repo --topic telegram
/issue-prioritizer owner/repo --search "label:bug in:title crash"
```
