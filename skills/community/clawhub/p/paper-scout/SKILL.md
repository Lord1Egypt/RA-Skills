---
name: paper_scout
description: Search and summarize research papers in robotics and related fields. Use when asked to find recent papers, digest academic literature, or scout publications from venues like TRO, IJRR, RAL, Science Robotics, CVPR, ICLR. Uses CrossRef as primary source and Google Scholar as backup.
metadata: { "openclaw": { "emoji": "🔭" } }
---

# SKILL.md - paper_scout

---

### Overview

`paper_scout` automates searching and summarizing research papers in robotics and related fields. It uses **CrossRef** as the primary data source, with **Google Scholar** as the supplementary source for missing fields or broader coverage.

---

### Functionality

1. **Primary Query Engine:**
   - **CrossRef**: Quick and structured search for venues like TRO, IJRR, Science Robotics, etc.

2. **Backup Source:**
   - **Google Scholar**: Scrapes data using real-time browser automation for keywords and specific venues.

3. **Filters:**
   - Keywords:
     > `muscle parameter estimation`, `reinforcement learning`, `imitation learning`, `human intention prediction`, `human-robot interaction collaboration`.
   - Top venues: TRO, IJRR, RAL, Science Robotics, TMech, CVPR, ICLR, ICCV.
   - Date: Year filtering to prioritize recent publications (e.g., `since 2024`).

4. **Data Outputs:**
   Structured Markdown reports saved to `~/Desktop/YYYY-MM-DD-academic-digest.md` with fields:
   - Title
   - Source venue (e.g., Science Robotics)
   - Year
   - Authors
   - Abstract
   - Major contributions/innovation points

---

### Example Configuration

```yaml
# paper_scout SKILL.yaml
crawl:
  sources:
    - crossref
    - scholar_google
queries:
  custom: []  # User-provided
  defaults:
    - reinforcement learning robotics
    - human intention prediction imitation learning
filters:
  venues: ["TRO", "IJRR", "Science Robotics", "RAL", "CVPR"]
  date: since:2024
output:
  path: ~/Desktop/{{today}}-academic-digest.md
  markdown: true
```

---

### Example Usage

1. Query Crossref for `reinforcement learning robotics` papers since 2024.
2. Supplement missing information by scraping Google Scholar (`sorted by date`).
3. Remove duplicates, filter results to top academic venues.
4. Save a Markdown digest to the desktop.

---

### Notes

- Automates cross-source integration with duplicate removal.
- Extensible for more specialized sources (e.g., IEEE, PubMed).
- Browser scraping (Google Scholar) requires interactive sessions for JS-heavy pages.