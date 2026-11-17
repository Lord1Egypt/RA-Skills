## Description:

Query free financial data APIs for stocks, crypto, macroeconomic data, SEC filings, and related market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anotb](https://clawhub.ai/user/anotb)

### License/Terms of Use:


## Use Case:

Developers and financial-data users use this skill to query market, crypto, macroeconomic, SEC filing, and company financial data through the open-market-data CLI. It helps agents produce commands, configuration guidance, and parseable CLI workflows for supported providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing the open-market-data npm package, and the release evidence notes that the package is unpinned.

Mitigation: Use a pinned or reviewed package version, especially in sensitive environments.

Risk: The CLI can store or use financial-data API keys.

Mitigation: Configure API keys only in environments where the CLI package and local storage behavior have been reviewed.

## Reference(s):

- [open-market-data homepage](https://github.com/anotb/open-market-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash examples; CLI commands may emit text, JSON, or plain output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require node, the omd binary, and optional provider API keys.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
