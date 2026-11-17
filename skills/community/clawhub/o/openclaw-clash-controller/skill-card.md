## Description:

Controls Clash for Windows proxy status, routing mode, and node selection through a local Clash controller.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icenoodle](https://clawhub.ai/user/icenoodle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users operating a Windows host with Clash for Windows use this skill to check proxy status, enable or disable proxy routing, and switch nodes from an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds a Clash controller secret and may authenticate to a local controller configured with that shared secret.

Mitigation: Rotate or replace the bundled secret, configure Clash with a private secret, and use it only with a local Clash controller you control.

Risk: Broad natural-language trigger phrases can change proxy routing without a clear confirmation step.

Mitigation: Require explicit Clash-specific commands or confirmation before allowing enable, disable, or node-switch operations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/icenoodle/skills/openclaw-clash-controller)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text status, confirmation, and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report local Clash proxy status and selected node when the controller is reachable.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
