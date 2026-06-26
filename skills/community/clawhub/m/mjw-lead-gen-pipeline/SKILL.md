---
name: lead-gen-pipeline
description: Full automated lead generation pipeline for web design agencies. Finds local businesses without websites or with broken sites, builds demo HTML sites for them, and sends personalized cold pitch emails. Use when asked to "find leads", "run the pipeline", "find businesses without websites", "build demo sites for leads", or "send pitches". Supports full-auto mode or step-by-step execution. Tracks all leads in leads.md.
---

# Lead Gen Pipeline

Full pipeline: find → qualify → build → pitch. Tracks everything in `leads.md`.

## Commands

| What you say | What runs |
|---|---|
| `run pipeline [trade] in [city, state]` | Full auto: find, qualify, build, deploy, email |
| `find leads [trade] in [city, state]` | Steps 1–2 only: search + qualify |
| `build sites` | Step 3–4: build + deploy pending leads |
| `send pitches` | Step 5: email all deployed-but-not-pitched leads |
| `show leads` | Print leads.md summary |

## Step 1: Find Leads

Use `web_search` with queries like:
- `"[trade] in [city] [state]"`
- `"best [trade] near [city]" site:yelp.com OR site:thumbtack.com`
- `"[trade] [city] [state] contact"`

Collect: business name, phone, address, website (if any), source URL.

Aim for 20–40 raw results before filtering.

## Step 2: Qualify Leads

For each business, check their website:
- **No website** → top priority lead ✅
- **Website loads but looks bad** (mobile broken, no SSL, >5 years old aesthetic) → good lead ✅
- **Good modern website** → skip ❌

Use `web_fetch` to check each URL. Look for: missing viewport meta, table layouts, broken images, no HTTPS.

Save qualified leads to `leads.md` using the schema in references/leads-schema.md.

Max 10–15 qualified leads per run to stay within email limits.

## Step 3: Build Demo Sites

For each qualified lead, generate a clean demo HTML site:

**Structure:**
- Hero: business name + tagline ("Serving [City] Since [Year]")
- Services: 3–5 services based on their trade
- Contact: phone number + service area
- Mobile responsive, pure HTML/CSS, no dependencies

Use their actual business name, phone, trade, and city.
Save to `demo-sites/[business-slug]/index.html`.

See references/demo-site-template.md for the HTML template.

## Step 4: Deploy Demo Sites

Deploy each demo site to the VPS. Use the site-cloner skill's VPS deploy pattern.

**Port allocation:** Start at 8090+ for lead gen demo sites (avoid conflicts with client sites).

Update `leads.md` with the live demo URL after deploy.

## Step 5: Send Pitch Emails

For each lead with status `deployed` and no `pitched_at` date:

Use the gog (Gmail) skill to send pitch emails.

**Email template:** See references/pitch-template.md

**Rules:**
- Max 20 emails/day
- Personalize: use their business name, city, trade
- Include their live demo URL
- Subject: `[Business Name] — Your New Website is Ready`

Update `leads.md` status to `pitched` + add `pitched_at` date after sending.

## leads.md Schema

See references/leads-schema.md for the full schema.

Quick format:
```
| Business | Phone | City | Trade | Website | Demo URL | Status | Pitched |
```

Status values: `qualified` → `built` → `deployed` → `pitched` → `replied` → `closed`
