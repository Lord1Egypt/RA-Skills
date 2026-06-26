---
name: mindstudio-http-request-block-skill
description: Configure and use the MindStudio HTTP Request block to send data to external APIs, webhooks, and web services. Use this skill whenever a user mentions HTTP requests, webhooks, calling an API, connecting to Make, Zapier, HubSpot, Airtable, Finnhub, or any external service from MindStudio, wants to fetch or POST data mid-workflow, or asks how to send workflow output somewhere. Always use this skill — do not attempt to configure an HTTP Request block from memory. Even if the request seems simple ("how do I POST to a webhook"), use this skill.
---

# MindStudio HTTP Request Block Skill

A production reference for configuring the HTTP Request block correctly, reliably, and safely across any MindStudio workflow.

---

## Step 1: Identify the Scenario and Interview the User

Before writing any configuration, determine what the user is trying to do. Match their intent to one of the five scenarios below, then ask only the questions listed for that scenario. Do not ask questions from other scenarios. Do not guess at variable names — use exactly what the user provides.

If the user's intent is already clear from context (e.g. they said "POST my AI output to a Make webhook"), skip straight to the questions for that scenario without asking them to confirm the scenario type.

---

### Scenario A: Fetch Data (GET)

**Trigger:** User wants to retrieve data from an API — weather, stock prices, user records, CRM contacts, etc.

**Ask the user:**
1. What is the API endpoint URL? (full URL including any path)
2. Does the endpoint require an API key or token? If yes, what is the header name (e.g. `Authorization`, `X-Api-Key`)?
3. Are there any query parameters needed to filter or specify the data? (e.g. `symbol=AAPL`, `user_id={{userId}}`)
4. What data do you need from the response? (so downstream handling can be configured correctly)

**Method:** `GET`
**Body:** None
**Content-Type:** `none`

---

### Scenario B: Send Data (POST)

**Trigger:** User wants to submit data to an external system — form submissions, JSON payloads, lead captures, AI output delivery, etc.

**Ask the user:**
1. What is the endpoint URL you are sending to?
2. Does the endpoint require an API key or token? If yes, what is the header name?
3. What variables from your workflow do you want to send? List the exact variable names (e.g. `{{customer_name}}`, `{{ai_output}}`, `{{email}}`).
4. Does the endpoint expect JSON, form data, or plain text?
5. What do you expect back in the response? (e.g. a confirmation ID, a status field, nothing)

**Method:** `POST`
**Content-Type:** `application/json` (default unless user specifies otherwise)

---

### Scenario C: Update or Modify (PATCH / PUT)

**Trigger:** User wants to update an existing record in an external system — CRM contact, database row, project record, etc.

**Ask the user:**
1. What is the base endpoint URL? (e.g. `https://api.example.com/contacts`)
2. What is the record ID variable name in your workflow? (e.g. `{{contact_id}}`, `{{record_id}}`) — this gets appended to the URL
3. Are you updating specific fields only (PATCH) or replacing the entire record (PUT)?
4. Which fields are being updated? List the exact variable names and what each field represents.
5. Does the endpoint require an API key or token? If yes, what is the header name?
6. What do you expect back in the response?

**Method:** `PATCH` (partial update) or `PUT` (full replacement)
**Content-Type:** `application/json`

---

### Scenario D: Delete a Resource (DELETE)

**Trigger:** User wants to remove a record or resource from an external system.

**Ask the user:**
1. What is the base endpoint URL?
2. What is the record ID variable name in your workflow? (gets appended to the URL)
3. Does the endpoint require an API key or token? If yes, what is the header name?
4. Confirm: this action is permanent. Is that the intent?
5. What do you expect back in the response? (many DELETE endpoints return 204 with no body)

**Method:** `DELETE`
**Body:** None
**Content-Type:** `none`

**Safety rule:** Never generate a DELETE configuration without explicit confirmation from the user that removal is the intended action.

---

### Scenario E: Trigger an External System

**Trigger:** User wants to fire a signal to an external system when something happens in the workflow — webhooks, Make/Zapier triggers, notifications, pipeline kicks, inter-workflow calls, etc.

**Ask the user:**
1. What is the webhook or trigger URL?
2. Does it require any authentication headers? (many webhooks do not)
3. What data do you want to include in the trigger payload? List exact variable names.
4. What does the external system return on success? (e.g. Make returns `{"accepted": true}`, some return 200 with no body)
5. Is there anything that should happen in the workflow after the trigger fires? (e.g. branch on success/failure, log the result)

**Method:** `POST`
**Content-Type:** `application/json`

---

## Step 2: Generate the Block Configuration

Once the user answers the questions for their scenario, output a complete, ready-to-paste block configuration using this structure:

```
URL          : [full URL, with variables where needed]
Method       : [GET / POST / PATCH / PUT / DELETE]
Content-Type : [application/json / none / other]

Headers:
  [Key]  : [Value]
  [Key]  : [Value]

Parameters (GET only):
  [key]  : [value]

Body:
[JSON or form structure using exact variable names]

Output Variable: [descriptiveName]
```

Then immediately follow with the downstream handling block:

```
On success (ok = true):
  - [what to do with the response]
  - [how to access specific fields]

On failure (ok = false):
  - Check {{outputVar.status}} for error code
  - [recommended branch or fallback]
```

---

## Block Output Fields

Every HTTP Request block returns four fields regardless of method or endpoint:

| Field | Type | Description |
|---|---|---|
| `ok` | Boolean | `true` if response status is in the 2xx range |
| `status` | Number | Numeric HTTP status code (e.g. `200`, `404`, `500`) |
| `statusText` | String | Status description (e.g. `"OK"`, `"Not Found"`) |
| `response` | String | Full response body as a raw string |

Access them downstream using:

```
{{outputVar.ok}}
{{outputVar.status}}
{{outputVar.statusText}}
{{outputVar.response}}
```

If the response body is JSON, pass `{{outputVar.response}}` to a downstream Generate Text or Run Function block to parse and extract fields. Never access nested fields directly from the raw response string.

---

## Configuration Field Reference

### URL
- Must be a complete, valid URL including `https://`
- Variables are supported: `https://api.example.com/users/{{userId}}`
- Never hardcode API keys or tokens in the URL — use headers

### Method

| Method | Use Case |
|---|---|
| `GET` | Retrieve data — no body |
| `POST` | Create a resource or trigger an action |
| `PATCH` | Partially update an existing resource |
| `PUT` | Fully replace an existing resource |
| `DELETE` | Remove a resource — no body |
| `HEAD` | Retrieve headers only |
| `OPTIONS` | Discover available methods |

### Headers

```
Content-Type    : application/json
Authorization   : Bearer {{apiKey}}
Accept          : application/json
X-Api-Key       : {{serviceKey}}
```

- Always include `Content-Type` when sending a body
- Always include `Authorization` when the endpoint requires it
- All values support `{{variable}}` syntax

### Parameters
Query string key-value pairs. Used with GET requests.

```
symbol    : {{ticker}}
token     : {{apiKey}}
from      : {{startDate}}
```

### Content Type

| Option | When to Use |
|---|---|
| `application/json` | Structured JSON data (most common) |
| `application/x-www-form-urlencoded` | HTML form submissions |
| `multipart/form-data` | File uploads or mixed form data |
| `text/plain` | Raw text payloads |
| `application/XML` | XML-based APIs |
| `custom` | Any content type not in this list |
| `none` | GET, HEAD, DELETE — no body |

### Body

**For `application/json`:**
```json
{
  "customer_name": "{{customer_name}}",
  "email": "{{email}}",
  "ai_output": "{{generatedText}}",
  "submitted_at": "{{timestamp}}"
}
```

**For `application/x-www-form-urlencoded`:**
```
customer_name={{customer_name}}&email={{email}}
```

**For GET / DELETE:** Leave body empty. Set Content-Type to `none`.

### Output Variable
Always set this. Use a descriptive name that reflects the source.

```
makeResponse
crmResult
stockData
userRecord
patchResult
```

---

## Request Construction Rules

1. **Method selection** — POST for create/trigger, PATCH for partial update, PUT for full replace, GET for read-only, DELETE for removal
2. **Headers** — always include `Content-Type` when sending a body; always include auth headers when required; never omit required headers
3. **Body** — every field must come from a real workflow variable or a hardcoded literal; never invent field values
4. **Variables** — use `{{variableName}}` syntax everywhere; use dot notation for nested data from upstream blocks
5. **Output variable** — always name it; always check `ok` before using `response` downstream

---

## Output Handling

### Success (ok = true, 2xx)
1. Check `{{outputVar.ok}}` is true before proceeding
2. Access raw body via `{{outputVar.response}}`
3. If body is JSON, parse it in a downstream block before using individual fields
4. Store or log relevant fields for use in the rest of the workflow

### Failure (ok = false, 4xx or 5xx)

| Status | Meaning | Fix |
|---|---|---|
| `400` | Bad Request | Body is malformed or missing required fields |
| `401` | Unauthorized | Missing or invalid API key / token |
| `403` | Forbidden | Valid key but insufficient permissions |
| `404` | Not Found | URL is wrong or resource does not exist |
| `422` | Unprocessable Entity | JSON is valid but field values are invalid |
| `429` | Rate Limited | Too many requests — add a Wait block |
| `500` | Server Error | External API issue — retry or alert |
| `503` | Service Unavailable | External API is down — retry later |

### Malformed Response
- Do not parse a non-JSON response as JSON
- Route to an error branch and log `{{outputVar.response}}` for debugging
- Never pass raw malformed content to downstream AI blocks

---

## Reliability Rules

**Missing required data:**
- Use a Condition block upstream to verify required variables are not empty before the HTTP Request block runs
- If a required field is missing, route to an error message block — never send an incomplete request

**API failure:**
- Always check `{{outputVar.ok}}` immediately after the block
- Branch on failure — never assume success

**Retry logic:**
- Add a Wait block between retries for flaky endpoints (rate limits, 503s)
- Maximum 2-3 retries before routing to a permanent failure state
- Never retry on 4xx — those are logic or config errors, not transient failures

**Response validation:**
- Verify `{{outputVar.response}}` is non-empty after a 2xx
- Confirm expected fields exist before passing to downstream blocks

---

## Safety Rules

Absolute. No exceptions.

1. Never send undefined or empty variables in the request body — validate upstream first
2. Never hallucinate field names — use only field names confirmed by the user or API documentation
3. Never hardcode API keys, tokens, or passwords in the URL or body — always inject via workflow variable
4. Never send a body with GET, HEAD, or DELETE requests
5. Never omit Content-Type when sending a body — mismatches cause silent failures
6. Never pass raw response strings to downstream AI blocks without labeling the format
7. Never retry on 4xx errors — retrying will not fix a bad request
8. Never generate a DELETE configuration without explicit user confirmation of intent

---

## Example Configurations

### Example 1: GET — Fetch Stock Quote from Finnhub

```
URL          : https://finnhub.io/api/v1/quote?symbol={{ticker}}&token={{finnhubApiKey}}
Method       : GET
Content-Type : none
Headers      :
  Accept : application/json
Body         : (empty)
Output Variable: stockData
```

```
On success: parse {{stockData.response}} — field "c" is current price
On failure: log {{stockData.status}} — check API key and ticker symbol
```

---

### Example 2: POST — Send AI Output to Make Webhook

```
URL          : https://hook.us1.make.com/{{webhookId}}
Method       : POST
Content-Type : application/json
Headers      :
  Content-Type : application/json
Body:
{
  "customer_name": "{{customer_name}}",
  "email": "{{email}}",
  "ai_output": "{{generatedText}}",
  "submitted_at": "{{timestamp}}"
}
Output Variable: makeResponse
```

```
On success: Make returns {"accepted": true} — log and continue
On failure: log {{makeResponse.status}} — verify webhook URL is active
```

---

### Example 3: PATCH — Update a CRM Contact

```
URL          : https://api.hubspot.com/crm/v3/objects/contacts/{{contact_id}}
Method       : PATCH
Content-Type : application/json
Headers      :
  Content-Type  : application/json
  Authorization : Bearer {{hubspotApiKey}}
Body:
{
  "properties": {
    "lead_score": "{{lead_score}}",
    "last_contacted": "{{timestamp}}",
    "notes": "{{ai_summary}}"
  }
}
Output Variable: crmResult
```

```
On success: {{crmResult.ok}} = true — record updated
On 404: contact_id is wrong — check the variable source block
On 422: field name mismatch — verify HubSpot property names
```

---

### Example 4: DELETE — Remove a Resource

```
URL          : https://api.example.com/records/{{record_id}}
Method       : DELETE
Content-Type : none
Headers      :
  Authorization : Bearer {{apiKey}}
Body         : (empty)
Output Variable: deleteResult
```

```
On success: status 204 — no body returned, deletion confirmed
On 404: record_id does not exist or was already deleted
On 403: API key does not have delete permissions
```

---

### Example 5: POST — Trigger a Zapier Webhook

```
URL          : https://hooks.zapier.com/hooks/catch/{{zapId}}/{{hookId}}/
Method       : POST
Content-Type : application/json
Headers      :
  Content-Type : application/json
Body:
{
  "event": "workflow_completed",
  "user_email": "{{email}}",
  "result": "{{ai_output}}",
  "timestamp": "{{timestamp}}"
}
Output Variable: zapierResponse
```

```
On success: Zapier returns {"status": "success"} — trigger confirmed
On failure: log {{zapierResponse.status}} — verify Zap is active and URL is correct
```

---

## Pre-Flight Checklist

**URL and method:**
- [ ] URL is complete and starts with `https://`
- [ ] Method matches the intended operation
- [ ] Dynamic values in the URL use `{{variableName}}` syntax

**Headers:**
- [ ] `Content-Type` is set and matches the body format
- [ ] Auth header is included if the endpoint requires it
- [ ] API key is injected from a variable — not hardcoded

**Body:**
- [ ] Content Type in block settings matches the `Content-Type` header
- [ ] Every field uses a real workflow variable or literal value
- [ ] No field has an undefined or empty variable
- [ ] Body is empty for GET and DELETE requests

**Output:**
- [ ] Output Variable is named and descriptive
- [ ] Downstream blocks check `{{outputVar.ok}}` before using `{{outputVar.response}}`
- [ ] A failure branch exists for `ok = false`
