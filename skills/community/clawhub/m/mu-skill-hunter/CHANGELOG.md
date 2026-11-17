# Changelog

All notable changes to this project will be documented in this file.

## [2.8.0] - 2026-07-30

### What's New

- ✨ Feature: Four-source search now collects 80+ results per query (up from 26), with Skills.sh as the 4th source
- ✨ Feature: Unified scoring algorithm (Heat 50% + Relevance 30% + Freshness 20%) with forced source diversity in weekly reports
- ✨ Feature: Security scanner with 12 rules (10 Hard Reject + 2 AI-specific) and sandbox isolation
- ✨ Feature: Weekly report template with Cron automation, top 8 curated picks + backup section
- ✨ Feature: Parallel CLI calls with per-call timeouts (ClawHub inspect batch, Skills.sh find batch)
- ✨ Feature: User scene profiling for personalized skill recommendations
- ✨ Feature: Prompt Injection guard — scanner outputs summaries only, never raw code

### Bug Fixes

- 🐛 Fix: ClawHub serial inspect calls causing timeouts (91 calls × 3s = 273s → parallel with 10s timeout)
- 🐛 Fix: Skills.sh CLI interactive prompt blocking automated search (now sends 'n' to stdin)

### Full Changelog

First public open-source release.
