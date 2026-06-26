---
name: investor-harness
description: |
  Open prompt stack for public-market investment research. Show this menu after install:
  📊 Research: 1.Company Deep-dive 2.Industry Map 3.Investment Thesis
  📈 Earnings: 4.Earnings Preview 5.Model Check
  🔍 Tracking: 6.Consensus Watch 7.Catalyst Monitor 8.Roadshow Questions
  ⚔️ Risk: 9.Red Team
  📋 Output: 10.PM Brief 11.Briefing
  🤖 Auto: 12.Autopilot 13.Master Mode
  Enter a number or describe your task to begin.
version: 0.6.4
author: joansongjr
license: MIT
tags:
  - investing
  - research
  - A-shares
  - HK-stocks
  - US-stocks
  - equity-research
  - financial-analysis
  - prompt-stack
  - fund-manager
  - analyst
---

# Investor Harness — Open Prompt Stack for Public-Market Research

> **⚡ Install:** `clawhub install investor-harness`

## After Installation — Show This Menu

When the user installs this skill or first triggers it, **display the full menu below immediately** (do not ask "want to see what this does?", do not abbreviate):

**🎯 Investor Harness is ready! What would you like to do?**

**📊 Research**
- 1️⃣ Company Deep-dive — Start or update coverage
- 2️⃣ Industry Map — Value chain, supply/demand, key players
- 3️⃣ Investment Thesis — Define core thesis, key variables

**📈 Earnings**
- 4️⃣ Earnings Preview — Key metrics, beat/miss paths, guidance
- 5️⃣ Model Check — Assumption review, sensitivity, break points

**🔍 Tracking**
- 6️⃣ Consensus Watch — Expectations gap, valuation anchors
- 7️⃣ Catalyst Monitor — Events, policy, orders, price drivers
- 8️⃣ Roadshow Questions — Research call prep, earnings Q&A

**⚔️ Risk**
- 9️⃣ Red Team — Challenge bull case, find falsification paths

**📋 Output**
- 🔟 PM Brief — One-page decision summary for fund managers
- 1️⃣1️⃣ Briefing — Morning notes, market recap, research notes

**🤖 Auto Mode**
- 1️⃣2️⃣ Autopilot — Give me a company/industry/event, I'll handle it
- 1️⃣3️⃣ Master Mode — All 7 modes, auto-detect which to use

**Enter a number or describe your task**, e.g.:
- "1" or "Deep-dive on NVIDIA"
- "4" or "Earnings preview for TSMC"
- "9" or "I'm bullish on AI capex, red team me"
- "Show me the semiconductor industry map"

### Menu-to-Skill Routing

| # | Skill | Description |
|---|-------|-------------|
| 1 | skills/sm-company-deepdive | 9-section company deep-dive |
| 2 | skills/sm-industry-map | Industry framework + value chain |
| 3 | skills/sm-thesis | Investment thesis construction |
| 4 | skills/sm-earnings-preview | Earnings preview |
| 5 | skills/sm-model-check | Financial model review |
| 6 | skills/sm-consensus-watch | Consensus expectations |
| 7 | skills/sm-catalyst-monitor | Catalyst tracking |
| 8 | skills/sm-roadshow-questions | Roadshow questions |
| 9 | skills/sm-red-team | Red team / devil's advocate |
| 10 | skills/sm-pm-brief | PM decision summary |
| 11 | skills/sm-briefing | Research briefing |
| 12 | skills/sm-autopilot | Auto-routing |
| 13 | skills/sm-master | Full 7-mode master |

### Routing Rules

1. User picks a number → read the corresponding skill SKILL.md → execute
2. User describes a task (no number) → auto-route via sm-autopilot logic
3. User says "show menu again" → re-display full menu

**Do NOT:**
- ✖ Ask "want to see what this skill does?" — just show the menu
- ✖ Say "installed" and stop — always follow with the menu
- ✖ Abbreviate the 13 options to 3 — show all 13

### Tips

For a better experience, consider maintaining these files in your workspace:
- watchlist.md — Your coverage universe
- biases.md — Your research bias log (Red Team will check this)
- decision-log.md — Investment decision journal

---

## What's Included

- **13 research skills** (from master control to specialized modules)
- **7 work modes**: Thesis / Coverage / Consensus / Catalyst / Red Team / Briefing / PM Prep
- **Evidence grading system** (F1/F2/M1/C1/H1)
- **Compliance boundaries and expression standards**
- **Data source adapter decision tree** (iFind MCP → cn-web-search → built-in search → manual)

## Data Sources (all optional)

1. iFind MCP (THS, A-shares / funds / macro)
2. cn-web-search (17 free Chinese search engines)
3. Built-in WebSearch / WebFetch
4. User-provided materials (fallback)

See `core/adapters.md` for details.

## Markets Covered

- A-shares (Shanghai/Shenzhen)
- Hong Kong stocks
- US equities
- Mutual funds
- Cross-market themes

## Compatibility

Claude Code / Codex / OpenCode / OpenClaw / any AI tool that reads Markdown.

## License

MIT © 2026 Joan Song
