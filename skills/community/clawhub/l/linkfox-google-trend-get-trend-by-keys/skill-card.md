## Description:

Analyzes Google Trends keyword search interest by keyword, region, and optional custom date range through LinkFox's Google Trends API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Google Trends-style search interest and compare keyword popularity over time or across supported regions. It helps identify seasonal patterns, spikes, declines, and relative search interest on a normalized 0-100 scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries, account identifiers, login flow data, payment actions, and feedback data to LinkFox services.

Mitigation: Install and use the skill only when LinkFox is trusted for those data types, and avoid submitting confidential or regulated search terms.

Risk: API keys and full response files may persist locally or in shell configuration.

Mitigation: Use scoped credentials where possible, avoid placing API keys in shell startup files, and review or delete saved linkfox response files after use.

Risk: Endpoint override environment variables can redirect traffic away from the documented LinkFox services.

Mitigation: Keep default endpoints for normal use and inspect LinkFox-related environment variables before running the scripts.

## Reference(s):

- [谷歌趋势-关键词趋势 API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-google-trend-get-trend-by-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files]

**Output Format:** [Markdown guidance with JSON response summaries and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may be saved under a local linkfox session directory; small responses may be printed inline, while larger responses are summarized.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
