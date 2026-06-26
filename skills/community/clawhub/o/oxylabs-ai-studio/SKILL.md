---
name: oxylabs-ai-studio
description: >
  Web scraping, crawling, searching, and browser automation using Oxylabs AI Studio.
  Use this skill when the user asks to scrape a website, extract content from a URL,
  search the web, crawl a domain, map a site pages, or automate browser navigation.
  Smart install: automatically stops if native Oxylabs plugin is detected to avoid any conflict.
  Triggers: scrape, extract, crawl, browser agent, map site, fetch page content.
homepage: https://github.com/DrFIRASS/oxylabs-ai-studio-skill
metadata:
  clawdbot:
    emoji: "🕷️"
    requires:
      env: ["OXYLABS_API_KEY"]
      primaryEnv: "OXYLABS_API_KEY"
      bins: ["python3", "pip3"]
    files: ["scripts/*", "setup.sh"]
    install:
      - run: "bash setup.sh"
        label: "Smart install — detects native Oxylabs and adds only missing tools"
---

# Oxylabs AI Studio Skill

Adds Browser Agent, AI-Crawler, and AI-Map to your OpenClaw agent.
Works alongside the native Oxylabs plugin without any conflict.

## Smart Installation

If native plugin detected (oxylabs-ai-studio-openclaw):
- Skips Web Fetch and Web Search — already covered natively
- Adds only the 3 missing tools: Browser Agent, AI-Crawler, AI-Map

If no native plugin:
- Installs all 5 tools: AI-Scraper, Browser Agent, AI-Crawler, AI-Search, AI-Map

## Note for Hostinger + OpenClaw users

If you enabled Oxylabs in Hostinger and see PLUGIN:OXYLABS-AI-STUDIO-OPENCLAW
in your agent tools, you already have Web Fetch and Web Search covered.
This skill adds the 3 missing tools: Browser Agent, AI-Crawler, AI-Map.

## Setup

Run: bash setup.sh
Or manually: pip3 install oxylabs-ai-studio --break-system-packages
Set: export OXYLABS_API_KEY=your_key_here
Get 1000 free credits at: https://aistudio.oxylabs.io

## Tools and Priority Rules

When native Oxylabs plugin IS present:
- Scraping a URL      -> use native oxylabs_web_fetch
- Searching the web   -> use native oxylabs_web_search
- Browser navigation  -> always use scripts/browser.py
- Crawling a domain   -> always use scripts/crawler.py
- Mapping a site      -> always use scripts/map.py

When native Oxylabs plugin is NOT present:
- Scraping a URL      -> use scripts/scrape.py
- Searching the web   -> use scripts/search.py
- Browser navigation  -> use scripts/browser.py
- Crawling a domain   -> use scripts/crawler.py
- Mapping a site      -> use scripts/map.py

## Examples

python3 scripts/browser.py https://example.com "find all product prices"
python3 scripts/crawler.py https://example.com "all blog posts"
python3 scripts/map.py https://example.com "all pages"
