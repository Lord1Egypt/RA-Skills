---
name: jobautopilot-bundle
description: Installs the full Job Autopilot pipeline — search jobs, tailor resumes, and submit applications. Convenience bundle that installs jobautopilot-search, jobautopilot-tailor, and jobautopilot-submitter in one step.
author: jerronl
version: "1.3.3"
homepage: https://github.com/jerronl/jobautopilot
tags:
  - job-search
  - resume
  - career
  - automation
metadata:
  clawdbot:
    emoji: "🤖"
    requires:
      bins:
        - python3
    files:
      - install.sh
      - setup.sh
---

# Job Autopilot — Full Bundle

Install all three Job Autopilot skills and run the full end-to-end pipeline:
**search → tailor → submit**.

## What this skill does

This is a **bundle installer only**. It contains two scripts:

- `install.sh` — runs `openclaw skills install` for each of the three sub-skills
- `setup.sh` — prompts for your personal info and writes a local config file

Neither script makes outbound network requests beyond `openclaw skills install`. No data is collected or sent to any server by these scripts. Note: the sub-skills (especially the submitter) use browser automation to navigate job sites — that browser activity does involve network traffic to those sites, initiated only when you explicitly request it.

## Install all three skills

```bash
openclaw skills install jobautopilot-bundle
openclaw skills install jobautopilot-search
openclaw skills install jobautopilot-tailor
openclaw skills install jobautopilot-submitter
```

Verify all four are loaded:

```bash
openclaw skills check | grep jobautopilot
```

## How it works

```
jobautopilot-search  ──►  jobautopilot-tailor  ──►  jobautopilot-submitter
   Find jobs               Tailor resume              Fill & submit forms
   Filter & track          Write cover letter         Verify & confirm
```

Just tell OpenClaw what you want:

> *"Search for software engineer jobs in New York"*

> *"Tailor my resume for the shortlisted jobs"*

> *"Submit applications for all resume-ready jobs"*

## Privacy & data storage

Setup collects personal information and stores it **locally only**:

| Data | Stored at |
|------|-----------|
| Name, email, phone, LinkedIn | `~/.openclaw/users/<you>/config.sh` |
| Resume files | Your existing folder (you choose during setup) |
| Tailored resumes & cover letters | `~/Documents/jobs/tailored/` (default, set during setup) |
| Job tracker | `~/.openclaw/workspace/job_search/job_application_tracker.md` |

No data is sent to any third party. Browser automation uses two isolated profiles (`search` and `apply`) created locally. **No passwords are stored by this skill.** Login to job sites uses browser-saved credentials or manual entry — the skill never reads or stores any password.

## Security

- **No outbound network calls from scripts**: `install.sh` and `setup.sh` operate locally only. The only network operations are `openclaw skills install` (downloading these skills) and browser navigation you explicitly request.
- **No password handling**: This skill does not read, store, or transmit any passwords. Login flows rely on your browser's own credential store.
- **Browser profiles**: Setup instructs you to manually create two isolated profiles (`search`, `apply`) using `openclaw browser profile create`. No browser profiles are created automatically by any script. You can inspect or delete them at any time.
- **Personal data**: Written only to `~/.openclaw/users/<you>/config.sh`. Setup automatically restricts this file to owner-only access (`chmod 600`). Read `setup.sh` in full before running to verify this.
- **Helper scripts**: All scripts in `scripts/` are plain shell, Python, and JavaScript with no obfuscation, no encoded payloads, no remote fetches at runtime.
- **EEOC fields**: Standard fields required by US job application forms (Equal Employment Opportunity Commission). Values are stored locally in your config and supplied only to forms you explicitly instruct the agent to fill. They are never logged or transmitted elsewhere.

## Requirements

- OpenClaw >= 2026.2.0
- Browser tool enabled
- `pip install python-docx`

## Support

If Job Autopilot saved you time, a coffee is appreciated:
paypal.me/ZLiu308
