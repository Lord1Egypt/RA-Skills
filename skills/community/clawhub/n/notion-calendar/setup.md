# Setup - Notion Calendar

If `~/notion-calendar/` does not exist or is empty, start with transparent onboarding. Explain which local files may be created, what data goes to Notion, and ask for confirmation before writing local memory.

## Your Attitude

Be operational and calm. Answer the immediate calendar question first when possible, then tighten the setup around real usage instead of turning the conversation into a form.

## Priority Order

### 1. First: Integration and Activation

In the first exchanges, clarify:
- Whether this should activate whenever the user asks about a Notion calendar, content calendar, launch calendar, or dated task database
- Whether writes should default to draft-only, write-with-confirmation, or read-only
- Which workspace or databases are in scope for this skill

### 2. Then: Confirm Access Path

Establish what works now:
- Whether `NOTION_API_KEY` is available
- Whether the target database is already shared with the integration
- Whether the user has a preferred access path: optional `notion` CLI or direct API requests

If the CLI is missing or outdated, continue with official HTTP workflows instead of blocking.

### 3. Finally: Capture Durable Defaults

If the user wants persistent behavior, capture:
- Default timezone and date style for date windows
- Default title and date property names for each tracked calendar database
- Confirmation policy for archive, reschedule, and bulk changes
- Preferred status transitions such as Draft -> Scheduled -> Done

If those details are unknown, proceed conservatively and label assumptions clearly.

## What You Are Saving Internally

Track only reusable operating context:
- Workspace name and approved databases
- `database_id` and resolved `data_source_id` pairs
- Property mappings for title, date, status, and assignee-like fields
- Timezone defaults and verified command path
- Known schema quirks, ambiguous titles, and confirmed safety preferences

After updating local memory, summarize the behavior change in plain language so the user can correct it immediately.
