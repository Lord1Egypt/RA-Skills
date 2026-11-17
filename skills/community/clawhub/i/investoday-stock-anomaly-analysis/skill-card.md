## Description:

Analyzes abnormal A-share stock movements by combining price action, market index context, sector movement, company events, announcements, news, and research sentiment into a structured explanation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenneth-bro](https://clawhub.ai/user/kenneth-bro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to explain why an A-share stock moved up, down, or sharply intraday, separating market-wide, sector, and company-specific drivers. The output is analytical context only and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock movement explanations may be mistaken for investment advice.

Mitigation: State that outputs are analytical only, avoid buy or sell recommendations, and require evidence-backed attribution.

Risk: Casual Chinese market questions may trigger the skill because of broad anomaly-analysis trigger phrases.

Mitigation: Confirm that the user wants an abnormal-movement explanation for a specific stock before presenting a full report.

Risk: Public market data, news, announcements, or research sentiment may be incomplete or stale.

Mitigation: Show the relevant time windows, cite available evidence categories, and report unavailable data as insufficient instead of inferring missing causes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenneth-bro/skills/investoday-stock-anomaly-analysis)
- [Publisher profile](https://clawhub.ai/user/kenneth-bro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public A-share market data, news, announcements, and research sentiment through the investoday-finance-data dependency.]

## Skill Version(s):

1.4.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
