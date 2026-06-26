# Skills Index Documentation

## About the Catalogue

`data/skills-catalogue.json` contains a curated index of quality ClawHub skills. It is the core data asset powering recommendations.

## How Skills Were Selected

Inclusion criteria:
- **50+ downloads** on ClawHub (proves minimum adoption)
- **No known VirusTotal flags** (security baseline)
- **Clear, specific purpose** (no vague "do everything" skills)
- **Active maintenance** (updated within last 90 days preferred)
- **Published on ClawHub** (official registry, not random GitHub repos)

Primary sources:
- ClawHub popular/trending listings
- VoltAgent/awesome-openclaw-skills curated list (5,200+ vetted skills from 13,700+ total)
- OpenClaw bundled system skills

## Catalogue Structure

```json
{
  "version": "1.0.0",
  "last_updated": "2026-03-22",
  "categories": {
    "category_name": {
      "description": "What this category covers",
      "skills": [
        {
          "name": "skill-name",
          "slug": "author/skill-name",
          "description": "One-line description",
          "author": "author-name",
          "downloads": 5000,
          "stars": 50,
          "last_updated": "2026-03-15",
          "permissions": ["filesystem:read"],
          "tags": ["tag1", "tag2"],
          "trust_score": 4.2,
          "install_cmd": "clawhub install skill-name"
        }
      ]
    }
  }
}
```

## Category Taxonomy

15 categories covering the major workflow domains:

| Category | Covers |
|---|---|
| coding | Software dev, code review, debugging, testing, git |
| communication | Email, Slack, Discord, Telegram, messaging |
| productivity | Tasks, calendar, notes, scheduling, project mgmt |
| research | Web search, summarization, data gathering |
| writing | Content, editing, blogging, copywriting, SEO |
| devops | Deploy, monitoring, CI/CD, servers, Docker |
| data | Analysis, spreadsheets, databases, SQL, viz |
| finance | Trading, portfolio, invoicing, expenses |
| security | Scanning, credentials, audit, encryption |
| automation | Cron, workflows, scraping, browser automation |
| media | Images, video, audio, podcasting |
| social | Social media posting, analytics, community |
| home | Smart home, IoT, Home Assistant |
| knowledge | PKM, Obsidian, Notion, documentation |
| maintenance | Agent optimization, memory cleanup, health |

## Contributing

Know a skill that should be in the catalogue? Open an issue at the GitHub repo with:
- Skill name and ClawHub URL
- Category it belongs to
- Why it deserves inclusion

## Versioning

The catalogue version increments when skills are added or removed. The `last_updated` field shows when the data was last refreshed. Run `/kungfu-update` to check if a newer version is bundled.

## Limitations

The catalogue is bundled with the skill, not fetched live. It may not include the newest ClawHub additions. Updates come with new skill versions via `clawhub update iknowkungfu`.
