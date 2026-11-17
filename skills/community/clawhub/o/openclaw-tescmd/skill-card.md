## Description:

Installation and setup guide for Tesla vehicle control and telemetry via the tescmd node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oceanswave](https://clawhub.ai/user/oceanswave)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and configure Tesla vehicle control and telemetry integration between OpenClaw Gateway and the tescmd node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing mutable external components can change behavior after review.

Mitigation: Prefer package-manager or signed-install methods and pin reviewed versions where possible.

Risk: Tesla, OpenClaw, and gateway credentials may be exposed through command lines or local configuration files.

Mitigation: Avoid placing secrets on command lines, restrict permissions on ~/.config/tescmd files, and rotate credentials if exposure is suspected.

Risk: The setup controls vehicle integration and requires interactive authentication and pairing.

Mitigation: Review the setup flow carefully before installation and keep human confirmation for browser login, vehicle pairing, and gateway approval steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oceanswave/skills/openclaw-tescmd)
- [OpenClaw Tesla plugin repository](https://github.com/oceanswave/openclaw-tescmd)
- [tescmd node repository](https://github.com/oceanswave/tescmd)
- [GitHub CLI Linux install documentation](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
- [Tailscale download](https://tailscale.com/download)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes interactive setup checkpoints that require user confirmation outside the agent.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
