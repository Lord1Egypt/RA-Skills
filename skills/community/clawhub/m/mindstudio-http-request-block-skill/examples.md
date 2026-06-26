# HTTP Request Block — Examples

Real-world block configurations for all five scenarios. Each example includes the full block setup, body structure, output variable, and downstream handling.

---

## Example 1: GET — Fetch Stock Quote from Finnhub

**Scenario:** Mid-workflow, fetch the current price of a stock ticker before an AI block decides whether to trigger an alert.

**What the user provided:**
- API: Finnhub
- Ticker variable: `{{ticker}}`
- API key variable: `{{finnhubApiKey}}`
- Needs: current price field `c` from the response

**Block Configuration:**
```
URL          : https://finnhub.io/api/v1/quote?symbol={{ticker}}&token={{finnhubApiKey}}
Method       : GET
Content-Type : none
Headers      :
  Accept : application/json
Body         : (empty)
Output Variable: stockData
```

**Expected Response:**
```json
{
  "c": 189.45,
  "d": -1.23,
  "dp": -0.64,
  "h": 191.00,
  "l": 188.20,
  "o": 190.10,
  "pc": 190.68
}
```

**Downstream Handling:**
```
On success (ok = true):
  - Pass {{stockData.response}} to a downstream Generate Text block
  - Parse the JSON and access current price via .c field
  - Use a Condition block: if price < threshold, trigger alert

On failure (ok = false):
  - Check {{stockData.status}}
  - 401: API key is invalid or missing
  - 422: ticker symbol is not recognized
```

---

## Example 2: GET — Fetch Company News from Finnhub

**Scenario:** Pull the latest news headlines for a stock ticker to feed into an AI analysis block.

**What the user provided:**
- API: Finnhub company news endpoint
- Ticker variable: `{{ticker}}`
- Date range variables: `{{startDate}}`, `{{endDate}}`
- API key variable: `{{finnhubApiKey}}`

**Block Configuration:**
```
URL          : https://finnhub.io/api/v1/company-news
Method       : GET
Content-Type : none
Headers      :
  Accept : application/json
Parameters   :
  symbol : {{ticker}}
  from   : {{startDate}}
  to     : {{endDate}}
  token  : {{finnhubApiKey}}
Body         : (empty)
Output Variable: newsData
```

**Expected Response:**
```json
[
  {
    "category": "company news",
    "datetime": 1712345678,
    "headline": "Apple reports record Q2 earnings",
    "id": 9876543,
    "source": "Reuters",
    "summary": "Apple Inc. reported...",
    "url": "https://reuters.com/..."
  }
]
```

**Downstream Handling:**
```
On success (ok = true):
  - Pass {{newsData.response}} to a Generate Text block
  - Instruct the AI to summarize headlines and flag negative sentiment
  - Combine with stock price data for full context

On failure (ok = false):
  - 403: API plan does not include news endpoint — upgrade required
  - 422: date format is incorrect — verify ISO format YYYY-MM-DD
```

---

## Example 3: POST — Send AI Output to a Make Webhook

**Scenario:** After an AI block qualifies a lead, POST the result to a Make webhook that routes it to a CRM and sends a Slack notification.

**What the user provided:**
- Make webhook URL: `https://hook.us1.make.com/abc123xyz`
- Variables to send: `{{customer_name}}`, `{{email}}`, `{{lead_score}}`, `{{ai_summary}}`, `{{timestamp}}`
- No auth required (Make webhooks are URL-authenticated)

**Block Configuration:**
```
URL          : https://hook.us1.make.com/abc123xyz
Method       : POST
Content-Type : application/json
Headers      :
  Content-Type : application/json
Body:
{
  "customer_name": "{{customer_name}}",
  "email": "{{email}}",
  "lead_score": "{{lead_score}}",
  "ai_summary": "{{ai_summary}}",
  "submitted_at": "{{timestamp}}"
}
Output Variable: makeResponse
```

**Expected Response:**
```json
{
  "accepted": true
}
```

**Downstream Handling:**
```
On success (ok = true):
  - Make returns {"accepted": true} — data was received
  - Log result and continue workflow

On failure (ok = false):
  - 404: webhook URL has been deactivated — check Make scenario
  - 400: body is malformed — verify all variable names are correct
```

---

## Example 4: POST — Submit Lead Form Data to HubSpot

**Scenario:** After a user completes an onboarding flow, create a new contact in HubSpot via the CRM API.

**What the user provided:**
- API: HubSpot Contacts API
- API key variable: `{{hubspotApiKey}}`
- Variables: `{{first_name}}`, `{{last_name}}`, `{{email}}`, `{{company}}`, `{{phone}}`

**Block Configuration:**
```
URL          : https://api.hubspot.com/crm/v3/objects/contacts
Method       : POST
Content-Type : application/json
Headers      :
  Content-Type  : application/json
  Authorization : Bearer {{hubspotApiKey}}
Body:
{
  "properties": {
    "firstname": "{{first_name}}",
    "lastname": "{{last_name}}",
    "email": "{{email}}",
    "company": "{{company}}",
    "phone": "{{phone}}"
  }
}
Output Variable: hubspotResult
```

**Expected Response:**
```json
{
  "id": "101",
  "properties": {
    "email": "jordan@example.com",
    "firstname": "Jordan",
    "lastname": "Ellis"
  },
  "createdAt": "2025-04-03T14:22:00Z"
}
```

**Downstream Handling:**
```
On success (ok = true):
  - Parse {{hubspotResult.response}} to extract contact ID
  - Store ID in a variable for use in downstream PATCH or follow-up blocks

On failure (ok = false):
  - 409: contact already exists — use PATCH to update instead
  - 401: API key is invalid or expired
  - 422: field name mismatch — verify HubSpot property names exactly
```

---

## Example 5: PATCH — Update a CRM Contact Record

**Scenario:** After an AI block scores a lead, write the updated score and summary back to the existing HubSpot contact.

**What the user provided:**
- API: HubSpot Contacts API
- Contact ID variable: `{{contact_id}}`
- Fields to update: `{{lead_score}}`, `{{ai_summary}}`, `{{timestamp}}`
- API key variable: `{{hubspotApiKey}}`

**Block Configuration:**
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
    "last_ai_summary": "{{ai_summary}}",
    "last_updated": "{{timestamp}}"
  }
}
Output Variable: patchResult
```

**Expected Response:**
```json
{
  "id": "101",
  "properties": {
    "lead_score": "87",
    "last_updated": "2025-04-03T15:00:00Z"
  }
}
```

**Downstream Handling:**
```
On success (ok = true):
  - Record updated — log {{patchResult.status}} (200) and continue

On failure (ok = false):
  - 404: contact_id does not exist — check the variable source block
  - 422: property name is wrong — verify exact HubSpot field names
  - 401: token expired — refresh API key
```

---

## Example 6: PUT — Replace a Full Record in Airtable

**Scenario:** Replace an entire row in an Airtable base with updated data generated by the workflow.

**What the user provided:**
- API: Airtable REST API
- Base ID variable: `{{airtableBaseId}}`
- Table name: `Projects`
- Record ID variable: `{{record_id}}`
- API key variable: `{{airtableApiKey}}`
- Full record variables: `{{project_name}}`, `{{status}}`, `{{owner}}`, `{{due_date}}`, `{{notes}}`

**Block Configuration:**
```
URL          : https://api.airtable.com/v0/{{airtableBaseId}}/Projects/{{record_id}}
Method       : PUT
Content-Type : application/json
Headers      :
  Content-Type  : application/json
  Authorization : Bearer {{airtableApiKey}}
Body:
{
  "fields": {
    "Project Name": "{{project_name}}",
    "Status": "{{status}}",
    "Owner": "{{owner}}",
    "Due Date": "{{due_date}}",
    "Notes": "{{notes}}"
  }
}
Output Variable: airtableResult
```

**Expected Response:**
```json
{
  "id": "recXyz123",
  "fields": {
    "Project Name": "Q2 Campaign",
    "Status": "In Progress"
  },
  "createdTime": "2025-03-01T10:00:00.000Z"
}
```

**Downstream Handling:**
```
On success (ok = true):
  - Full record replaced — log record ID from {{airtableResult.response}}

On failure (ok = false):
  - 404: record_id is wrong or record was deleted
  - 422: field name does not match Airtable column name exactly — names are case-sensitive
```

---

## Example 7: DELETE — Remove a Record from an External API

**Scenario:** After a workflow determines a temporary record is no longer needed, delete it from an external project management API.

**What the user provided:**
- API: internal project tool
- Record ID variable: `{{project_id}}`
- API key variable: `{{projectApiKey}}`
- User confirmed: deletion is intentional and permanent

**Block Configuration:**
```
URL          : https://api.projecttool.example.com/projects/{{project_id}}
Method       : DELETE
Content-Type : none
Headers      :
  Authorization : Bearer {{projectApiKey}}
Body         : (empty)
Output Variable: deleteResult
```

**Expected Response:**
```
Status: 204 No Content
Body: (empty)
```

**Downstream Handling:**
```
On success (ok = true):
  - Status 204 with no body is the standard success response for DELETE
  - Do not attempt to parse {{deleteResult.response}} — it will be empty
  - Log {{deleteResult.status}} and route to confirmation step

On failure (ok = false):
  - 404: record does not exist or was already deleted
  - 403: API key does not have delete permissions — check scope
  - Never retry a DELETE on 4xx — the request is invalid, not transient
```

---

## Example 8: POST — Trigger a Zapier Webhook

**Scenario:** After an AI workflow completes a document, fire a Zapier webhook that emails the result to the user and logs it in Google Sheets.

**What the user provided:**
- Zapier webhook URL: `https://hooks.zapier.com/hooks/catch/{{zapId}}/{{hookId}}/`
- Variables: `{{email}}`, `{{document_title}}`, `{{ai_output}}`, `{{timestamp}}`
- No auth required

**Block Configuration:**
```
URL          : https://hooks.zapier.com/hooks/catch/{{zapId}}/{{hookId}}/
Method       : POST
Content-Type : application/json
Headers      :
  Content-Type : application/json
Body:
{
  "event": "document_completed",
  "user_email": "{{email}}",
  "document_title": "{{document_title}}",
  "content": "{{ai_output}}",
  "completed_at": "{{timestamp}}"
}
Output Variable: zapierResponse
```

**Expected Response:**
```json
{
  "status": "success",
  "id": "zap_run_abc123"
}
```

**Downstream Handling:**
```
On success (ok = true):
  - Zapier returns {"status": "success"} — trigger confirmed
  - Log and end workflow or continue to next step

On failure (ok = false):
  - 404: Zap is turned off or URL is wrong — check Zapier dashboard
  - 400: body is malformed — verify all variable names resolve correctly
```

---

## Common Patterns Across All Examples

| Pattern | Rule |
|---|---|
| Auth header | Always inject via `{{variable}}` — never hardcode |
| Output variable naming | Use descriptive names: `stockData`, `crmResult`, `makeResponse` |
| Response parsing | Always pass `{{outputVar.response}}` to a downstream block before accessing fields |
| Failure branching | Always check `{{outputVar.ok}}` immediately after the block |
| GET requests | Never include a body — set Content-Type to `none` |
| DELETE requests | Confirm intent before configuring — action is permanent |
| 4xx errors | Never retry — fix the request logic upstream |
