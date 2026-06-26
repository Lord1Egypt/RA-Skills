# Config Schema — newsletter-launch

The agent writes this JSON file after the setup wizard, then passes it to the scripts.

## Full Schema

```json
{
  "name": "The Trade Wire",
  "slug": "trade-wire",
  "audience": "Independent home service contractors (HVAC, plumbing, electrical, roofing)",
  "monetization": "Sponsorships, affiliate links (Amazon Associates), paid tier",
  "publish_day": "Tuesday",
  "seed_keywords": [
    "hvac contractor pricing guide 2026",
    "plumbing flat rate pricing guide",
    "home service contractor profit margins"
  ],
  "beehiiv_pub_id": "pub_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "beehiiv_api_key": "rKe...",
  "auto_post": false,
  "affiliate_tag": "thetradewire-20",
  "timezone": "America/Chicago",
  "owner_name": "Michael",
  "telegram_user_id": "8671387767",
  "style_reader": "Busy solo operators who skim on mobile between jobs",
  "style_tone": "Direct and no-fluff, lead with money or risk",
  "style_vocab": "flat-rate pricing, callback rate, service call — never use leverage or synergy"
}
```

## Field Notes

| Field | Required | Notes |
|-------|----------|-------|
| name | ✅ | Full newsletter name |
| slug | ✅ | Lowercase, hyphens only. Used for file paths and cron names |
| audience | ✅ | One sentence. Used in cron prompts and project files |
| monetization | ✅ | One sentence. Stored in project memory |
| publish_day | ✅ | Default: Tuesday |
| seed_keywords | ✅ | 3–5 keywords to seed the research brief |
| beehiiv_pub_id | ✅ | Required for KPI pull and auto-post |
| beehiiv_api_key | ✅ | Required for KPI pull and auto-post |
| auto_post | ✅ | true only if on Beehiiv Scale/Enterprise plan |
| affiliate_tag | ❌ | Optional. Leave empty string if none |
| timezone | ❌ | IANA timezone. Default: America/Chicago. Controls all cron fire times |
| owner_name | ❌ | Your name. Used in cron alert messages. Default: "you" |
| telegram_user_id | ✅ | For cron failure alerts |
| style_reader | ✅ | Who the reader is and how they consume content |
| style_tone | ✅ | Tone description (feeds into writing-style.md generation) |
| style_vocab | ✅ | Words/phrases to use or avoid (feeds into writing-style.md generation) |

## Slug Rules
- Lowercase letters, digits, hyphens only
- Must be unique — used as the project directory name
- Example: "The Roofing Report" → "roofing-report"
