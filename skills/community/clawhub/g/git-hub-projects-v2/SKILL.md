---
name: github-projects-v2
description: "Manage GitHub Projects v2 using the `gh project` CLI. Use this skill when the agent needs to list backlog items, set project fields (status, iteration, priority, etc.). Requires `project` scope: run `gh auth refresh -s project` if commands fail with auth errors."
---

# GitHub Projects v2 Skill

## Auth prerequisite

```bash
gh auth status                  # verify scopes
gh auth refresh -s project      # add project scope if missing
```

> **ID note:** Most `gh project` commands take a project **number** (e.g. `1`) + `--owner`.
> `item-edit` is the exception — it requires `--project-id` with the GraphQL node ID (e.g. `PVT_xxx`).
> Get it with: `gh project list --owner <owner> --format json | jq '.projects[] | select(.number==1) | .id'`

---

## 1. List backlog items

```bash
# List all items (default 30, use --limit to raise)
gh project item-list <number> --owner <owner> --limit 100

# Filter by status — show only backlog
gh project item-list <number> --owner <owner> --query "status:Backlog"

# Filter open issues assigned to you
gh project item-list <number> --owner <owner> --query "assignee:@me is:issue is:open"

# JSON output for scripting
gh project item-list <number> --owner <owner> --format json \
  | jq '.items[] | {id, title, status}'
```

---

## 2. Set fields on an item (status, iteration, priority, etc.)

`item-edit` requires the project node ID and item node ID — both available from `item-list --format json`.

```bash
# Get project node ID
PROJECT_ID=$(gh project list --owner <owner> --format json \
  | jq -r '.projects[] | select(.number==<number>) | .id')

# Get item IDs and current field values
gh project item-list <number> --owner <owner> --format json | jq '.items[]'

# Get field IDs and option IDs (needed for single-select and iteration fields)
gh project field-list <number> --owner <owner> --format json | jq '.fields[]'

# Set a single-select field (e.g. Status, Priority)
gh project item-edit --project-id $PROJECT_ID --id <item-node-id> \
  --field-id <field-node-id> --single-select-option-id <option-id>

# Set an iteration field (e.g. Sprint)
gh project item-edit --project-id $PROJECT_ID --id <item-node-id> \
  --field-id <field-node-id> --iteration-id <iteration-id>

# Set a date field
gh project item-edit --project-id $PROJECT_ID --id <item-node-id> \
  --field-id <field-node-id> --date "2025-12-31"

# Set a number field (e.g. Story Points)
gh project item-edit --project-id $PROJECT_ID --id <item-node-id> \
  --field-id <field-node-id> --number 5

# Clear any field value
gh project item-edit --project-id $PROJECT_ID --id <item-node-id> \
  --field-id <field-node-id> --clear
```

---

## 3. Add a comment to an issue

```bash
# Add a comment (issue number, not project item ID)
gh issue comment <issue-number> --repo <owner>/<repo> --body "Your comment here"

# From a file
gh issue comment <issue-number> --repo <owner>/<repo> --body-file comment.md
```

---

## 4. Create an issue and add it to the project

```bash
# Create issue in a repo
ISSUE_URL=$(gh issue create \
  --repo <owner>/<repo> \
  --title "Fix login timeout" \
  --body "Users are being logged out after 5 minutes." \
  --assignee "@me" \
  --label "bug")

# Add the new issue to the project
gh project item-add <number> --owner <owner> --url "$ISSUE_URL"
```

---

## 5. Create a sub-issue

Native `gh issue` doesn't support sub-issues yet. Use the `gh-sub-issue` extension:

```bash
# Install once
gh extension install yahsan2/gh-sub-issue

# Create a new issue as a sub-issue of an existing parent
gh sub-issue create --parent <parent-issue-number> \
  --repo <owner>/<repo> \
  --title "Implement login endpoint" \
  --body "POST /api/login"

# Link an existing issue as a sub-issue of a parent
gh sub-issue add <parent-issue-number> <child-issue-number> --repo <owner>/<repo>

# List sub-issues of a parent
gh sub-issue list <parent-issue-number> --repo <owner>/<repo>
```

If the extension is not available, fall back to GraphQL:

```bash
gh api graphql -f query='
  mutation($parentId: ID!, $childId: ID!) {
    addSubIssue(input: { issueId: $parentId, subIssueId: $childId }) {
      issue { number title }
      subIssue { number title }
    }
  }
' -F parentId=<parent-node-id> -F childId=<child-node-id>
```
