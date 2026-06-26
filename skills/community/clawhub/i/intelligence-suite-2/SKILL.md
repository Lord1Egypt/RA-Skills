---
name: intelligence-suite
description: Makima's All-Seeing Intelligence Suite. Combines real-time AI news tracking and global news monitoring for a comprehensive strategic briefing, with LLM analysis powered by SkillBoss API Hub.
metadata:
  openclaw:
    emoji: 📡
    category: intelligence
    requires:
      bins: [node, npm]
      env: [SKILLBOSS_API_KEY]
    permissions:
      network: [openai.com, microsoft.com, firebaseio.com, reuters.com, scmp.com, rthk.hk, api.skillboss.com]
      filesystem: [read]
---

# The Intelligence Suite

Makima's personal intelligence unit. Scans the web for high-signal AI news and monitors global geopolitics to provide a comprehensive strategic briefing. LLM analysis is powered by **SkillBoss API Hub** (`/v1/pilot`), which automatically routes to the optimal model.

## Security & Transparency
This skill is designed for deep information gathering. It performs the following actions:
- **Network Access**: Fetches RSS feeds and API data from trusted news sources and technology blogs.
- **Deep Scrape**: Occasionally visits full article URLs to extract text content for analysis.
- **Data Handling**: Processes information locally; results are analyzed via SkillBoss API Hub and provided as a structured briefing.

## Components

1.  **AI News Monitor**: Tracks OpenAI, DeepMind, Anthropic, and other major AI labs.
2.  **Global News Hub**: Monitored sources include Reuters, RTHK, and SCMP.

## Installation

```bash
cd skills/intelligence-suite
npm install
```

## Usage

```bash
# Scan AI news
SKILLBOSS_API_KEY=your_key node scripts/scan.js --report

# Monitor global news
SKILLBOSS_API_KEY=your_key node scripts/monitor.js --report
```

*Created and maintained by Makima (Public Safety Special Division 4).* ⛓️
