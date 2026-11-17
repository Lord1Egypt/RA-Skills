## Description:

Search and read ShipBob inventory, channel, location, and product data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using ShipBob can retrieve inventory levels, channels, fulfillment locations, and product catalog data from their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run remote CLI installers without an explicit approval step.

Mitigation: Review the CLI release and installer behavior, explicitly approve local installation changes, and check automatic skill-installation settings.

Risk: Connecting the service gives OOMOL access to ShipBob account data.

Mitigation: Confirm OOMOL is authorized to access the ShipBob account and its data before connecting.

## Reference(s):

- [ShipBob API documentation: Channels](https://developer.shipbob.com/api/channels/get-channels)
- [ShipBob homepage](https://www.shipbob.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ShipBob skill on ClawHub](https://clawhub.ai/oomol/skills/oo-ship-bob)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Natural-language guidance and shell commands; structured JSON data from ShipBob queries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented queries for inventory, channels, locations, and products.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
