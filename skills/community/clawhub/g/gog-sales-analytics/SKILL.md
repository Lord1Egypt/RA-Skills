---
name: GOG Weekly Sales Analytics
description: Automated weekly workflow that scrapes GOG store discounts, analyzes the full discounted-game dataset with Gemini, generates a markdown insights report, and syncs it to Feishu Drive. Use for recurring game-deal reporting and team distribution.
tags: ['gog', 'sales', 'gemini', 'feishu', 'workflow', 'analytics']
metadata: {"openclaw":{"emoji":"🎮"}}
---

# GOG Weekly Sales Analytics

Automated workflow that:

1. Scrapes weekly discounted game data from the GOG store
2. Analyzes the **full** set of discounted games with Google Gemini to surface best-value deals
3. Generates a markdown report with insights and recommendations
4. Syncs the report to a shared Feishu Drive folder for team access
5. Publishes the workflow as a reusable skill on ClawHub

## Usage

```bash
cp .env.example .env
# Fill in API keys in .env
pip install -r requirements.txt
python main.py
```

## Environment

| Variable | Purpose |
| --- | --- |
| `GEMINI_API_KEY` | Gemini analysis |
| `FEISHU_APP_ID` / `FEISHU_APP_SECRET` | Feishu Drive auth (tenant_access_token) |
| `FEISHU_DRIVE_FOLDER_ID` | Target Drive folder for the report |
| `CLAWHUB_API_TOKEN` | ClawHub publishing |

## Notes

- Feishu upload uses the `upload_all` multipart/form-data API (metadata in the form body, binary via `files`).
- Gemini analysis processes every discounted game in the dataset — there is no 20-item cap.

## Skills Used

- web-scraper: GOG store data extraction
- gemini: AI-powered sales analysis and report generation
- feishu-drive: Cloud storage sync and permission management
- gog: Game metadata and platform integration
- clawhub: Skill publishing and distribution
