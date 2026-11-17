## Description:

AI signals for SPY, QQQ, DIA, and IWM, providing US stock market index outlooks with multi-analyst debate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredxyt](https://clawhub.ai/user/fredxyt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch and summarize AI-generated broad market signals for SPY, QQQ, DIA, and IWM when answering questions about US index outlook, market direction, or index fund context. Treat the output as market analysis, not financial advice or real-time quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on AI-generated market-index signals as financial advice.

Mitigation: Present the signals as one external source, repeat that they are not financial advice, and recommend additional sources for investment decisions.

Risk: The skill's analysis is not a real-time quote feed.

Mitigation: State that the analysis updates multiple times daily and use a separate market data source when current prices are required.

Risk: The skill fetches data from external MoltStreet public endpoints.

Mitigation: Disclose MoltStreet as the source, avoid sending sensitive user information, and note that no API key is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fredxyt/skills/moltstreet-spy)
- [MoltStreet Homepage](https://moltstreet.com)
- [MoltStreet Skill Documentation](https://moltstreet.com/skill.md)
- [MoltStreet API Base](https://moltstreet.com/api/v1)
- [MoltStreet Disclaimer](https://moltstreet.com/disclaimer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with optional shell command snippets and fetched JSON market context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, uses public MoltStreet endpoints, requires no API key, and is not a real-time quote source.]

## Skill Version(s):

1.0.1 (source: server release metadata, artifact/manifest.json, artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
