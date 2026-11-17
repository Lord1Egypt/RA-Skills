## Description:

Manages authorized Shopee store discount promotions through LinkFox wrappers for the Shopee Open API Discount module, including create, list, update, end, delete, item-level, and SIP discount operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to create, inspect, update, end, or delete Shopee discount promotions for stores that have already been authorized through the companion LinkFox Shopee auth skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Shopee promotion authority, API keys, phone-based login, and payment flows.

Mitigation: Install only when the publisher is trusted, keep API keys out of shell history and shared profiles, and use the official HTTPS LinkFox gateway.

Risk: Create, update, end, and delete operations can change live Shopee store discount campaigns.

Mitigation: Require explicit human confirmation before any store-changing discount action.

Risk: Full API responses are persisted locally and may contain sensitive store or promotion data.

Mitigation: Keep saved response files out of repositories and shared workspaces unless they have been reviewed and sanitized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-discount)
- [Shopee Discount API index](https://open.shopee.com/documents/v2/v2.discount.add_discount?module=99&type=1)
- [Discount module API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Small responses are printed in full; larger responses are summarized after the complete JSON response is saved under a LinkFox session data directory.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
