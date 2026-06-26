# Environment — credentials format

Credentials are stored in `/root/.openclaw/workspace/.env/galim.env`.

Same Ministry of Education student IDs and passwords work for both portals.

```bash
# Galim Pro
GALIM_USERNAME_CHILD1=<student_id>
GALIM_PASSWORD_CHILD1=<password>
GALIM_USERNAME_CHILD2=<student_id>
GALIM_PASSWORD_CHILD2=<password>

# Optional display names
# GALIM_NAME_CHILD1=Child 1
# GALIM_NAME_CHILD2=Child 2

# Ofek (same credentials)
OFEK_USERNAME_CHILD1=<student_id>
OFEK_PASSWORD_CHILD1=<password>
OFEK_USERNAME_CHILD2=<student_id>
OFEK_PASSWORD_CHILD2=<password>

# Optional display names
# OFEK_NAME_CHILD1=Child 1
# OFEK_NAME_CHILD2=Child 2
```

## Run

```bash
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/fetch_tasks.py
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/fetch_tasks.py --json
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/galim_fetch_tasks.py
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/unified_report.py
```
