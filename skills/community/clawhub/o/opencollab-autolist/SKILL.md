---
name: opencollab-autolister
version: 1.0.18
description: |
    a crypto-native freelancing marketplace where clients pay in USDC. The agent
  creates a compelling profile, posts skills, bids on matched jobs, and pings
  new gigs daily — all   from the MoneyMachine demand matrix.
compatibility: Requires Python, requests, Zo Computer
metadata:
  author: ssyopros.zo.computer
  category:   tags: opencollab, freelance, crypto, usdc, 
# opencollab-autolister


## What This Does

1. Registers account if needed (or uses existing credentials)
2. Creates a compelling profile headline and bio
3. Posts skills from the MoneyMachine demand matrix (sorted by demand_score)
4. Bids on matched jobs 
## OpenCollab Profile Setup

Profile fields to populate:
- **Headline**: Something punchy that communicates what you deliver
  e.g. "Options Trading Bot Dev | DeFi Sniper Bots | Smart Contract Auditor"
- **Bio**: Masters-level technical background, specific deliverables
- **Skills tags**: Use exact keywords from demand matrix
- **Rate**: Start at $50-150/hr, scale up as you get reviews

## Skills to List (Priority Order)

From demand_matrix.json:
1. Smart Contract Audit ($500+/audit)
2. DeFi Protocol Integration ($350+/project)
3. Pump.fun Sniper Bot ($400+/bot)
4. Options Trading Backtester ($250+/project)
5. AI Model Fine-Tuning ($300+/project)

## How It Works

The agent (you/Zo) will:
1. Check OpenCollab for job matches daily
2. Score each job by: budget × skill_match × client_reputation
3. Submit proposals only for jobs where score > threshold
4. Track win rate and adjust pricing

## Files

- `scripts/autolister.py` — Main script
- `scripts/profiler.py` — Creates compelling profile
- `scripts/job_scorer.py` — Scores and ranks jobs

## API Notes

OpenCollab uses a REST API for:
- GET /jobs — list available jobs
- POST /proposals — submit proposal
- GET /profile — get current profile

(Use web search to find current API endpoints and authentication method)

## Deliverable

The autolister outputs:
- Profile URL
- Active skill listings count
- Daily new jobs found
- Proposals submitted
- Win rate tracking
