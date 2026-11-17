# Quota Handling

ALWAYS call `GET /v1/user` and check both limits before creating or restoring a project:

- `data.quota.projects` — active (non-archived) project count vs limit
- `data.quota.storage` — bytes used by active projects vs limit

If `unlimited` is `true` for a resource, skip that check. Archived projects do NOT count toward either limit.

## When a Limit Is Reached

Error codes: `PROJECT_LIMIT_REACHED`, `STORAGE_LIMIT_REACHED`.

Follow this sequence in order. DO NOT skip steps or jump to "upgrade".

### Step 1 — Explain

Tell the user which limit they hit and their current numbers.
Example: "You've used 5 of 5 project slots. You need to free a slot before creating a new project."

### Step 2 — Offer to archive

List the user's active projects (`GET /v1/projects`). Ask which ones they no longer need active. Archive those via `actions/archive-project.md`. Then retry the original operation.

### Step 3 — Offer to replace

If the user wants to keep all projects active, offer to replace an existing project's content with the new files using `actions/replace-project.md`. This reuses the slot and URL.

### Step 4 — Suggest upgrade (last resort only)

Only after the user declines both Step 2 and Step 3, say:
"You can upgrade your plan at https://litehost.io/dashboard for more capacity."

## Golden Rule

Always keep the user moving forward. Never dead-end on a limit error.
