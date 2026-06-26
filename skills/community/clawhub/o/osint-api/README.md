# OSINT API — ClawHub Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)](https://clawhub.ai/skills/osint-api)
[![Version](https://img.shields.io/badge/version-0.6.0-green)](https://github.com/ahsan-tariq-ai/osint-api)

Professional OSINT intelligence reports via API. Multiple RSS feeds across 15 categories with enriched analysis, domain recon, and automated feed health monitoring.

## Install

```bash
openclaw skills install osint-api
```

Or set the required API key:

```bash
export OSINT_API_KEY="your_key_here"
```

Get a key at https://osint.ahsan-tariq-ai.xyz

## Usage

```bash
# Get today's intelligence reports
python3 scripts/osint_api.py reports

# Filter by category
python3 scripts/osint_api.py reports --category geopolitics

# List categories
python3 scripts/osint_api.py categories

# Domain recon
python3 scripts/osint_api.py recon --domain google.com

# Social media lookup
python3 scripts/osint_api.py social --username username

# Breach check
python3 scripts/osint_api.py breach --email user@example.com
```

## API

All endpoints documented in `SKILL.md`. Base URL: `https://osint.ahsan-tariq-ai.xyz/api/v1`

## Source

- GitHub: https://github.com/ahsan-tariq-ai/osint-api
- Dashboard: https://osint.ahsan-tariq-ai.xyz/osint-dashboard
