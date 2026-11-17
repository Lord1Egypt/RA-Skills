## Description:

Financial data research via the PlusE API for stock fundamentals, options analysis, market sentiment, institutional activity, financial statements, macroeconomic data, market news, and ML price predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghsinche](https://clawhub.ai/user/wanghsinche)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to collect and synthesize PlusE financial data for ticker research, options research, market sentiment checks, macroeconomic context, earnings preparation, and structured market reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented MCP URL can place PLUSEFIN_API_KEY in the URL, which may expose the secret through logs, history, or shared configuration.

Mitigation: Use bearer-header authentication or protected secret configuration, and rotate any key that has already been used in a URL.

Risk: Implicit invocation can allow the agent to call PlusE automatically for finance-related prompts.

Mitigation: Disable implicit invocation unless automatic calls to PlusE are intended for the deployment.

Risk: Financial research outputs may influence trading or investment decisions.

Mitigation: Review outputs against trusted sources and treat generated reports as research support rather than investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanghsinche/skills/plusefin-analysis)
- [PlusE Skill Homepage](https://github.com/plusefin/plusefin-skill)
- [PlusE API Console](https://console.plusefin.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands and API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PLUSEFIN_API_KEY for API-backed financial data; outputs depend on the PlusE service response and the user's requested symbols, series, or market topic.]

## Skill Version(s):

2.0.0 (source: server release metadata, user changelog, artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
