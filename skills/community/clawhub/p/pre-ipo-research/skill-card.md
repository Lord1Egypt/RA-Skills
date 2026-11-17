## Description:

Query Jarsy, Hyperliquid, PreStocks, Polymarket and Hiive snapshots through Pre-IPO Observer; screen companies, examine opportunity signals and prediction topics, and read published company research with dated Contrary/Sacra sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackstoic](https://clawhub.ai/user/hackstoic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research pre-IPO companies across five public snapshot sources, inspect freshness and source links, and summarize dated published reports. It is suited for screening and research context, not trading, account operation, or investment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Natural-language answers include a Jarsy referral link, which can affect neutrality and user trust.

Mitigation: Review responses for promotional framing and use --json when a neutral machine-consumable output is needed.

Risk: Pre-IPO market data and report content may be stale snapshots, third-party estimates, or platform-specific metrics.

Mitigation: Preserve timestamps, cutoff dates, units, status flags, and source labels; present findings as research context rather than investment advice.

Risk: Published report text and external links are evidence, not fresh verification of current company facts.

Mitigation: Label report cutoff/version and verify current operating or financing facts against primary sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hackstoic/skills/pre-ipo-research)
- [Pre-IPO Observer](https://preipo.polyos.ai)
- [API and command guide](artifact/references/api.md)
- [Reading published company research](artifact/references/reports.md)
- [Jarsy guide](artifact/references/jarsy.md)
- [Hyperliquid contracts guide](artifact/references/hyperliquid.md)
- [PreStocks guide](artifact/references/prestocks.md)
- [Polymarket guide](artifact/references/polymarket.md)
- [Hiive50 manual snapshot guide](artifact/references/hiive.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Natural-language research summaries with optional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Natural-language answers include source timing, units, and a Jarsy referral line; --json returns machine-consumable JSON without added narrative.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
