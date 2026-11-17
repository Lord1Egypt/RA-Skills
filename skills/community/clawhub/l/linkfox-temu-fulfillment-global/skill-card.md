## Description:

Helps agents use LinkFox's Temu Global fulfillment integration for Buy-Shipping labels, cooperative warehouse fulfillment, seller-fulfilled shipment updates, and tracking across 23 supported API operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketplace operators use this skill to prepare and execute Temu Global fulfillment workflows such as purchasing shipping labels, submitting cooperative warehouse fulfillment, confirming seller-fulfilled shipments, and checking tracking status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing fulfillment operations can create, confirm, cancel, or retrieve shipment and tracking data.

Mitigation: Require explicit user confirmation before shipment creation, confirmation, cancellation, token storage, or paid plan purchases, and review request parameters before running scripts.

Risk: Local token and response files may contain reusable credentials or customer and merchant fulfillment data.

Mitigation: Use the skill only in trusted workspaces, restrict access to token and output directories, and delete sensitive local files when they are no longer needed.

Risk: Custom gateway environment variables can redirect credential-bearing requests to an unintended endpoint.

Mitigation: Use the default LinkFox gateway unless the configured endpoint is expected and controlled by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-fulfillment-global)
- [API reference](references/api.md)
- [Access token authorization and retrieval](references/access-token.md)
- [Partner Global fulfillment catalog](references/partner-global-catalog.md)
- [Fulfillment API document index](references/apis/README.md)
- [Temu Partner Global fulfillment documentation](https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands; called scripts emit JSON and may save JSON response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts require LinkFox API credentials and either a Temu accessToken or saved storeKey; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
