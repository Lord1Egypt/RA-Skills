---
name: clawhub-security-check
version: 1.0.0
author: marianachow0321
description: Pre-installation security assessment for ClawHub skills. Run before any skill install.
homepage: https://github.com/marianachow0321/openclaw-preinstall-security-check
triggers:
  - install skill
  - skill install
  - clawhub install
  - is this skill safe
  - check skill security
---

# ClawHub Security Check

Mandatory pre-installation security assessment for ClawHub skills with optional sandbox testing.

## When to Use

- User wants to install a ClawHub skill (`openclaw skill install`, `npx clawhub install`)
- User asks about skill safety or wants to check a skill before installing
- BEFORE executing any skill installation command

## Workflow

### 1. Extract Skill Info

Parse the skill identifier:
- Full URL: `https://clawhub.ai/author/skill-name`
- Short: `skill-name` or `author/skill-name`

### 2. Fetch ClawHub & GitHub Data

```bash
web_fetch("https://clawhub.ai/{author}/{skill-name}")
web_fetch("https://github.com/{author}/{repo}")
```

Extract: author, description, download count, stars, last commit date, verified status, file structure.

### 3. Calculate Risk Score

See `references/risk-scoring.md` for the full scoring table.

Score is 0–100 (higher = safer):
- **80–100**: Very safe → skip sandbox, approve
- **60–79**: Safe → approve, optional sandbox
- **40–59**: Moderate → sandbox required
- **20–39**: High risk → sandbox required
- **0–19**: Very high risk → reject immediately

### 4. Sandbox Testing (Conditional)

**Run sandbox IF** score is 20–79 AND skill has executables or unknown author.

**Skip IF** score ≥ 80 (trusted), documentation-only, or score < 20 (reject).

Spawn an isolated sub-agent session to install and analyze the skill:
- List all files and executables
- Grep for suspicious patterns (`curl|sh`, `eval`, `exec`, `rm -rf`, `sudo`, `~/.ssh`, `~/.aws`, `base64.*decode`)
- Check for network calls
- Return structured JSON with findings

See `references/sandbox-procedure.md` for the full sub-agent task template.

### 5. Generate Report

See `references/report-templates.md` for all report formats.

Present a concise security report with verdict (SAFE / NEEDS REVIEW / NOT SAFE), author info, trust rating, and a clear action instruction. If user asks "why" or "details", show expanded findings.

### 6. Handle User Response

- **yes** → run `openclaw skill install [skill-name]`
- **no** → cancel, suggest alternatives
- **details** → show full analysis, then re-ask

## Safety Rules

- Never install without explicit user confirmation
- Security check cannot be skipped or bypassed
- Err on caution for unknown sources
- If no internet, block installation entirely
- Limit concurrent sandbox sessions to 1
