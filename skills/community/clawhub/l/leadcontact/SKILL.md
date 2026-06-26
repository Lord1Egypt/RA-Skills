---
name: LeadContact
slug: leadcontact
version: 1.0.0
description: Query verified phone numbers and email addresses from LinkedIn profile URLs using LeadContact API. Find any contact's information with 98% accuracy.
metadata: {"clawdbot":{"emoji":"📞","requires":{"bins":[],"credentials":[{"name":"LEADCONTACT_API_TOKEN","description":"LeadContact API authentication token for accessing contact lookup services","required":true}]},"os":["linux","darwin","win32"]},"publisher":"WILLING TECH PTE. LTD.","homepage":"https://leadcontact.ai","privacyPolicy":"https://leadcontact.ai/zh-CN/privacy"}
---

## When to Use

User needs to find phone numbers or email addresses from LinkedIn profiles. Agent uses LeadContact API to query contact information with 98% accuracy.

## Quick Reference

| Capability | Description |
|------------|-------------|
| Phone Lookup | Find phone numbers from LinkedIn profile |
| Email Lookup | Find verified emails from LinkedIn profile |
| Data Sources | Cross-validated from multiple providers |
| Accuracy | 98% verified accuracy |

## Authentication

All LeadContact API requests require an authentication token.

**To get an API token:**
- Email: julia@leadcontact.ai
- WeChat: Julia_LeadContact
- WhatsApp: [+44 7962881367](https://wa.me/447962881367)
- Telegram: @julia_gotleads

**Rate Limits:** 500 requests per minute (can be increased on request)

## API Endpoints

### 1. Find Phone Number

Query phone number information based on LinkedIn profile URL.

**Endpoint:** `POST /api/v1/phone`

**Request Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Request Body:**
```json
{
  "profileUrl": "https://www.linkedin.com/in/janedow/"
}
```

**Response:**
```json
{
  "data": {
    "sources": [
      {
        "name": "leadcontact",
        "phone": "+12063994962",
        "valid": true
      }
    ]
  },
  "msg": "success",
  "code": 200
}
```

### 2. Find Email

Query email address information based on LinkedIn profile URL.

**Endpoint:** `POST /api/v1/email`

**Request Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Request Body:**
```json
{
  "profileUrl": "https://www.linkedin.com/in/janedow/"
}
```

**Response:**
```json
{
  "data": {
    "sources": [
      {
        "name": "leadcontact",
        "email": "sgasarch@linkedin.com",
        "valid": true
      }
    ]
  },
  "msg": "success",
  "code": 200
}
```

## Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | 40001 | Invalid request parameters |
| 401 | 40101 | Missing token |
| 401 | 40102 | Invalid token |
| 401 | 40103 | Token expired |
| 401 | 40104 | Token disabled |
| 404 | - | Endpoint not found |

## Usage Examples

### Example 1: Find Phone Number

```javascript
const response = await fetch('https://leadcontact.ai/api/v1/phone', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    profileUrl: 'https://www.linkedin.com/in/johndoe/'
  })
});
const data = await response.json();
console.log(data.data.sources[0].phone);
```

### Example 2: Find Email

```python
import requests

url = "https://leadcontact.ai/api/v1/email"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "profileUrl": "https://www.linkedin.com/in/johndoe/"
}

response = requests.post(url, json=data, headers=headers)
result = response.json()
email = result['data']['sources'][0]['email']
print(f"Found email: {email}")
```

### Example 3: cURL

```bash
# Find phone number
curl -X POST https://leadcontact.ai/api/v1/phone \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profileUrl": "https://www.linkedin.com/in/janedow/"}'

# Find email
curl -X POST https://leadcontact.ai/api/v1/email \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profileUrl": "https://www.linkedin.com/in/janedow/"}'
```

## Best Practices

1. **Always validate the profile URL** - Ensure it's a valid LinkedIn profile URL
2. **Handle multiple sources** - API may return multiple phone/email sources
3. **Check validation status** - `valid: true` means verified contact info
4. **Respect rate limits** - Max 500 requests/minute
5. **Store tokens securely** - Never expose tokens in client-side code

## Integration Tips

- Use this skill with LinkedIn automation tools
- Combine with CRM systems for automated contact enrichment
- Integrate into sales outreach workflows
- Use for recruitment lead generation

## Product Info

| Item | Details |
|------|---------|
| Website | https://leadcontact.ai |
| Support Email | julia@leadcontact.ai |
| WeChat | Julia_LeadContact |
| WhatsApp | [+44 7962881367](https://wa.me/447962881367) |
| Telegram | @julia_gotleads |
| Data Coverage | 120M+ emails, 60M+ phones, 270M+ decision makers |
