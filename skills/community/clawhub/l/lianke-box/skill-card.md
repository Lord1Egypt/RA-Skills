## Description:

Lianke Print Box helps agents guide users through remote printing, printer and job status checks, scanning, and device management for Lianke cloud print boxes through the lk-print CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nullying](https://clawhub.ai/user/nullying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and end users use this skill to obtain workflow guidance and shell commands for authenticating Lianke devices, submitting print jobs, checking printer or job status, scanning documents, and managing cloud print box devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party CLI from a mutable Git repository.

Mitigation: Review and pin a trusted lk-print CLI version before use in sensitive or managed environments.

Risk: The CLI handles API keys, device credentials, print files, and scanned documents through a cloud-connected service path.

Mitigation: Treat credentials as secrets and avoid sensitive print or scan jobs unless the Lianke service, devices, and network handling meet the user's requirements.

## Reference(s):

- [Lianke Print Box on ClawHub](https://clawhub.ai/nullying/skills/lianke-box)
- [lk-print CLI repository](https://github.com/liankenet/lk-print-box.git)
- [Lianke Open Platform](https://open.liankenet.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a configured lk-print CLI and Lianke API key, device ID, and device key.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
