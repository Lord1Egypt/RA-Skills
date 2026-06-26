# 3-Minute Demo Script (Global Nuclear Brief)

## 0:00–0:20 — Problem + Pitch
"Policy and regulatory shifts in nuclear energy are global and fast. Teams waste time scanning scattered sources. We built **Global Nuclear Brief**, an OpenClaw skill that turns live updates into a grounded, decision‑ready brief in minutes."

## 0:20–0:45 — Architecture (1 sentence)
"Apify pulls live nuclear policy/regulatory news, and Contextual generates a structured brief grounded only in those sources."

## 0:45–1:45 — Live Run
Run:
```bash
python3 bin/nuclear_brief.py \
  --query "nuclear energy policy OR nuclear regulation" \
  --topic "Global nuclear energy policy" \
  --audience "policy analysts" \
  --country "US" \
  --timeframe "7d"
```
Callouts while it runs:
- "This is the live source pull from Apify."
- "Now Contextual synthesizes a brief grounded in those sources only."

## 1:45–2:30 — Output Walkthrough
Highlight:
- Top changes
- Why it matters
- Recommended actions
- Sources (titles + links)

## 2:30–3:00 — Why it wins
"This is a real workflow: live data → grounded reasoning → actionable output. It’s immediately useful and production‑shaped."

---

# Demo Checklist
- [ ] APIFY_API_TOKEN set
- [ ] CONTEXTUAL_API_KEY set
- [ ] Run command once before demo to warm up
- [ ] Know 1–2 sources to point at
- [ ] Keep to 3 minutes (no slides)
