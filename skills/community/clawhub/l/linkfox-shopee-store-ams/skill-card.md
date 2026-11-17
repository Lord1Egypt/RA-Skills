## Description:

Helps agents manage Shopee AMS affiliate marketing for authorized stores through LinkFox, including Open Campaign and Targeted Campaign product, affiliate, commission, and performance operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopee store operators and their agents use this skill to inspect and manage affiliate marketing campaigns, affiliates, commission settings, and performance reports for stores already authorized through LinkFox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use LinkFox credentials for authorized Shopee stores and perform live affiliate campaign changes.

Mitigation: Install and run it only for stores the user is authorized to manage, and review bulk or mutating AMS actions before execution.

Risk: Saved response files may contain sensitive business, campaign, affiliate, or performance data.

Mitigation: Store outputs in an appropriate workspace, limit access to generated linkfox data directories, and avoid sharing response files without review.

Risk: Onboarding and billing flows can create account setup or payment actions.

Mitigation: Use onboarding or payment commands only when the user intentionally requests LinkFox account setup, API key recovery, or plan purchase.

Risk: Environment overrides for gateway URLs can redirect requests away from the default LinkFox endpoints.

Mitigation: Avoid setting gateway override environment variables unless the endpoint is trusted and intentionally selected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-ams)
- [Shopee AMS API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [Shopee Open Platform AMS Index](https://open.shopee.com/documents/v2/v2.ams.get_open_campaign_added_product?module=127&type=1)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a linkfox session data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
