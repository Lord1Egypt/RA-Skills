## Description:

Matic Trades API - AI toolbox (AI_PICK), Twelve Data (SMART_SEARCH), autonomous charting for stocks, crypto, indicators, charts, news, and sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ortmind](https://clawhub.ai/user/ortmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route natural-language market research, financial data, and chart-analysis requests to the Matic Trades API, then summarize returned JSON and image links for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance prompts and any included market context are sent to the external Matic Trades service.

Mitigation: Use the skill only when that data sharing is acceptable, avoid secrets or sensitive trading information in prompts, and keep MATIC_API_KEY private.

Risk: Overriding MATIC_TRADES_API_BASE can redirect prompts and bearer-token authenticated requests to another endpoint.

Mitigation: Use the default HTTPS API base unless you control and trust the alternate endpoint.

## Reference(s):

- [Matic Trades API skill reference](references/api.md)
- [Matic Trades product site](https://matictrades.com)
- [Matic Trades API base](https://api.matictrades.com/api/v1)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw creating skills documentation](https://docs.openclaw.ai/tools/creating-skills)
- [ClawHub skill page](https://clawhub.ai/ortmind/skills/matic-trades)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with shell commands, JSON-derived results, and optional image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MATIC_API_KEY or MATIC_TRADES_API_KEY; MATIC_TRADES_API_BASE can override the default HTTPS API base.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
