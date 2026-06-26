# Google Maps Batch Search — Practical Guide

## Overview

This document covers the practical steps for batch-searching Google Maps using agent-browser, extracting candidate listings, and handling common issues.

---

## Search Strategy

### Multi-keyword search

Don't just search one keyword. Derive search terms from the profile's business tags.

**Generic keyword mapping** (customize per industry):

| Industry | Search terms |
|-----------|-------------|
| Auto body / collision | "auto body shop", "auto body repair", "collision repair", "collision center" |
| Paint / coating | "paint shop", "spray booth", "auto paint shop", "powder coating" |
| Manufacturing | "machine shop", "fabrication shop", "CNC machining", "metal fabrication" |
| HVAC | "HVAC contractor", "heating and cooling", "air conditioning service" |
| Dental / medical | "dental lab", "dental clinic", "medical equipment" |

**Rule**: Derive search terms from the source customer's industry. Always use 2-4 keyword variations per area.

**Rule**: Use 2-4 keyword variations per search area to maximize coverage.

### Multi-area search

When the source customer serves multiple nearby cities, search each city separately and merge results.

**Example**: Source customer is in Kirkland WA, serving Bellevue/Redmond/Bothell → search all 4 cities.

**Merge & dedup rules**:
- Same name + same address → duplicate (keep the one with more data)
- Same name + different address → likely different locations of a chain (keep both)
- Same address + different name → different businesses (keep both)

---

## Agent-Browser Search Process

### Step 1: Open Google Maps search

```bash
agent-browser open "https://www.google.com/maps/search/auto+body+shop+Kirkland+WA"
```

Wait 3-4 seconds for full page load.

### Step 2: Extract listings from feed

```bash
# Get the feed region's text content
agent-browser eval "document.querySelector('[role=feed]')?.innerText?.substring(0, 5000)"
```

This returns all visible listing summaries including: name, rating, business type, address, phone, open/closed status.

### Step 3: Extract interactive elements (for clicking)

```bash
agent-browser snapshot -i
```

Find `article` elements with business names — their links are what you click to open detail panels.

### Step 4: Get detail panel data

Click on a business name link, wait 2-3 seconds, then:

```bash
agent-browser eval "document.body?.innerText?.substring(0, 5000)"
```

The detail panel appears alongside the feed and contains: full address, phone, hours, website, services, reviews summary, posts.

### Step 5: Close and move to next

After extracting data from the detail panel, you can either:
- Click another listing in the feed (faster, stays on same page)
- Or close the detail panel first with the close button

---

## Common Issues & Solutions

### "Restricted View" (受限视图)

Google Maps shows a restricted view when not logged in. Impact:
- **Can see**: Business name, rating, address, phone, hours, website, business type
- **Cannot see**: Review count, individual reviews, some photos, full service list

**Workaround**: Use `web_fetch` to visit the business's own website for enrichment. Use Yelp/BBB as supplementary sources for review counts.

### List only shows 7-8 results

The initial view shows ~7-8 listings. To see more:
```bash
agent-browser scroll down 3000
```
Then re-extract. Google Maps loads more results on scroll.

### eval returns empty for articles

Some pages render differently. Try:
```bash
# Fallback: get body text
agent-browser eval "document.body?.innerText?.substring(0, 6000)"

# Or try feed selector with different attribute
agent-browser eval "document.querySelector('[role=feed]')?.innerText"
```

### Pages not loading

Add explicit wait after navigation:
```bash
agent-browser open "https://www.google.com/maps/search/..."
sleep 4
agent-browser eval "..."
```

---

## Data Extraction Template

For each listing in the feed, extract these fields:

| Field | Source | Extraction method |
|-------|--------|-------------------|
| Name | Feed text | Parse from listing text |
| Rating | Feed text | Number before "汽车车身修理厂" or similar type label |
| Address | Feed text | After the type label |
| Phone | Feed text | Number in (xxx) xxx-xxxx format |
| City | Search query | From the search location |
| Has website | Feed snapshot | "网站" link visible in interactive elements |
| Chain marker | Feed text | Known chain names: Crash Champions, Caliber, Fix Auto, CARSTAR, etc. |
| Online booking | Feed text | "在线预订" link visible |
| Open/closed | Feed text | Current status |

**Regex patterns for extraction** (Chinese UI):
```
Rating:     /(\d\.\d)\n/ (number before business type)
Phone:      /\((\d{3}\)\s?\d{3}-\d{4})/
Address:    After business type label, before "已结束营业" or "正在营业"
```

---

## Performance Tips

1. **Batch by city** — Search one city at a time, extract all listings, then move to next city
2. **Don't click into every detail** — Feed-level data (name, rating, phone, address) is sufficient for initial screening. Only click into details for high-priority candidates
3. **Use eval over snapshot** — `eval` with `innerText` is faster than `snapshot -i` for bulk text extraction
4. **Close browser between cities** — Prevents memory buildup: `agent-browser close` then reopen for next search
5. **Parallel with web_fetch** — While agent-browser searches Maps, use `web_fetch` to visit websites of already-identified candidates

---

## Search Area Radius Guidelines

| Scenario | Radius | Rationale |
|----------|--------|-----------|
| 1 known customer | 50mi / 80km | Broad enough for similar businesses |
| 2-3 clustered customers | 30mi / 50km from center | Area is validated by multiple data points |
| Dense urban area | 15-20mi / 25-30km | More businesses per square mile |
| Rural area | 75-100mi / 120-160km | Businesses are spread out |
| User-specified | Use user's range | Always respect user preference |

**Search multiple cities** when the source customer serves a metro area (e.g., Seattle metro → Kirkland + Bellevue + Redmond + Bothell).
