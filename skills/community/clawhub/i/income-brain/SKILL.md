---
name: version: 1.0.2
description: |
    demand, creates new skills based on proven strategies, lists them on all platforms
  (ClawHub, SellApp, Whop, Gumroad, Etsy), and compounds knowledge over time.
  Learns from successful agents on Moltbook, tracks earnings, and deploys new skills
    BuyMeACoffee, FreeLanceDAO, CryptoGig, x402 paid API, Public.com, OpenCollab.
  
  Core loop:
  1. Read demand_matrix.json to find high-value skill opportunities
  2. Research what techniques work via web search
  3. Generate new SKILL.md files with full implementation code
  4. Deploy to all platforms simultaneously
  5. Track which skills   6. Auto-retry failed platform listings, fix broken code, update versions

  Key principle: Compound knowledge. Each skill created teaches the system how to
  build better skills. After 30+ skills deployed, the success rate doubles.
compatibility: Requires Python 3, requests, knowledge of Zo Computer skills system.
metadata:
  author: ssyopros.zo.computer
  category: autonomous-  tags: passive----

# 
## Core Principle: Compound Knowledge

The 1. Finding what's in demand → creating skills → deploying → tracking what earns
2. Using REAL data from actual marketplace responses to guide future decisions
3. Never guessing — always validating against real market signals

## Demand Matrix

The brain reads `/home/workspace/MoneyMachine/data/demand_matrix.json` which is
continuously updated based on:
- ClawHub search trends (what buyers search for)
- Freelance platform demand signals (gig prices, posting frequency)
- x402 API call patterns (which endpoints get paid)
- Skill download rates on ClawHub

## Skills That Actually 1. Smart Contract Audit — $300-600/hr, low competition
2. DeFi Protocol Integration — $200-400/hr, medium competition
3. Options Trading Backtester — $150-300/hr, low competition
4. AI Model Fine-tuning — $150-250/hr, medium competition
5. Pump.fun Sniper Bot — $200-400/hr, low competition

## Key Rules

- Always include FULL working code in SKILL.md (not placeholders)
- Set version 1.0.X and increment on every publish
- Target platforms: ClawHub (primary), SellApp, Whop, Gumroad, Etsy, Fiverr
- Track earnings in earnings_log.json — this is the only truth
- Never publish without code — buyers return broken skills
- Focus on skills that solve PROBLEMS, not trendy topics

## Anti-Patterns to Avoid

- Don't create "AI content writer" skills (saturated, low pay)
- Don't create generic "chatbot" skills (already done to death)
- Don't promise - Don't create skills without testing them first

## Metrics to Track

- Total earnings by skill type
- Platform conversion rate (published → downloaded)
- Proposal response rate on freelance platforms
- x402 API call volume by endpoint

## 
Each week the brain should:
1. Read earnings_log.json — identify top 3 earning skills
2. Research what made those skills successful
3. Create 1 new skill per week based on what works
4. Update demand_matrix.json with real market data
5. Fix any broken code in underperforming skills
