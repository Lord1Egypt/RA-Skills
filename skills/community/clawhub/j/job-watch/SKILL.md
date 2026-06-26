---
name: job-watch
description: Automated job search with 7‑day filtering, scoring, and weekly report. To run the skill send "run job watch now".
metadata:
  clawdbot:
    emoji: "💼"
    requires:
      env: []
    files: []
---
# Job Watch Skill

Automated job search across Moroccan job boards. Filters last 7 days, scores matches against your profile, and produces a structured report.

## When to Use
- When you want a weekly automated job search across multiple platforms
- When you need jobs filtered by your specific skills and preferences
- When you want scored job matches delivered as structured reports

## External Endpoints
| URL | Purpose | Data Sent |
|-----|---------|-----------|
| alwadifa-maroc.com | Job search | Search queries only |
| dreamjob.ma | Job search | Search queries only |
| rekrute.com | Job search | Search queries only |
| emploi-public.ma | Job search | Search queries only |
| anapec.org | Job search | Search queries only |

## Security & Privacy
- **No credentials required**: This skill uses public job board scraping only
- **No data persistence**: Job data is not stored externally; reports saved locally only
- **Rate limiting respected**: Respects robots.txt and platform rate limits
- **No PII transmission**: Your profile data stays in local memory files

## Version History
- **1.0.0** (2026-04-03) - Initial release with Moroccan job market focus

## Execution Instructions (CRITICAL)

When the user says **"run job watch now"**, **DO NOT run any shell commands** (including `find`, `ls`, `cat`, `bash`, `python`). This skill is designed to be executed entirely by the AI using web-scraping and browser tools, ensuring it works across all OpenClaw configurations without requiring local file system access.

### Steps to Execute

1. **Load user profile** from `~/.openclaw/workspace/skills/job-watch/memory/profile.md`
2. **Load scoring rules** from `~/.openclaw/workspace/skills/job-watch/memory/scoring.md`
3. **Load platform list** from `~/.openclaw/workspace/skills/job-watch/memory/platforms.md`
4. **For each platform**, scrape jobs posted in the last 7 days (use browser tools or HTTP requests)
5. **Filter** jobs that match user’s target role, location, and keywords
6. **Score** each job (0–100) based on scoring rules
7. **Generate report** in the format below
8. **Save report** to `~/.openclaw/workspace/skills/job-watch/memory/reports/YYYY-MM-DD-job-watch-report.md`

### Report Format (copy-paste friendly)

```markdown
# Job Watch Report – YYYY-MM-DD

## Summary
- Total jobs found: X
- New matches this week: Y
- Average score: Z

## Top Matches (score ≥ 80)
| Score | Title | Company | Platform | Link |
|-------|-------|---------|----------|------|

## Other Matches (score 60–79)
| Score | Title | Company | Platform | Link |

## Low Matches (score < 60) – optional
| Score | Title | Company | Platform | Link |

## Notes / Next Steps
- Apply to top matches by [date]
- Update profile keywords if low matches persist
```

### Example Trigger

User says: *"run job watch now"*

AI executes the steps above and outputs the report directly in the chat.
