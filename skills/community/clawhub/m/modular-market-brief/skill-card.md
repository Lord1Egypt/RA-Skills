## Description:

Generate modular, data-backed market reports (AM/PM) across global assets for daily market briefs, premarket/aftermarket summaries, cross-asset dashboards, sector/asset trend tables, top movers blocks, and a single best-idea wrap-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boilerrat](https://clawhub.ai/user/boilerrat)

### License/Terms of Use:


## Use Case:

External users and finance-focused agents use this skill to assemble concise AM/PM market briefs across equities, rates, FX, commodities, crypto, movers, trend patterns, and one best-idea summary. It is intended for informational market analysis rather than trade execution or personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data, mover lists, and BUY/SELL/WAIT labels may be stale, incomplete, rate-limited, or misread as trading advice.

Mitigation: Treat generated briefs as informational, label trend outputs as simple patterns, review source data before acting, and include risks or invalidation for any best-idea summary.

Risk: Optional helper scripts depend on public finance endpoints and Python packages whose behavior or availability may change.

Mitigation: Review and pin Python dependencies for production use, run scripts in a controlled environment, and replace movers providers when an endpoint changes or fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boilerrat/skills/modular-market-brief)
- [Yahoo Finance screener endpoint](https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved)
- [TMX Canadian markets](https://money.tmx.com/en/canadian-markets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown market brief with optional JSON or markdown tables from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should present trend labels as patterns, include rationale and invalidation where applicable, and avoid certainty language.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
