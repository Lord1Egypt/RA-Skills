## Description:

Analyzes Amazon product listing titles to tokenize terms, count keyword frequency, and extract scene, audience, material, and other attribute dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce analysts use this skill to analyze previously retrieved product titles, identify frequent title terms, and compare scene, audience, material, feature, and other attribute patterns across listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product/title data and account metadata to LinkFox-backed services.

Mitigation: Install only when that data sharing is intended, and verify LINKFOX_* endpoint variables point to trusted LinkFox hosts.

Risk: The skill includes account login, API-key generation, billing, payment-order, and broad local persistence behaviors.

Mitigation: Use a secure secret manager for API keys, avoid agent-handled SMS login when possible, and require explicit approval before billing or payment-order actions.

Risk: The LinkFox title-analysis service can consume paid compute credits and may incur high cost for large title sets.

Mitigation: Warn the user about potential credit usage before calls, keep requests to one attribute dimension, and rely on the provided cache instead of repeating identical calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-product-title-analyze)
- [商品标题分词分析 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes one requested title-attribute dimension per call; large API responses are summarized in stdout while the full JSON response is written under the local linkfox session data directory.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
