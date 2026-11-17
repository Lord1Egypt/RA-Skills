## Description:

持仓诊断 is a Prana-hosted portfolio diagnosis skill for A-share investors that analyzes submitted holdings and returns a report with quantitative risk metrics, charts, warnings, and optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luokeer52](https://clawhub.ai/user/luokeer52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to submit A-share portfolio holdings for remote diagnosis of position balance, volatility, beta, Sharpe ratio, maximum drawdown, risk warnings, and optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio details entered into the skill are sent to an off-host Prana service.

Mitigation: Submit only data appropriate for remote processing and confirm the configured Prana endpoint and data-handling expectations before use.

Risk: API credentials can be stored locally in config/api_key.txt.

Mitigation: Prefer environment variables or PRANA_SKILL_SKIP_WRITE_API_KEY=1, and do not commit local credential files to public repositories.

Risk: Supplying an untrusted base URL could forward prompts and credentials to the wrong service.

Mitigation: Use only trusted HTTPS Prana endpoints and avoid overriding --base-url unless the endpoint is verified.

Risk: Portfolio diagnosis and optimization suggestions may be inaccurate or misleading if used as financial advice.

Mitigation: Treat outputs as informational analysis and review decisions with appropriate financial judgment before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luokeer52/skills/portfolio-diagnosis)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or text portfolio diagnosis report returned by the remote Prana workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quantitative risk metrics, charts, warnings, and optimization suggestions derived from submitted holdings.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
