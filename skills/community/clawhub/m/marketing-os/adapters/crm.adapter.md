# CRM Adapter

## Purpose
Interface specification for connecting CRM systems to the Marketing OS for customer data, lead management, and campaign targeting.

---

## Interface Contract

### Adapter Name
`crm`

### Supported Operations

| Operation | Method | Description |
|---|---|---|
| `get_contacts` | GET | Retrieve contact/lead list with filters |
| `get_segments` | GET | Retrieve audience segments |
| `create_segment` | POST | Create a new audience segment |
| `update_contact` | PUT | Update contact properties |
| `get_deal_pipeline` | GET | Retrieve sales pipeline data |
| `log_activity` | POST | Log marketing touchpoint on a contact |
| `get_campaign_contacts` | GET | Get contacts associated with a campaign |
| `sync_feedback` | POST | Push campaign feedback/results back to CRM |

---

### Input Schema (Request)

```json
{
  "operation": "string — one of the supported operations",
  "parameters": {
    "filters": {
      "segment_id": "string",
      "tags": ["string"],
      "status": "string — active | lead | customer | churned",
      "created_after": "ISO 8601",
      "custom_fields": { "key": "value" }
    },
    "contact_id": "string — for single contact operations",
    "segment_definition": {
      "name": "string",
      "rules": [
        {
          "field": "string",
          "operator": "equals | contains | greater_than | less_than | in",
          "value": "any"
        }
      ]
    },
    "activity": {
      "type": "email_sent | ad_impression | page_visit | form_submit | purchase",
      "campaign_id": "string",
      "timestamp": "ISO 8601",
      "metadata": {}
    },
    "limit": "number",
    "offset": "number"
  },
  "auth": {
    "method": "api_key | oauth2",
    "credentials_ref": "string"
  }
}
```

### Output Schema (Response)

```json
{
  "adapter": "crm",
  "operation": "string",
  "timestamp": "ISO 8601",
  "status": "success | partial | error",
  "data": {
    "contacts": [
      {
        "contact_id": "string",
        "email": "string",
        "name": "string",
        "company": "string",
        "status": "string",
        "segment_ids": ["string"],
        "tags": ["string"],
        "lifetime_value": "number",
        "last_activity": "ISO 8601",
        "custom_fields": {}
      }
    ],
    "segments": [
      {
        "segment_id": "string",
        "name": "string",
        "size": "number",
        "created_at": "ISO 8601"
      }
    ],
    "total_results": "number",
    "has_more": "boolean"
  },
  "metadata": {
    "source": "string — CRM name (e.g., HubSpot, Salesforce, Pipedrive)",
    "sync_timestamp": "ISO 8601",
    "rate_limit_remaining": "number"
  },
  "error": {
    "code": "string",
    "message": "string",
    "retryable": "boolean"
  }
}
```

---

## Potential CRM Systems

| CRM | API | Notes |
|---|---|---|
| HubSpot | REST API v3 | Free tier available, good for startups |
| Salesforce | REST API | Enterprise-grade, complex setup |
| Pipedrive | REST API | Sales-focused, simpler API |
| Airtable | REST API | Lightweight, flexible schema |
| Notion (as CRM) | REST API | Minimal, good for solo operators |

---

## Integration Steps

1. Implement the adapter interface for your chosen CRM
2. Register in `configs/system.config.json` under `adapters.crm`
3. Set `enabled: true`, provide endpoint and auth
4. Test with `get_contacts` call
5. The Marketing Operator will use this adapter to:
   - Target campaign audiences
   - Log marketing activities on contacts
   - Sync campaign results back to CRM

---

## Data Privacy

- All contact data must comply with GDPR/CCPA
- PII should never be stored in Marketing OS memory — reference by contact_id only
- Log activities but not personal data in execution logs
- Implement data deletion endpoint for compliance requests
