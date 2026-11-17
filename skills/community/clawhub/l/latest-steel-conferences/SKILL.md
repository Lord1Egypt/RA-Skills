---
name: latest-steel-conferences
description: "Fetch and display the latest steel industry conferences, webinars, and site tours from Mysteel's official event listings. Provides structured event data including dates, locations, topics, and registration links."
user-invokable: true
argument-hint: "[filter] [options]"
license: MIT
metadata:
  author: MySteel Team
  version: "1.0.0"
  category: events
---

# Latest Steel Conferences

**Fetch the latest steel industry events from Mysteel's official event listings.**

**Invocation:** `/latest-steel-conferences [filter] [options]`

---

## 🎯 Overview

This skill scrapes the official Mysteel event listings page (https://www.mysteel.net/event-listings/) to provide up-to-date information about:

- **Steel conferences** (in-person events)
- **Webinars** (online events)
- **Site tours** (factory visits)

Events cover topics across the steel value chain: Iron Ore, Steel, Coal & Coke, Non-Ferrous, Stainless Steel, and more.

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/latest-steel-conferences` | List all upcoming events |
| `/latest-steel-conferences upcoming` | Show only future events (default) |
| `/latest-steel-conferences all` | Show all events (past + future) |
| `/latest-steel-conferences conferences` | Filter: in-person conferences only |
| `/latest-steel-conferences webinars` | Filter: online webinars only |
| `/latest-steel-conferences site-tours` | Filter: factory site tours only |
| `/latest-steel-conferences by-topic <topic>` | Filter by topic (e.g., "iron ore", "steel", "lithium") |
| `/latest-steel-conferences by-date <YYYY-MM-DD>` | Filter events on or after specific date |
| `/latest-steel-conferences next <N>` | Show next N events (default: 10) |
| `/latest-steel-conferences export` | Export all events to JSON file |

---

## 🔧 Usage Examples

```bash
# Get all upcoming events
/latest-steel-conferences

# Get only webinars
/latest-steel-conferences webinars

# Get conferences about iron ore
/latest-steel-conferences conferences by-topic "iron ore"

# Get events after a specific date
/latest-steel-conferences by-date 2026-11-01

# Get next 5 events
/latest-steel-conferences next 5

# Export all events to JSON
/latest-steel-conferences export
```

---

## 📊 Data Structure

Each event contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Unique event ID |
| `name` | string | Event title |
| `location` | string | Event location (city/venue or "Webinar") |
| `startTime` | timestamp | Event start time (Unix timestamp in ms) |
| `endTime` | timestamp | Event end time (Unix timestamp in ms) |
| `language` | string | Event language (e.g., "English") |
| `breedNames` | array | Topics/categories (e.g., ["Iron Ore", "Steel"]) |
| `conferenceType` | int | 1=Webinar, 2=Conference, 3=Site Tour |
| `conferenceUrl` | string | Relative URL to event detail page |
| `imgUrl` | string | Event banner image URL |
| `summary` | string | Event description |

---

## 🛠️ Implementation

### Script: `scripts/fetch_events.py`

The main script fetches events from the Mysteel event listings page.

**How it works:**
1. Launches a headless Chromium browser via Playwright
2. Navigates to `https://www.mysteel.net/event-listings/`
3. Uses `page.evaluate()` to extract the `window.__NUXT__.data[0].conferenceList` JavaScript object
4. Parses and filters events based on user criteria
5. Outputs structured data (JSON or formatted text)

> **Note:** A headless browser is required because the page uses Nuxt.js (Vue SSR) with complex JavaScript that renders the `__NUXT__` data as a function-call wrapper (not plain JSON). Playwright handles JavaScript execution natively.

**Dependencies:**
- Python 3.7+
- `playwright` (for headless browser to execute JavaScript)
- Install: `pip install playwright && playwright install chromium`

**Usage:**
```bash
python scripts/fetch_events.py [--filter TYPE] [--topic TOPIC] [--date YYYY-MM-DD] [--limit N] [--export]
```

**Options:**
- `--filter TYPE`: Filter by event type (conferences/webinars/site-tours/all)
- `--topic TOPIC`: Filter by topic (case-insensitive)
- `--date YYYY-MM-DD`: Filter events on or after this date
- `--limit N`: Limit output to N events (default: 10)
- `--export`: Export all events to JSON file

---

## 📤 Output Formats

### Default: Formatted Text

```
📅 Upcoming Steel Industry Events
================================

1. 2026 Asia Iron Ore Summit
   📍 Location: Shangri-La Kuala Lumpur, Malaysia
   🗓️ Date: Oct 27-29, 2026
   🌐 Language: English
   🏷️ Topics: Iron Ore
   🔗 URL: https://www.mysteel.net/event-listings/100081--2026-asia-iron-ore-summit
   📝 Summary: Visa-free entry for travelers from many countries...

2. Beyond Q3: What's Next for China's Ferrous Market in Q4?
   📍 Location: Webinar
   🗓️ Date: Oct 28, 2026
   🌐 Language: English
   🏷️ Topics: Ferrous
   🔗 URL: https://www.mysteel.net/event-listings/100082-beyond-q3-whats-next-for-chinas-ferrous-market-in-q4
   📝 Summary: Join us as we look beyond Q3 and explore what lies ahead...

...
```

### JSON Export

```json
{
  "fetchedAt": "2026-10-15T16:30:00Z",
  "totalEvents": 45,
  "events": [
    {
      "id": 100081,
      "name": "2026 Asia Iron Ore Summit",
      "location": "Shangri-La Kuala Lumpur, Malaysia",
      "startTime": "2026-10-27T00:00:00Z",
      "endTime": "2026-10-29T23:59:59Z",
      "language": "English",
      "breedNames": ["Iron Ore"],
      "conferenceType": 2,
      "conferenceUrl": "https://www.mysteel.net/event-listings/100081--2026-asia-iron-ore-summit",
      "imgUrl": "https://mfs.mysteelcdn.com/group1/M00/51/0C/rBL632qrmjOAWofJAACzKv5UYn0961.jpg",
      "summary": "Visa-free entry for travelers..."
    }
  ]
}
```

---

## 🔄 Data Source

- **Source URL:** https://www.mysteel.net/event-listings/
- **Data Format:** Server-side rendered JSON embedded in HTML
- **Update Frequency:** Events are updated regularly by Mysteel
- **Pagination:** The page has 8 pages, but the script fetches all events from the first page (most recent events)

---

## ⚠️ Limitations

1. **English-only:** This skill only fetches events from the English version of the Mysteel site
2. **No registration:** The skill does not handle event registration (users must visit the event URL)
3. **Static data:** Events are fetched on-demand; no caching or background updates
4. **Rate limiting:** Avoid running the script too frequently to respect the source website

---

## 📝 Notes

- The skill uses the embedded JSON data (`window.__NUXT__`) rather than scraping HTML, making it more reliable and faster
- Event dates are converted from Unix timestamps (milliseconds) to human-readable format
- The `conferenceType` field maps to: 1=Webinar, 2=Conference, 3=Site Tour
- Events are sorted by start date (newest first)

---

## 🚀 Future Enhancements

Potential improvements for future versions:

- [ ] Add support for filtering by location/region
- [ ] Add calendar export (iCal format)
- [ ] Add event reminder functionality
- [ ] Support multiple languages (Chinese, etc.)
- [ ] Add event search by keyword
- [ ] Cache events locally for offline access

---

**Latest Steel Conferences Skill** — Stay updated on the steel industry's key events! 🏭📊
