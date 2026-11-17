## Description:

Fetches batch TikTok Shop product details for known product IDs or URLs, including sales, GMV, livestream, video, influencer, price, rating, commission, and listing-status metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and developers use this skill to compare known TikTok Shop products side by side using multi-period sales, GMV, livestream, video, influencer, pricing, rating, commission, and listing-status data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok product IDs, URLs, and related session metadata are sent to LinkFox services.

Mitigation: Use the skill only with data you are comfortable sharing with LinkFox, and avoid adding unnecessary personal or sensitive information.

Risk: Full API responses are stored on disk in the working directory.

Mitigation: Review generated JSON files for sensitive product or session details and apply appropriate retention and access controls.

Risk: Onboarding and billing flows may involve phone numbers, SMS codes, payment methods, or credit purchases.

Mitigation: Run those flows only when you explicitly intend to authenticate or purchase credits, and verify plan and payment details before continuing.

Risk: Environment-variable endpoint overrides can redirect LinkFox API traffic.

Mitigation: Use endpoint overrides only in trusted development setups and avoid them in normal production use.

## Reference(s):

- [EchoTik API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-batch-product-detail)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, comparison tables, shell commands, and JSON API responses or summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are written to local JSON files; large responses may be summarized unless inline output is requested. Calls consume LinkFox credits.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
