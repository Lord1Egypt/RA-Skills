## Description:

Remotely controls GLKVM IP-KVM devices and attached hosts through HTTP API workflows for screenshots, OCR, keyboard and mouse input, Fingerbot and ATX power actions, device management, firmware upgrades, and virtual MSD storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzefu](https://clawhub.ai/user/duzefu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and administrators use this skill to operate authorized GLKVM-managed hosts remotely, inspect screen state, send keyboard and mouse input, manage host power, update device firmware, and prepare virtual media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles full-control GLKVM credentials and session tokens.

Mitigation: Use a private per-session cookie file, treat it as a credential, and delete tokens after the task.

Risk: Transport examples disable certificate verification, which can weaken protection on untrusted networks.

Mitigation: Use the skill only on trusted management networks and prefer valid certificates or pinned certificates or public keys.

Risk: Screenshots and OCR may expose sensitive data from the attached host.

Mitigation: Treat screen captures and OCR output as sensitive and avoid retaining them beyond the task.

Risk: Power, reset, firmware, and virtual media operations can disrupt service or cause data loss.

Mitigation: Require explicit user confirmation before disruptive operations and use only trusted firmware or ISO sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzefu/skills/glkvm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GLKVM IP address and admin password supplied by an authorized user.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
