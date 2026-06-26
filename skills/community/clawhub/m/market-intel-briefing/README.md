# market-intel-briefing

Turn scattered public research into sourced, decision-ready market intelligence briefs for client-facing operators.

## What it does

This skill builds concise commercial briefs from market, competitor, company, or theme-specific public information. It separates confirmed facts from unverified claims, translates findings into commercial implications, and gives operators a defensible stance with practical next actions and a client-facing talk track.

## Who it's for

Agency and service operators in the AI/agent ecosystem and B2B SaaS who need to turn research into client-ready output.

## Install

```bash
clawhub install market-intel-briefing
```

## Usage

Trigger the skill by asking for a market intelligence brief, competitor summary, category update, or commercial briefing. Examples:

**Company brief:**
> Build a market intel brief on Anthropic over the last 90 days. Focus on product launches, pricing changes, enterprise partnerships, and developer ecosystem moves.

**Competitive comparison:**
> Create a 30-day competitive brief for three edge AI infrastructure vendors: Company A, Company B, Company C. Focus on launches, pricing, partnerships, and enterprise traction.

**Change detection:**
> What changed in the AI agent tooling category in the last two weeks? Focus on material product, pricing, or partnership changes.

**Infrastructure/jurisdiction comparison:**
> Compare Alberta, Saskatchewan, and BC for data center development. Cover power availability, permitting, water, policy, and speed to execution.

**Sparse-data / emerging category:**
> Summarize what's known about AI-native workflow automation startups. Flag where evidence is thin.

## Output structure

The default brief includes:

1. **Scope and framing** — topic, geography, time window, coverage limits
2. **Key confirmed developments** — sourced, dated, confidence-labeled
3. **Notable unverified or weakly supported claims** — clearly separated from confirmed facts
4. **Commercial implications** — what changed and why it matters to operators
5. **Current justified stance** — the strongest position the evidence supports
6. **Recommended next 3 actions** — practical, proportional to evidence strength
7. **Client-facing talk track** — short, usable, evidence-proportional
8. **Sources** — linked and tiered by quality

## Key principles

- **Evidence discipline**: confirmed facts, reported claims, and inferences are always labeled separately
- **No fake monitoring**: the skill does not pretend to have continuous data feeds
- **Scope control**: overly broad asks get narrowed before synthesis
- **Proportional confidence**: thin evidence produces cautious stances, not empty briefs
- **Operator usefulness**: every brief ends with something the operator can do or say this week

## Reference files

The skill loads supporting references as needed:

| File | Used when |
|------|-----------|
| `source-and-claim-rubric.md` | Source quality or claim strength matters |
| `output-patterns.md` | User needs a variant format |
| `commercial-translation.md` | Moving from research to operator-facing actions |
| `comparison-frames.md` | Side-by-side jurisdiction/competitor comparisons |
| `opportunity-ranking.md` | Scanning for underserved workflows or gaps |

## Version

v0.8 — public-flagship ready. Passed RALPH quality threshold (median >= 40/45, no cases below 34) after 11 evaluation rounds on a 17-case test corpus.

## License

Published by NorthlineAILabs.
