---
name: lemlist-outreach
description: Run personalized email outreach campaigns via Lemlist. Manage campaigns, sequences, and tasks, track lead engagement, search people and company databases, and automate outreach workflows with labeling and scheduling.
---

# Lemlist

![Lemlist](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/lemlist.svg)

Run personalized email outreach campaigns via Lemlist. Manage campaigns and sequences, track lead engagement, search people and company databases, handle tasks, and automate outreach with labels and schedules.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=lemlist-outreach) for hosted connection flows and credentials so you do not need to configure Lemlist API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Lemlist |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Lemlist API     │
│   (User Chat)   │     │   (OAuth)    │     │   (v1)          │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device   │                       │
         │  3. Connect Lemlist│                      │
         │                   │  4. Secure Token      │
         │                   │  5. Proxy Requests    │
         │                   │                       │
         ▼                   ▼                       ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │ Lemlist  │
   │  File    │      │ Auth     │           │ Campaigns│
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Lemlist again."

## Quick Start

```bash
# List campaigns
clawlink_call_tool --tool "lemlist_get_list_campaigns" --params '{}'

# Get campaign stats
clawlink_call_tool --tool "lemlist_get_campaign_stats" --params '{"campaign_id": "CAMPAIGN_ID"}'

# Get team info
clawlink_call_tool --tool "lemlist_get_team_info" --params '{}'
```

## Authentication

All Lemlist tool calls are authenticated automatically by ClawLink using the user's connected Lemlist team.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Lemlist API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=lemlist and connect Lemlist (requires an active Lemlist team).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `lemlist` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration lemlist
```

**Response:** Returns the live tool catalog for Lemlist.

### Reconnect

If Lemlist tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=lemlist
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration lemlist`

## Security & Permissions

- Access is scoped to the connected Lemlist team only.
- **All write operations require explicit user confirmation.** Before executing any campaign, lead, or sequence action, confirm the target resource and intended effect with the user.
- Destructive actions (delete schedule, unsubscribe lead, delete unsubscribed email) are marked as high-impact and must be confirmed.
- Campaign creation returns IDs nested under `result['data']` — store campaignId, sequenceId, scheduleId from responses.
- Lead status changes (mark interested/not interested, pause) affect ongoing outreach — confirm before executing.

## Tool Reference

### Campaigns

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_list_campaigns` | List all campaigns for the team with IDs, names, statuses | Read |
| `lemlist_get_campaign_by_id` | Get campaign details by ID | Read |
| `lemlist_get_campaign_stats` | Get campaign performance metrics within a date range | Read |
| `lemlist_get_campaign_export_start` | Start async CSV export of all campaign statistics | Write |
| `lemlist_get_campaign_export_status` | Check status of campaign export job | Read |
| `lemlist_get_campaign_sequences` | Get all sequences for a campaign with steps and conditions | Read |
| `lemlist_get_export_campaign_leads` | Export campaign leads with state filtering (JSON or CSV) | Read |
| `lemlist_post_create_campaign` | Create a new campaign (returns campaignId, sequenceId, scheduleId) | Write |
| `lemlist_patch_update_campaign` | Update campaign settings (name, stop-on behaviors, flags) | Write |
| `lemlist_post_pause_campaign` | Pause a running campaign | Write |

### Leads

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_retrieve_lead_by_email` | Get lead details by email address | Read |
| `lemlist_post_create_lead_in_campaign` | Create a lead and add to a campaign with optional enrichment | Write |
| `lemlist_post_mark_lead_as_interested` | Mark a lead as interested in all campaigns | Write |
| `lemlist_post_mark_lead_as_interested_in_campaign` | Mark a lead as interested in a specific campaign | Write |
| `lemlist_post_mark_lead_as_not_interested` | Mark a lead as not interested in all campaigns | Write |
| `lemlist_patch_mark_lead_as_not_interested_in_campaign` | Mark a lead as not interested in a specific campaign | Write |
| `lemlist_post_pause_lead` | Pause a lead in all campaigns or a specific campaign | Write |
| `lemlist_delete_unsubscribe_lead_from_campaign` | Unsubscribe a lead from a specific campaign | Write |
| `lemlist_post_add_variables_to_lead` | Add custom variables to a lead | Write |

### Sequences

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_patch_update_sequence_step` | Update a sequence step (subject, message, delay) | Write |
| `lemlist_post_add_step_to_sequence` | Add a new step (email, LinkedIn, conditional) to a sequence | Write |

### Schedules

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_post_create_schedule` | Create a new schedule (returns scheduleId — store for campaign association) | Write |
| `lemlist_patch_update_schedule` | Update an existing schedule's days, time window, limits | Write |
| `lemlist_delete_delete_schedule` | Permanently delete a schedule by ID | Write |
| `lemlist_post_associate_schedule_with_campaign` | Associate a schedule with a campaign | Write |

### Tasks

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_list_tasks` | List all pending tasks assigned to team members | Read |
| `lemlist_post_create_task` | Create a manual task associated with a contact, company, or lead | Write |
| `lemlist_update_task` | Update task assignment, scheduling, and status | Write |
| `lemlist_post_ignore_tasks` | Mark one or more tasks as ignored | Write |

### Unsubscribes & Suppression

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_retrieve_unsubscribes` | List all unsubscribed people | Read |
| `lemlist_get_get_unsubscribe_email` | Check if a specific email is unsubscribed | Read |
| `lemlist_get_export_unsubscribes` | Download CSV of all unsubscribed email addresses | Read |
| `lemlist_post_add_unsubscribe_email_domain` | Add an email or domain to the unsubscribed list | Write |
| `lemlist_delete_delete_unsubscribe_email` | Remove an email from the unsubscribed list | Write |

### Labels

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_list_labels` | List all labels for inbox organization | Read |
| `lemlist_get_label` | Get label details by ID | Read |
| `lemlist_post_create_label` | Create a new label for inbox conversations | Write |

### Companies

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_list_companies` | List all companies in CRM with pagination | Read |
| `lemlist_list_company_notes` | Get all notes for a specific company | Read |
| `lemlist_create_company_note` | Add a note to a company record | Write |
| `lemlist_search_companies_database` | Search companies database with filters and keywords | Read |
| `lemlist_get_companies_schema` | Get schema definition for company records | Read |

### People Database

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_search_people_database` | Search people database with filters, keywords, pagination | Read |
| `lemlist_get_people_schema` | Get schema definition for people records | Read |
| `lemlist_get_database_filters` | Discover available search filters for people and companies | Read |

### Contact Messages

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_contact_messages` | Get all messages exchanged with a specific contact | Write |

### Activity & Analytics

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_retrieve_activities` | Get recent campaign activities filtered by campaign, type, limit | Read |

### Team & Users

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_team_info` | Get team settings, members, webhooks, and enabled features | Read |
| `lemlist_get_list_team_senders` | Get all team members and their associated campaigns | Read |
| `lemlist_get_user` | Get user details by ID including LinkedIn settings and mailboxes | Read |
| `lemlist_get_user_info` | Get authenticated user information | Read |
| `lemlist_get_list_watchlist_signals` | Get paginated watchlist signals with filtering | Read |

### Credits

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_team_credits` | Get remaining credits in the team | Read |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `lemlist_get_all_webhooks` | List all configured webhooks for the team | Read |

## Code Examples

### List campaigns

```bash
clawlink_call_tool --tool "lemlist_get_list_campaigns" \
  --params '{}'
```

### Get campaign stats

```bash
clawlink_call_tool --tool "lemlist_get_campaign_stats" \
  --params '{"campaign_id": "CAMPAIGN_ID", "start_date": "2024-01-01", "end_date": "2024-01-31"}'
```

### Create a lead in campaign

```bash
clawlink_call_tool --tool "lemlist_post_create_lead_in_campaign" \
  --params '{"campaign_id": "CAMPAIGN_ID", "email": "lead@example.com", "first_name": "John"}'
```

### Mark lead as interested

```bash
clawlink_call_tool --tool "lemlist_post_mark_lead_as_interested" \
  --params '{"lead_id": "LEAD_ID"}'
```

### Create a task

```bash
clawlink_call_tool --tool "lemlist_post_create_task" \
  --params '{"contact_id": "CONTACT_ID", "title": "Follow up call", "due_date": "2024-12-15"}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Lemlist is connected.
2. Call `clawlink_list_tools --integration lemlist` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `lemlist`.
5. If no Lemlist tools appear, direct the user to https://claw-link.dev/dashboard?add=lemlist.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List campaigns → Get stats → Show results         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call          │
│                                                             │
│  Example: Preview lead create → User approves → Execute     │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Campaign creation returns IDs nested under `result['data']` (e.g., `result['data']['campaignId']`). Store these for subsequent operations.
- Schedules return `scheduleId` — store it for association with campaigns or sequences.
- Avoid creating unused schedules; delete them when no longer needed.
- Lead status changes affect all campaigns or specific campaigns depending on the tool used.
- Company notes are for tracking annotations and activities on company records.
- People and companies database search supports free-text and structured filtering.
- Verify returned `teamId` matches the intended workspace before passing to campaign-creation.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration lemlist`. |
| Missing connection | Lemlist is not connected. Direct the user to https://claw-link.dev/dashboard?add=lemlist. |
| Permission error | The authenticated user lacks permission for this operation. |
| Campaign not found | The campaign ID does not exist. Verify with `lemlist_get_list_campaigns`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

## Resources

- [Lemlist API Documentation](https://docs.lemlist.com/)
- [Lemlist Campaign Management](https://help.lemlist.com/en/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=lemlist-outreach
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Instantly Campaigns](https://clawhub.ai/hith3sh/instantly-campaigns) — For Instantly cold email campaigns
- [Kit Email Marketing](https://clawhub.ai/hith3sh/kit-email-marketing) — For Kit email broadcasts and sequences
- [LinkedIn Social](https://clawhub.ai/hith3sh/linkedin-social) — For LinkedIn outreach and connection management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=lemlist-outreach)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)