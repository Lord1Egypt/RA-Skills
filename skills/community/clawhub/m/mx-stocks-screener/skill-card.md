## Description:

Natural language screener for investment assets across global markets, including A-shares, ETFs, bonds, HK and US stocks, and funds, with CSV and text-description outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment analysts use this skill to screen A-share, Hong Kong, U.S. equity, ETF, fund, convertible-bond, and sector data with natural-language criteria for asset discovery, cross-market monitoring, portfolio construction, and strategy review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports may preserve untrusted spreadsheet formulas from remote financial data.

Mitigation: Open generated CSV files with formula execution disabled or inspect them before using them in spreadsheet software or sharing them.

Risk: The skill depends on an external Eastmoney API service and requires an EM_API_KEY credential.

Mitigation: Install only if the service is trusted, keep the API key out of code and logs, and confirm the key can be reset or revoked.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/mx-stocks-screener)
- [Financial AI Analyst publisher profile](https://clawhub.ai/user/financial-ai-analyst)
- [Eastmoney Miaoxiang API key service](https://ai.eastmoney.com/mxClaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell and Python examples; generated CSV and text description files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and writes query results to a configurable local output directory.]

## Skill Version(s):

1.0.15 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
