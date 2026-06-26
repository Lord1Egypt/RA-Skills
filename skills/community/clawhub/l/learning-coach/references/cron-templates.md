# Per-Subject Cron Templates (v0.3)

Use `scripts/subject_cron.py` to generate schedule templates by subject.

Templates:
- `light`: weekdays only coaching
- `standard`: daily coaching + 2 curation refreshes weekly
- `intensive`: earlier/later daily cadence + 3 curation refreshes weekly

Flow:
1. Generate candidate jobs JSON.
2. Show jobs to user and ask approval.
3. Apply approved jobs with `setup_cron.py` or user-selected method.
