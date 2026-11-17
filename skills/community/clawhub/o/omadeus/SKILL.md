---
name: maestro
description: Interact with the Maestro API to create tasks, list tasks, and send room messages using the configured OpenClaw Maestro connection.
---

# Maestro Skill

## Purpose

Use this skill whenever a user wants to interact with Maestro by creating tasks, listing tasks, or sending messages.

## Configuration

Read configuration from the active OpenClaw configuration (`openclaw.json`).

Configuration path:

```text
channels.omadeus
```

Required values:

- `baseUrl`
- `apiKey`
- `openClawMemberId`

Never hardcode, expose, print, or ask the user for these values.

## Authentication

Every request must include:

```http
Accept: application/json, text/plain, */*
ApiToken: <channels.omadeus.apiKey>
```

Never use `Authorization: Bearer`.

## Base URL

Always use:

```text
https://<channels.omadeus.baseUrl>
```

## Workflow

1. Read configuration.
2. Validate required fields.
3. Build the request.
4. Send the request.
5. Validate the response.
6. Return a concise user-friendly result.

## Operations

### Create Task

Endpoint:

```text
POST /dolphin/apiv1/nuggets
```

Request body:

```json
{
  "title": "...",
  "description": "...",
  "kind": "task",
  "priority": "low|medium|high|urgent",
  "memberReferenceId": "<channels.omadeus.openClawMemberId>"
}
```

Rules:

- Generate a concise title.
- Generate a clear description from user input.
- Default priority is `low`.
- Never send `stage`.
- Do not invent missing technical details.

### List Tasks

Endpoint:

```text
GET /dolphin/apiv1/global/taskviews?sort=-recentMessageAt&take=25&zone=tasklists-tasks
```

Rules:

- Use requested `take` if provided.
- Present readable results.
- Do not dump raw JSON.

### Send Message

Endpoint:

```text
POST /jaguar/apiv1/rooms/{room_id}/messages
```

Body:

```json
{"body":"<message>"}
```

Rules:

- Never invent a room id.
- Ask only if no room id is available.

## Error Handling

If any of the following are missing, do not send requests:

- channels.omadeus.baseUrl
- channels.omadeus.apiKey
- channels.omadeus.openClawMemberId

Report a configuration error without exposing internal values.

## Security

Never:

- expose credentials
- log credentials
- hardcode URLs
- hardcode member IDs
- include secrets in responses

## Response Guidelines

- Confirm successful operations.
- Include task id when returned.
- Summarize errors clearly.
