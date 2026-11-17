## Description:

Monitor stock and crypto holdings, get price alerts, and track portfolio performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manually track stock, ETF, and crypto holdings, check delayed price snapshots, set price alerts, and review approximate portfolio performance without connecting a brokerage account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate during ordinary stock or crypto price lookups because its triggers are broad.

Mitigation: Use it only when portfolio context is intended, and state when a query should not use remembered holdings or alerts.

Risk: Delayed or approximate portfolio figures could be mistaken for exact trading or tax data.

Mitigation: Label portfolio calculations as approximate, disclose data freshness limits, and verify trading or tax-relevant figures with a brokerage or authoritative records.

Risk: Portfolio holdings and performance are sensitive financial data that could be exposed in shared contexts.

Mitigation: Avoid displaying holdings, values, positions, or performance in public channels or shared workspaces without explicit user confirmation.

Risk: Destructive portfolio actions could remove holdings or alerts unintentionally.

Mitigation: Require fresh explicit confirmation before removals, resets, bulk deletions, or clearing alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/portfolio-watcher-hardened)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)
- [Faberlens safety evaluation](https://faberlens.ai/explore/portfolio-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with concise portfolio summaries, price alert instructions, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portfolio figures should be labeled approximate and delayed; destructive portfolio changes require fresh explicit confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
