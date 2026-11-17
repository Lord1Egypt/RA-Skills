---
name: narrated-walkthrough-to-a-numbered-sop-document
description: "Narrated Walkthrough to a Numbered SOP Document: Turns talking through a job out loud into a written, numbered standard operating procedure. Built for the people who actually know the equipment and have no time to write documentation: maintenance and facilities teams, field service, manufacturing, labs, franchise operations, and any owner trying to get a process out of their own head before handing it over. Walk the machine or the task and narrate it, saying the step number out loud as you go."
version: 1.0.1
homepage: https://www.agentpmt.com/agent-workflow-skills/narrated-walkthrough-to-a-numbered-sop-document
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agent-workflow-skills/narrated-walkthrough-to-a-numbered-sop-document"}}
---
# Narrated Walkthrough to a Numbered SOP Document

## Freshness
Last updated: `2026-07-26`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Workflow Does
Turns talking through a job out loud into a written, numbered standard operating procedure. Built for the people who actually know the equipment and have no time to write documentation: maintenance and facilities teams, field service, manufacturing, labs, franchise operations, and any owner trying to get a process out of their own head before handing it over. Walk the machine or the task and narrate it, saying the step number out loud as you go, and the workflow pulls the transcript of each new Plaud recording and turns it into a clean procedure document: a title, the equipment or process it covers, tools and safety notes gathered into their own sections, then numbered steps in the order you said them, with your asides and warnings kept attached to the step they belong to. Filler, false starts and interruptions are dropped; the technical content is left in your words rather than rewritten into corporate documentation voice. It lands as a Google Doc so it stays editable and exports to PDF or Word, and anything the narration left ambiguous is flagged at the end for you to fill in rather than being invented. Say each step number aloud and the transcript carries its own index, which makes pairing photos to steps afterwards mechanical instead of guesswork.

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
{"action":"start_workflow","skill_id":"narrated-walkthrough-to-a-numbered-sop-document"}
```

```json
{"action":"end_workflow","skill_id":"narrated-walkthrough-to-a-numbered-sop-document","rating":5,"comment":"completed"}
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
3. List Plaud Recordings
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: Call list_files with the widened UTC date_from and date_to from the window step. Plaud's timestamps are inconsistent and must be handled deliberately: the name field carries the recording's LOCAL time (for example '2026-07-25 19:53:50') while start_at and created_at are UTC written as naive strings with no Z and no offset (the same recording reads '2026-07-25T23:53:50'). Treat start_at as UTC, convert it into the user's timezone, and only then decide whether the recording falls inside the requested local window. An evening local recording carries the next day's UTC date, so comparing the raw string silently misfiles it. Carry each recording's name and duration forward, both of which help judge whether it is a narrated procedure. Then skip any recording id already in the processed log.
4. Each New Recording
   - Iterate over the configured collection, then continue through the connected workflow path.
5. Fetch Transcript
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: Call get_transcript with this recording's file id, reusing Plaud's existing transcript when one exists.
6. Summarize the Run
   - Prompt: Tell the user which procedures were written, which need a human, and what was skipped.
7. Judge and Structure the Procedure
   - Prompt: Decide whether this recording is genuinely someone narrating a procedure, and if it is, turn it into an ordered numbered standard operating procedure.
8. Write the SOP Document
   - Tool product: Google Docs Connector.
   - Tool skill: `../google-docs-connector`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-docs-connector.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-docs-connector`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-docs-connector.
   - Tool instructions: Only for recordings judged to be procedures. Create a Google Doc: title and process at the top with the local recorded date, then tools and materials, then safety notes, then the numbered steps as a numbered list, and finally the ambiguities section headed as needing review. Leave it editable so the user can drop photos beside the steps and export to PDF or Word. Write no document for a recording judged not to be a procedure.
9. Log the Run
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: Append one row for this recording either way. For a documented procedure: recording id, local recorded time, procedure title, doc link, step count, open ambiguity count. For a skipped recording: recording id, local recorded time, status skipped, and the reason it was judged not a procedure. Both mark it processed so it is never examined twice, and the skip reasons let the user spot a walkthrough that was wrongly rejected.

## Tool Skill Links
- Get Users Current Time / Date: `../get-users-current-time-date`; ClawHub https://clawhub.ai/agentpmt/get-users-current-time-date; skills.sh `npx skills add AgentPMT/agent-skills --skill get-users-current-time-date`; marketplace https://www.agentpmt.com/marketplace/user-timezone-datetime
- Plaud: `../plaud`; ClawHub https://clawhub.ai/agentpmt/plaud; skills.sh `npx skills add AgentPMT/agent-skills --skill plaud`; marketplace https://www.agentpmt.com/marketplace/plaud
- Google Docs Connector: `../google-docs-connector`; ClawHub https://clawhub.ai/agentpmt/google-docs-connector; skills.sh `npx skills add AgentPMT/agent-skills --skill google-docs-connector`; marketplace https://www.agentpmt.com/marketplace/google-docs-connector
- Google Sheets: `../google-sheets`; ClawHub https://clawhub.ai/agentpmt/google-sheets; skills.sh `npx skills add AgentPMT/agent-skills --skill google-sheets`; marketplace https://www.agentpmt.com/marketplace/google-sheets-api

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Workflow page: https://www.agentpmt.com/agent-workflow-skills/narrated-walkthrough-to-a-numbered-sop-document
- AgentPMT workflows: https://www.agentpmt.com/agent-workflow-skills
