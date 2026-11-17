# Latest Steel Conferences

> 🔧 **MyClaw Skill** — Fetch the latest steel industry conferences, webinars, and site tours from Mysteel's official event listings.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)]()

---

## 📖 Overview

**Latest Steel Conferences** is a MyClaw skill that scrapes [Mysteel's official event listings](https://www.mysteel.net/event-listings/) to provide real-time information about upcoming steel industry events worldwide.

Whether you're a steel trader, analyst, procurement manager, or industry researcher — this skill helps you stay on top of the conferences, webinars, and site tours that matter.

### What It Does

- ✅ Fetches **all upcoming steel events** from Mysteel's English site
- ✅ Filters by **event type**: conferences, webinars, site tours
- ✅ Filters by **topic**: Iron Ore, Steel, Coal & Coke, Non-Ferrous, Lithium, etc.
- ✅ Filters by **date range**
- ✅ Outputs in **human-readable text** or **structured JSON**
- ✅ Exports to **JSON file** for integration with other tools
- ✅ No API key required — works out of the box

### Data Source

All data comes from [Mysteel's official event listings page](https://www.mysteel.net/event-listings/), the English-language portal of Shanghai SteelUnion (Mysteel), one of the world's leading commodity data and information providers.

---

## 🚀 Quick Start

### Installation

1. Download or clone this skill into your MyClaw skills directory:

```bash
# Place in your MyClaw skills folder
skills/
└── latest-steel-conferences/
    ├── SKILL.md
    ├── README.md
    └── scripts/
        └── fetch_events.py
```

2. Install dependencies:

```bash
pip install playwright
playwright install chromium
```

3. No additional API keys needed — works out of the box!

### Basic Usage

```bash
# Show all upcoming events
/latest-steel-conferences

# Show only webinars
/latest-steel-conferences webinars

# Show conferences about iron ore
/latest-steel-conferences conferences by-topic "iron ore"

# Show events after a specific date
/latest-steel-conferences by-date 2026-11-01

# Export all events to JSON
/latest-steel-conferences export
```

### Direct Script Usage

You can also run the Python script directly:

```bash
python scripts/fetch_events.py --filter conferences --topic "iron ore" --limit 5
python scripts/fetch_events.py --format json --all
python scripts/fetch_events.py --export
```

---

## 📋 Commands Reference

| Command | Description |
|---------|-------------|
| `/latest-steel-conferences` | List all upcoming events (default: next 10) |
| `/latest-steel-conferences upcoming` | Show only future events |
| `/latest-steel-conferences all` | Show all events (past + future) |
| `/latest-steel-conferences conferences` | Filter: in-person conferences only |
| `/latest-steel-conferences webinars` | Filter: online webinars only |
| `/latest-steel-conferences site-tours` | Filter: factory site tours only |
| `/latest-steel-conferences by-topic <topic>` | Filter by topic (e.g., "iron ore", "steel", "lithium") |
| `/latest-steel-conferences by-date <YYYY-MM-DD>` | Filter events on or after specific date |
| `/latest-steel-conferences next <N>` | Show next N events |
| `/latest-steel-conferences export` | Export all events to JSON file |

---

## 📊 Sample Output

### Text Format

```
📅 Upcoming Steel Industry Events
==================================================
   Total: 10 event(s)
   Source: https://www.mysteel.net/event-listings/
   Fetched: 2026-10-15 16:30:00

1. 2026 Asia Iron Ore Summit
   📍 Location: Shangri-La Kuala Lumpur, Malaysia
   🗓️  Date: Oct 27-29, 2026
   🌐 Language: English
   📋 Type: Conference
   🏷️  Topics: Iron Ore
   🔗 URL: https://www.mysteel.net/event-listings/100081--2026-asia-iron-ore-summit
   📝 Summary: Visa-free entry for travelers from many countries...

2. Beyond Q3: What's Next for China's Ferrous Market in Q4?
   📍 Location: Webinar
   🗓️  Date: Oct 28, 2026
   🌐 Language: English
   📋 Type: Webinar
   🏷️  Topics: Ferrous
   🔗 URL: https://www.mysteel.net/event-listings/100082-beyond-q3-whats-next...
   📝 Summary: Join us as we look beyond Q3 and explore what lies ahead...
```

### JSON Format

```json
{
  "fetchedAt": "2026-10-15T16:30:00+00:00",
  "source": "https://www.mysteel.net/event-listings/",
  "totalEvents": 10,
  "events": [
    {
      "id": 100081,
      "name": "2026 Asia Iron Ore Summit",
      "location": "Shangri-La Kuala Lumpur, Malaysia",
      "startDate": "2026-10-27T00:00:00+00:00",
      "endDate": "2026-10-29T23:59:59+00:00",
      "dateRange": "Oct 27-29, 2026",
      "language": "English",
      "type": "Conference",
      "topics": ["Iron Ore"],
      "url": "https://www.mysteel.net/event-listings/100081--2026-asia-iron-ore-summit",
      "summary": "Visa-free entry for travelers..."
    }
  ]
}
```

---

## 🏷️ Supported Topics

The skill can filter by any of these industry topics (and more):

| Topic | Description |
|-------|-------------|
| **Iron Ore** | Iron ore markets, pricing, and trade |
| **Steel** | Steel production, pricing, and market analysis |
| **Ferrous** | Broad ferrous metals coverage |
| **Coal & Coke** | Coking coal, thermal coal, and coke markets |
| **Non-Ferrous** | Copper, aluminum, zinc, nickel, etc. |
| **Stainless Steel** | Stainless steel markets and nickel/chrome |
| **Lithium** | Lithium and battery materials |
| **Steel Scrap** | Scrap metal markets and recycling |
| **Ferroalloys** | Manganese, silicon, chrome alloys |

You can also search by any keyword — the skill will match against event names, topics, and descriptions.

---

## 🔧 Technical Details

### How It Works

1. **Launches** a headless Chromium browser via Playwright
2. **Navigates** to `https://www.mysteel.net/event-listings/`
3. **Extracts** the event data from `window.__NUXT__.data[0].conferenceList` using `page.evaluate()`
4. **Enriches** each event with computed fields (formatted dates, URLs, type names)
5. **Filters** based on user criteria (type, topic, date)
6. **Outputs** in the requested format (text or JSON)

### Why Playwright?

The Mysteel event page is built with Nuxt.js (Vue SSR). The `__NUXT__` data is wrapped in a complex JavaScript function call with variable references — not plain JSON. While there is also an XHR endpoint (`/english/notice/queryList`), it requires specific session parameters.

Using Playwright to execute the JavaScript natively is:

- ✅ **Reliable** — handles the Nuxt.js function wrapper automatically
- ✅ **Accurate** — gets the exact same data the browser sees
- ✅ **Simple** — no need to reverse-engineer the JS function or API params
- ✅ **Fast** — headless mode, no visible browser window

### Dependencies

The script requires **Playwright** for headless browser automation:

```bash
pip install playwright
playwright install chromium
```

**Why Playwright?** The Mysteel event page uses Nuxt.js (Vue SSR) with complex JavaScript that renders the `__NUXT__` data as a function-call wrapper (not plain JSON). Playwright handles JavaScript execution natively, making data extraction reliable and straightforward.

**Additional standard library modules used:**
- `json` — JSON parsing
- `datetime` — Date handling
- `argparse` — Command-line arguments

---

## ⚠️ Limitations

- **English-only**: Only fetches from the English version of the Mysteel site
- **No registration**: Does not handle event registration (visit the event URL to register)
- **Static data**: Events are fetched on-demand; no background sync
- **Rate limiting**: Avoid running too frequently to respect the source website
- **First page only**: Fetches the most recent events (page 1 of 8)

---

## 🤝 Contributing

Found a bug or have a feature request? Feel free to:

1. Open an issue on the skill repository
2. Submit a pull request with your changes
3. Contact the MyClaw team

### Potential Enhancements

- [ ] Multi-language support (Chinese, etc.)
- [ ] Calendar export (iCal format)
- [ ] Event reminder notifications
- [ ] Location-based filtering
- [ ] Keyword search across all event fields
- [ ] Local caching for offline access
- [ ] Pagination support (fetch all 8 pages)

---

## 📄 License

MIT License — free for personal and commercial use.

---

## 🏢 About Mysteel

**Mysteel** (Shanghai SteelUnion, stock code: 300226) is a leading global provider of commodity data and information services. With over 20 years of experience, Mysteel covers 8 major industries including ferrous metals, non-ferrous metals, energy & chemicals, building materials, and more.

- **Website**: [https://www.mysteel.com](https://www.mysteel.com)
- **English Portal**: [https://www.mysteel.net](https://www.mysteel.net)
- **Data Services**: Price indices, market analysis, industry reports

---

**Made with ❤️ for the global steel community**

*Stay updated on the steel industry's key events!* 🏭📊
