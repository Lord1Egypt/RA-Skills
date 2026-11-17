## Description:

Supports Shopee store authorization and management for separate ERP and Ads applications, including OAuth URL generation, authorized-store lookup, and authorization-status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to bind Shopee stores to LinkFox, distinguish ERP and Ads authorization records, and confirm which store identity and application type are ready for downstream Shopee workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox account access and sends credential-bearing requests to configurable LinkFox endpoints.

Mitigation: Install only after reviewing the publisher, and run it in a clean environment with trusted LINKFOX_* URL variables.

Risk: OAuth authorization URLs and API responses may be copied to the clipboard or retained in local linkfox output directories.

Mitigation: Avoid shared machines, avoid exposing terminal output, and inspect or delete generated linkfox cache files after use.

Risk: The onboarding flow can request phone verification codes and create paid billing orders.

Mitigation: Provide phone codes or payment confirmation only when you explicitly intend to set up or purchase LinkFox service access.

Risk: Automatic feedback reporting may send skill feedback to LinkFox.

Mitigation: Do not include secrets, authorization URLs, shop identifiers, or other sensitive business data in feedback content.

## Reference(s):

- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-auth)
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts persist full API responses under a local linkfox session directory and may print full or summarized JSON depending on response size.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
