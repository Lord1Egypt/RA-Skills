## Description:

Get stock screener list data from Intellectia API (no auth) and summarize results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[intellectiaai](https://clawhub.ai/user/intellectiaai)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to fetch Intellectia stock, ETF, or crypto screener rows and summarize market screener results from the documented API response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries Intellectia's external API for stock screener data.

Mitigation: Install only if external API access to Intellectia is acceptable for the target environment.

Risk: The evidence notes an unpinned Python dependency on requests.

Mitigation: Use an isolated Python environment and consider pinning requests before installation.

Risk: Returned market predictions and probabilities may be mistaken for financial advice.

Mitigation: Treat screener predictions as informational and apply independent financial review before making investment decisions.

## Reference(s):

- [Intellectia API Base URL](https://api.intellectia.ai)
- [Stock Screener List Endpoint](https://api.intellectia.ai/gateway/v1/stock/screener-list)
- [ClawHub Skill Page](https://clawhub.ai/intellectiaai/skills/intellectia-stock-screener)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON response examples, cURL commands, and Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents API query parameters and response fields for stock screener data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
