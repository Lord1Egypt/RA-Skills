---
name: kelly-sizer
description: "Calculate optimal bet sizes using Kelly Criterion. Supports single bets, fractional Kelly (quarter/half/three-quarter), multi-bet portfolio sizing, and max-bet enforcement. Use when asked about bet sizing, how much to bet, position sizing, Kelly Criterion, or bankroll allocation."
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: ["python3"]
---

# Kelly Criterion Bet Sizer

Calculate mathematically optimal bet sizes based on your edge and bankroll.

## When to Use

Use this skill when the user asks about:
- How much to bet on a specific wager
- Kelly Criterion or optimal bet sizing
- Position sizing for a bet with known edge
- Fractional Kelly or conservative bet sizing
- Sizing multiple simultaneous bets
- Maximum bet limits or bankroll allocation

## Odds Conversion Reference

Before computing Kelly, convert all odds to decimal probability format:

| Format | Example | To Decimal Odds | To Implied Prob |
|--------|---------|-----------------|-----------------|
| American (+) | +150 | 1 + odds/100 = 2.50 | 100/(odds+100) |
| American (-) | -200 | 1 + 100/|odds| = 1.50 | |odds|/(|odds|+100) |
| Decimal | 2.50 | Already decimal | 1/decimal |
| Probability | 40% | 1/prob | Already prob |

## Operations

### 1. Single Bet — Full Kelly

Calculate the optimal Kelly stake for a single bet. User must provide: bankroll, odds (any format), and their estimated true probability.

```bash
python3 -c "
import sys
bankroll = float(sys.argv[1])
odds_input = sys.argv[2]
true_prob = float(sys.argv[3])

# Convert odds to decimal
if odds_input.startswith('+'):
    decimal_odds = 1 + int(odds_input[1:]) / 100
elif odds_input.startswith('-'):
    decimal_odds = 1 + 100 / abs(int(odds_input[1:]))
else:
    decimal_odds = float(odds_input)

b = decimal_odds - 1  # net odds
p = true_prob
q = 1 - p

# Kelly fraction
kelly_f = (b * p - q) / b if b > 0 else 0
kelly_f = max(kelly_f, 0)  # never negative

implied_prob = 1 / decimal_odds
edge = true_prob - implied_prob

print(f'Odds: {odds_input} (decimal: {decimal_odds:.4f})')
print(f'Implied prob: {implied_prob:.2%} | Your estimate: {true_prob:.2%} | Edge: {edge:.2%}')
print(f'Kelly fraction: {kelly_f:.4f} ({kelly_f:.2%} of bankroll)')
print(f'Recommended stake: \${kelly_f * bankroll:.2f} of \${bankroll:.2f} bankroll')
if kelly_f <= 0:
    print('⚠️  No edge detected — Kelly says do not bet')
elif kelly_f > 0.10:
    print('⚠️  Kelly > 10% — consider fractional Kelly to reduce variance')
" BANKROLL ODDS TRUE_PROB

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-kelly-sizer-skill/](https://agentbets.ai/guides/openclaw-kelly-sizer-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
