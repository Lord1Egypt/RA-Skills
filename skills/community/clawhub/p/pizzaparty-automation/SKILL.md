---
name: pizzaparty-automation
description: Twitch engagement via PizzaParty.gg - 4 daily sessions for LevelUpLove
version: 2.0.0
author: Migration from Agent Zero
---

# PizzaParty.gg Automation Skill

## Overview
Earn PizzaParty points by engaging with spotlighted Twitch streamers. Uses Playwright for dashboard scraping + Twitch IRC for chat.

## Purpose
- Login to PizzaParty.gg via Discord OAuth
- Scrape 'Now Live' spotlighted streamers and ranks
- Chat in Twitch channels via IRC (Twitch browser login blocked)
- Maximize points: Diamond (7/min) → Bronze (3/min)

## Pizza Party Points System
| Rank | Points/Minute |
|------|---------------|
| Diamond | 7 |
| Platinum | 6 |
| Gold | 5 |
| Silver | 4 |
| Bronze | 3 |
**Spotlight Bonus:** 1.25x multiplier

## Input Variables
| Variable | Description | Example |
|----------|-------------|---------|
| PIZZAPARTY_EMAIL | Discord OAuth email | papawespeak@outlook.com |
| PIZZAPARTY_PASSWORD | OAuth password | (configured in env) |
| TWITCH_OAUTH_TOKEN | IRC token (oauth:xxx) | from Twitch dev console |
| TWITCH_USERNAME | IRC username | wespeak |
| TWITCH_CLIENT_ID | App client ID | horyw2un78l... |
| TWITCH_CLIENT_SECRET | App secret | zgxphb18sw... |

## Technical Approach (Hybrid)
1. Playwright browser → PizzaParty dashboard login (Discord OAuth)
2. Scrape 'Now Live' ➔ streamer names + ranks
3. Twitch IRC (port 6697 SSL) ➔ chat messages (NOT browser)
4. Rate limit: 20 msg/30s per channel

## Triggers
Sessions: 09:00, 13:00, 17:00, 21:00 SAST (4 daily)
Duration: 10-15 min per session
Messages: 1-3 per streamer, 10-20 messages per session

## Files
- index.py - Main automation
- schedules/default.json - Session schedule
- .env.example - Configuration

## Notes
- PizzaParty uses Discord OAuth NOT Twitch direct
- Partner Push: 100 msg/48h cap
- Personal account (not bot): papawespeak@outlook.com
