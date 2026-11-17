## Description:

Assist with express delivery services including shipping cost estimation, logistics tracking, order creation with QR code, and order cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanghai-kb](https://clawhub.ai/user/shanghai-kb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shipping support agents use this skill to estimate courier fees, query package tracking, create shipment orders that return a QR code, and cancel existing shipment orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles personal shipment data and order changes while the security summary flags unsafe execution, logging, and command-line handling concerns.

Mitigation: Use non-sensitive test data until logging and command-line handling are fixed, and review requested actions before execution.

Risk: A bundled API key is present in the artifact configuration.

Mitigation: Remove or rotate the bundled credential and configure user-specific API credentials through environment variables.

Risk: Order cancellation can change real shipment state.

Mitigation: Require explicit user confirmation before cancelling an order and verify the courier brand and order identifier.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shanghai-kb/skills/kuaidihelp-skill)
- [Kuaidihelp Open Platform](http://open.kuaidihelp.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shipment pricing, tracking information, order QR-code links, cancellation results, and prompts for missing required shipping parameters.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
