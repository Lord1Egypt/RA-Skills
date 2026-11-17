## Description:

Research Pendle PT markets for hold-to-par ideas, near-expiry rotations, and looped PT strategies across money markets such as Morpho and Euler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moshu](https://clawhub.ai/user/moshu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and DeFi researchers use this skill to evaluate Pendle principal token markets, compare natural PT yield against practical loopability, and produce decision-oriented research before considering capital deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled PT rankings and market snapshots can become stale or misleading.

Mitigation: Rerun the live scanners and independently verify market liquidity, borrow depth, and route status before relying on recommendations.

Risk: Leveraged PT loop analysis may be mistaken for transaction-ready financial advice.

Mitigation: Use outputs as advisory research only, keep conservative LTV buffers, and review protocol and underlying-asset risk before any wallet transaction.

Risk: Manual Contango route information may not represent currently verified app support.

Mitigation: Label manual routes clearly and verify exact PT and quote-asset support in Contango before using them.

## Reference(s):

- [Pendle PT Ranking Framework](references/ranking-framework.md)
- [Manual Contango PT Comparison Framework](references/manual-contango-comparison.md)
- [Pendle Markets](https://app.pendle.finance/trade/markets)
- [Pendle Pencosystem](https://pendle.finance/pencosystem)
- [ClawHub Skill Page](https://clawhub.ai/moshu/skills/pendle-pt-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or Discord-style bullet guidance, with optional local JSON snapshots and Markdown research briefs from bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory DeFi research and should be refreshed with live scans and independently verified before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
