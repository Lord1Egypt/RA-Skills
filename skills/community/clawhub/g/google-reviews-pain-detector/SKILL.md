# Google Reviews Pain Detector

**Skill:** `google-reviews-pain-detector`  
**Purpose:** Scrape Google reviews for businesses and detect "pain words" that signal missed calls, poor phone coverage, and lost customers — hot signals for Gracie AI Receptionist leads.

---

## What It Does

1. Accepts a business name (+ optional address) as input
2. Searches Google for `[business name] reviews` and scrapes result pages
3. Also attempts to scrape Google Maps reviews directly
4. Scans all review text for pain words indicating missed calls / unreachable staff
5. Outputs: business name, matched pain words, example snippets, and a **PAIN SCORE** (0–10)
6. Can run against the full Master Lead List with `--list`
7. Can append HOT-tagged leads (score ≥ 3) to the Master Lead List with `--save`

---

## Pain Words Detected

```
voicemail, no answer, hard to reach, couldn't get through, called 3 times,
never called back, missed call, didn't answer, goes to voicemail,
unanswered, unreachable, left a message
```

---

## Usage

### Single business
```bash
cd ~/StudioBrain/00_SYSTEM/skills/google-reviews-pain-detector
python3 detector.py "P.A.C. Plumbing Staten Island"
python3 detector.py "Victory Auto Repair" --address "3735 Victory Blvd, SI"
```

### Full lead list scan
```bash
python3 detector.py --list
```

### Scan + save HOT leads (score ≥ 3) back to master list
```bash
python3 detector.py --list --save
```

### JSON output
```bash
python3 detector.py "Rafi's Auto Repair" --json
python3 detector.py --list --json
```

---

## Output Example

```
══════════════════════════════════════════════════════
🔍 P.A.C. Plumbing, Heating & A/C
══════════════════════════════════════════════════════
📍 Address: 545 Port Richmond Ave, SI 10302
🔥 PAIN SCORE: 6/10
🎯 Pain Words Found: voicemail (3), no answer (1), never called back (1)

📋 Example Snippets:
  • "...went to voicemail every time I called after hours..."
  • "...no answer on Saturday, had to find another plumber..."
  • "...never called back after leaving a message..."

✅ HOT LEAD — Strong signal for Gracie AI Receptionist pitch
```

---

## Dependencies

- Python 3.9+
- Scrapling skill at `~/StudioBrain/00_SYSTEM/skills/scrapling/` (with `.venv`)
- No additional installs required

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This file |
| `detector.py` | Main script |
