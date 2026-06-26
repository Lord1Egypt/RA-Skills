# Upstream Issue

Register feature requests or bug reports on external open-source repositories.

## When to Use

- When a dependency (provider, library, framework) lacks a needed feature
- When an upstream bug blocks your workflow
- When filing feature requests on third-party repos (e.g. `<vendor-org>/<provider>`)

## Procedure

### Step 1: Duplicate Check

Search for existing issues on the target repository:

```bash
GH_TOKEN="$(gh auth token --user <account>)" gh search issues --repo <owner>/<repo> "<keywords>" --json number,title,state --limit 20
```

| Result | Action |
|--------|--------|
| Exact match (OPEN) | Report URL to user. Do not create new issue |
| Exact match (CLOSED) | Check close reason. If wontfix/not-planned, report and stop. If fixed, verify the fix version |
| Similar but not exact | Note the similar issues in the draft for cross-reference |
| No match | Proceed to Step 2 |

### Step 2: Draft Issue

Write the issue draft to the artifacts folder:

```text
.ralph/docs/generated/issue-draft-upstream-<repo>-<slug>.md
```

**Draft structure** (English only — external repos are PUBLIC):

Metadata (repository, duplicate check, similar issues) is stored in **YAML frontmatter** to prevent accidental inclusion in the issue body when posting via `--body-file`.

```markdown
---
repository: <owner>/<repo>
title: "[Feature Request / Bug Report]: <concise title>"
duplicate_check: "No matching issues found (searched: '<keywords>')"
similar_issues: []  # or [123, 456]
---

## Description

<Clear description of the missing feature or bug>

## Current Behavior

<What happens now>

## Expected Behavior

<What should happen>

## Workaround (if any)

<Current workaround being used>

## Environment

- Provider/library version: <version>
- Relevant config: <minimal reproduction>
```

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|--------------------------|
| 1 | Put repository/duplicate-check in markdown body | Store in YAML frontmatter (`---` block) |
| 2 | Use `--body-file` with raw draft (frontmatter included) | Strip frontmatter before posting (Step 5) |
| 3 | Duplicate metadata in both frontmatter and body | Single source: frontmatter only |

### Step 3: Sanitize (MANDATORY)

Before presenting to user, apply `opensource.md` sanitization rules:

| Check | Action |
|-------|--------|
| Language = English | All content must be English (PUBLIC repo) |
| No internal IPs/hosts | Remove `<private-IP>`, `<internal-host>`, `<internal-project>` references |
| No user paths | Remove `/Users/*/`, `~/.claude/` paths |
| No internal tool names | Remove instance names of internal automation servers, identity providers, etc. |
| No UUIDs | Replace with generic placeholders |

### Step 4: User Review (MANDATORY — AskUserQuestion)

Present the draft and ask for approval:

```javascript
AskUserQuestion({
  question: "Upstream issue draft ready. Review and approve?",
  options: [
    { label: "Approve and create", description: "Create issue on <owner>/<repo>" },
    { label: "Edit first", description: "I'll modify the draft, then re-review" },
    { label: "Skip", description: "Don't create the issue" }
  ]
})
```

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|--------------------------|
| 1 | Create issue without AskUserQuestion | Always ask for approval before `gh issue create` |
| 2 | Post draft with Korean text to PUBLIC repo | English only — translate before posting |
| 3 | Include internal infra details in the issue | Generalize: "our Terraform setup", not "<automation-server> on <private-IP>" |
| 4 | Skip duplicate check | Always search first — duplicate issues annoy maintainers |

### Step 5: Create Issue

After approval, strip frontmatter and post body only:

```bash
# 1. Extract title from frontmatter
# 2. Strip frontmatter (everything between first --- and second ---) to get body-only content
# 3. Write body to temp file
# 4. Create issue with extracted title + body-only file

GH_TOKEN="$(gh auth token --user <account>)" gh issue create \
  -R <owner>/<repo> \
  --title "<title from frontmatter>" \
  --body-file <body-only-temp-file>
```

**Frontmatter stripping**: Read the draft file, extract content after the closing `---`, write to a temp file, use that as `--body-file`. The frontmatter metadata (repository, duplicate_check, similar_issues) must NOT appear in the posted issue body.

Report the created issue URL to the user.

### Step 5b: Update Existing Issue (when editing, not creating)

When the task is to **update an existing upstream issue** (not create a new one):

1. **Try `gh issue edit --body`** first
2. **If edit fails** (permission denied on external repo) → **STOP and AskUserQuestion**

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|--------------------------|
| 1 | Edit fails → auto-fallback to `gh issue comment` | Edit fails → AskUserQuestion with options: (a) post as comment, (b) post draft content in chat for user to paste, (c) skip |
| 2 | "Body edit impossible, so I'll comment instead" autonomous decision | User decides the fallback — comment on external repos is a permanent, visible action |
| 3 | Any `gh issue comment` on external repos without AskUserQuestion | `opensource.md` "GitHub Issue/PR Comment Ban" applies to ALL external repo write actions |

### Step 6: Record

- Add the upstream issue URL to `fix_plan.md` under the relevant BLOCKED item
- Update the BLOCKED status: `BLOCKED (upstream issue: <owner>/<repo>#N)`
