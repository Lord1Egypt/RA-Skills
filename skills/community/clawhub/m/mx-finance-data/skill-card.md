## Description:

Queries Eastmoney financial data from natural-language requests across A-shares, Hong Kong and US equities, ETFs, funds, bonds, indices, sectors, shareholders, issuers, and companies, returning structured Excel and Markdown results for investment and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to fetch market quotes, financial indicators, company information, valuation data, and financial tables from natural-language finance questions. It supports research workflows such as investment analysis, market monitoring, trade review, sector analysis, credit review, financial statement review, and asset allocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undocumented API endpoint override can expose EM_API_KEY if invoked with an untrusted URL.

Mitigation: Use the documented CLI path, avoid custom API endpoint parameters, and keep the key revocable.

Risk: The skill depends on a user-provided Eastmoney API key and third-party API workflow.

Mitigation: Install only when the Eastmoney workflow is trusted, protect the EM_API_KEY value, and run in an isolated Python environment with reviewed dependency versions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/financial-ai-analyst/skills/mx-finance-data)
- [Eastmoney Miaoxiang Claw Service](https://ai.eastmoney.com/mxClaw)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions]

**Output Format:** [CLI status text plus Excel workbooks and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and writes results under miaoxiang/mx_finance_data; multi-entity queries process up to 500 recognized entities per run.]

## Skill Version(s):

1.0.12 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
