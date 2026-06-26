---
name: forms-for-google-drive
description: |
  Google Forms API integration with managed OAuth. Create forms, add questions, export responses to Excel, and summarize response data. Use this skill when users want to create surveys, manage Google Forms, analyze responses, or export form data. Requires a free API key from the Forms for Google Drive App.
compatibility: Requires network access and valid Forms for Google Drive API key
metadata:
  author: burningflower
  version: "1.0"
  clawdbot:
    emoji: 📋
    requires:
      env:
        - GFORMS_API_KEY
---

# Forms for Google Drive

Access Google Forms with managed OAuth authentication. Create forms, add questions, retrieve and export responses to Excel — all via natural language.

## Quick Start

```python
import urllib.request, os, json
req = urllib.request.Request('https://api.gformsfree.com/skill/forms/list')
req.add_header('Authorization', f'Bearer {os.environ["GFORMS_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

## Base URL

```
https://api.gformsfree.com/skill
```

## Authentication

All requests require the API key in the Authorization header:

```
Authorization: Bearer $GFORMS_API_KEY
```

**Environment Variable:** Set your API key as `GFORMS_API_KEY`:

```bash
export GFORMS_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Download the Forms for Google Drive App:
   https://apps.apple.com/us/app/forms-for-google-drive/id6468928038
2. Sign in with your Google account
3. Go to **Settings → Connect AI Agent**
4. Copy your API key

---

## API Reference

### List Forms

```bash
GET /forms/list
```

```python
import urllib.request, os, json
req = urllib.request.Request('https://api.gformsfree.com/skill/forms/list')
req.add_header('Authorization', f'Bearer {os.environ["GFORMS_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

**Response:**
```json
{
  "forms": [
    {
      "formId": "1BxiM...",
      "title": "Customer Feedback",
      "responderUri": "https://forms.gle/xxx",
      "editUri": "https://docs.google.com/forms/d/xxx/edit"
    }
  ]
}
```

---

### Get Form

```bash
GET /forms/{formId}
```

```python
import urllib.request, os, json
req = urllib.request.Request('https://api.gformsfree.com/skill/forms/FORM_ID')
req.add_header('Authorization', f'Bearer {os.environ["GFORMS_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

---

### Create Form

Create a new Google Form with questions in a single request.

```bash
POST /forms/create
```

```python
import urllib.request, os, json
data = json.dumps({
  "title": "Customer Feedback Survey",
  "description": "We'd love to hear from you.",
  "questions": [
    {
      "type": "TEXT",
      "title": "What is your name?",
      "required": True
    },
    {
      "type": "RADIO",
      "title": "How satisfied are you?",
      "required": True,
      "options": ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied"]
    },
    {
      "type": "SCALE",
      "title": "Rate your experience",
      "low": 1,
      "high": 5,
      "lowLabel": "Poor",
      "highLabel": "Excellent"
    },
    {
      "type": "CHECKBOX",
      "title": "Which features do you use?",
      "options": ["Feature A", "Feature B", "Feature C"]
    }
  ]
}).encode()
req = urllib.request.Request(
  'https://api.gformsfree.com/skill/forms/create',
  data=data, method='POST'
)
req.add_header('Authorization', f'Bearer {os.environ["GFORMS_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

**Response:**
```json
{
  "formId": "1BxiM...",
  "responderUri": "https://forms.gle/xxx",
  "editUri": "https://docs.google.com/forms/d/xxx/edit"
}
```

**Question types:** `TEXT` · `RADIO` · `CHECKBOX` · `SCALE` · `DATE` · `TIME`

---

### List Responses

```bash
GET /forms/{formId}/responses
```

```python
import urllib.request, os, json
req = urllib.request.Request('https://api.gformsfree.com/skill/forms/FORM_ID/responses')
req.add_header('Authorization', f'Bearer {os.environ["GFORMS_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

---

### Summarize Responses

Get a natural language summary of all form responses.

```bash
GET /forms/{formId}/summary
```

```python
import urllib.request, os, json
req = urllib.request.Request('https://api.gformsfree.com/skill/forms/FORM_ID/summary')
req.add_header('Authorization', f'Bearer {os.environ["GFORMS_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

Use the returned `summary` field to present trends and insights to the user.

---

### Export Responses to Excel

Generate a downloadable Excel file of all form responses.

```bash
POST /forms/export
```

```python
import urllib.request, os, json
data = json.dumps({"formId": "FORM_ID"}).encode()
req = urllib.request.Request(
  'https://api.gformsfree.com/skill/forms/export',
  data=data, method='POST'
)
req.add_header('Authorization', f'Bearer {os.environ["GFORMS_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

**Response:**
```json
{
  "downloadUrl": "https://api.gformsfree.com/skill/files/xxx.xlsx",
  "expiresIn": 600
}
```

Return `downloadUrl` to the user. Remind them the link expires in **10 minutes**.

---

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing or invalid request parameters |
| 401 | Invalid or missing API key — check `GFORMS_API_KEY` |
| 403 | Subscription expired — renew in the Forms for Google Drive App |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Google Forms API |

### Troubleshooting: API Key Issues

Verify your key is valid:

```python
import urllib.request, os, json
req = urllib.request.Request('https://api.gformsfree.com/skill/auth/check')
req.add_header('Authorization', f'Bearer {os.environ["GFORMS_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
```

If invalid, regenerate in the app: **Settings → Connect AI Agent → Regenerate Key**

---

## Agent Instructions

- **Never** expose the `GFORMS_API_KEY` value in any message to the user
- Always confirm with the user before creating or modifying a form
- When creating a form, ask for: topic, target audience, number of questions, and preferred question types
- After creating a form, always return both `responderUri` (share with respondents) and `editUri` (for editing)
- When exporting, always remind the user the download link expires in 10 minutes
- Confirm twice before deleting any form

## Resources

- [Forms for Google Drive App](https://apps.apple.com/us/app/forms-for-google-drive/id6468928038)
- [Google Forms API Reference](https://developers.google.com/workspace/forms/api/reference/rest)
