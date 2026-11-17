## Description:

Helps agents manage Shopee Add-On Deal promotions for authorized stores by using LinkFox scripts for the Shopee Open API Add-On Deal module, including creation, listing, item updates, deletion, and early termination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators, e-commerce teams, and developers use this skill to create, inspect, update, end, or delete Shopee Add-On Deal promotions for stores already authorized through the companion LinkFox Shopee auth skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform operational changes to Shopee Add-On Deal promotions for authorized stores.

Mitigation: Review the intended shop, merchant, promotion, item, and action before running create, update, delete, or end operations.

Risk: The skill handles LinkFox API keys, Shopee store access, account onboarding, SMS-code login, billing, and payment flows.

Mitigation: Install only if you trust LinkFox, keep generated API keys secret, and do not submit SMS codes or payment actions unless the user explicitly intends that step.

Risk: The scripts persist full API responses to local JSON files that may include sensitive store or promotion data.

Mitigation: Review and protect saved LinkFox output files, and remove sensitive response files when they are no longer needed.

Risk: Environment URL overrides can redirect API traffic away from the default LinkFox endpoints.

Mitigation: Avoid setting gateway or login URL override environment variables unless the endpoint is trusted and expected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-add-on-deal)
- [Shopee Add-On Deal API Index](https://open.shopee.com/documents/v2/v2.add_on_deal.add_add_on_deal?module=111&type=1)
- [API Parameter and Field Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses; full responses are also saved as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Small responses are printed in full; larger responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
