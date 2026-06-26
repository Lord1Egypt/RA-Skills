# Gracie CRM Skill

A lightweight CLI CRM for tracking Gracie AI Receptionist sales leads.

## Location
`~/StudioBrain/00_SYSTEM/skills/gracie-crm/`

## Data Store
`crm.json` — JSON array of lead objects

## Commands

```bash
cd ~/StudioBrain/00_SYSTEM/skills/gracie-crm

# List all leads sorted by follow-up date
python3 crm.py list

# Add a new lead
python3 crm.py add --name "Victory Auto" --phone "718-698-9896" --category "auto"

# Log a call result
python3 crm.py call <id> --outcome "no answer" --followup "2026-03-01"

# Add a note to a lead
python3 crm.py note <id> "Owner is Mike, best time is 8am"

# Show leads due today or overdue
python3 crm.py today

# Import leads from MASTER_LEAD_LIST.md
python3 crm.py import

# Show pipeline summary
python3 crm.py pipeline
```

## Status Values
- `new` — Not yet contacted
- `called` — Call made
- `no_answer` — No answer
- `interested` — Lead showed interest
- `demo_sent` — Demo/proposal sent
- `closed_won` — Deal closed ✅
- `closed_lost` — Deal lost ❌

## Lead Schema
```json
{
  "id": 1,
  "name": "Victory Auto Repair",
  "phone": "718-698-9896",
  "category": "auto",
  "status": "new",
  "calls": [{"date": "2026-02-27", "outcome": "no answer", "notes": ""}],
  "notes": [],
  "followup_date": null,
  "added": "2026-02-27"
}
```

## Categories
- `auto` — Auto repair shops
- `hvac` — HVAC / plumbing
- `dental` — Dental practices
- `insurance` — Insurance agencies
- `medical` — Medical offices
- `legal` — Law firms
- `other` — Everything else

## Skill Trigger
Use this skill when Jay asks to:
- Check leads / call list
- Log a call outcome
- See what follow-ups are due
- Add a new prospect
- Review the Gracie sales pipeline
