---
name: meeting-notes-generator
description: AI-powered meeting notes generator - automatic transcription, summary, action items extraction, and task assignment. Turns meeting recordings or text into professional meeting minutes in seconds.
command-dispatch: tool
command-tool: meeting_notes_generator
command-arg-mode: raw
metadata: {"openclaw": {"emoji": "📝", "requires": {"bins": ["python3"]}}}
---

# 📝 Meeting Notes Generator - AI Meeting Assistant

Transform your meetings from chaos to clarity. Automatically generate professional meeting notes, extract action items, assign owners, and track follow-ups.

## Why This Skill?

- **Save 30+ minutes** per meeting on note-taking
- **Never miss an action item** again
- **Professional formatting** that stakeholders love
- **Multi-language support** for global teams

## Features

### Core Functions
| Feature | Description |
|---------|-------------|
| 📝 **Summary Generator** | Extract key discussion points and decisions |
| ✅ **Action Items** | Auto-identify tasks with owners and deadlines |
| 📋 **Attendee List** | Track who was in the meeting |
| ⏰ **Timeline** | Map out discussion topics by time |
| 🎯 **Priorities** | Flag high/medium/low priority items |
| 📤 **Export** | Export to Markdown, Notion, Email |

### Supported Input
- Meeting transcript text
- Meeting recording (with timestamps)
- Chat/ Slack discussion export
- Manual meeting notes (raw)

## Commands

### Generate Meeting Notes
```
/meeting-notes generate <meeting_type> [--summary] [--actions] [--timeline]

Options:
  daily       - Daily standup meeting
  weekly      - Weekly team meeting
  one-on-one  - 1:1 meeting
  project     - Project review meeting
  client      - Client meeting
  brain        - Brainstorming session
```

Examples:
```
/meeting-notes generate weekly
/meeting-notes generate daily --summary --actions
/meeting-notes generate client --timeline --actions
```

### Quick Templates
```
/meeting-notes template <type>

Types:
  standup     - Daily standup template
  retro       - Sprint retrospective
  planning    - Sprint planning
  review      - Code/project review
  all-hands   - All hands meeting
```

### Action Item Management
```
/meeting-notes actions <command>

Commands:
  list        - Show all action items
  add <item>  - Add new action item
  complete    - Mark item as done
  overdue     - Show overdue items
```

### Export
```
/meeting-notes export <format>

Formats:
  markdown    - Markdown file
  notion      - Notion-compatible format
  email       - Email summary format
  json        - JSON for integration
```

## Usage Examples

### Example 1: Weekly Team Meeting
```
Input:
/meeting-notes generate weekly

Output:
# Weekly Team Meeting Notes
**Date:** 2026-03-03
**Time:** 14:00-15:00
**Attendees:** @Alice, @Bob, @Carol

## 📋 Summary
- Q1 goals review completed
- Resource allocation discussed
- New project timeline approved

## ✅ Action Items
| Task | Owner | Due | Priority |
|------|-------|-----|:--------:|
| Update project plan | @Alice | Mar 5 | 🔴 High |
| Schedule client demo | @Bob | Mar 7 | 🟡 Medium |
| Review design specs | @Carol | Mar 10 | 🟢 Low |

## 📅 Next Meeting
Tuesday, March 10, 2026 @ 14:00
```

### Example 2: Daily Standup
```
Input:
/meeting-notes generate daily

Output:
# Daily Standup - March 3, 2026

## 👥 Updates
**Alice:** Completed API integration, working on tests
**Bob:** Deployed to staging, waiting for feedback  
**Carol:** Design review done, moving to implementation

## 🔜 Blockers
- None reported

## ✅ Today's Tasks
- [ ] Alice: Complete unit tests
- [ ] Bob: Fix staging bugs
- [ ] Carol: Start mobile layouts
```

### Example 3: 1-on-1 Meeting
```
Input:
/meeting-notes generate one-on-one

Output:
# 1:1 Meeting Notes
**With:** Manager
**Date:** 2026-03-03

## 🎯 Career Discussion
- Progress on Q1 goals reviewed
- Feedback on recent presentation positive
- Growth areas identified: leadership skills

## 🤔 Questions Raised
1. Opportunities for mentorship?
2. Timeline for promotion consideration?

## 📝 Action Items
- [ ] Schedule skip-level meeting
- [ ] Prepare mid-year review docs
```

## Input Format Options

### Option 1: Raw Text
Paste meeting transcript or notes directly after the command.

### Option 2: Quick Entry
Use built-in templates and fill in the blanks.

### Option 3: File Input
Specify a file containing meeting notes:
```
/meeting-notes from-file meeting.txt
```

## Advanced Options

### Include/Exclude Sections
```
/meeting-notes generate weekly --summary --actions --no-timeline
```

### Priority Filtering
```
/meeting-notes actions --priority high
```

### Date Range
```
/meeting-notes actions --from 2026-03-01 --to 2026-03-07
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `/mn` | Quick generate meeting notes |
| `/mn w` | Generate weekly notes |
| `/mn d` | Generate daily standup |
| `/mn a` | Show action items |

## Integration

### Notion Export
Export directly to Notion with formatting preserved.

### Email Summary
Send meeting notes to all attendees with one command.

### Calendar Sync
Link action items to Google Calendar/Outlook.

## Templates Library

### Daily Standup
```
## What I did yesterday
-

## What I'll do today
-

## Blockers
-
```

### Weekly Retro
```
## What went well
-

## What could improve
-

## Action items for next sprint
-
```

### Project Kickoff
```
## Project Overview
- Name:
- Goal:
- Timeline:

## Key Stakeholders
-

## Milestones
1.
2.
3.

## Risks
-
```

## Tips for Best Results

1. **Be specific** with meeting type for better formatting
2. **Include attendees** for action item assignment
3. **Set clear deadlines** to generate actionable items
4. **Use priorities** to help team focus

## Common Use Cases

| Scenario | Command |
|----------|---------|
| Quick standup | `/meeting-notes generate daily` |
| Team weekly | `/meeting-notes generate weekly` |
| Client call | `/meeting-notes generate client` |
| Action review | `/meeting-notes actions list` |
| Export team report | `/meeting-notes export markdown` |

## Success Stories

> "This tool saved me 2 hours every week on meeting admin. The action item tracking alone is worth it."
> — Product Manager

> "Finally, a meeting notes tool that actually organizes the chaos into something useful."
> — Engineering Lead

## Technical Details

- **Processing**: Local + Cloud AI for summary generation
- **Languages**: English, Chinese, Japanese, Spanish (auto-detect)
- **Storage**: SQLite for action item tracking
- **Export**: Markdown, JSON, HTML, PDF

## Pricing Tiers

| Feature | Free | Pro | Team |
|---------|:----:|:---:|:----:|
| Meeting generation | 10/mo | Unlimited | Unlimited |
| Action item tracking | ✅ | ✅ | ✅ |
| Export formats | Markdown | All | All |
| Priority sorting | ❌ | ✅ | ✅ |
| Team collaboration | ❌ | ❌ | ✅ |
| API access | ❌ | ✅ | ✅ |

---

**Tag:** #meeting #notes #productivity #ai #team #workflow

**Version:** 1.0.0

**Author:** 浮光AI助手 (FogLight AI)

**Support:** Issues and feedback welcome

---

Ready to transform your meetings? Try:
```
/meeting-notes generate weekly
```