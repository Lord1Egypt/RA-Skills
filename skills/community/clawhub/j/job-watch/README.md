# Job Watch – Automated Job Search for OpenClaw

[![ClawHub Skill](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.com)

**Automated job search across Moroccan job boards. Filters last 7 days, scores matches, and produces a clean report.**

## ✨ Value
- Saves hours of manual searching
- Finds jobs matching your exact profile and scoring rules
- Works entirely in OpenClaw – no scripts, no shell commands
- Respects rate limits and public data only

## 📦 Installation

```bash
clawhub install job-watch
```

Or install from source:
```bash
clawhub install https://github.com/ElFilaliHamza/job-watch-skill
```

## 🚀 Quick Start

1. After installation, set up your profile in `~/.openclaw/workspace/skills/job-watch/memory/profile.md`
2. Customize scoring rules in `memory/scoring.md`
3. List your target platforms in `memory/platforms.md`
4. Say to your OpenClaw agent: **"run job watch now"**

The AI will scrape, filter, score, and output a report directly in the chat.

## 📋 Example Report

```
# Job Watch Report – 2026-04-03

## Summary
- Total jobs found: 24
- New matches this week: 7
- Average score: 73

## Top Matches (score ≥ 80)
| Score | Title | Company | Platform | Link |
|-------|-------|---------|----------|------|
| 95 | Senior Full Stack Developer | ABC Corp | rekrute.com | [link] |
| 88 | Data Engineer | XYZ Ltd | dreamjob.ma | [link] |
```

## 🔧 Configuration Files (in `memory/`)

| File | Purpose |
|------|---------|
| `profile.md` | Your target role, skills, location, preferred keywords |
| `scoring.md` | Points system (e.g., +10 for "remote", +20 for exact title match) |
| `platforms.md` | List of job boards and search URLs |

See the `examples/` directory for templates.

## 🔒 Security & Privacy
- No credentials or API keys required
- All data stays on your local machine
- No personal information is ever transmitted
- Public job boards only – respects `robots.txt`

## 🤝 Contributing
Issues and pull requests welcome at [GitHub repo](https://github.com/ElFilaliHamza/job-watch-skill).

## 📄 License
MIT – see LICENSE file in GitHub repo.

## ⚠️ Disclaimer
This skill is for personal use only. Always verify job listings on the original platform before applying.