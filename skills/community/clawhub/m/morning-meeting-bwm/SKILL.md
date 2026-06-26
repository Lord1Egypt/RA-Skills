# Morning Meeting Automation

## Overview

This skill handles the 9:00 AM daily standup automation for Blue World Marketing.

## Workflow

1. **10:00 AM Trigger** (1 hour after 9:00 AM meeting starts)
2. Read #morningmeeting Slack channel for human + AI conversation
3. Parse transcript for tasks and assignments
4. Delegate to appropriate AI agents
5. Execute any tasks agents can handle immediately
6. Send summary report back to #morningmeeting

## AI Agent Task Routing

| Task Type | Assigned Agent |
|-----------|---------------|
| Code/Development | Cipher |
| WordPress/WooCommerce | Sienna |
| n8n Automation | Daniel |
| SEO/GEO | Leo |
| Content Writing | Samantha |
| Image/Video | Frank |
| Social Media | Alex |
| Finance/Orders | Riley |
| Research | Morgan/Jamie |
| Security | Quinn |
| Infrastructure | Parker |
| Project Management | Jordan |
| Brand/Campaigns | Casey |
| Email Marketing | Drew |
| Customer Support | Taylor |

## Memory Storage

- Meeting summaries: `memory/meetings/YYYY-MM-DD-morning-meeting.md`
- Task assignments: `memory/tasks/active-tasks.md`
- Completed tasks: `memory/tasks/completed/`

## Slack Channels

- Input: `#morningmeeting`
- AI Activity Updates: `#openclaw-report-news`

## Cron Schedule

```
0 10 * * 1-5  # 10:00 AM weekdays (1 hour after 9 AM meeting)
```
