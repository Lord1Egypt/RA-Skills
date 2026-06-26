---
name: icp-modeler
description: Generate research-backed Ideal Customer Profiles (ICPs) for mortgage and real estate products. Returns full buyer personas, Meta/Google ad targeting parameters, trigger phrases, content tone, and platform routing — no generic demographics, only actionable targeting intelligence.
version: 1.0.2
author: drivenautoplex1
price: 0
tags:
  - marketing
  - real-estate
  - mortgage
  - crypto
  - audience-targeting
  - customer-research
  - ad-targeting
  - meta-ads
  - google-ads
  - content-strategy
  - sales
  - lead-generation
  - personas
  - direct-response
metadata:
  openclaw:
    requires:
      env:
        - ANTHROPIC_API_KEY
      anyBins:
        - python3
    primaryEnv: ANTHROPIC_API_KEY
    emoji: "🎯"
    homepage: https://github.com/drivenautoplex1/openclaw-skills
    install:
      - kind: uv
        package: anthropic
        bins: []
---

# ICP Modeler Skill

Know exactly who you're talking to before you write a single word of copy. The ICP Modeler generates battle-tested buyer profiles for mortgage and real estate products — with specific ad targeting parameters, trigger phrases, pain points, and platform routing built in.

## Free vs Premium

**Free tier (no API key needed):**
- `--demo` — full crypto-mortgage ICP profile, zero API calls, shows complete output format
- `--list` — see all 5 available ICPs
- `--product <name>` — display any pre-built ICP profile (works offline)
- `--output json` — export any ICP as structured JSON for your own workflows

**Premium tier (ANTHROPIC_API_KEY):**
- `--generate-content "3 facebook posts"` — LLM writes content specifically tuned to the ICP's triggers, tone, and platform presence
- `--generate-content "30s video script"` — ICP-targeted video script
- `--generate-content "email subject lines"` — subject lines optimized for this buyer's psychology
- Unlimited content generation via Claude Haiku (~$0.001 per call)

The pre-built profiles alone are worth installing — most "targeting" is just age/income. This gives you psychology.

## What this skill does

For each product, generates a complete buyer intelligence package:

1. **Full buyer persona** — age, income, location, occupation, pain points, dream outcome
2. **Trigger phrases** — exact words and phrases this buyer types into Google and says out loud
3. **Content tone guide** — how to speak to this buyer without triggering skepticism
4. **Platform routing** — where this ICP actually hangs out (X, Reddit, LinkedIn, Facebook groups)
5. **Meta ad targeting** — ages, interests, placements, custom audience strategy
6. **Google Ads targeting** — keywords, match types, negative keywords, audience layers

## Available ICPs

| Product | Headline |
|---------|----------|
| `crypto-mortgage` | The Crypto Holder Who Won't Sell |
| `credit-repair` | The Almost-Ready Buyer |
| `va-loan` | The Veteran Who Doesn't Know What They Have |
| `realtor-partner` | The Agent Who Needs a Lender They Can Trust |
| `first-time-buyer` | The Overwhelmed First-Timer |

Aliases work: `crypto`, `va`, `credit`, `realtor`, `first-time`

## Usage

```bash
# See the crypto-mortgage ICP with zero setup
python3 icp_modeler.py --demo

# List all available ICPs
python3 icp_modeler.py --list

# Pull a full ICP profile
python3 icp_modeler.py --product "crypto mortgage"
python3 icp_modeler.py --product va-loan
python3 icp_modeler.py --product first-time-buyer

# Export as JSON (pipe into other tools)
python3 icp_modeler.py --product credit-repair --output json

# Generate ICP-tuned content (requires ANTHROPIC_API_KEY)
python3 icp_modeler.py --product crypto --generate-content "3 facebook posts"
python3 icp_modeler.py --product va-loan --generate-content "30s video script"
python3 icp_modeler.py --product first-time --generate-content "email subject lines"

# Version
python3 icp_modeler.py --version
```

## Example output (crypto-mortgage ICP)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICP: Crypto-Backed Mortgage (Fannie Mae / Coinbase / Better)
     "The Crypto Holder Who Won't Sell"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEMOGRAPHICS
  age                  30-48
  income               $120K-$400K household
  location             Target metro, key submarkets and growth corridors
  occupation           Software engineer, finance, entrepreneur, executive

PAIN POINTS
  • Doesn't want to sell crypto and trigger $50K-$500K capital gains tax event
  • Doesn't qualify for traditional mortgage because crypto income isn't W2
  • Feels stuck — 'I have the wealth but can't access it for real estate'

TRIGGER PHRASES
  "don't sell your crypto to buy a house"
  "pledge crypto as collateral"
  "no capital gains event"
  "Fannie Mae crypto"

META AD TARGETING
  Ages:      28-50
  Interests: Cryptocurrency, Bitcoin, Ethereum, XRP, DeFi
  Placement: Facebook Feed, Instagram Feed, Instagram Stories
  Income:    Top 25%
```

## Connecting to other skills

Pipe ICP JSON into the content scorer and content calendar:

```bash
# Generate ICP → score the content it suggests → build a calendar
python3 icp_modeler.py --product crypto --output json > icp.json
python3 icp_modeler.py --product crypto --generate-content "5 linkedin posts" | \
  python3 ../content-scorer/score_content.py --stdin
```

## Multi-vertical use

The ICP framework applies to:
- Any **mortgage** vertical (FHA, VA, USDA, jumbo, crypto-backed, HELOC)
- **Real estate agents** targeting specific buyer profiles
- **Credit repair** services targeting pre-approval candidates
- **Financial services** with segmented buyer journeys
- **Coaching/consulting** with defined client personas

Extend by adding your own ICP dict to the `ICPS` dictionary in `icp_modeler.py`.
