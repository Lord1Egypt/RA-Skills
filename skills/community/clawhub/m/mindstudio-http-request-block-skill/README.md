# MindStudio HTTP Request Block Skill

A production-ready skill for configuring the MindStudio HTTP Request block correctly, reliably, and safely — across any workflow and any external service.

---

## What This Skill Does

This skill guides the configuration of MindStudio's HTTP Request block for any scenario where a workflow needs to talk to an external system. It interviews the user based on what they're trying to do, then outputs a complete, ready-to-paste block configuration including URL, method, headers, body, output variable, and downstream response handling.

It covers five scenarios:

- **Fetch Data** — GET requests to APIs (weather, stock prices, user records, etc.)
- **Send Data** — POST requests with JSON payloads, form submissions, AI output delivery
- **Update or Modify** — PATCH and PUT requests to update existing records
- **Delete Resources** — DELETE requests to remove records from external systems
- **Trigger External Systems** — Webhooks, Make, Zapier, pipeline triggers, inter-workflow calls

---

## When to Use This Skill

Use this skill any time a MindStudio workflow needs to:

- Call a REST API mid-workflow
- POST data to a Make or Zapier webhook
- Fetch live data from Finnhub, HubSpot, Airtable, or any external service
- Update or delete a record in an external system
- Trigger an external automation after an AI block completes
- Send workflow output somewhere outside MindStudio

---

## What the User Needs to Provide

The skill asks only the questions relevant to the user's scenario. At minimum:

| Scenario | Required from User |
|---|---|
| GET | Endpoint URL, query params, auth header (if needed) |
| POST | Endpoint URL, workflow variable names to send, auth (if needed) |
| PATCH / PUT | Endpoint URL, record ID variable, fields being updated, auth |
| DELETE | Endpoint URL, record ID variable, explicit confirmation of intent |
| Webhook / Trigger | Webhook URL, payload variable names, auth (if needed) |

---

## What the Skill Outputs

For every request, the skill generates:

1. A complete block configuration (URL, method, headers, content type, body, output variable)
2. Downstream handling instructions (success path, failure path, status code reference)
3. A pre-flight checklist to validate before saving the block

---

## Block Output Fields Reference

Every HTTP Request block returns four fields:

| Field | Type | Description |
|---|---|---|
| `ok` | Boolean | `true` if status is in the 2xx range |
| `status` | Number | Numeric HTTP status code |
| `statusText` | String | Status description |
| `response` | String | Full response body as a raw string |

Access them downstream using `{{outputVar.ok}}`, `{{outputVar.status}}`, etc.

---

## Supported HTTP Methods

`GET` `POST` `PATCH` `PUT` `DELETE` `HEAD` `OPTIONS`

---

## Supported Content Types

`application/json` `application/x-www-form-urlencoded` `multipart/form-data` `text/plain` `text/HTML` `application/XML` `custom` `none`

---

## Files in This Skill

| File | Purpose |
|---|---|
| `SKILL.md` | Full skill instruction set used by the AI |
| `README.md` | This file — overview and usage guide |
| `examples.md` | Real-world configuration examples for all five scenarios |
| `skill.json` | Skill metadata for registry and tooling |

---

## Safety Rules (Summary)

- Never send undefined or empty variables in a request body
- Never hardcode API keys or tokens — always inject via workflow variable
- Never send a body with GET, HEAD, or DELETE requests
- Never retry on 4xx errors — those are logic errors, not transient failures
- Never generate a DELETE configuration without explicit user confirmation

---

## Author

Built by Sol — MindStudio builder and educator.
Published for the MindStudio community via GitHub.
