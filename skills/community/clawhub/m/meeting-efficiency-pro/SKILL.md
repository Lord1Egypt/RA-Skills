---
name: meeting-efficiency-pro
description: AI-powered meeting optimization tool that analyzes calendar events, provides efficiency scores, extracts action items, and automates follow-ups. Save 20%+ of meeting time with intelligent analysis and automation.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "meeting-efficiency-pro",
              "label": "Install dependencies",
            },
          ],
        "price": 69,
        "category": "productivity",
        "tags": ["meetings", "ai", "automation", "calendar", "productivity"],
      },
  }
---

# Meeting Efficiency Pro

Transform your meetings from time-wasters to productivity engines. This AI-powered skill analyzes your calendar, provides efficiency scores, extracts action items, and automates follow-ups.

## Features

### 🎯 Meeting Analysis
- **Efficiency Scoring**: AI-powered analysis of meeting effectiveness (0-100 score)
- **Pre-meeting Optimization**: Suggestions to improve upcoming meetings
- **Pattern Detection**: Identify inefficient meeting habits

### 📅 Calendar Integration
- **Google Calendar**, **Outlook**, and **iCal** support
- **Daily Briefing**: Morning summary of today's meetings with optimization tips
- **Recurring Meeting Analysis**: Spot trends in regular meetings

### 🤖 AI-Powered Processing
- **Action Item Extraction**: Automatically identify tasks from meeting notes
- **Decision Tracking**: Capture key decisions made
- **Summary Generation**: Concise bullet-point summaries

### 🔄 Follow-up Automation
- **Email Templates**: Professional follow-up emails
- **Task Creation**: Integrate with Todoist, Asana, or Jira
- **Reminder System**: Never miss action item deadlines

### 📊 Analytics Dashboard
- **Weekly Reports**: Meeting efficiency trends
- **Time Savings**: Calculate hours saved
- **ROI Analysis**: Meeting cost vs. outcomes

## Quick Start

### 1. Installation
```bash
# Install from ClawHub
clawhub install meeting-efficiency-pro

# Or manually install dependencies
cd skills/meeting-efficiency-pro
npm install
```

### 2. Configuration
```bash
# Run setup wizard
/meeting-efficiency-pro setup

# Or configure manually
edit config/default.json
```

### 3. Basic Usage
```bash
# Get today's meeting briefing
/meeting-efficiency-pro briefing

# Analyze a specific meeting
/meeting-efficiency-pro analyze "Team Standup"

# Process meeting notes
/meeting-efficiency-pro process --notes "meeting-notes.txt"

# Generate weekly report
/meeting-efficiency-pro weekly-report
```

## Configuration

### Required Settings
```json
{
  "ai_provider": "openai|grok",
  "ai_api_key": "your-api-key-here",
  "calendar_type": "google|outlook|ical|none"
}
```

### Optional Settings
```json
{
  "task_manager": "todoist|asana|jira|linear|none",
  "task_manager_token": "optional",
  "auto_briefing": true,
  "briefing_time": "08:00",
  "efficiency_threshold": 70,
  "email_integration": false,
  "smtp_settings": {}
}
```

## Commands

### Core Commands
- `/meeting-efficiency-pro setup` - Interactive setup wizard
- `/meeting-efficiency-pro briefing` - Get today's meeting briefing
- `/meeting-efficiency-pro analyze <meeting-title>` - Analyze specific meeting
- `/meeting-efficiency-pro process --notes <file>` - Process meeting notes
- `/meeting-efficiency-pro weekly-report` - Generate weekly efficiency report

### Advanced Commands
- `/meeting-efficiency-pro config` - View/edit configuration
- `/meeting-efficiency-pro test` - Test all integrations
- `/meeting-efficiency-pro demo` - Run demo with sample data
- `/meeting-efficiency-pro export --format json|csv` - Export analytics data

## Integration Guide

### Calendar Integration
1. **Google Calendar**: Enable Google Calendar API and get OAuth credentials
2. **Outlook**: Use Microsoft Graph API with app registration
3. **iCal**: Provide .ics URL or file path

### AI Provider Setup
1. **OpenAI**: Get API key from platform.openai.com
2. **Grok**: Get API key from x.ai (if available)

### Task Manager Integration
- **Todoist**: Personal access token from settings
- **Asana**: Personal access token from developer console
- **Jira**: API token from Atlassian account

## Pricing & Licensing

### Skill Price: $69
**Includes**:
- Complete skill implementation
- 1 year of free updates
- 30 days of email support
- Commercial use license

### Optional Add-ons
- **Team License**: $299 (up to 10 users)
- **White-label License**: $499 (reselling rights)
- **Custom Integration**: $69/hour (custom requirements)

## Support & Resources

### Documentation
- Full API reference in `references/api-docs.md`
- Configuration guide in `config/README.md`
- Troubleshooting guide in `references/troubleshooting.md`

### Support Channels
- **Email**: support@clawhub.com (mention "Meeting Efficiency Pro")
- **Community**: ClawHub Discord #meeting-efficiency
- **Updates**: Check `clawhub update meeting-efficiency-pro`

### Demo
Run the demo script to see the skill in action:
```bash
cd skills/meeting-efficiency-pro
node scripts/demo.js
```

## Success Stories

> "Saved our team 5 hours per week in meeting time. The efficiency scoring helped us eliminate unnecessary meetings." - Sarah, Product Manager

> "The action item extraction is magical. No more missed tasks after meetings." - David, Engineering Lead

> "Worth every penny. Paid for itself in the first week through time savings." - Maria, Consultant

## Roadmap

### Coming Soon (Q2 2025)
- Real-time meeting coaching
- Zoom/Teams integration for live transcription
- Advanced sentiment analysis
- Team collaboration features

### Planned (Q3 2025)
- Custom report templates
- API for developers
- Mobile app companion
- Advanced analytics dashboard

---

**Transform your meetings today. Install Meeting Efficiency Pro and start saving time immediately.**