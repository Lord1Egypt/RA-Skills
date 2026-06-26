# Issue Dependencies & Sub-issues

Manage GitHub native **Issue Relationships**: blocked-by / blocking dependencies AND parent-child (sub-issue) hierarchies. Uses `addBlockedBy` / `removeBlockedBy` for sequential dependencies and `addSubIssue` / `removeSubIssue` for hierarchical breakdown.

## When to Use

- After creating issues in a multi-issue feature chain that has a clear sequential order
- After confirming a plan (e.g., `code-workflow` step 2) where downstream issues exist
- Before starting work on an issue — verify all blocked-by predecessors are resolved
- Before merging a PR — verify the issue's blockedBy is empty (or all resolved)
- **After concluding a PR/issue priority order in chat** — when analysis lands on "X must merge before Y" (file overlap, base-branch typecheck regression, base dependency, etc.), immediately apply `addBlockedBy(issueId=Y, blockingIssueId=X)`. The chat conclusion is itself the explicit trigger — do not wait for the user to say "please apply the block now"

### PR-PR Dependencies (HARD STOP — native unsupported, must use a workaround)

**GitHub Issue Dependencies is Issue-only.** The `PullRequest` type has no `blockedBy` / `blocking` fields, and the `addBlockedBy` mutation returns `Field 'blockedBy' doesn't exist on type 'PullRequest'` against PR node IDs. Verification:

```bash
gh api graphql -f query='query { repository(owner:"<o>", name:"<r>") {
  issueOrPullRequest(number:<PR#>) { __typename ... on PullRequest { blockedBy(first:1) { nodes { number } } } }
} }'
# → undefinedField error
```

Therefore, PR-to-PR dependencies are expressed via:

| Method | When to apply | Effect |
|--------|---------------|--------|
| (A) Add a `## Depends on\n- #<upstream>` section in the downstream PR body + a "rebase after #N merge" note in the Test Plan | Merge-order dependency between PRs that share the same base (both target main) | GitHub UI shows cross-links automatically + reviewer sees the order |
| (B) Set the downstream PR's base to the upstream PR's head (Stacked PRs) | When the dependent code itself is required (working on top of upstream changes) | GitHub auto-rebases when the base merges |
| (C) Set `addBlockedBy` on a shared tracking issue (each PR closes that issue) | Multiple PRs implementing one issue in parts | Uses the issue's Relationships panel |

**For this trigger case (priority conclusion), choosing the medium requires AskUserQuestion** — let the user choose between "(A) body cross-link only is enough" and "(C) create a new tracking issue then register native blocked-by". (B) applies only when there is a code dependency.

| Option | Effect | Cost |
|--------|--------|------|
| (A) `## Depends on` in the downstream PR body | Reviewer sees it in the body + GitHub timeline cross-link | 0 (text only). Not searchable / filterable |
| (C) Shared tracking issue (may be newly created) — create the tracking issue with `gh issue create`, then call `Issue.addBlockedBy` | Native blocked-by displayed in GitHub Relationships panel + searchable / dashboard visible | 1–2 extra issues |

**Self-check (right after a PR-PR priority conclusion)**: if option (C) is feasible, **emit an AskUserQuestion that defaults to recommending (C)**. Do not silently apply (A) only — keep (A) alone only when the user picks "body is enough". Because of the `git.md` "do not autonomously create issues" rule, the (C) issue creation must wait for explicit user approval.

| # | Don't | Do |
|---|-------|-----|
| 1 | Assume without verifying that "PRs are Issue nodes so `addBlockedBy` works" and call the mutation | Run a Step 2 query first to confirm `__typename` and `blockedBy` field existence. If it is a PR, branch into (A) / (B) / (C) |
| 2 | Report the priority conclusion in chat without applying it to GitHub state | The conclusion is itself the call trigger. In the same response turn, update the (A) PR body or invoke (C) `addBlockedBy` on the issue |
| 3 | Over-apply the "scope discipline" rule with "the user did not explicitly ask, so I'll defer" | Fact analysis implies applying the result to GitHub. Scope discipline forbids adding **new work** the user did not ask for, NOT applying the **answer** that was concluded |

**Self-check (every time, right before reporting a PR/issue priority conclusion)**:
1. Does the report text contain priority words such as "merge X first", "Y blocked by X", "X → Y rebase is natural"?
2. If yes → check the node type → if Issue, invoke Step 2 → 3 → 4; if PR, branch (A)/(B)/(C) and execute
3. Include the call result (URL or PR number) on the last line of the report

## GitHub Issue Dependencies (Native Feature)

GitHub Issues exposes the following GraphQL fields for issue-level dependencies:

| Field | Description |
|-------|-------------|
| `Issue.blockedBy` | Issues that block this one (must complete first) |
| `Issue.blocking` | Issues that this one blocks |
| `Issue.issueDependenciesSummary` | `{ totalBlockedBy, totalBlocking }` summary counts |
| `Issue.duplicateOf` | Duplicate-of relationship |

UI display: Issue detail page → **Relationships** panel → "Blocked by" / "Blocking" sections.

This is distinct from:
- **Sub-issues** (`Issue.subIssues` / `Issue.parent`) — hierarchical parent-child, used for breaking down a large issue into smaller ones
- **GitHub Projects v2 Dependencies** — Project-scoped, requires Project board setup
- **Cross-references** (timeline `CrossReferencedEvent`) — auto-generated from `#N` mentions in body/comments, no semantic meaning

### Avoid confusing Sub-issue vs Blocked-by (HARD STOP)

| Relationship | Meaning | Direction | Example |
|--------------|---------|-----------|---------|
| **sub-issue** | A is a sub-task of B (containment) | A.parent = B | #306 (environment fix) is a sub-issue of #283 (E2E automation) |
| **blocked-by** | A cannot start until B finishes (sequential) | A.blockedBy = [B] | #282 (test hardening) starts only after #255 (redirect normalization) completes |

**Never set parent blocked-by on a sub-issue**: if sub-issue A is set as blocked-by on parent B, a circular contradiction results — B's completion needs A, and A's start needs B's completion. The sub-issue relationship already expresses containment; a separate blocked-by is unnecessary.

| # | Don't | Do |
|---|-------|-----|
| 1 | Set a sub-issue as blocked-by on its parent | Keep only the sub-issue relationship; do not set blocked-by |
| 2 | Mechanically convert "below in the diagram" to "blocked-by" | Decide the relationship type first (containment vs sequence), then set only the appropriate relationship |

## Procedure

### Step 1: Source the Dependency Map

Identify the chain to apply. Two valid sources:

| Source | When | Format |
|--------|------|--------|
| `code-workflow` plan frontmatter | Plan was written with explicit `blocked_by` matrix | YAML `chain:` array |
| ad-hoc text instruction | User describes the chain in conversation | Build matrix from conversation |

Plan frontmatter example:

```yaml
---
plan: <name>
chain:
  - issue: 282
    blocked_by: [255]
  - issue: 253
    blocked_by: [282]
---
```

### Step 2: Fetch Issue Node IDs

GraphQL `addBlockedBy` requires GitHub node IDs (not issue numbers). Fetch in one query:

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql -f query='
  query {
    repository(owner:"<owner>", name:"<repo>") {
      i255: issue(number:255) { id }
      i282: issue(number:282) { id }
      i253: issue(number:253) { id }
    }
  }
'
```

Save IDs into the plan frontmatter `node_ids:` map for reuse.

### Step 3: Inspect Existing Dependencies

Before adding, query the current state to avoid duplicate mutations:

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql -f query='
  query {
    repository(owner:"<owner>", name:"<repo>") {
      issue(number: <N>) {
        blockedBy(first:10) { nodes { number title } }
        blocking(first:10) { nodes { number title } }
        issueDependenciesSummary { totalBlockedBy totalBlocking }
      }
    }
  }
'
```

Compare with the desired matrix → identify only the missing relationships.

### Step 4: Add Dependencies (one at a time, sequentially)

For each missing relationship, run `addBlockedBy`:

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql \
  -f query='mutation($issueId:ID!,$blockingIssueId:ID!) {
    addBlockedBy(input:{issueId:$issueId, blockingIssueId:$blockingIssueId}) {
      issue { number issueDependenciesSummary { totalBlockedBy } }
    }
  }' \
  -f issueId="<TARGET_ID>" \
  -f blockingIssueId="<BLOCKING_ID>"
```

- `issueId`: the issue being blocked (downstream)
- `blockingIssueId`: the issue that blocks (upstream)

**Do not repeatedly call external APIs** — apply 1 at a time, verify response, get user confirmation before next.

### Step 5: Verify

After applying, re-query Step 3 → confirm `blockedBy` matches the plan's `blocked_by` array.

```bash
for N in <list of issue numbers>; do
  GH_TOKEN="$(gh auth token --user <account>)" gh api graphql \
    -f query="query { repository(owner:\"<owner>\", name:\"<repo>\") { issue(number:$N) { blockedBy(first:5) { nodes { number } } } } }"
done
```

UI verification: open each issue page → Relationships panel → confirm "Blocked by" lists the predecessors.

## Sub-issue Management (Parent-Child Hierarchy)

GitHub Issues supports native **sub-issue** relationships via `addSubIssue` / `removeSubIssue` GraphQL mutations and `Issue.subIssues` / `Issue.parent` query fields.

**Sub-issue ≠ Blocked-by**: Sub-issues represent hierarchical breakdown (A is part of B), NOT sequential dependency (A must finish before B starts). See the "Avoid confusing Sub-issue vs Blocked-by" table above.

### When to Use Sub-issues

| Scenario | Use Sub-issue? | Example |
|----------|---------------|---------|
| Task is a sub-task of a larger Epic/Issue | **Yes** | #314 (translate permissions list) is a sub-issue of #343 (user management feature) |
| Multiple small tasks compose one feature | **Yes** | Break #200 (SSO integration) into #201, #202, #203 |
| Task must finish before another starts | **No** — use blocked-by | #255 must complete before #282 starts |

### Sub-issue Procedure

#### Step S1: Identify Parent and Child Issue Node IDs

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql -f query='
  query {
    repository(owner:"<owner>", name:"<repo>") {
      parent: issue(number:<PARENT_NUMBER>) { id }
      child: issue(number:<CHILD_NUMBER>) { id }
    }
  }
'
```

#### Step S2: Check Existing Sub-issues

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql -f query='
  query {
    repository(owner:"<owner>", name:"<repo>") {
      issue(number:<PARENT_NUMBER>) {
        subIssues(first:20) { nodes { number title state } }
        subIssuesSummary { total completed percentCompleted }
      }
    }
  }
'
```

If the child issue already appears in `subIssues.nodes`, skip Step S3.

#### Step S3: Add Sub-issue

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql \
  -f query='mutation($parentId:ID!,$childId:ID!) {
    addSubIssue(input:{issueId:$parentId, subIssueId:$childId}) {
      issue { number subIssuesSummary { total completed percentCompleted } }
      subIssue { number title }
    }
  }' \
  -f parentId="<PARENT_NODE_ID>" \
  -f childId="<CHILD_NODE_ID>"
```

- `issueId` (parentId): the parent issue that contains the sub-issue
- `subIssueId` (childId): the issue to add as a sub-issue

#### Step S4: Verify

Re-query Step S2 → confirm the child appears in `subIssues.nodes`.

### Remove Sub-issue

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql \
  -f query='mutation($parentId:ID!,$childId:ID!) {
    removeSubIssue(input:{issueId:$parentId, subIssueId:$childId}) {
      issue { number subIssuesSummary { total } }
      subIssue { number }
    }
  }' \
  -f parentId="<PARENT_NODE_ID>" \
  -f childId="<CHILD_NODE_ID>"
```

### Sub-issue Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Add only a `- #N` text link in the body and call "sub-issue registration done" | Create the native relationship via the `addSubIssue` GraphQL mutation |
| 2 | Update only the parent body after `gh issue create` | `gh issue create` → `addSubIssue` → update parent body (all three steps are required) |
| 3 | Substitute Sub-issue for blocked-by | Sub-issue = containment (A is part of B). Blocked-by = sequence (B before A). Do not mix |

## Removal

To remove an incorrect blocked-by relationship:

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql \
  -f query='mutation($issueId:ID!,$blockingIssueId:ID!) {
    removeBlockedBy(input:{issueId:$issueId, blockingIssueId:$blockingIssueId}) {
      issue { number }
    }
  }' \
  -f issueId="<TARGET_ID>" \
  -f blockingIssueId="<BLOCKING_ID>"
```

## Pre-merge Check (Integration with merge.md)

Before squashing/merging a PR, verify the linked issue's `blockedBy` is empty or all resolved:

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh api graphql -f query='
  query { repository(owner:"<owner>", name:"<repo>") {
    issue(number:<N>) {
      blockedBy(first:10) { nodes { number state title } }
    }
  } }
'
```

If any node has `state: OPEN`, **block the merge** and report the predecessor issue. The merge of the dependent should wait until predecessors are CLOSED.

## Auto-population from `code-workflow` Plan

When `code-workflow/steps.md` step 3 (User Review) generates a plan with downstream work, the plan frontmatter should declare `chain:` and `blocked_by:`. After plan approval, the dependencies topic procedure applies the chain to GitHub.

```text
code-workflow plan (frontmatter chain:)
  └─→ github-flow/dependencies (Step 2-4: apply to GitHub)
        └─→ github-flow/merge (Step 5: pre-merge blockedBy check)
```

## Don't / Do

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|--------------------------|
| 1 | Use `Closes #N` / `Fixes #N` keywords for issue-issue blocking | These work only for PR → issue. Use `addBlockedBy` for issue → issue |
| 2 | Manually write `## Blocked by\n- #N` in issue body | Issue body markdown is not parsed by GitHub for dependencies. Use `addBlockedBy` so it appears in the Relationships panel |
| 3 | Add 5+ dependencies in a single bash for-loop | API rate limit + abuse detection. Apply 1 at a time with user confirmation |
| 4 | Skip Step 3 (existing dependencies query) | `addBlockedBy` is idempotent but wastes API calls. Always query first |
| 5 | Use Sub-issues for sequential blocking | Sub-issues = hierarchical breakdown, not blocking. Use blockedBy for "must complete X before Y" |
| 6 | Hardcode issue node IDs in conversation | IDs change across forks/clones. Always fetch via Step 2, store in plan frontmatter |
| 7 | Add only a `- #N` text link in the body and declare "sub-issue done" | Create the native relationship via the `addSubIssue` mutation. Body links are a supplement |
| 8 | Update only the parent body after `gh issue create` | `gh issue create` → `addSubIssue` → update parent body (all three steps required) |

## Rules

- **Default off for creation-time auto-application**: Do NOT auto-apply `addBlockedBy` on every issue/PR creation. Apply only on these triggers:
  - User explicitly requests blocked-by application
  - Plan with `chain:` frontmatter exists
  - **Chat-time priority conclusion** (PR-PR or issue-issue ordering decided in the current conversation) — apply immediately, same turn as the conclusion report
- **PR repo language**: Same as plan-to-issue.md — GraphQL mutations don't post text, but if the dependency check is reported in fix_plan or PR comments, apply Korean/English rules per repo visibility.
- **fix_plan reflection only**: For local-only tracking without GitHub UI changes, record the dependency map in plan frontmatter and reference from fix_plan.md. Skip Step 4 (no `addBlockedBy` calls).

## Related

- `plan-to-issue.md` — issue body/comment management. Dependencies are separate from body content
- `merge.md` — Step 5 pre-merge check uses Step 3 query
- "Do not repeatedly call external APIs" principle — applied to Step 4 (1 at a time, confirm before next)
