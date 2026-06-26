---
name: linear-agent
description: Full Linear project management via native GraphQL API. Superior to shell-script alternatives — auto-resolves identifiers (ENG-42), moves issues by state name, generates plain-English backlog summaries, syncs git commits to issue states, zero dependencies.

⚠️ This is an unofficial community skill and is not affiliated with or endorsed by Linear, Inc.
---

# linear-agent

Full Linear project management via GraphQL API.

## What I do
- Create, update, and search issues
- Move issues through workflow states by name
- Manage cycles and sprints
- Summarize team backlogs in plain English
- Sync git commit messages to issue states (e.g. "fixes ENG-42")
- Create and manage projects
- Post comments on issues

## Setup
Requires LINEAR_API_KEY environment variable.
Get your key at: Linear → Settings → Security & Access → API Keys
Set your Linear API key:
```
LINEAR_API_KEY=lin_api_yourkey
```
Get your key at: Linear → Settings → Security & Access → API Keys

## Usage
Works as both an OpenClaw skill and standalone CLI:
```
node index.js list-teams
node index.js create-issue --title "My issue" --teamId ENG
node index.js backlog-summary --teamId ENG
```
