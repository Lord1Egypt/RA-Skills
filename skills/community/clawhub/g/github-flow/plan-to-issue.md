# Plan to Issue

Convert plan/research MD files into GitHub issue body or comments.

## When to Use

- After code-workflow step 2 (plan) to register the plan as a GitHub issue
- When a plan file needs to be shared with the team via GitHub
- When discussion items need to be posted as issue comments

## Procedure

### Step 1: Read Source Material

Read the plan/research file and identify:
- Implementation checklist items
- Verification/test plan
- Open questions / discussion items
- Changed file list

### Step 2: Classify Content → Body vs Comment

| Content | Target | Format |
|---------|--------|--------|
| Implementation checklist | Body | `- [ ]` checkbox list |
| Verification plan | Body | Table: feature / procedure / expected result |
| Changed file summary | Body | Table: file / change description |
| Open questions (undecided items) | **Comment** | Numbered list with context |
| Progress updates | **Comment** | Timestamped note |

### Step 3: Sanitize Internal Paths

**Before writing to GitHub**, strip all internal paths:

| Pattern to Remove | Replacement |
|-------------------|-------------|
| `.ralph/docs/generated/plan-*.md` | (remove entirely or replace with inline content) |
| `.ralph/docs/generated/research-*.md` | (remove entirely) |
| `.ralph/fix_plan.md` | (remove entirely) |
| `.omc/plans/*.md` | (remove entirely) |
| Session IDs, timestamps from fix_plan | (remove entirely) |

### Step 4: Ensure Verification Plan

If the source material lacks a verification plan, **add one before posting**.

Template:
```markdown
### Verification
| Feature | Procedure | Expected Result |
|---------|-----------|-----------------|
| ... | ... | ... |
```

This is a hard requirement — do not post an issue body without verification.

### Step 5: Enforce English for Public Repos

```bash
gh repo view --json isPrivate -q '.isPrivate'
```

If `false` (public repo):
1. **All text must be English** — title, body, comments. No exceptions.
2. If source material (Logseq, fix_plan, plan.md) is in Korean, **translate to English** before posting.
3. Scan the final body for Hangul characters (Unicode range U+AC00 to U+D7A3 — use `grep -P '\p{Hangul}'`). If found, translate before `gh issue create/edit`.
4. **HARD STOP — Hangul detection is a blocking error**: if `grep -P '\p{Hangul}'` matches the prepared body or title, **abort `gh issue create/edit` immediately** and report `BLOCKED: Hangul characters found in PUBLIC repo content` to fix_plan. Do not "translate-as-you-write" — produce a fully translated draft first, scan, then post.
5. **Hangul scan command**:
   ```bash
   echo "$BODY" | grep -P '\p{Hangul}' && echo "BLOCKED: Hangul detected" || echo "OK: English only"
   ```
   Run this for both `--title` and `--body` before posting.
6. **Ralph autonomous mode applies same rule** — no exception for autonomous loops; this rule overrides any `--no-confirm` or speed pressure.

### Step 5.1: Match Repository Language Convention for Private Repos

If `true` (private repo):
1. Inspect the language of existing issue titles:
   ```bash
   gh issue list --limit 5 --json title -q '.[].title'
   ```
2. **If existing issues are in Korean, write Korean**; if English, write English.
3. If no existing issues, follow the language of the repository's README / CLAUDE.md.

### Step 5.5: PUBLIC repo personal data sanitization (CRITICAL — HARD STOP)

**On PUBLIC repos, run personal-data verification immediately after the English check.** An issue body is permanently recorded on GitHub once posted, so user environment information, unrelated project data, or real identifiers must not be included.

**Forbidden patterns (HARD STOP — abort posting on detection)**:

| Pattern | Example | Replacement |
|---------|---------|-------------|
| UUID v4 (real session / resource ID) | `<uuid-v4>` | `"session-id"`, `"abc-1234-..."` (placeholder) |
| User home path | `/Users/<name>/...`, `/home/<name>/...` | `~/`, `/home/user/` |
| User-environment tool names | file-sync daemon, dotfile manager, version manager, journal app, git GUI | generic terms (e.g. "file synchronization", "version manager") |
| Tools / services from other projects | unrelated identity providers, automation servers, secret stores, cloud accounts, edge CDNs | remove — irrelevant to this issue |
| Internal host / IP | `<private-IP>`, internal hostnames, internal project codenames | generic phrasing or remove |
| Real metrics extracted from user data | "5496 lines, 4208 unique UUIDs" | "hundreds or thousands of records" |
| Real file paths from user data | `<uuid>.jsonl` | "test fixture file" |
| User-environment narration ("in my session", "in my environment") | "across different cwd's" | generic scenario description |

**Sanitization verification commands** — caller supplies the keyword sets and host prefixes used in their environment via env vars (e.g. `PII_TOOL_KEYWORDS`, `PII_INTERNAL_HOST_RE`):

```bash
# UUID v4
echo "$BODY" | grep -P '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}' && echo "BLOCKED: UUID detected"

# User path
echo "$BODY" | grep -E '/Users/[a-z]+|/home/[a-z]+' && echo "BLOCKED: user path detected"

# External tool names (substitute the keyword set from your environment)
echo "$BODY" | grep -iE "${PII_TOOL_KEYWORDS:-<tool-keyword-set>}" && echo "BLOCKED: external tool name"

# Internal IP / host (substitute the prefix set from your environment)
echo "$BODY" | grep -E "${PII_INTERNAL_HOST_RE:-<internal-host-prefix>}" && echo "BLOCKED: internal hostname/IP"
```

If any of the four commands matches, **HARD STOP** — abort `gh issue create/edit`, remove the offending data from the body, and retry.

**Principles**:
- Every example / number / name in the issue body must be **public-safe, transformed data**.
- Even for a bug found in your own session/environment, **write the reproduction scenario in generalized form** (e.g. "build a fixture to reproduce" instead of citing a specific UUID or statistic).
- Debugging notes like "this happened in my environment" are allowed only at the issue-draft stage. Sanitize before posting.

**Ralph autonomous mode applies the same rule**: the sanitization HARD STOP must not be bypassed even in autonomous loops.

### Step 6: Post to GitHub

**If issue already exists** (`gh issue view <number>`):
1. Body update: `gh issue edit <number> --body "..."`
2. Discussion comment: `gh issue comment <number> --body "..."`

**If issue needs creation**:
1. `gh issue create --title "..." --body "..."`
2. Follow up with discussion comment if needed

### Step 7: Suggest Milestone

After issue creation/update, suggest a Milestone based on existing milestones:

```bash
gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.state=="open") | "\(.title)\t\(.description)"'
```

Present open milestones via **AskUserQuestion** and apply:

```bash
gh issue edit <NUMBER> --milestone "<selected>"
```

If no milestone fits, skip — do not create new milestones without user instruction.

### Step 7.5: Allocation verification — show the reconciliation table to the user (REQUIRED)

**After every issue update is complete, emit a reconciliation table to prove that every source item was allocated:**

```markdown
| ID | Scenario | Issue | Status |
|----|----------|-------|--------|
| A1 | ... | #222 | ✅ |
| B1 | ... | #282 | ✅ |
| ... | ... | ❌ MISSING | — |
```

- List **every** item from the source material (research / plan).
- Show which issue each item landed in.
- **If any item is missing, add it to the corresponding issue immediately** — do not report "complete".
- The user must be able to read this table and confirm nothing was dropped.

**Forbidden**: reporting "complete" after issue updates without producing the reconciliation table.

### Step 8: Post-publish tracking — record the draft → issue mapping (CRITICAL)

**Immediately after `gh issue create` or `gh issue edit`, record traceability information in two places.** If the mapping is lost after posting, the next session may republish the same draft, or you may lose track of which issue came from which draft.

**8-1. Append the mapping to the issue-draft file's YAML frontmatter**:

Issue draft files must store metadata in a top-level **YAML frontmatter (`---`)** block. When posting completes, add or update the `posted_to` field.

```yaml
---
title: "Allowlist release-please bot PRs in block-merge-without-review hook"
labels:
  - enhancement
repo: es6kr/skills
posted_to: "https://github.com/es6kr/skills/issues/36"
---
```

When an existing issue is overwritten via `edit`, include a string or URL list in `posted_to` of the form `Overwrote Issue #N (originally created from <other-draft>.md, YYYY-MM-DD)`.

**8-2. Update the `Issue Drafts` section entry in `fix_plan.md`**:

Existing format:
```markdown
- [BLOCKED] Handle duplicate message UUIDs — `web-each-key-duplicate.md`
```

Format after posting:
```markdown
- [BLOCKED] Handle duplicate message UUIDs — `web-each-key-duplicate.md` → **Issue #N** (posted YYYY-MM-DD)
```

**Add the entry if it does not already exist in the Issue Drafts section.** If it exists, only append the `→ Issue #N (date)` segment.

**8-3. Verification commands**:

```bash
# Is the posted_to field present in the draft's frontmatter?
grep -E "^posted_to:[[:space:]]*" .ralph/issue-drafts/<draft>.md

# Is the → Issue #N mapping recorded in fix_plan?
grep -E "<draft>\.md.*→ \*\*Issue #" .ralph/fix_plan.md
```

Both commands must match for Step 8 to be complete. If only one matches, it is incomplete — add the missing record immediately.

**Forbidden**:
- Reporting "issue posted" without recording the mapping.
- Updating only the draft file while leaving fix_plan unchanged (or vice versa).
- "I'll do it later, it's minor" — the mapping is already lost by the next session.

### Step 9: Update fix_plan

After posting, update the corresponding fix_plan entry:
- Add issue number reference
- Remove BLOCKED if it was "pending plan review"

## Example

### Input: plan-183-user-access-log.md

Contains:
- Implementation: `recordSystemLog` util + 6 routes
- Verification: 2 test cases
- Open question: none

### Output

**Issue #183 body update** (via `gh issue edit 183 --body "..."`):
```markdown
## Implementation Plan
- [ ] Create `lib/system-log.ts` with `recordSystemLog()`
- [ ] Add log calls to 6 user/authority CRUD routes

## Verification
| Feature | Procedure | Expected |
|---------|-----------|----------|
| CRUD logging | Create user → check /api/system-log | Log entry with INFO level |
| Level filter | Query system-log with level param | Filtered results |
```

(No `.ralph/docs/` paths, no session IDs)

## Rules

- **Use YAML Frontmatter for Draft Metadata**: All draft files MUST start with a YAML frontmatter block (`---`) containing `title`, `labels`, `repo`, and optional `posted_to`. This keeps metadata clean and separated from the markdown body.
- **Issue title must be descriptive prose** — conventional-commit prefixes are forbidden (applies from draft authoring time, not only right before posting).
- **H1 is FORBIDDEN in issue drafts** — the title must be defined only via the YAML frontmatter `title:` field. Do not add an H1 in the body (creates duplication and pollutes `--body-file`).
- **Verification plan required** — do not post an issue body without a Verification section (Step 4)
- **Sanitize internal paths** before posting (Step 3)

### Draft File Format (HARD STOP — applies from draft file creation)

**Issue draft files must follow the structure below:**

```markdown
---
title: "Unit tests for session search phase 1 and 2"
labels:
  - testing
repo: es6kr/claude-code-sessions
---

### Problem
...
```

| # | Don't | Do |
|---|-------|-----|
| 1 | `# Issue Draft: Add unit tests for searchSessions` (using H1 as the body title) | Put the title only in the YAML `title:` field; no H1 in the body |
| 2 | `title: "test(core): add unit tests..."` (contains commit prefix) | `title: "Unit tests for session search phase 1 and 2"` |
| 3 | `title: "feat(web): add retry logic"` | `title: "Add retry logic for API calls"` |
| 4 | `title: "fix: handle duplicate UUIDs"` | `title: "Handle duplicate message UUIDs in Svelte MessageList"` |

**Self-check (right after authoring a draft file, every time):**
1. Is there an H1 (`# ...`) in the body? → Move it into the `title:` field and delete the H1 line.
2. Does the `title:` value contain a conventional-commit prefix (`fix(`, `feat(`, `test(`, `chore:`, `refactor:`, ...)? → Remove it and rewrite as prose.
3. Does the `title:` value describe "what it does / what the problem is"?

### Issue Title Format (HARD STOP — self-check right before `gh issue create/edit`)

| # | Don't | Do |
|---|-------|-----|
| 1 | `fix(authentik): migrate media storage` | `Migrate Authentik media storage from /media to /data` |
| 2 | `feat(web): add retry logic` | `Add retry logic for API calls` |
| 3 | `chore: update dependencies` | `Update dependencies` |
| 4 | `test(core): add unit tests for searchSessions` | `Unit tests for session search phase 1 and 2` |

**Self-check (right before `gh issue create/edit`, every time):**
1. Does the title contain a conventional-commit prefix (`fix(`, `feat(`, `test(`, `chore:`, ...)? → Remove it.
2. On a private repo, did you use a language different from the repository's convention? → See Step 5.1.
3. Does the title describe "what it does" in prose form?
