# Ticket Pipeline: Subagent Instructions

When dispatching a subagent to handle a ticket, include these instructions:

## Subagent Task Template

```
You are handling ticket <TICKET-ID> for <AGENT_NAME>.

**Issue:** <GITHUB_ISSUE_URL>
**Repo:** <LOCAL_REPO_PATH> (clone if missing)
**GitHub token:** Read GITHUB_TOKEN from workspace .env
**Git identity:** <BOT_NAME> <<BOT_EMAIL>>

## Step 1: Understand the ticket
- Fetch the full issue from GitHub API
- If there are screenshot URLs in the issue body, analyze them with the image tool
- Read the relevant files in the codebase to understand the context

## Step 2: Post analysis comment
Post a comment on the GitHub issue with:
- What the bug/feature is (from screenshots + description)
- Which files/components are affected
- Your proposed approach

## Step 3: Implement
- For TEST tickets (body contains "test" or no real bug described): make a trivial commit (add a comment line to a relevant file)
- For real tickets: implement the fix with tests
- Branch name: fix/<ticket-id>-<short-description> or feat/<ticket-id>-<short-description>
- Commit message: "fix: <description> (<TICKET-ID>)" or "feat: ..."

## Step 4: Open PR
- Push branch
- Open PR via GitHub API referencing the issue
- PR title: "<type>: <description> (<TICKET-ID>)"
- PR body: "Closes #<issue-number>\n\n<brief description of changes>"

## Step 5: Notify
- Write PR URL to memory/<ticket-id>-pr.txt
- Use sessions_send tool targeting label "main" with: "🏭 <TICKET-ID> PR ready: <PR_URL> — <one-line summary>"
- Output: PR_URL=<url>
```

## Repo Management

Clone repos on demand, keep them in `workspace/repos/<repo-name>`:

```bash
cd workspace/repos
git clone https://<BOT_USERNAME>:${GITHUB_TOKEN}@github.com/<ORG>/<REPO>.git
cd <REPO>
git config user.name "<BOT_NAME>"
git config user.email "<BOT_EMAIL>"
git remote set-url origin https://<BOT_USERNAME>:${GITHUB_TOKEN}@github.com/<ORG>/<REPO>.git
```

## State Tracking

Update `memory/support-tickets.json` after each dispatch:

```json
[
  {
    "ticket_id": "TD-0015",
    "email_from": "user@example.com",
    "issue_url": "https://github.com/org/repo/issues/2",
    "pr_url": "https://github.com/org/repo/pull/3",
    "status": "pr_open",
    "created_at": "2026-03-14T23:00:00Z"
  }
]
```

Status values: `dispatched` → `pr_open` → `merged`

TinyDesk (or equivalent) handles user-facing notifications on merge. No need to email the submitter.
