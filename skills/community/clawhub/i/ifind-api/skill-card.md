## Description:

China iFinD Skill(同花顺Skill) helps agents query THS iFinD financial data for A-shares, funds, bonds, futures, indices, macroeconomic indicators, fund valuation, announcements, and related market data through documented iFinD API endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinabs](https://clawhub.ai/user/sinabs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and financial analysts use this skill to let an agent fetch Chinese market, fundamentals, macroeconomic, fund, announcement, and portfolio-related data from THS iFinD. It is suited to data lookup and workflow assistance where the user already has a valid iFinD refresh token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on IFIND_REFRESH_TOKEN, and the security evidence warns that sharing or storing a long-lived token unsafely can expose account access.

Mitigation: Use a secure secret-management path for IFIND_REFRESH_TOKEN, avoid pasting tokens into chat, and restrict file permissions if local storage is unavoidable.

Risk: The skill exposes portfolio_manage actions that may alter portfolio data.

Mitigation: Do not allow portfolio_manage mutation actions unless the user explicitly intends to let the agent alter portfolio data.

## Reference(s):

- [API_REFERENCE.md](references/API_REFERENCE.md)
- [ClawHub skill page](https://clawhub.ai/sinabs/skills/ifind-api)
- [THS iFinD](https://www.51ifind.com)
- [iFinD Quant API](https://quantapi.51ifind.com)
- [iFinD Quant API base endpoint](https://quantapi.51ifind.com/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API request or response content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IFIND_REFRESH_TOKEN and network access to quantapi.51ifind.com; portfolio_manage endpoints can mutate portfolio data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
