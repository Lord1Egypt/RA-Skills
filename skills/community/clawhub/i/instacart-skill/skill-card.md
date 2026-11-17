## Description:

Place grocery orders on Instacart via browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigdaddyluke](https://clawhub.ai/user/bigdaddyluke)

### License/Terms of Use:


## Use Case:

External users use this agent skill to build and manage Instacart grocery carts, including search, reorder, smart lookback from order history, and nightly auto-replenishment summaries. The skill requires explicit confirmation before checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate an Instacart account with saved delivery address and payment details.

Mitigation: Require explicit user confirmation before placing an order and review item count, subtotal, fees, tip, total, delivery address, and payment method before checkout.

Risk: The skill may retrieve Instacart login verification codes through an authenticated email CLI.

Mitigation: Prefer manually supplied verification codes unless the user trusts the configured gog email access.

Risk: A loosely scoped INSTACART_URL could direct browser automation away from the intended service.

Mitigation: Keep INSTACART_URL restricted to the real Instacart domain before opening the browser.

Risk: Nightly replenishment can make automated cart changes based on order history.

Mitigation: Use external controls for scheduled runs and review all cart changes before any purchase.

## Reference(s):

- [Instacart](https://www.instacart.com)
- [ClawHub Instacart skill page](https://clawhub.ai/bigdaddyluke/skills/instacart-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw browser, gog CLI when email-code retrieval is enabled, and INSTACART_URL and INSTACART_EMAIL environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
