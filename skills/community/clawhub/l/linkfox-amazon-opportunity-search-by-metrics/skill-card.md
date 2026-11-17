## Description:

Reverse-searches US Amazon niche and keyword opportunities from a historical metrics pool using business filters such as market size, growth, competition, pricing, demographics, product features, and review themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agent users use this skill to turn business criteria such as low competition, growth, pain points, demographics, or pricing gaps into matching US Amazon niche and keyword candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox account and API credentials to call opportunity-search and account workflows.

Mitigation: Install only when LinkFox account/API access is intended, keep API keys in a controlled secret store, and avoid adding long-lived keys to shell startup files when a safer store is available.

Risk: The onboarding flow can request phone numbers, SMS codes, and billing actions.

Mitigation: Share phone numbers or SMS codes only when intentionally registering or logging in, and confirm any plan, payment method, or payment QR code before proceeding.

Risk: The skill can send feedback payloads and supports endpoint override environment variables.

Mitigation: Review feedback content before sending it and keep endpoint override variables limited to trusted LinkFox endpoints.

Risk: API calls may consume paid compute credits, including successful empty-result calls.

Mitigation: Confirm cost-sensitive searches with the user, reuse the same parameters when possible, and widen filters deliberately instead of repeated automatic probing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-opportunity-search-by-metrics)
- [亚马逊商业洞察反向选品 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API parameters; script execution returns JSON or a summary plus a saved JSON file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are saved under a linkfox session data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
