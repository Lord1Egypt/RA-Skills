# Henry OS — AI Chief of Staff Framework

> **Stop being the bottleneck in your own business.**

Henry OS transforms OpenClaw into a fully autonomous business partner that runs 24/7 — finding opportunities, managing your pipeline, handling communications, and executing tasks while you focus on high-leverage work.

---

## What Henry OS Does

### 🎯 Proactive Intelligence
Henry doesn't wait for instructions. He continuously monitors your inboxes, calendars, job boards, and social channels — surfacing opportunities and flagging what needs attention before you even know it exists.

### 💰 Revenue Pipeline Automation
- **Opportunity Hunting**: Scans Upwork, LinkedIn, Reddit, Indie Hackers, and niche communities for freelance/consulting leads matching your skills
- **Lead Scoring**: Rates opportunities by fit, effort, and revenue potential
- **Outreach Prep**: Drafts personalized proposals and messages ready for your approval
- **Pipeline Management**: Tracks every lead from discovery to close in Mission Control

### 📧 Communications Management
- **Inbox Triage**: Reads and categorizes emails by urgency (Action Needed / FYI / Noise)
- **Draft Replies**: Prepares responses to common requests, waiting for your one-tap approval
- **Follow-up Automation**: Never drops the ball on pending conversations
- **Cross-Channel**: Works across Mail.app, Gmail, iMessage, SMS, WhatsApp

### 📅 Calendar & Life Ops
- **Daily Briefings**: Morning agenda with priorities, meetings, and action items
- **Smart Scheduling**: Blocks focus time around deep work, prepares for meetings
- **Reminders & Follow-ups**: Automatically creates follow-up tasks after calls and events
- **Conflict Detection**: Flags scheduling issues before they become problems

### 🛠️ Software Delivery
- **Client Projects**: End-to-end delivery from requirements to deployment
- **Code Generation**: Writes production-quality code in any language
- **Testing & QA**: Validates work before presenting it to you
- **Documentation**: Auto-generates READMEs and handoff docs

### 📺 YouTube Intelligence
- **Content Processing**: Watches videos, extracts actionable insights
- **Implementation**: Automatically applies relevant techniques to your active projects
- **Knowledge Base**: Builds a searchable library of insights from every video you consume

---

## Installation

### One-Line Install

```bash
curl -fsSL https://henryos.ai/install.sh | bash
```

That's it. Henry OS installs in under 5 minutes and starts working immediately.

### What Gets Installed

- **Mission Control Dashboard** — Web UI at http://localhost:3333 for monitoring and management
- **Henry Master Agent** — Your autonomous operator running 24/7
- **Specialist Sub-Agents** — Scout, Builder, Writer, Analyst, Operator, Hunter, Watcher
- **Native Apple Integrations** — Mail.app, Messages.app, Calendar.app, Contacts.app
- **Tooling Stack** — All required CLIs and dependencies auto-configured

---

## Quick Start

### 1. Launch Mission Control

After installation, open your browser to:
```
http://localhost:3333
```

This is your command center. From here you can:
- View system health and agent status
- Manage your task board (Kanban: Backlog / In Progress / Blocked / Done)
- Browse memory and learning loops
- Monitor your opportunity pipeline
- Chat directly with Henry

### 2. Configure Your Profile

Henry needs to know about you to be effective:

```bash
# Set your core details
henry config set name "Your Name"
henry config set email "you@example.com"
henry config set timezone "Australia/Brisbane"

# Define your skills (comma-separated)
henry config set skills "web development,react,node,python,automation"

# Set your target rates
henry config set hourly_rate 150
henry config set project_min 2000
```

### 3. Connect Your Accounts

Henry works with your existing Apple apps — no new logins needed:

```bash
# Grant permissions (macOS will prompt)
henry setup permissions

# Verify connections
henry status
```

### 4. Start Your First Hunt

```bash
# Launch the opportunity hunter
henry spawn hunter

# Check what's been found
henry pipeline
```

### 5. Review Your Morning Brief

Every morning, Henry prepares a briefing:
- Overnight activity summary
- Today's calendar and priorities
- Top 3 opportunities to pursue
- Tasks requiring approval
- System health check

---

## Configuration Options

### Core Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `name` | Your name | System username |
| `email` | Primary email | — |
| `timezone` | Your timezone | System timezone |
| `skills` | Comma-separated skill list | — |
| `hourly_rate` | Target hourly rate | 100 |
| `project_min` | Minimum project value | 1000 |

### Opportunity Hunting

| Setting | Description | Default |
|---------|-------------|---------|
| `hunt.enabled` | Enable automated hunting | true |
| `hunt.frequency` | Check interval (minutes) | 60 |
| `hunt.sources` | Sources to monitor | upwork,linkedin,reddit |
| `hunt.min_budget` | Minimum budget threshold | 500 |

### Communications

| Setting | Description | Default |
|---------|-------------|---------|
| `email.triage` | Auto-triage emails | true |
| `email.drafts` | Draft replies for approval | true |
| `messages.monitor` | Monitor iMessage/SMS | true |
| `approval.required` | Require approval for sends | true |

### Notifications

| Setting | Description | Default |
|---------|-------------|---------|
| `notify.channel` | Primary notification channel | imessage |
| `notify.quiet_hours` | Don't notify during these hours | 23:00-08:00 |
| `notify.urgent_only` | Only notify for urgent items | false |

### Advanced

```bash
# View all settings
henry config list

# Edit config file directly
henry config edit

# Reset to defaults
henry config reset
```

---

## Mission Control Dashboard

The dashboard has six main sections:

### 1. System Health Bar
- Token usage and costs
- Uptime and agent count
- Current status indicators

### 2. Task Board
Live Kanban with four columns:
- **Backlog** — Queued work
- **In Progress** — Active tasks
- **Blocked** — Waiting on external input
- **Done** — Completed work

### 3. Memory Viewer
Three tabs:
- **Episodic** — Daily activity logs
- **Semantic** — Knowledge base (contacts, tools, learnings)
- **Procedural** — Playbooks and runbooks

### 4. Learning Loop Log
- Last 10 learning cycles
- Provisional lessons
- Promote/reject actions

### 5. Cron Monitor
- Scheduled tasks
- Run history
- Manual triggers

### 6. Approval Gate Banner
Amber full-width alert for anything needing your sign-off.

---

## Sub-Agents

Henry spawns specialized agents for different work types:

| Agent | Role | When Spawned |
|-------|------|--------------|
| **Henry-Scout** | Research, scraping, monitoring | Intelligence gathering |
| **Henry-Builder** | Coding, automation, infrastructure | Software projects |
| **Henry-Writer** | Content, proposals, docs | Communications |
| **Henry-Analyst** | Data synthesis, scoring, modeling | Analysis tasks |
| **Henry-Operator** | Scheduling, inbox, reminders | Life ops |
| **Henry-Hunter** | Opportunity ID, lead research | Revenue pipeline |
| **Henry-Watcher** | YouTube monitoring, media intel | Content processing |

Spawn agents manually:
```bash
henry spawn hunter    # Start hunting
henry spawn builder   # Begin a build task
henry spawn analyst   # Analyze data
```

Check agent status:
```bash
henry agents
```

---

## Troubleshooting

### Installation Issues

**Problem**: Install script fails with permission error
```bash
# Solution: Run with explicit bash
bash -c "$(curl -fsSL https://henryos.ai/install.sh)"
```

**Problem**: Node version too old
```bash
# Solution: Update Node.js first
brew install node  # macOS
# or
nvm install 20
```

### Connection Issues

**Problem**: Mission Control won't load
```bash
# Check if server is running
henry status

# Restart Mission Control
henry restart dashboard

# Check logs
henry logs
```

**Problem**: Apple app permissions denied
```bash
# Re-run permission setup
henry setup permissions

# Or manually grant in:
# System Preferences → Security & Privacy → Privacy → Automation
```

### Agent Issues

**Problem**: Agent won't spawn
```bash
# Check resource limits
henry status --resources

# View agent logs
henry logs --agent henry-hunter-01
```

**Problem**: Agent stuck/running too long
```bash
# List running agents
henry agents

# Terminate specific agent
henry terminate henry-hunter-01

# Kill all agents and restart
henry reset agents
```

### Opportunity Hunting

**Problem**: No opportunities found
- Verify your skills are configured: `henry config get skills`
- Check hunt sources: `henry config get hunt.sources`
- Review minimum budget threshold
- Try manual search: `henry hunt --manual "react developer"`

**Problem**: Too many low-quality leads
- Increase minimum budget: `henry config set hunt.min_budget 2000`
- Refine skill keywords to be more specific
- Add negative keywords to exclude

### Email/Communications

**Problem**: Not seeing emails in Mission Control
- Verify Mail.app has messages in inbox
- Check permissions: `henry setup permissions`
- Force sync: `henry sync email`

**Problem**: Drafts not being created
- Ensure `email.drafts` is enabled: `henry config get email.drafts`
- Check approval settings aren't blocking

### Getting Help

```bash
# View all commands
henry --help

# Get help for specific command
henry hunt --help

# Check system diagnostics
henry doctor

# Export logs for support
henry logs --export
```

### Community & Support

- **Documentation**: https://docs.henryos.ai
- **GitHub Issues**: https://github.com/shannonlinnan/henry-os/issues
- **Discord**: https://discord.gg/henryos
- **Email**: support@henryos.ai

---

## Privacy & Security

Henry OS is designed with privacy-first principles:

- **Local-First**: Your data stays on your machine
- **No Cloud Dependencies**: Works entirely offline after installation
- **Apple Native**: Uses macOS native APIs, no third-party bridges
- **Transparent**: All code is open source and auditable
- **Approval Gates**: Sensitive actions require your explicit approval

---

## Roadmap

- [x] Core framework and Mission Control
- [x] Native Apple integrations
- [x] Opportunity hunting pipeline
- [x] YouTube intelligence
- [ ] Windows/Linux support
- [ ] Browser extension for web clipping
- [ ] Mobile companion app
- [ ] Team/enterprise multi-agent mode
- [ ] Industry-specific agent packs

---

## License

MIT License — see [LICENSE](https://github.com/shannonlinnan/henry-os/blob/main/LICENSE) for details.

---

**Built with OpenClaw** | **Made by Shannon Linnan** | ** henryos.ai **
