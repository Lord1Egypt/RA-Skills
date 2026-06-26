---
name: nyc-311-reporter
description: Automate NYC 311 service request filing by browsing the 311 portal with Playwright. Scrapes complaint categories, finds forms, fills them with user data, and submits reports. Use when the user wants to file a complaint via NYC 311 and needs end-to-end browser automation.
---

# NYC 311 Reporter

Automates NYC 311 complaint filing using Playwright for browser automation.

## Workflow

### Step 1: Read User Complaint
Extract from natural language:
- **Location** — Where is the issue?
- **Description** — What is happening?
- **Vehicle/Details** — Car make, model, color, plate if available
- **Duration** — How long has it been there?
- **Photos** — Does the user have photos?

### Step 2: Scrape Categories
Run the browser script to explore available complaint categories:

```bash
python3 scripts/browse_311.py scrape
```

### Step 3: Find the Right Form
For fire hydrant complaints:

```bash
python3 scripts/browse_311.py find
```

### Step 4: Fill and Submit
Run with your complaint details:

**Dry run (preview only):**
```bash
python3 scripts/browse_311.py submit \
  --location "726 DeKalb Avenue, Brooklyn, NY" \
  --vehicle "Gray Nissan Micra" \
  --duration "10 hours" \
  --name "Ricardo Díaz" \
  --email "ricardo@example.com" \
  --phone "+19299990000"
```

**Actual submission:**
```bash
python3 scripts/browse_311.py submit \
  --location "726 DeKalb Avenue, Brooklyn, NY" \
  --vehicle "Gray Nissan Micra" \
  --duration "10 hours" \
  --name "Ricardo Díaz" \
  --email "ricardo@example.com" \
  --phone "+19299990000" \
  --submit
```

## User Profile

Store user information in `assets/config.json`:

```json
{
  "name": "Ricardo Díaz",
  "phone": "+19299990000",
  "email": "ricardo@example.com",
  "home_address": "726 DeKalb Avenue",
  "work_address": "726 DeKalb Avenue",
  "apartment": "1E",
  "preferred_contact": "email",
  "notify_updates": true
}
```

## Scripts

- `scripts/browse_311.py` — Main automation script:
  - `scrape` — List all complaint categories
  - `find` — Find the fire hydrant/parking form
  - `submit` — Fill and optionally submit the form

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## Notes

- Screenshots are saved to `/tmp/` for review
- The script handles JavaScript-heavy pages
- Run without `--submit` first to verify the form fills correctly
- If 311 portal has technical issues, the script will report errors