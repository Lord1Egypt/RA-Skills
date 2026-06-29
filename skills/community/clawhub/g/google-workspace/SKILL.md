---
name: google-workspace
description: Plan, audit, and safely execute Google Workspace admin, Gmail, Calendar, Drive, Groups, and user lifecycle work. Use when Codex is asked to help with Workspace migrations, account cleanups, permission audits, group rollouts, mailbox/calendar changes, or API/GAM/gcloud command planning.
---

# Google Workspace

Use this skill to turn Google Workspace administration requests into safe,
reviewable plans and commands. Default to read-only discovery before proposing
changes, and keep destructive operations behind explicit confirmation.

## Workflow

1. Identify the workspace surface: Admin Directory, Gmail, Calendar, Drive,
   Groups, Vault, or shared drives.
2. Establish the actor and auth path: browser admin console, `gam`, `gcloud`,
   service account with domain-wide delegation, or direct Google API calls.
3. Gather read-only evidence first:
   - affected users, groups, aliases, calendars, labels, drives, or files
   - current ownership and permission state
   - exact scope of change and rollback path
4. Produce a preview plan with commands or API calls marked as `read`,
   `proposed write`, or `rollback`.
5. Ask for approval before any write, delete, transfer, suspend, archive, or
   sharing-change operation.

## Command Guidance

Prefer commands that can be copied and audited. Use placeholders for domains,
users, groups, and file IDs until the user provides real values.

For `gam`, prefer patterns like:

```bash
gam info user user@example.com
gam print groups member user@example.com
gam print drivefileacls query "owner = 'user@example.com'"
```

For `gcloud`, first confirm the active project and account:

```bash
gcloud config list account project
gcloud auth list
```

For direct API calls, name the API, HTTP method, endpoint, required OAuth scope,
and dry-run/read-only equivalent when one exists.

## Safety Rules

- Never invent customer domains, user emails, group names, file IDs, or org-unit
  paths.
- Treat suspended users, external sharing, delegated mailboxes, super-admin
  accounts, Vault holds, and shared drive ownership as high-risk.
- Before bulk changes, generate a CSV or JSON input schema and a rollback
  export.
- For deletions, prefer suspend/archive/transfer workflows unless the user has
  explicitly requested irreversible deletion.
- For mail/calendar migrations, separate identity mapping, data transfer,
  delegation, forwarding, and retention policy steps.

## Reusable Resources

- Read `references/scopes.md` when selecting API scopes or explaining OAuth
  permissions.
- Run `scripts/workspace-change-plan.mjs <input.json>` to turn a small JSON
  change set into a Markdown rollout checklist.

Example input:

```json
{
  "title": "Sales group cleanup",
  "owner": "admin@example.com",
  "changes": [
    {
      "kind": "group-membership",
      "target": "sales@example.com",
      "action": "remove stale members",
      "risk": "medium",
      "rollback": "restore exported membership CSV"
    }
  ]
}
```
