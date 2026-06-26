---
name: cold-email
description: Generate hyper-personalized cold email sequences using AI. Turn lead data into high-converting outreach campaigns.
metadata:
  clawdbot:
    requires:
      env:
        - SKILLBOSS_API_KEY
---

# SkillBoss API Hub - AI Cold Email Generator

Generate personalized cold email sequences from lead data. SkillBoss API Hub uses AI to research prospects and craft unique, relevant outreach - not templates.

## Setup

1. Get your API key at https://app.skillbossai.com/settings (Integrations → API Keys)
2. Set `SKILLBOSS_API_KEY` in your environment

## How It Works

This skill calls the SkillBoss API Hub (`POST https://api.skillbossai.com/v1/pilot`) with `type: "chat"` to generate personalized cold email sequences for each lead. The AI automatically researches the lead's context and crafts relevant outreach based on company, title, and LinkedIn/website data.

## Endpoints

All requests go to the SkillBoss API Hub unified endpoint:

```
POST https://api.skillbossai.com/v1/pilot
Authorization: Bearer {SKILLBOSS_API_KEY}
Content-Type: application/json
```

### Single Lead — Generate Email Sequence

Generate a cold email sequence for one lead (3–5 emails per lead). The request uses `type: "chat"` with a structured prompt containing lead data and sequence options.

```json
{
  "type": "chat",
  "inputs": {
    "messages": [
      {
        "role": "system",
        "content": "You are an expert cold email copywriter. Generate personalized cold email sequences based on lead data. Each email should be unique, relevant, and high-converting. Return a JSON object with a 'sequence' array."
      },
      {
        "role": "user",
        "content": "Generate a cold email sequence for this lead:\n\nName: {lead.name}\nTitle: {lead.title}\nCompany: {lead.company}\nEmail: {lead.email}\nCompany Website: {lead.company_website}\nLinkedIn: {lead.linkedin_url}\n\nOptions:\n- Number of emails: {options.email_count}\n- Signature: {options.email_signature}\n- Campaign angle: {options.campaign_angle}\n- CTAs to use: {options.approved_ctas}\n\nReturn JSON: {\"sequence\": [{\"step\": 1, \"subject\": \"...\", \"body\": \"...\"}, ...]}"
      }
    ]
  },
  "prefer": "quality"
}
```

**Response (200):**
```json
{
  "status": "success",
  "result": {
    "choices": [
      {
        "message": {
          "content": "{\"sequence\": [{\"step\": 1, \"subject\": \"...\", \"body\": \"...\"}, {\"step\": 2, \"subject\": \"...\", \"body\": \"...\"}, {\"step\": 3, \"subject\": \"...\", \"body\": \"...\"}]}"
        }
      }
    ]
  }
}
```

**Parsing the result:**
```python
import json
raw = response.json()["result"]["choices"][0]["message"]["content"]
sequence = json.loads(raw)["sequence"]
```

### Batch — Generate for Multiple Leads

For multiple leads, call the endpoint once per lead or construct a batch prompt:

```json
{
  "type": "chat",
  "inputs": {
    "messages": [
      {
        "role": "system",
        "content": "You are an expert cold email copywriter. Generate personalized cold email sequences for each lead. Return a JSON object with a 'leads' array."
      },
      {
        "role": "user",
        "content": "Generate cold email sequences for these leads:\n\n{leads_json}\n\nOptions: email_count={options.email_count}, list_name={options.list_name}\n\nReturn JSON: {\"leads\": [{\"email\": \"...\", \"sequence\": [{\"step\": 1, \"subject\": \"...\", \"body\": \"...\"}]}]}"
      }
    ]
  },
  "prefer": "quality"
}
```

**Response parsing:**
```python
raw = response.json()["result"]["choices"][0]["message"]["content"]
result = json.loads(raw)
leads_with_sequences = result["leads"]
```

## Python Code Example

```python
import requests, os, json

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillbossai.com/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

def generate_cold_email_sequence(lead: dict, options: dict = None) -> list:
    """Generate a personalized cold email sequence for one lead."""
    if options is None:
        options = {}

    email_count = options.get("email_count", 3)
    signature = options.get("email_signature", "")
    angle = options.get("campaign_angle", "")
    ctas = options.get("approved_ctas", [])

    user_content = (
        f"Generate a cold email sequence for this lead:\n\n"
        f"Name: {lead.get('name', '')}\n"
        f"Title: {lead.get('title', '')}\n"
        f"Company: {lead.get('company', '')}\n"
        f"Email: {lead.get('email', '')}\n"
        f"Company Website: {lead.get('company_website', '')}\n"
        f"LinkedIn: {lead.get('linkedin_url', '')}\n\n"
        f"Options:\n"
        f"- Number of emails: {email_count}\n"
        f"- Signature: {signature}\n"
        f"- Campaign angle: {angle}\n"
        f"- CTAs to use: {ctas}\n\n"
        f'Return JSON: {{"sequence": [{{"step": 1, "subject": "...", "body": "..."}}, ...]}}'
    )

    result = pilot({
        "type": "chat",
        "inputs": {
            "messages": [
                {"role": "system", "content": "You are an expert cold email copywriter. Generate personalized cold email sequences based on lead data. Each email should be unique, relevant, and high-converting. Return a JSON object with a 'sequence' array."},
                {"role": "user", "content": user_content}
            ]
        },
        "prefer": "quality"
    })

    raw = result["result"]["choices"][0]["message"]["content"]
    return json.loads(raw)["sequence"]
```

## Lead Fields

Each lead must include a valid **`email`**; it is used to map the lead through processing. All other fields are optional but improve personalization.

| Field | Required | Description |
|-------|----------|-------------|
| `email` | **Yes** | Lead's email address |
| `name` | No | Full name or first name (improves personalization) |
| `company` | No | Company name (improves personalization) |
| `title` | No | Job title (improves personalization) |
| `company_website` | No | Company URL for research |
| `linkedin_url` | No | LinkedIn profile for deeper personalization |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `list_name` | string | Auto | Display name for this list |
| `email_count` | number | 3 | Emails per lead (1-5) |
| `email_signature` | string | None | Signature appended to emails |
| `campaign_angle` | string | None | Context for personalization |
| `approved_ctas` | array | None | CTAs to use in emails |

## Response Format (SkillBoss API Hub)

| 能力 | pilot type | 结果路径 |
|------|-----------|---------|
| Cold email generation | `chat` | `result.choices[0].message.content` (JSON string, parse with `json.loads`) |

## Errors

| Code | Description |
|------|-------------|
| 400 | Invalid request body |
| 401 | Invalid or missing SKILLBOSS_API_KEY |
| 429 | Rate limit exceeded; retry later |

## Usage Examples

"Generate a cold email for the VP of Sales at Stripe"
"Create outreach sequences for these 10 leads"
"Write a 3-email sequence targeting marketing directors at SaaS companies"
