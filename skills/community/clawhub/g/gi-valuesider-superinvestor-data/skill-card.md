## Description:

Fetches Superinvestors' 13F portfolio holdings and buy/sell activity from ValueSider for portfolio, holdings, and trading-activity questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laimiaohua](https://clawhub.ai/user/laimiaohua)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to fetch and parse public ValueSider 13F portfolio holdings and recent buy/sell activity for named superinvestors, managers, or funds. Results should be presented as sourced portfolio data, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live use can make outbound requests to valuesider.com and may fetch third-party financial data for an ambiguous finance request.

Mitigation: Confirm the requested manager, fund, or guru before live fetching when the request is ambiguous, and label results as ValueSider 13F portfolio data rather than financial advice.

Risk: Dependency versions are specified as minimums, which can reduce reproducibility across installs.

Mitigation: Install in a least-privileged Python environment and use pinned dependencies or a lockfile when reproducible execution matters.

## Reference(s):

- [ValueSider](https://valuesider.com)
- [ValueSider Value Investors](https://valuesider.com/value-investors)
- [ValueSider Guru Portfolio URL Template](https://valuesider.com/guru/{guru_slug}/portfolio)
- [ValueSider Guru Activity URL Template](https://valuesider.com/guru/{guru_slug}/portfolio-activity)
- [ClawHub Skill Page](https://clawhub.ai/laimiaohua/skills/gi-valuesider-superinvestor-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional JSON produced by parser scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include portfolio summaries, holdings, activity rows, source URLs, and command snippets for fetching or parsing.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
