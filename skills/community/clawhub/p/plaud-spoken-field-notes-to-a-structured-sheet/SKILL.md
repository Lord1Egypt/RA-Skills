---
name: plaud-spoken-field-notes-to-a-structured-sheet
description: "Plaud Spoken Field Notes to a Structured Sheet: Turns a spoken site visit into a filled-in spreadsheet row, so measurements and specs never get typed up twice. Built for anyone who dictates structured details on the job rather than writing them down: window and flooring measurements, equipment specs, inspection findings, punch lists, service call notes. Say the details out loud in the same order each visit (client, room, width, drop, colour, notes) and the workflow reads each new Plaud recordin."
version: 1.0.1
homepage: https://www.agentpmt.com/agent-workflow-skills/plaud-spoken-field-notes-to-a-structured-sheet
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agent-workflow-skills/plaud-spoken-field-notes-to-a-structured-sheet"}}
---
# Plaud Spoken Field Notes to a Structured Sheet

## Freshness
Last updated: `2026-07-26`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Workflow Does
Turns a spoken site visit into a filled-in spreadsheet row, so measurements and specs never get typed up twice. Built for anyone who dictates structured details on the job rather than writing them down: window and flooring measurements, equipment specs, inspection findings, punch lists, service call notes. Say the details out loud in the same order each visit (client, room, width, drop, colour, notes) and the workflow reads each new Plaud recording, pulls its transcript, extracts only the values actually spoken, and appends them as one row to your Google Sheet under whatever column headers you have already set up. Values are never inferred: if a measurement was not said, the cell is left empty and flagged in the run summary rather than guessed, because a fabricated number on a quote is worse than a blank one. Recordings that are not field dictations (meetings, personal memos, ambient audio) are logged as skipped and produce no row. A Processed tab records every recording id so the workflow can run on a schedule without duplicating rows. Pair it with your own quote template and the spreadsheet row becomes the quote.

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
{"action":"start_workflow","skill_id":"plaud-spoken-field-notes-to-a-structured-sheet"}
```

```json
{"action":"end_workflow","skill_id":"plaud-spoken-field-notes-to-a-structured-sheet","rating":5,"comment":"completed"}
```

## Workflow Process
1. Get User Timezone and Date
   - Tool product: Get Users Current Time / Date.
   - Tool skill: `../get-users-current-time-date`.
   - ClawHub page: https://clawhub.ai/agentpmt/get-users-current-time-date.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill get-users-current-time-date`.
   - Marketplace: https://www.agentpmt.com/marketplace/user-timezone-datetime.
   - Tool instructions: Get the user's current local date, time, timezone and UTC offset. Everything downstream, the requested window, the recording timestamps and any spoken relative date, is resolved against this and never against the server clock.
2. Ask for the Recording Window
   - Prompt: Establish the exact window of recordings this run covers, in the user's own timezone.
3. List Plaud Recordings
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: Call list_files with the widened UTC date_from and date_to from the previous step. Plaud's timestamps are inconsistent and must be handled deliberately: the name field carries the recording's LOCAL time (for example '2026-07-25 19:53:50') while start_at and created_at are UTC written as naive strings with no Z and no offset (the same recording reads '2026-07-25T23:53:50'). Treat start_at as UTC, convert it into the user's timezone, and only then decide whether the recording falls inside the requested local window. An evening local recording carries the next day's UTC date, so comparing the raw string silently misfiles it. Display and log times in the user's local timezone. Then drop any recording id already in the Processed tab so a scheduled run never repeats work.
4. Each New Recording
   - Iterate over the configured collection, then continue through the connected workflow path.
5. Fetch Transcript
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: Call get_transcript with this recording's file id. Reuse Plaud's own transcript rather than re-transcribing.
6. Summarize the Run
   - Prompt: Report what was captured this run so the user can spot a bad extraction before acting on it.
7. Extract Spoken Fields
   - Prompt: Turn a spoken site-visit dictation into one structured row matching the column headers of the target sheet.
8. Append Row to Sheet
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: Append the extracted row to the data tab at the true table end, writing any timestamp in the user's local timezone. Then log the recording id to the Processed tab so it is never handled twice. Skipped recordings are logged to Processed with their reason and no data row.

## Tool Skill Links
- Get Users Current Time / Date: `../get-users-current-time-date`; ClawHub https://clawhub.ai/agentpmt/get-users-current-time-date; skills.sh `npx skills add AgentPMT/agent-skills --skill get-users-current-time-date`; marketplace https://www.agentpmt.com/marketplace/user-timezone-datetime
- Plaud: `../plaud`; ClawHub https://clawhub.ai/agentpmt/plaud; skills.sh `npx skills add AgentPMT/agent-skills --skill plaud`; marketplace https://www.agentpmt.com/marketplace/plaud
- Google Sheets: `../google-sheets`; ClawHub https://clawhub.ai/agentpmt/google-sheets; skills.sh `npx skills add AgentPMT/agent-skills --skill google-sheets`; marketplace https://www.agentpmt.com/marketplace/google-sheets-api

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Workflow page: https://www.agentpmt.com/agent-workflow-skills/plaud-spoken-field-notes-to-a-structured-sheet
- AgentPMT workflows: https://www.agentpmt.com/agent-workflow-skills
