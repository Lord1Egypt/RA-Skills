---
name: pantry-tracker
description: Track grocery purchases and monitor food freshness using Supabase. Use when monitoring grocery orders, checking what food is expiring, logging pantry items, getting morning freshness summaries, or managing food waste. Email scanning is done by the agent using its existing email skill (e.g. gog for Gmail) — this skill does not access email directly or require email credentials.
requires:
  env:
    - name: SUPABASE_URL
      description: Supabase project URL (e.g. https://xxx.supabase.co)
      required: true
    - name: SUPABASE_KEY
      description: Supabase anon key (NOT service role key). Safe for client-side use.
      required: true
---

# Pantry Tracker

Track grocery items from purchase to plate (or trash). Parses grocery order emails, stores items in Supabase with estimated expiry dates, and sends daily summaries of what needs eating.

## Setup

### 1. Supabase
Create a Supabase project and run the schema in `references/supabase-schema.sql` in the SQL editor.

Store credentials as env vars:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

Use the **anon key** (not the service role key). The anon key is safe for client-side use and sufficient for all pantry operations. Never use the service role key — it bypasses Row Level Security.

### 2. Cron Jobs
Set up two cron jobs in OpenClaw:

**Email scanner** (every 2-4 hours):
Use the agent's existing email tool (e.g. `gog` for Gmail, or whatever email skill is installed) to search for grocery order confirmations. This skill does NOT access email directly — the agent reads email through its own authenticated tools, then passes parsed items to the pantry CLI.
```
Search email for recent grocery orders (Whole Foods, Instacart, Amazon Fresh, Costco, Walmart). Parse item names and quantities. For each item, look up shelf life in references/shelf-life.md and calculate expires_at from today. Write items to a JSON array and run: python3 scripts/pantry.py bulk-add /tmp/pantry-items.json
```

**Morning summary** (daily, e.g. 7am):
```
Run: python3 scripts/pantry.py summary
If output is not "PANTRY_OK", send the summary to the user.
```

## CLI Reference

All commands: `python3 scripts/pantry.py <command>`

| Command | Description |
|---------|-------------|
| `add <name> -c <category> -q <qty> -e <days>` | Add single item |
| `bulk-add <file.json>` | Add items from JSON (email parse output) |
| `expiring [--days N]` | Show items expiring within N days (default 3) |
| `status` | Full pantry overview by category |
| `use <name>` | Mark item as used |
| `toss <name>` | Mark item as tossed/wasted |
| `refresh` | Auto-update statuses (fresh → use-soon → expired) |
| `summary` | Morning summary for cron (outputs PANTRY_OK if nothing urgent) |

### Bulk-add JSON format
```json
[
  {
    "name": "Strawberries",
    "category": "produce",
    "quantity": "1 lb",
    "expires_days": 5,
    "source": "whole-foods",
    "order_id": "111-1234567"
  }
]
```

## Email Parsing Guide

When scanning grocery emails, extract:
1. **Item name** — normalize to common name (e.g., "Org Strawberries 1lb" → "Strawberries")
2. **Quantity** — preserve as-is from email ("2 lbs", "1 bunch", "6 ct")
3. **Category** — assign: produce, dairy, meat, bakery, pantry, frozen, other
4. **Shelf life** — look up in `references/shelf-life.md`. If not listed, estimate conservatively.
5. **Source** — which store (whole-foods, instacart, costco, etc.)

### Supported email patterns
- **Whole Foods / Amazon Fresh**: Subject contains "Your delivery" or "order delivered"
- **Instacart**: Subject contains "delivery complete" or "order receipt"
- **Costco**: Subject contains "order confirmation"
- **Walmart**: Subject contains "delivery confirmed"

Search email for these patterns. Parse the item list from the email body. When in doubt about an item's category or shelf life, use conservative estimates.

## Manual Usage

Users can also say things like:
- "Add chicken breast to the pantry, expires in 2 days"
- "What's expiring soon?"
- "Mark the strawberries as used"
- "I tossed the leftover salmon"
- "What's in my pantry right now?"

Map these to the appropriate CLI commands.
