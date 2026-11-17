## Description:

A Hong Kong IPO research assistant that gathers public data on margin financing, cornerstone investors, ratings, grey-market activity, A/H discounts, and allotment odds for agent-assisted IPO analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marvae](https://clawhub.ai/user/marvae)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to collect and summarize Hong Kong IPO market data, compare IPO attributes, estimate allotment odds, and produce research support for IPO subscription decisions. The source skill states that third-party public data is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The profile command may store capital, risk preference, margin preference, and broker in a local user-profile file and may print that profile into chat or logs.

Mitigation: Create scripts/config/user-profile.yaml only after informed consent, avoid sensitive account data, and review chat or log output before sharing.

Risk: The skill is a Hong Kong IPO research tool based on third-party public market data and can produce financial analysis that may be incomplete or stale.

Mitigation: Treat outputs as research support rather than investment advice and verify current offering terms, prospectuses, and broker data before acting.

Risk: The release executes Python scripts with external dependencies.

Mitigation: Use an isolated Python environment, avoid sudo, and consider pinning or reviewing dependencies before installation.

## Reference(s):

- [Analysis Guide](references/analysis-guide.md)
- [IPO Mechanism Guide](references/ipo-mechanism.md)
- [API Guide](references/api-guide.md)
- [AiPO API Documentation](references/aipo-api.md)
- [Risk Preferences Guide](references/risk-preferences.md)
- [AiPO Data Source](https://aipo.myiqdii.com)
- [AASTOCKS IPO Data Source](https://www.aastocks.com/tc/stocks/market/ipo/)
- [ClawHub Skill Page](https://clawhub.ai/marvae/skills/hk-ipo-research-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON or table-formatted CLI output, and local YAML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query third-party public market data sources and may read or print an optional local user profile.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
