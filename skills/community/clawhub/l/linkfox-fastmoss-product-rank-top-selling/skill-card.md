## Description:

Queries FastMoss data for TikTok global e-commerce top-selling product rankings, with daily, weekly, monthly, and category-based analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and analysts use this skill to inspect TikTok Shop top-selling product rankings across supported global markets, time windows, and categories. It helps agents return ranked product data and concise tabular summaries without adding subjective business advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle LinkFox/FastMoss account access, API keys, phone verification, and billing workflows.

Mitigation: Review requests for phone numbers, SMS codes, API keys, plan purchases, or payment QR codes before allowing the agent to proceed.

Risk: Endpoint override environment variables can redirect account or ranking requests.

Mitigation: Use endpoint override variables only for infrastructure you control, and keep the default LinkFox endpoints for normal use.

Risk: API keys may be exposed if stored casually in shell profile files or shared logs.

Mitigation: Prefer secure secret storage and avoid pasting API keys into shared terminals, logs, or public configuration.

Risk: Each ranking lookup consumes paid compute credits.

Mitigation: Confirm repeated, paginated, or changed-parameter lookups with the user when cost expectations are unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-fastmoss-product-rank-top-selling)
- [FastMoss-TikTok热销榜单 API 参考](artifact/references/api.md)
- [解决认证和算力问题](artifact/references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON API responses, saved JSON data files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The tool saves complete API responses under a local linkfox data directory, prints small responses as JSON, and summarizes larger responses unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
