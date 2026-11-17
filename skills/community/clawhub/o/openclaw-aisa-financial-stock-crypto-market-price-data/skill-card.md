## Description:

Query real-time and historical financial data across equities and crypto, including prices, market moves, metrics, and trends for analysis, alerts, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external agent users use this skill to query AIsa market-data APIs for stock and cryptocurrency prices, financial statements, company news, analyst estimates, SEC filings, interest rates, insider activity, institutional ownership, and screening workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to AISA_API_KEY for authenticated market-data requests.

Mitigation: Install and run it only in environments where the AIsa credential is intended for this use, and avoid exposing the key in prompts, logs, or shared command output.

Risk: Automated or repeated API calls may consume paid AIsa credits.

Mitigation: Review the provider account limits, expected query volume, and returned usage cost before enabling repeated or unattended workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-financial-stock-crypto-market-price-data)
- [OpenClaw Homepage](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and may consume paid AIsa API credits when requests are executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
