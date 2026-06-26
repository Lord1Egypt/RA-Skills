---
name: instantly-campaign-builder
description: Create and manage Instantly.ai email campaigns via API. Use when the user wants to create a cold email campaign, add leads to Instantly, configure email sequences with variables, set up A/B testing variants, activate a campaign, or manage outbound email automation. Triggers on any mention of Instantly, cold email campaign, outbound sequence, email outreach, lead import, or campaign activation.
metadata: {"openclaw":{"primaryEnv":"INSTANTLY_API_KEY","requires":{"env":["INSTANTLY_API_KEY"]}}}
---

# Instantly Campaign Builder

Build and manage Instantly.ai cold email campaigns via API v2.

## Auth

All requests require:
```
Authorization: Bearer {INSTANTLY_API_KEY}
Content-Type: application/json
Base URL: https://api.instantly.ai
```

## Workflow — Follow this order

### Step 1: Create the campaign

`POST /api/v2/campaigns`

Required fields:
- `name` — campaign name
- `email_list` — array of sender email addresses
- `sequences` — message steps (see Step 2)

Optional but recommended:
- `daily_limit` — max emails per day
- `daily_max_leads` — max new leads contacted per day
- `email_gap` — seconds between sends
- `open_tracking`, `link_tracking` — boolean
- `stop_on_reply`, `stop_on_auto_reply`, `stop_for_company` — boolean
- `text_only`, `first_email_text_only` — boolean
- `campaign_schedule` — object with `start_date`, `end_date`, `schedules` (times/days/timezone)

### Step 2: Configure sequences (messages)

The `sequences` field is an array but **only the first element is used**. Put all steps in one item.

Each step has:
- `type`: always `"email"`
- `delay`: number (wait before this step)
- `delay_unit`: `"minutes"`, `"hours"`, or `"days"`
- `variants`: array of message variants (A/B testing)

Each variant has:
- `subject`: email subject line
- `body`: email body (HTML or plain text)
- `v_disabled`: boolean (set `true` to disable a variant)

**Variable syntax in subject and body:** `{{variableName}}`

Core variables: `{{firstName}}`, `{{lastName}}`, `{{companyName}}`, `{{email}}`, `{{phone}}`, `{{website}}`

Custom variables: any name, e.g. `{{city}}`, `{{offer}}`, `{{icebreaker}}`

Example 3-step ARA sequence:
```json
{
  "sequences": [
    {
      "steps": [
        {
          "type": "email",
          "delay": 0,
          "delay_unit": "days",
          "variants": [
            {
              "subject": "{{firstName}}, {{offer}}",
              "body": "Bonjour {{firstName}},\n\n{{icebreaker}}\n\nNous proposons {{offer}} pour les entreprises à {{city}}.\n\nCordialement"
            }
          ]
        },
        {
          "type": "email",
          "delay": 3,
          "delay_unit": "days",
          "variants": [
            {
              "subject": "Re: {{firstName}}, suite à mon message",
              "body": "{{firstName}},\n\nJe me permets de relancer..."
            }
          ]
        },
        {
          "type": "email",
          "delay": 5,
          "delay_unit": "days",
          "variants": [
            {
              "subject": "Dernière relance {{firstName}}",
              "body": "{{firstName}},\n\nDernier message de ma part..."
            }
          ]
        }
      ]
    }
  ]
}
```

### Step 3: Declare campaign variables

`POST /api/v2/campaigns/{campaign_id}/variables`

```json
{
  "variables": ["firstName", "companyName", "city", "offer", "icebreaker"]
}
```

Declare every custom variable name used in your sequences here.

### Step 4: Add leads

**Single lead:** `POST /api/v2/leads`
```json
{
  "email": "lead@example.com",
  "first_name": "Jean",
  "last_name": "Dupont",
  "company_name": "Acme SAS",
  "campaign": "campaign-uuid",
  "custom_variables": {
    "city": "Paris",
    "offer": "audit IA gratuit",
    "icebreaker": "J'ai vu votre post LinkedIn sur la transformation digitale"
  }
}
```

**Bulk (max 1000 per request):** `POST /api/v2/leads/add`
```json
{
  "campaign_id": "campaign-uuid",
  "leads": [
    {
      "email": "lead1@example.com",
      "first_name": "Jean",
      "last_name": "Dupont",
      "company_name": "Acme SAS",
      "custom_variables": { "city": "Paris", "offer": "audit IA gratuit" }
    },
    {
      "email": "lead2@example.com",
      "first_name": "Marie",
      "last_name": "Martin",
      "company_name": "Beta Corp",
      "custom_variables": { "city": "Lyon", "offer": "démo chatbot" }
    }
  ]
}
```

Notes:
- Use `campaign_id` OR `list_id`, not both
- If `campaign` is provided on single lead, `email` is required
- Deduplication flags: `skip_if_in_campaign`, `skip_if_in_workspace`, `skip_if_in_list`

### Step 5: Activate the campaign

`POST /api/v2/campaigns/{campaign_id}/activate`

Only activate after leads are added and sequences are configured.

### Modifying an existing campaign

`PATCH /api/v2/campaigns/{campaign_id}`

Same `sequences` structure as creation. Use this to update messages after campaign is created.

## A/B Testing

Add multiple variants per step:
```json
{
  "type": "email",
  "delay": 0,
  "delay_unit": "days",
  "variants": [
    {
      "subject": "Version A — {{firstName}}",
      "body": "Approche directe...",
      "v_disabled": false
    },
    {
      "subject": "Version B — {{firstName}}",
      "body": "Approche soft...",
      "v_disabled": false
    }
  ]
}
```

## Required API Scopes

- Leads: `leads:create`, `leads:all`, `all:create`, or `all:all`
- Campaigns: `campaigns:create`, `campaigns:all`, `all:create`, or `all:all`
- Campaign update: `campaigns:update`, `campaigns:all`, `all:update`, or `all:all`

## Checklist before activation

1. Campaign created with sequences and variables in subject/body
2. Variables declared via `/campaigns/{id}/variables`
3. Leads added with matching `custom_variables`
4. Sender emails configured and warmed up
5. Schedule set if needed
6. Campaign activated via `/campaigns/{id}/activate`
