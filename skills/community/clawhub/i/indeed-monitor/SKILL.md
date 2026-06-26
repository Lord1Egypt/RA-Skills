---
name: indeed-monitor
description: "Monitor Indeed job postings for businesses hiring receptionists, customer service reps, or front desk staff in target areas. Each posting = a confirmed Gracie lead (they have call volume + budget). Outputs enriched lead list with company name, phone (when available), location, and pain point summary."
---

# Indeed Monitor Skill

Scrapes Indeed for businesses actively hiring front-desk/receptionist roles.
A business hiring for these roles = confirmed pain point for Gracie.

## Quick Commands

```bash
# RECOMMENDED: Browser version (cleanest results, requires Chrome relay ON)
python3 ~/StudioBrain/00_SYSTEM/skills/indeed-monitor/monitor_browser.py
python3 ~/StudioBrain/00_SYSTEM/skills/indeed-monitor/monitor_browser.py --save

# Fallback: Scrapling version (no relay needed, slightly noisier)
source ~/StudioBrain/00_SYSTEM/skills/scrapling/.venv/bin/activate
python3 ~/StudioBrain/00_SYSTEM/skills/indeed-monitor/monitor.py
python3 ~/StudioBrain/00_SYSTEM/skills/indeed-monitor/monitor.py --save

# Custom search
python3 ~/StudioBrain/00_SYSTEM/skills/indeed-monitor/monitor.py --query "dental receptionist" --location "Brooklyn, NY"
```

## Search Targets (Default)
- receptionist
- customer service representative
- front desk
- office manager
- call center

## Target Areas (Default)
- Staten Island, NY
- Brooklyn, NY
- Bronx, NY

## Output
Each lead includes:
- Company name
- Job title
- Location
- Salary (if listed)
- Post date
- Job URL (for research)
- Pain point summary
