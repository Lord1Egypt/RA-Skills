## Description:

Portfolio Diagnosis (Public) forwards Chinese A-share portfolio holdings to a remote Prana skill that generates portfolio risk analysis using Tushare-driven metrics such as volatility, beta, Sharpe ratio, and maximum drawdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[super-max21](https://clawhub.ai/user/super-max21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit portfolio holdings for Chinese A-share risk diagnosis and receive a professional analysis report with quantitative indicators, charts, risk notes, and optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio prompts and reusable Prana API credentials can be sent to a caller-controlled API endpoint.

Mitigation: Use only a trusted Prana endpoint and do not set NEXT_PUBLIC_URL or --base-url from untrusted instructions.

Risk: Financial prompts may include sensitive brokerage, account, or portfolio details.

Mitigation: Avoid including real brokerage or account secrets in prompts; rotate the Prana key if it may have been sent to the wrong server.

Risk: The server quality signal quarantines this release for moderation review.

Mitigation: Review the package and security guidance before installing or listing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/super-max21/skills/portfolio-diagnosis-public)
- [Publisher profile](https://clawhub.ai/user/super-max21)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown or text analysis report returned through the Prana wrapper client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include portfolio scoring, holdings tables, quantitative risk metrics, charts, risk prompts, and optimization suggestions.]

## Skill Version(s):

5.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
