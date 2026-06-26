# 🦞 lobstr

> Score any startup idea in 60 seconds. No API keys. No setup.

## What this skill does

When a user says `/lobstr "idea"`, you run a full startup idea scan:

1. **Competitor search** — finds real competitors via live web search
2. **LOBSTR score** — scores the idea across 6 dimensions (0–100 each)
3. **GRID investor signal** — checks how many EU VCs are active in this space

You get back a formatted score card to show the user. By default, output is **private** — nothing is published anywhere.

## When to use this

Use lobstr whenever a user:
- Asks you to evaluate, validate, or score a startup idea
- Wants to know if a business concept is worth pursuing
- Needs a competitive landscape analysis for a new product
- Asks "should I build this?"

## How to run

```bash
# Default: private score card
python3 scripts/lobstr.py "the startup idea goes here"

# Publish to runlobstr.com and get a share URL
python3 scripts/lobstr.py "the idea" --public

# Also post to m/lobstrscore on Moltbook
python3 scripts/lobstr.py "the idea" --public --moltbook

# Raw JSON output (for agent-to-agent piping)
python3 scripts/lobstr.py "the idea" --json
```

No API keys are needed — the skill calls the hosted scoring API at runlobstr.com automatically.

### Flags

| Flag | Effect |
|------|--------|
| (none) | Private output — score card to stdout only |
| `--public` | Publish to runlobstr.com and show share URL |
| `--moltbook` | Post to m/lobstrscore on Moltbook |
| `--json` | Output raw JSON instead of formatted card |

## What comes back

```
🦞 LOBSTR SCAN
"AI-powered legal contracts for SMEs"

LOBSTR SCORE  45/100  [====------]

L  Landscape   🔴  15/100  Saturated with well-funded players.
O  Opportunity 🟢  75/100  Large market, every SME needs contracts.
B  Biz model   🟡  60/100  SaaS model is solid, defensibility questionable.
S  Sharpness   🔴  20/100  Undifferentiated. AI is table stakes.
T  Timing      🟢  85/100  Perfect timing. Legal tech is hot.
R  Reach       🟢  70/100  Good reach via online channels.

VERDICT
Tough market, undifferentiated product. Needs a radical rethink.

🚫 NOT YET.
```

## LOBSTR dimensions

| | Dimension | What it measures |
|---|---|---|
| **L** | Landscape | How crowded is the competitive space? |
| **O** | Opportunity | Is there a real, large market? |
| **B** | Business model | Is monetization clear and defensible? |
| **S** | Sharpness | How differentiated vs alternatives? |
| **T** | Timing | Is the market timing right? |
| **R** | Reach | How easily can this scale? |

Score ranges: 🟢 ≥ 70, 🟡 50–69, 🔴 < 50. Overall score is weighted (S and B count more).

## API keys (optional — for power users only)

The default mode uses the free hosted API (5 scans/day, no keys needed).

For **unlimited scans**, the user can set both:
```bash
export ANTHROPIC_API_KEY=<key>
export EXA_API_KEY=<key>
```

This activates BYOK mode — the skill runs the full pipeline locally instead of calling runlobstr.com.

## Install

ClawHub: https://clawhub.ai/rednix/lobstr

## Links

- [runlobstr.com](https://runlobstr.com) — score cards and scan archive
- [GRID](https://grid.nma.vc) — EU investor database
- [NMA](https://nma.vc) — built by NMA

## License

MIT
