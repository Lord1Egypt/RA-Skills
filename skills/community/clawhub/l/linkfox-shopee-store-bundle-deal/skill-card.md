## Description:

Helps agents manage Shopee store Bundle Deal promotions through LinkFox by using Shopee Open API Bundle Deal operations for creating, listing, updating, ending, and deleting bundle deals and bundle deal items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, developers, and operations teams can use this skill to inspect and manage authorized Shopee store Bundle Deal campaigns. It supports common promotion workflows such as creating a bundle deal, adding or updating items, listing campaign status, ending a campaign early, and deleting bundle deal records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that create, update, end, or delete live Shopee Bundle Deal promotions.

Mitigation: Review all promotion parameters and destructive actions with the account owner before running create, update, end, or delete commands.

Risk: The skill may guide LinkFox account setup, SMS-code login, API-key configuration, and paid plan purchase flows.

Mitigation: Prefer pre-provisioned API keys, avoid agent-mediated SMS login when possible, and require explicit user confirmation before payment or plan-selection steps.

Risk: Credential-bearing network calls are made through LinkFox endpoints and can be redirected by endpoint override environment variables.

Mitigation: Use trusted network environments and do not set endpoint override variables unless the destination is controlled and trusted.

Risk: Full API responses may be written to persistent local JSON files.

Mitigation: Run the skill in an appropriate workspace, restrict access to saved response files, and avoid including unnecessary secrets in request payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-bundle-deal)
- [Shopee Bundle Deal API reference](https://open.shopee.com/documents/v2/v2.bundle_deal.add_bundle_deal?module=110&type=1)
- [Bundle Deal API and field reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [Add bundle deal](references/apis/add-bundle-deal.md)
- [Get bundle deal list](references/apis/get-bundle-deal-list.md)
- [Update bundle deal](references/apis/update-bundle-deal.md)
- [End bundle deal](references/apis/end-bundle-deal.md)
- [Delete bundle deal](references/apis/delete-bundle-deal.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response summaries; scripts may also save full API responses as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include live Shopee promotion data, LinkFox account setup guidance, and saved local JSON output paths.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
