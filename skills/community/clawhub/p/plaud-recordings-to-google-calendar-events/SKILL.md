---
name: plaud-recordings-to-google-calendar-events
description: "Plaud Recordings to Google Calendar Events: Puts the meetings you agree to out loud straight onto your Google Calendar, without Zapier in the middle. Plaud's own app has no Calendar integration, so this closes that gap directly: each new recording is scanned, the transcript pulled, and any genuine scheduling commitment spoken in it (\"let's do Tuesday at 3\", \"I'll come back out Thursday morning\") is extracted with the relative date resolved against the recording's own date and your timezone. Eac."
version: 1.0.1
homepage: https://www.agentpmt.com/agent-workflow-skills/plaud-recordings-to-google-calendar-events
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agent-workflow-skills/plaud-recordings-to-google-calendar-events"}}
---
# Plaud Recordings to Google Calendar Events

## Freshness
Last updated: `2026-07-26`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Workflow Does
Puts the meetings you agree to out loud straight onto your Google Calendar, without Zapier in the middle. Plaud's own app has no Calendar integration, so this closes that gap directly: each new recording is scanned, the transcript pulled, and any genuine scheduling commitment spoken in it ("let's do Tuesday at 3", "I'll come back out Thursday morning") is extracted with the relative date resolved against the recording's own date and your timezone. Each one becomes a Google Calendar event with the agreed time, a title naming who and what, and the surrounding quote from the transcript in the description so you can see exactly what was said. Vague intentions with no time attached ("we should catch up sometime") are deliberately ignored rather than guessed into a slot. Because it uses the full Google Calendar connector it also reads back, so an agent can answer what your week looks like from the same connection. A Google Sheet ledger records every recording id and every event created, so a scheduled run never double-books you.

## Required Setup
- AgentPMT overview: `../what-is-agentpmt`.
- Account MCP/REST setup: `../agentpmt-account-mcp-rest-api-setup`.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

## Workflow Session Management
Call `AgentPMT-Workflow-Skills` with `start_workflow` before the first step and `end_workflow` after the final step.

```json
{"action":"start_workflow","skill_id":"plaud-recordings-to-google-calendar-events"}
```

```json
{"action":"end_workflow","skill_id":"plaud-recordings-to-google-calendar-events","rating":5,"comment":"completed"}
```

## Workflow Process
1. Get User Timezone and Date
   - Tool product: Get Users Current Time / Date.
   - Tool skill: `../get-users-current-time-date`.
   - ClawHub page: https://clawhub.ai/agentpmt/get-users-current-time-date.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill get-users-current-time-date`.
   - Marketplace: https://www.agentpmt.com/marketplace/user-timezone-datetime.
   - Tool instructions: Get the user's current local date, time, timezone and UTC offset. The requested window, every recording timestamp, and every relative date spoken in a recording are resolved against this and never against the server clock.
2. Ask for the Recording Window
   - Prompt: Establish the exact window of recordings this run covers, in the user's own timezone.
3. List Plaud Recordings
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: Call list_files with the widened UTC date_from and date_to from the previous step. Plaud's timestamps are inconsistent and must be handled deliberately: the name field carries the recording's LOCAL time (for example '2026-07-25 19:53:50') while start_at and created_at are UTC written as naive strings with no Z and no offset (the same recording reads '2026-07-25T23:53:50'). Treat start_at as UTC, convert it into the user's timezone, and only then decide whether the recording falls inside the requested local window. This matters twice over here, because the recording's local date is also the anchor for resolving every relative date spoken inside it. Then skip any recording id already in the ledger sheet.
4. Each New Recording
   - Iterate over the configured collection, then continue through the connected workflow path.
5. Fetch Transcript
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: Call get_transcript with this recording's file id, reusing Plaud's existing transcript when one is available.
6. Summarize the Run
   - Prompt: Tell the user exactly what landed on their calendar and what was deliberately left off.
7. Extract Scheduling Commitments
   - Prompt: Find every concrete scheduling commitment spoken in the conversation and resolve it to a real calendar date and time in the user's timezone.
8. Create Calendar Events
   - Tool product: Google Calendar.
   - Tool skill: `../google-calendar`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-calendar.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-calendar`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-calendar.
   - Tool instructions: Create each extracted event on the user's primary calendar in their own timezone, putting the source quote and the recording link in the description. If an event with the same title and start time already exists, leave it alone rather than creating a duplicate.
9. Log to Ledger Sheet
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: Append the recording id, its local recorded time, the events created, and any recordings that yielded nothing, so the next run skips them and the user has an audit trail of what was scheduled from which conversation. Write all times in the user's local timezone.

## Tool Skill Links
- Get Users Current Time / Date: `../get-users-current-time-date`; ClawHub https://clawhub.ai/agentpmt/get-users-current-time-date; skills.sh `npx skills add AgentPMT/agent-skills --skill get-users-current-time-date`; marketplace https://www.agentpmt.com/marketplace/user-timezone-datetime
- Plaud: `../plaud`; ClawHub https://clawhub.ai/agentpmt/plaud; skills.sh `npx skills add AgentPMT/agent-skills --skill plaud`; marketplace https://www.agentpmt.com/marketplace/plaud
- Google Calendar: `../google-calendar`; ClawHub https://clawhub.ai/agentpmt/google-calendar; skills.sh `npx skills add AgentPMT/agent-skills --skill google-calendar`; marketplace https://www.agentpmt.com/marketplace/google-calendar
- Google Sheets: `../google-sheets`; ClawHub https://clawhub.ai/agentpmt/google-sheets; skills.sh `npx skills add AgentPMT/agent-skills --skill google-sheets`; marketplace https://www.agentpmt.com/marketplace/google-sheets-api

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Workflow page: https://www.agentpmt.com/agent-workflow-skills/plaud-recordings-to-google-calendar-events
- AgentPMT workflows: https://www.agentpmt.com/agent-workflow-skills
