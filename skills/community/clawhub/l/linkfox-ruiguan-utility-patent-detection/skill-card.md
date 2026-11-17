## Description:

Searches for similar US utility and invention patents from product information to help cross-border e-commerce sellers review patent and TRO risk before listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and their agents use this skill to check product titles and descriptions against similar US utility or invention patents before selling. It helps prioritize patent records for review, highlight TRO indicators, and avoid presenting similarity results as legal conclusions.

### Deployment Geography for Use:

Global; patent search coverage is currently limited to US patents.

## Known Risks and Mitigations:

Risk: Product descriptions, patent-query context, API credentials, and session metadata may be sent to LinkFox services.

Mitigation: Use the skill only with approved data, avoid confidential pre-launch product details without approval, and store API keys in a secure secret manager or environment configuration.

Risk: Endpoint override environment variables can redirect credential-bearing requests.

Mitigation: Use default LinkFox endpoints unless the override target is fully controlled and trusted.

Risk: Billing and payment actions may consume credits or create orders.

Mitigation: Review plan, payment method, and order details before paying; require user confirmation before additional high-cost calls.

Risk: Patent similarity results can be mistaken for legal advice or a definitive infringement determination.

Mitigation: Present results factually, distinguish active from invalid patents, and recommend patent-attorney review for legal conclusions.

Risk: Complete API responses are automatically persisted in the working directory.

Mitigation: Keep the workspace access-controlled and remove saved patent-search outputs when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-ruiguan-utility-patent-detection)
- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [Ruiguan Utility Patent Detection API](https://tool-gateway.linkfox.com/ruiguan/utilityPatentDetection)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with patent-result tables, shell commands, and JSON API responses saved to local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are persisted under the working directory; large responses may be summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
