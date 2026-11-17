## Description:

Use Plonky.ai to upload, analyze, and forecast recurring time-series data for planning and budgeting, with guidance on data quality and model suitability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addysmoke](https://clawhub.ai/user/addysmoke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and planning teams use this skill to decide whether time-series forecasting is appropriate, prepare suitable datasets, call Plonky.ai forecasting tools, and present forecast results with reliability caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecasting datasets may be uploaded to Plonky.ai.

Mitigation: Avoid uploading confidential, regulated, or customer-identifiable data unless organizational policy permits that use.

Risk: Forecasts and backtests can consume Plonky.ai API credits.

Mitigation: Check available credits before forecasting and avoid unnecessary batch or repeated forecast runs.

Risk: Weak, sparse, monthly, irregular, or event-driven data can produce unreliable forecasts.

Mitigation: Analyze the dataset before forecasting, run a backtest, and present poor-accuracy results as directional estimates only.

## Reference(s):

- [Plonky.ai API Docs](https://plonky.ai/agents)
- [Plonky.ai MCP Server](https://github.com/addysmoke/plonkyai_mcp)
- [ClawHub Skill Page](https://clawhub.ai/addysmoke/skills/plonky-time-series-forecasting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance and forecast summaries with tool calls, metrics, caveats, and relevant Plonky.ai links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecasting workflow may upload user datasets to Plonky.ai and consume API credits.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
