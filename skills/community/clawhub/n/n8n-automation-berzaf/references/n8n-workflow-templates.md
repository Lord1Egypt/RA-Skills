# n8n Workflow Templates

Import these JSON snippets into your n8n instance.
Each one matches exactly one webhook endpoint in the SKILL.md.

---

## How to Import

1. Open your n8n instance
2. Click "New Workflow"
3. Click the three-dot menu → "Import from JSON"
4. Paste the JSON below
5. Update any credentials (email, CRM, social accounts)
6. Activate the workflow
7. Copy the webhook URL into your `N8N_WEBHOOK_BASE_URL`

---

## Workflow 1 — Lead Nurture Email Sequence

**Webhook path:** `/webhook/lead-nurture`  
**Trigger:** POST request from OpenClaw  

**Nodes needed in n8n:**
- Webhook (trigger)
- Wait node (Day 1, Day 3, Day 7, Day 14)
- Send Email node x4 (Gmail or SMTP)
- Google Sheets / Airtable node (log the lead)

**n8n JSON template:**
```json
{
  "name": "Lead Nurture Sequence",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "lead-nurture",
        "responseMode": "responseNode",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Log to Sheet",
      "type": "n8n-nodes-base.googleSheets",
      "parameters": {
        "operation": "append",
        "sheetId": "YOUR_SHEET_ID",
        "range": "Leads!A:F",
        "values": {
          "Name": "={{ $json.first_name }}",
          "Email": "={{ $json.email }}",
          "Source": "={{ $json.source }}",
          "Date": "={{ $now }}"
        }
      }
    },
    {
      "name": "Day 1 Email",
      "type": "n8n-nodes-base.gmail",
      "parameters": {
        "to": "={{ $json.email }}",
        "subject": "Welcome {{ $json.first_name }} — here's what's next",
        "message": "Hi {{ $json.first_name }},\n\nThanks for connecting..."
      }
    },
    {
      "name": "Wait 3 Days",
      "type": "n8n-nodes-base.wait",
      "parameters": {
        "amount": 3,
        "unit": "days"
      }
    },
    {
      "name": "Day 3 Value Email",
      "type": "n8n-nodes-base.gmail",
      "parameters": {
        "to": "={{ $('Webhook').item.json.email }}",
        "subject": "{{ $('Webhook').item.json.first_name }}, quick tip for you",
        "message": "Hey {{ $('Webhook').item.json.first_name }},\n\nHere is something valuable..."
      }
    },
    {
      "name": "Respond to OpenClaw",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "respondWith": "json",
        "responseBody": "{\"status\": \"queued\", \"sequence_id\": \"seq_{{ $now.toMillis() }}\"}"
      }
    }
  ]
}
```

---

## Workflow 2 — Social Media Auto-Post

**Webhook path:** `/webhook/social-post`  
**Trigger:** POST request from OpenClaw  

**Nodes needed in n8n:**
- Webhook (trigger)
- IF node (check which platforms)
- Twitter/X node
- LinkedIn node
- Facebook node
- Respond to Webhook node

**Key setup:**
- Connect your social accounts in n8n credentials
- The `platforms` array from OpenClaw determines which branches run

**Payload received:**
```json
{
  "content": "Your post text here",
  "platforms": ["linkedin", "x"],
  "schedule_time": null,
  "hashtags": ["automation", "n8n"]
}
```

**Response format:**
```json
{
  "status": "posted",
  "post_ids": {
    "linkedin": "urn:li:share:xxxxx",
    "x": "1234567890"
  }
}
```

---

## Workflow 3 — Meeting Follow-Up

**Webhook path:** `/webhook/meeting-followup`  
**Trigger:** POST request from OpenClaw  

**Nodes needed:**
- Webhook (trigger)
- Set node (build email body from action items array)
- Gmail/SMTP node (send follow-up)
- Google Sheets node (log meeting)
- Respond to Webhook node

**Email template to use in n8n:**
```
Subject: Great connecting today, {{ contact_name }} — next steps inside

Hi {{ contact_name }},

Really enjoyed our conversation today about {{ meeting_topic }}.

As promised, here are our agreed action items:
{{ action_items | join('\n- ', '- ') }}

{{ next_step ? 'Next step: ' + next_step : '' }}

Looking forward to moving this forward.

Best,
[Your Name]
```

---

## Workflow 4 — CRM Contact Update

**Webhook path:** `/webhook/crm-update`  
**Trigger:** POST request from OpenClaw  

**Supported CRMs (pick one):**
- Google Sheets (free, simple)
- Airtable (free tier available)
- HubSpot (free CRM)
- GoHighLevel
- Any CRM with n8n integration

**For Google Sheets CRM setup:**
```
Sheet columns: Name | Email | Status | Notes | Follow-Up Date | Last Updated
```

**n8n flow:**
1. Webhook receives payload
2. Search existing contacts by email
3. If found → update row
4. If not found → create new row
5. Respond with contact_id

---

## Workflow 5 — Competitor Monitor

**Webhook path:** `/webhook/competitor-monitor`  
**Trigger:** POST request from OpenClaw (or daily cron)  

**Nodes needed:**
- Webhook (trigger)
- HTTP Request node x N (one per competitor URL)
- HTML Extract node (scrape pricing, headlines, changes)
- AI/LLM node (summarize changes using Claude API)
- Respond to Webhook with formatted markdown report

**Competitor list — set in n8n as workflow variables:**
```json
{
  "competitors": [
    {"name": "Competitor A", "url": "https://competitor-a.com/pricing"},
    {"name": "Competitor B", "url": "https://competitor-b.com/blog"},
    {"name": "Competitor C", "url": "https://competitor-c.com"}
  ]
}
```

**Response format:**
```json
{
  "status": "complete",
  "report": "# Competitor Report — March 2026\n\n## Competitor A\n..."
}
```

---

## Workflow 6 — Invoice Reminder

**Webhook path:** `/webhook/invoice-reminder`  
**Trigger:** POST request from OpenClaw  

**Email tone by reminder_type:**
- `first` — Friendly: "Just a gentle reminder..."
- `second` — Firm: "Following up on our previous message..."
- `final` — Urgent: "This invoice is now [X] days overdue..."

**Gmail template variables:**
```
To: {{ client_email }}
Subject: 
  first: "Invoice #{{ invoice_number }} — Friendly Reminder"
  second: "Invoice #{{ invoice_number }} — Second Notice"
  final: "URGENT: Invoice #{{ invoice_number }} — Final Notice"
```

---

## Workflow 7 — Content Repurpose

**Webhook path:** `/webhook/content-repurpose`  
**Trigger:** POST request from OpenClaw  

**Nodes needed:**
- Webhook (trigger)
- HTTP Request node (fetch URL content or YouTube transcript)
- Claude/OpenAI API node (repurpose into 4 formats)
- Respond to Webhook with all content versions

**Claude prompt to use in n8n:**
```
You are a content repurposing expert. Given the following content:

{{ $json.scraped_content }}

Create 4 versions:

1. TWITTER/X THREAD (8-12 tweets, hook tweet first, end with CTA)
2. LINKEDIN POST (professional tone, 150-300 words, 3-5 hashtags)
3. EMAIL SNIPPET (50-100 words, conversational, for newsletter)
4. SHORT HOOK (one punchy sentence for Reels/TikTok caption)

Brand voice: {{ $json.brand_voice }}

Return as JSON with keys: thread, linkedin, email, hook
```

---

## Workflow 8 — Daily Briefing

**Webhook path:** `/webhook/daily-briefing`  
**Trigger:** POST request from OpenClaw (or 8am cron job)  

**Nodes needed:**
- Webhook (trigger)
- Google Sheets node (new leads last 24h)
- Gmail node (count unread emails)
- Twitter/LinkedIn API (yesterday's engagement)
- AI node (summarize + generate top 3 priorities)
- Respond to Webhook with full briefing

**Briefing markdown format:**
```markdown
# Daily Briefing — {{ date }}

## New Leads (Last 24 Hours)
- {{ lead_count }} new leads
- Hottest: {{ top_lead_name }} from {{ source }}

## Email Inbox
- {{ unread_count }} unread emails
- {{ urgent_count }} marked urgent

## Social Performance (Yesterday)
- LinkedIn: {{ li_impressions }} impressions, {{ li_engagements }} engagements
- X: {{ x_impressions }} impressions, {{ x_followers_delta }} new followers

## Your Top 3 Priorities Today
1. {{ priority_1 }}
2. {{ priority_2 }}
3. {{ priority_3 }}
```

---

## Health Check Endpoint

Set up a simple health check in n8n:

**Webhook path:** `/webhook/health`  
**Method:** GET  
**Response:**
```json
{
  "status": "ok",
  "instance": "your-n8n-instance",
  "workflows_active": 8,
  "timestamp": "ISO timestamp"
}
```

This is what OpenClaw calls when you type "n8n status".

---

## Quick Setup Checklist

- [ ] n8n instance running (cloud or self-hosted)
- [ ] All 8 workflows imported and activated
- [ ] Credentials connected (Gmail, social, CRM)
- [ ] Webhook URLs noted
- [ ] N8N_WEBHOOK_BASE_URL exported in terminal
- [ ] N8N_API_KEY exported in terminal
- [ ] OpenClaw gateway restarted
- [ ] "n8n status" test passed
- [ ] Test trigger for Workflow 1 sent successfully
