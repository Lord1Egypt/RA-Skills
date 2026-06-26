---
name: perfexcrm-api
description: >
  Manage PerfexCRM from any messaging app. Full CRUD for customers, invoices,
  leads, tickets, projects, contracts, and 13 more resources (170 API endpoints).
  Check overdue invoices, create leads, reply to tickets, track project progress
  — all through natural conversation on WhatsApp, Telegram, Slack, or Discord.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    primaryEnv: PERFEXCRM_API_KEY
    requires:
      bins:
        - curl
      env:
        - PERFEXCRM_API_URL
        - PERFEXCRM_API_KEY
    links:
      homepage: https://perfexapi.com
      repository: https://github.com/sattip/perfexcrm-api-webhooks-module
      documentation: https://perfexapi.com/docs
    author: OBS Technologies
---

# PerfexCRM API Skill

Manage your entire PerfexCRM installation through conversation. This skill connects to the PerfexCRM API & Webhooks module, giving you access to 170 API endpoints across 19 resources.

**Get the API module:** https://perfexapi.com

## Environment Variables

Set these before using the skill:

```bash
export PERFEXCRM_API_URL="https://your-crm.com/api/v1"
export PERFEXCRM_API_KEY="your-api-key-here"
```

- `PERFEXCRM_API_URL`: Your PerfexCRM installation URL with `/api/v1` suffix
- `PERFEXCRM_API_KEY`: API key created in PerfexCRM Admin > Setup > API & Webhooks > API Keys

## Authentication

All requests use the `X-API-KEY` header. The key controls which resources and operations are available.

## Available Resources (19)

| Resource | List | Get | Create | Update | Delete | Sub-resources |
|----------|:----:|:---:|:------:|:------:|:------:|:---:|
| Customers | ✅ | ✅ | ✅ | ✅ | ✅ | contacts, invoices, estimates, projects, contracts, tickets |
| Invoices | ✅ | ✅ | ✅ | ✅ | ✅ | payments (paginated) |
| Leads | ✅ | ✅ | ✅ | ✅ | ✅ | activity_log, proposals |
| Tickets | ✅ | ✅ | ✅ | ✅ | ✅ | replies, assign, status |
| Projects | ✅ | ✅ | ✅ | ✅ | ✅ | tasks, milestones, files, discussions (all paginated) |
| Contracts | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Tasks | ✅ | ✅ | ✅ | ✅ | ✅ | comments, checklist, followers, timers |
| Estimates | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Proposals | ✅ | ✅ | ✅ | ✅ | ✅ | comments |
| Expenses | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Staff | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Credit Notes | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Subscriptions | ✅ | ✅ | — | — | — | — |
| Payments | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Items | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Contacts | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Timesheets | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Notes | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Utilities | ✅ | — | — | — | — | currencies, countries, taxes, payment_modes, groups |

## Common Operations

### Customers

**List all customers:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/customers"
```

**Search customers:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/customers?search=acme"
```

**Create a customer:**
```bash
curl -s -X POST -H "X-API-KEY: $PERFEXCRM_API_KEY" -H "Content-Type: application/json" \
  "$PERFEXCRM_API_URL/customers" \
  -d '{"company":"Acme Corp","phonenumber":"+1234567890","city":"New York","state":"NY","country":"US"}'
```

**Get a specific customer:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/customers/123"
```

**Get customer's invoices:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/customers/123/invoices"
```

### Invoices

**List all invoices:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/invoices"
```

**Filter overdue invoices:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/invoices?status=overdue"
```

**Create an invoice:**
```bash
curl -s -X POST -H "X-API-KEY: $PERFEXCRM_API_KEY" -H "Content-Type: application/json" \
  "$PERFEXCRM_API_URL/invoices" \
  -d '{"clientid":123,"currency":1,"items":[{"description":"Web Development","qty":1,"rate":2500}]}'
```

**Get invoice payments (paginated):**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/invoices/45/payments?page=1&per_page=25"
```

### Leads

**List leads:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/leads"
```

**Create a lead:**
```bash
curl -s -X POST -H "X-API-KEY: $PERFEXCRM_API_KEY" -H "Content-Type: application/json" \
  "$PERFEXCRM_API_URL/leads" \
  -d '{"name":"John Smith","email":"john@example.com","phonenumber":"+1234567890","company":"TechCorp","source":1,"status":1}'
```

### Tickets

**List open tickets:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/tickets?status=open"
```

**Reply to a ticket:**
```bash
curl -s -X POST -H "X-API-KEY: $PERFEXCRM_API_KEY" -H "Content-Type: application/json" \
  "$PERFEXCRM_API_URL/tickets/55/replies" \
  -d '{"message":"Thank you for reaching out. We are looking into this issue."}'
```

**Assign a ticket:**
```bash
curl -s -X PUT -H "X-API-KEY: $PERFEXCRM_API_KEY" -H "Content-Type: application/json" \
  "$PERFEXCRM_API_URL/tickets/55/assign" \
  -d '{"assigned":3}'
```

### Projects

**List projects:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/projects"
```

**Get project tasks (paginated):**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/projects/10/tasks?page=1&per_page=25"
```

**Get project milestones:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/projects/10/milestones"
```

### Tasks

**Create a task:**
```bash
curl -s -X POST -H "X-API-KEY: $PERFEXCRM_API_KEY" -H "Content-Type: application/json" \
  "$PERFEXCRM_API_URL/tasks" \
  -d '{"name":"Review proposal","rel_id":10,"rel_type":"project","startdate":"2026-03-15","duedate":"2026-03-20","priority":2,"assignees":[3]}'
```

## Pagination

All list endpoints support pagination:

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `page` | 1 | — | Page number |
| `per_page` | 25 | 100 | Results per page |
| `limit` | 25 | 100 | Alias for per_page |

Response includes pagination metadata:
```json
{
  "data": [...],
  "meta": {
    "total": 150,
    "per_page": 25,
    "current_page": 1,
    "last_page": 6,
    "from": 1,
    "to": 25
  }
}
```

## Response Filtering

**Select specific fields:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/customers?fields=id,company,phonenumber"
```

**Include related data:**
```bash
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/projects?include=members,tasks"
```

## Sorting & Search

```bash
# Sort by date descending
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/invoices?sort=date&order=desc"

# Search across all fields
curl -s -H "X-API-KEY: $PERFEXCRM_API_KEY" "$PERFEXCRM_API_URL/customers?search=acme"
```

## Webhook Events (100+)

The module fires 100+ webhook events for real-time notifications. Key events:

- `customer.created`, `customer.updated`, `customer.deleted`
- `invoice.created`, `invoice.paid`, `invoice.overdue`
- `lead.created`, `lead.converted`, `lead.status_changed`
- `ticket.created`, `ticket.reply_added`, `ticket.status_changed`
- `project.created`, `task.created`, `task.completed`
- `payment.received`, `contract.signed`, `estimate.accepted`

## Error Handling

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (missing or invalid parameters) |
| 401 | Unauthorized (invalid or missing API key) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Resource not found |
| 429 | Rate limited |
| 500 | Server error |

## Recommended Agent Behavior

When the user asks about their CRM data:

1. **Always paginate** large result sets — use `?per_page=25` and iterate if needed
2. **Use `?fields=`** to reduce response size — only fetch columns you need
3. **Search first** — use `?search=` before listing all records
4. **Summarize results** — don't dump raw JSON, extract key information
5. **Confirm destructive actions** — ask before deleting records
6. **Use natural language** — translate user intent to the correct API call

## Links

- **Buy PerfexAPI Module:** https://perfexapi.com
- **API Documentation:** https://perfexapi.com/docs
- **Full Changelog:** https://perfexapi.com/changelog
- **MCP Integration:** https://perfexapi.com/mcp (for AI coding tools)
- **n8n Workflows:** https://perfexapi.com/templates/n8n
