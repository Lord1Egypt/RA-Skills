## Description:

Fetch real-time OpenRouter usage totals and historical per-model spend for usage, spend, cost breakdown, or OpenRouter stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosseyre](https://clawhub.ai/user/rosseyre)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, operators, and OpenRouter account users use this skill to check current OpenRouter spend, remaining credits, and recent per-model usage from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenRouter API keys may be exposed if stored in a local credentials.env file or shared with source archives.

Mitigation: Prefer environment variables or managed secrets, keep credentials.env out of source control, restrict file permissions, and rotate keys if exposure is suspected.

Risk: Usage totals and per-model breakdowns can differ because activity data covers completed UTC days.

Mitigation: Treat same-day totals as live account data and use the model breakdown after UTC rollover for historical analysis.

## Reference(s):

- [OpenRouter key usage endpoint](https://openrouter.ai/api/v1/auth/key)
- [OpenRouter activity endpoint](https://openrouter.ai/api/v1/activity)
- [OpenRouter credits endpoint](https://openrouter.ai/api/v1/credits)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text digest with optional shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports today, week, and month usage totals, balance information, and up to eight recent model-spend entries when a management key is available.]

## Skill Version(s):

1.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
