---
name: one-plaud-recording-several-differently-formatted-summaries
description: "One Plaud Recording, Several Differently Formatted Summaries: Gets you past the one-template-per-recording ceiling. The Plaud app applies a single AutoFlow template to a recording, so if you want a short recap for yourself, a decisions-only version for the people who missed it, and a clean action list for your task manager, you are re-running or rewriting by hand. This workflow reads the transcript once and produces every format you have defined in a single pass: you list the output formats you."
version: 1.0.1
homepage: https://www.agentpmt.com/agent-workflow-skills/one-plaud-recording-several-differently-formatted-summaries
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agent-workflow-skills/one-plaud-recording-several-differently-formatted-summaries"}}
---
# One Plaud Recording, Several Differently Formatted Summaries

## Freshness
Last updated: `2026-07-26`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Workflow Does
Gets you past the one-template-per-recording ceiling. The Plaud app applies a single AutoFlow template to a recording, so if you want a short recap for yourself, a decisions-only version for the people who missed it, and a clean action list for your task manager, you are re-running or rewriting by hand. This workflow reads the transcript once and produces every format you have defined in a single pass: you list the output formats you want in a Google Sheet, each with a name and a description of the shape and audience, and the workflow generates all of them from the same source text and writes them into one Google Doc per recording with a section for each. Because every version comes from the same read of the transcript, they stay consistent with each other rather than drifting the way separately generated summaries do. Formats are yours to change at any time by editing the sheet, with no re-recording and no template juggling in the app. A processed log keeps each recording to a single pass so it can run on a schedule over everything new.

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
{"action":"start_workflow","skill_id":"one-plaud-recording-several-differently-formatted-summaries"}
```

```json
{"action":"end_workflow","skill_id":"one-plaud-recording-several-differently-formatted-summaries","rating":5,"comment":"completed"}
```

## Workflow Process
1. Get User Timezone and Date
   - Tool product: Get Users Current Time / Date.
   - Tool skill: `../get-users-current-time-date`.
   - ClawHub page: https://clawhub.ai/agentpmt/get-users-current-time-date.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill get-users-current-time-date`.
   - Marketplace: https://www.agentpmt.com/marketplace/user-timezone-datetime.
   - Tool instructions: Get the user's current local date, time, timezone and UTC offset. The requested window and every recording timestamp are resolved against this and never against the server clock.
2. Ask for the Recording Window
   - Prompt: Establish the exact window of recordings this run covers, in the user's own timezone.
3. Read Output Formats
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: Read the formats tab: each row defines one output the user wants, with a name, the audience it is for, and a description of its shape and length. These rows are the whole configuration; do not assume a fixed set of formats.
4. List Plaud Recordings
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: Call list_files with the widened UTC date_from and date_to from the window step. Plaud's timestamps are inconsistent and must be handled deliberately: the name field carries the recording's LOCAL time (for example '2026-07-25 19:53:50') while start_at and created_at are UTC written as naive strings with no Z and no offset (the same recording reads '2026-07-25T23:53:50'). Treat start_at as UTC, convert it into the user's timezone, and only then decide whether the recording falls inside the requested local window. An evening local recording carries the next day's UTC date, so comparing the raw string silently misfiles it. Then skip any recording id already in the processed log.
5. Each New Recording
   - Iterate over the configured collection, then continue through the connected workflow path.
6. Fetch Transcript
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: Call get_transcript with this recording's file id, reusing Plaud's existing transcript when one exists.
7. Summarize the Run
   - Prompt: Report what was produced this run.
8. Generate Every Configured Format
   - Prompt: Produce every output format the user has configured from one reading of this transcript.
9. Write the Multi-Format Doc
   - Tool product: Google Docs Connector.
   - Tool skill: `../google-docs-connector`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-docs-connector.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-docs-connector`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-docs-connector.
   - Tool instructions: Create one document for this recording with a clearly headed section for each configured format, in the order the sheet lists them, and the recording's local date and time plus a link back to it at the top.
10. Log the Run
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: Append the recording id, its local recorded time, the doc link, and which formats were produced to the processed log so the recording is not handled again.

## Tool Skill Links
- Get Users Current Time / Date: `../get-users-current-time-date`; ClawHub https://clawhub.ai/agentpmt/get-users-current-time-date; skills.sh `npx skills add AgentPMT/agent-skills --skill get-users-current-time-date`; marketplace https://www.agentpmt.com/marketplace/user-timezone-datetime
- Google Sheets: `../google-sheets`; ClawHub https://clawhub.ai/agentpmt/google-sheets; skills.sh `npx skills add AgentPMT/agent-skills --skill google-sheets`; marketplace https://www.agentpmt.com/marketplace/google-sheets-api
- Plaud: `../plaud`; ClawHub https://clawhub.ai/agentpmt/plaud; skills.sh `npx skills add AgentPMT/agent-skills --skill plaud`; marketplace https://www.agentpmt.com/marketplace/plaud
- Google Docs Connector: `../google-docs-connector`; ClawHub https://clawhub.ai/agentpmt/google-docs-connector; skills.sh `npx skills add AgentPMT/agent-skills --skill google-docs-connector`; marketplace https://www.agentpmt.com/marketplace/google-docs-connector

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Workflow page: https://www.agentpmt.com/agent-workflow-skills/one-plaud-recording-several-differently-formatted-summaries
- AgentPMT workflows: https://www.agentpmt.com/agent-workflow-skills
