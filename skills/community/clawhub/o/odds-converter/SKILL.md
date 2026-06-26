---
name: odds-converter
description: "Convert between American odds, decimal odds, fractional odds, implied probability, and Kalshi contract prices. Use when asked to convert odds formats, explain what odds mean, or compare odds across platforms."
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: ["python3"]
---

# Odds Converter

Convert between any odds format: American (+150, -200), decimal (2.50), fractional (3/2), implied probability (40%), and Kalshi contract price ($0.40).

## When to Use

Use this skill when the user asks about:
- Converting odds from one format to another
- What specific odds mean (e.g., "what does -150 mean?")
- Comparing odds from different platforms that use different formats
- Implied probability of any odds value
- Kalshi contract price equivalents for sportsbook odds
- Batch converting multiple odds values

## Operations

### 1. American Odds → All Formats

Convert a single American odds value to every other format. Replace ODDS with the value (e.g., -150 or +200):

```bash
python3 -c "
odds = ODDS
if odds < 0:
    impl = abs(odds) / (abs(odds) + 100)
elif odds > 0:
    impl = 100 / (odds + 100)
else:
    impl = 0.5
dec = round(1 / impl, 4) if impl > 0 else 0
from fractions import Fraction
frac = Fraction(1 - impl, impl).limit_denominator(100) if impl > 0 else 'N/A'
kalshi = round(impl, 2)
print(f'American: {odds:+d}')
print(f'Decimal:  {dec}')
print(f'Fractional: {frac}')
print(f'Implied Prob: {impl*100:.2f}%')
print(f'Kalshi Price: \${kalshi}')
"
```

### 2. Decimal Odds → All Formats

Convert decimal odds to every other format. Replace DEC with the value (e.g., 2.50):

```bash
python3 -c "
dec = DEC
impl = 1 / dec if dec > 0 else 0
if impl > 0.5:
    amer = round(-(impl / (1 - impl)) * 100)
elif impl < 0.5:
    amer = round(((1 - impl) / impl) * 100)
else:
    amer = 100
from fractions import Fraction
frac = Fraction(dec - 1).limit_denominator(100) if dec > 1 else '0/1'
kalshi = round(impl, 2)
print(f'Decimal:  {dec}')
print(f'American: {amer:+d}')
print(f'Fractional: {frac}')
print(f'Implied Prob: {impl*100:.2f}%')
print(f'Kalshi Price: \${kalshi}')
"
```

### 3. Fractional Odds → All Formats

Convert fractional odds to every other format. Replace NUM and DEN with numerator and denominator (e.g., 3 and 2 for 3/2):

```bash
python3 -c "
num, den = NUM, DEN
dec = round((num / den) + 1, 4)
impl = den / (num + den)
if impl > 0.5:
    amer = round(-(impl / (1 - impl)) * 100)
elif impl < 0.5:
    amer = round(((1 - impl) / impl) * 100)
else:
    amer = 100
kalshi = round(impl, 2)
print(f'Fractional: {num}/{den}')
print(f'Decimal:  {dec}')
print(f'American: {amer:+d}')
print(f'Implied Prob: {impl*100:.2f}%')
print(f'Kalshi Price: \${kalshi}')
"
```

### 4. Implied Probability → All Formats

Convert an implied probability to every other format. Replace PROB with the probability as a decimal (e.g., 0.40 for 40%):

```bash
python3 -c "
impl = PROB
dec = round(1 / impl, 4) if impl > 0 else 0
if impl > 0.5:
    amer = round(-(impl / (1 - impl)) * 100)
elif impl < 0.5:
    amer = round(((1 - impl) / impl) * 100)
else:
    amer = 100
from fractions import Fraction
frac = Fraction(1 - impl, impl).limit_denominator(100) if impl > 0 else 'N/A'
kalshi = round(impl, 2)
print(f'Implied Prob: {impl*100:.2f}%')
print(f'American: {amer:+d}')
print(f'Decimal:  {dec}')
print(f'Fractional: {frac}')
print(f'Kalshi Price: \${kalshi}')
"
```

### 5. Batch Convert

Convert a list of American odds values to all formats at once. Replace the list with actual values:

```bash
python3 -c "
odds_list = [-150, +200, -110, +300, -400]
print(f'{\"American\":>10} {\"Decimal\":>10} {\"Implied\":>10} {\"Kalshi\":>10} {\"Fractional\":>12}')
print('-' * 56)
for odds in odds_list:
    if odds < 0:
        impl = abs(odds) / (abs(odds) + 100)
    elif odds > 0:
        impl = 100 / (odds + 100)
    else:
        impl = 0.5
    dec = round(1 / impl, 4)
    from fractions import Fraction
    frac = Fraction(1 - impl, impl).limit_denominator(100)
    kalshi = round(impl, 2)
    print(f'{odds:>+10d} {dec:>10.2f} {impl*100:>9.1f}% {\"$\" + str(kalshi):>10} {str(frac):>12}')
"
```

## Output Rules

1. Always show ALL five formats in conversion output
2. American odds must include the +/- sign (e.g., +150, -200)
3. Decimal odds to 2-4 decimal places depending on value
4. Implied probability as a percentage with 1-2 decimal places
5. Kalshi price as a dollar value between $0.01 and $0.99
6. Fractional odds simplified to lowest terms with denominator ≤ 100
7. For batch conversions, use a table format with aligned columns
8. When a user says "what does X mean" — convert to all formats AND explain in plain English (e.g., "-150 means you risk $150 to win $100, implying a 60% chance")

## Error Handling

- If the user provides odds of exactly 0, explain that 0 is not valid in any odds format
- If the user provides implied probability > 1.0 or < 0, ask if they meant a percentage (e.g., 60 → 0.60)
- If the user provides decimal odds ≤ 1.0, explain that decimal odds must be greater than 1.0
- If the user gives a fraction with 0 denominator, explain it's invalid
- If the format is ambiguous (e.g., "150"), ask whether they mean +150 American or 1.50 decimal

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-odds-converter-skill/](https://agentbets.ai/guides/openclaw-odds-converter-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
