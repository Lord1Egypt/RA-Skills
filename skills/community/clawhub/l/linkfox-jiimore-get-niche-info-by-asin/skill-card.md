## Description:

Analyzes Amazon niche segments associated with a product ASIN, including competitive intensity, brand concentration, new-product success rate, and market opportunity signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and e-commerce analysts use this skill to query ASIN-driven niche market data and compare demand, sales, pricing, advertising, brand, and competition metrics for supported marketplaces.

### Deployment Geography for Use:

Global use; marketplace data is limited to US, JP, and DE.

## Known Risks and Mitigations:

Risk: The skill can handle phone/SMS login and expose generated API keys in command output.

Mitigation: Use only a trusted LinkFox account, avoid placing SMS codes or secrets in logged command lines, and treat generated API keys as sensitive credentials.

Risk: The onboarding flow can create payment orders when billing or quota issues occur.

Mitigation: Require an explicit user decision before creating an order and show payment details for review before continuing.

Risk: The skill writes full API responses locally and may send feedback to a separate LinkFox service.

Mitigation: Review saved response files for sensitive data, apply workspace retention controls, and disclose feedback reporting when user comments are submitted.

Risk: Endpoint environment variables can redirect requests away from the expected LinkFox services.

Mitigation: Verify configured endpoint variables before use and prefer the documented LinkFox service URLs unless an approved deployment requires overrides.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-jiimore-get-niche-info-by-asin)
- [API reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses, inline shell commands, and saved local response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script saves full responses locally, summarizes responses larger than 8 KB unless inline output is requested, and uses a 24-hour local cache.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
