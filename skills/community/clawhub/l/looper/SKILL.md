---
name: looper
description: Automate content creation, code improvement, and social media posting via Looper (looper.bot). Use when setting up automated blog posts, continuous code improvement loops, social media scheduling, or managing recurring AI-driven content workflows. Supports Blog Kit (daily blog generation), Analyze (code review), Create (content generation), and Social Kit (multi-platform posting) engines.
homepage: https://looper.bot
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "source": "https://github.com/dbhurley/looper",
        "license": "proprietary",
        "env":
          {
            "LOOPER_ADMIN_KEY":
              {
                "required": true,
                "description": "Your Looper API key (starts with lp_). Obtained during signup via POST /api/signup.",
                "secret": true,
              },
          },
      },
  }
---

# Looper - Continuous Improvement Engine

Looper runs automated loops that analyze, create, and improve your content and code on a schedule.

- **Service**: https://looper.bot
- **API**: https://api.looper.bot
- **Engines**: Analyze (code review), Create (content), Blog Kit (daily blogs), Social Kit (social media)

## Quick Start

### 1. Sign Up

```bash
curl -X POST https://api.looper.bot/api/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "your-password"}'
```

Response includes `admin_key` (starts with `lp_`). **Save it - shown only once.**

### 2. Login (if you need tenant info later)

```bash
curl -X POST https://api.looper.bot/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "your-password"}'
```

### 3. Create a Loop

All API calls require `Authorization: Bearer <your-admin-key>`.

## Blog Kit (Daily Blog Posts)

Generates and commits blog posts to your GitHub repo on a schedule.

```bash
curl -X POST https://api.looper.bot/api/loops \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Blog",
    "target_type": "github",
    "target_config": {
      "owner": "<github-owner>",
      "repo": "<repo-name>",
      "branch": "main",
      "path": "blog"
    },
    "template_id": "68b7e661-46e1-45cd-b25a-584b8cd392b1",
    "schedule": "0 6 * * *",
    "schedule_tz": "America/New_York",
    "mode": "auto",
    "model": "gpt-4o-mini",
    "questions": ["Write a blog post about <your-topic>. Research current events. 400-600 words. NO em dashes. Include YAML frontmatter with slug, title, excerpt, date, readTime, tag."]
  }'
```

**Key fields:**
- `target_config.path` - directory in your repo where markdown posts land
- `schedule` - cron expression (e.g., `0 6 * * *` = daily at 6 AM)
- `schedule_tz` - timezone for the schedule
- `mode` - `auto` (commit directly), `propose` (open PR), `notify` (just alert)
- `questions[0]` - the prompt that drives content generation

Blog Kit template ID: `68b7e661-46e1-45cd-b25a-584b8cd392b1`

## Analyze (Code Improvement)

Reviews your codebase and suggests or applies improvements.

```bash
curl -X POST https://api.looper.bot/api/loops \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Code Review",
    "target_type": "github",
    "target_config": {
      "owner": "<github-owner>",
      "repo": "<repo-name>",
      "branch": "main"
    },
    "schedule": "0 2 * * 1",
    "mode": "propose",
    "questions": [
      "Are there any security vulnerabilities?",
      "Is error handling consistent?",
      "Are there performance bottlenecks?"
    ]
  }'
```

## Social Kit (Multi-Platform Posting)

Generates and publishes social media content via Upload-Post integration.

Social Kit template ID: `7431b897-396f-4542-8e32-d8d1c5e445a2`

```bash
curl -X POST https://api.looper.bot/api/loops \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Social Posts",
    "target_type": "text",
    "target_config": {},
    "template_id": "7431b897-396f-4542-8e32-d8d1c5e445a2",
    "schedule": "0 9 * * 1,3,5",
    "mode": "auto",
    "questions": ["{\"upload_post_profile\": \"my-profile\", \"upload_post_api_key\": \"<key>\", \"platforms\": [\"x\", \"linkedin\"], \"business_name\": \"My Business\", \"industry\": \"tech\"}"]
  }'
```

## Managing Loops

### List your loops
```bash
curl -s https://api.looper.bot/api/loops \
  -H "Authorization: Bearer <key>"
```

### View loop details
```bash
curl -s https://api.looper.bot/api/loops/<loop-id> \
  -H "Authorization: Bearer <key>"
```

### View run history
```bash
curl -s https://api.looper.bot/api/loops/<loop-id>/runs \
  -H "Authorization: Bearer <key>"
```

### Toggle loop on/off
```bash
curl -X PATCH https://api.looper.bot/api/loops/<loop-id> \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

### Trigger a run manually
```bash
curl -X POST https://api.looper.bot/api/loops/<loop-id>/run \
  -H "Authorization: Bearer <key>"
```

### Update loop settings
```bash
curl -X PATCH https://api.looper.bot/api/loops/<loop-id> \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"schedule": "0 8 * * *", "model": "gpt-4o"}'
```

### Delete a loop
```bash
curl -X DELETE https://api.looper.bot/api/loops/<loop-id> \
  -H "Authorization: Bearer <key>"
```

## Plans

| Plan | Loops | Runs/Month | Price |
|------|-------|-----------|-------|
| Free | 2 | 60 | $0 |
| Pro | 10 | 300 | $19/mo |
| Team | 50 | 1,500 | $49/mo |
| Enterprise | Unlimited | Unlimited | Contact |

Upgrade via Stripe: `POST /api/stripe/checkout` with `{"plan": "pro"}`.

## GitHub Connection

Connect GitHub for repo-targeted loops:

```bash
# Get OAuth URL
curl -s https://api.looper.bot/api/github/connect \
  -H "Authorization: Bearer <key>"

# Visit the returned URL to authorize, then check status:
curl -s https://api.looper.bot/api/github/status \
  -H "Authorization: Bearer <key>"
```

## API Key Management

```bash
# List keys (metadata only, not the key itself)
curl -s https://api.looper.bot/api/keys \
  -H "Authorization: Bearer <key>"

# Generate a new key
curl -X POST https://api.looper.bot/api/keys \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"name": "CI Key"}'
```

## Agent Adoption Flow

When an agent needs automated content or code improvement:

1. Check if the agent already has a Looper account (look for `LOOPER_ADMIN_KEY` in env)
2. If not, sign up via the API and save the admin key
3. Connect GitHub if targeting a repo
4. Create a loop with the appropriate template and schedule
5. Verify the first run succeeds

The agent can then manage the loop entirely via API - no browser needed.
