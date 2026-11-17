## Description:

Queries EchoTik TikTok Shop new product ranking data to help users identify trending new products across 16 regional markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border e-commerce sellers and product researchers use this skill to retrieve daily TikTok Shop new product rankings, compare regional performance metrics, and present the results in tables without subjective business advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox credentials, API keys, phone-based login, team/account data, and payment-order details.

Mitigation: Use only in trusted runtimes, avoid sharing secrets in chat or logs, and prefer first-party account pages or a secret store for API key management.

Risk: Endpoint override environment variables can redirect requests away from the expected LinkFox services.

Mitigation: Set endpoint override variables only when you control the destination and have verified the runtime environment.

Risk: API responses and cached results are persisted locally, which may expose product research queries or account-adjacent metadata on shared machines.

Mitigation: Run the skill in a private workspace, review generated local files before sharing the project, and clean local LinkFox output when it is no longer needed.

Risk: The skill consumes paid LinkFox credits and includes billing and order flows.

Mitigation: Confirm credit cost and user intent before repeated calls, plan purchases, or payment-order creation.

Risk: Automatic feedback reporting may send details about user intent, outcomes, or problems to LinkFox.

Mitigation: Review feedback content before submission when sensitive user or business context is involved.

## Reference(s):

- [EchoTik-TikTok新品榜 API 参考](artifact/references/api.md)
- [解决认证和算力问题](artifact/references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-list-new-product-rank)
- [LinkFox Skills](https://skill.linkfox.com/)
- [EchoTik ranking API endpoint](https://tool-gateway.linkfox.com/echotik/listNewProductRank)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API results or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses to a local JSON file, prints small responses inline, and summarizes large responses unless inline output is requested.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
