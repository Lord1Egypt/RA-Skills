## Description:

A-share quantitative data analysis skill that helps agents use AkShare to retrieve market quotes, historical K-line data, financial data, sector information, and related stock research data.

This skill is for research and development only.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:


## Use Case:

External developers and analysts use this skill to ask an agent for AkShare-based A-share quotes, historical prices, financial indicators, sector data, fund flows, IPO data, and related research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial market data may be delayed, unavailable, inaccurate, or unsuitable for investment decisions.

Mitigation: Treat results as research data, verify important outputs against authoritative financial sources, and do not rely on the skill as investment advice.

Risk: AkShare and upstream financial data websites can change, causing package, network, or interface failures.

Mitigation: Install dependencies in a dedicated virtual environment, pin and review AkShare before use, and add exception handling and retry logic around data calls.

Risk: Some documented features or helper script paths may require fixes before they work reliably.

Mitigation: Review and test commands in a local environment before using the skill in repeatable workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/new-akshare-stock)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks; CLI examples can return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require network access to financial data sources; results are research data and not investment advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
