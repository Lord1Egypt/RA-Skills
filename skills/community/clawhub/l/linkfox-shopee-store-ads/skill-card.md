## Description:

Shopee（虾皮）店铺站内广告 Ads skill for calling 23 Shopee Open API Ads endpoints through LinkFox, including ad balance checks, manual product ads, campaign performance, GMS ads, keyword recommendations, and budget or ROI suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to manage and inspect Shopee store ads from an agent, after confirming LinkFox API key setup and AD authorization for the target shop. It supports account balance, recommendations, product ad creation and editing, CPC and campaign performance reporting, and GMS campaign workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Shopee shop advertising data and API keys, and may persist full API responses that contain business data.

Mitigation: Review saved response files, remove sensitive outputs when no longer needed, and only run the skill in workspaces where persisting ad data is acceptable.

Risk: Onboarding and billing flows can involve account setup, payment orders, or SMS-based login steps.

Mitigation: Use those flows only when explicitly intended, avoid sharing SMS codes unnecessarily, and verify payment details before creating or presenting orders.

Risk: Endpoint override or proxy configuration could send requests to unexpected hosts.

Mitigation: Confirm no endpoint override environment variables point to untrusted hosts before using the Shopee Ads proxy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-ads)
- [Shopee Ads API index](https://open.shopee.com/documents/v2/v2.ads.get_total_balance?module=117&type=1)
- [API reference](references/api.md)
- [Onboarding and auth/billing guidance](references/onboarding.md)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses or saved response-file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save complete API responses under the current working directory and print either complete JSON or a summarized response depending on response size.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
