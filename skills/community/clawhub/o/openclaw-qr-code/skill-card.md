## Description:

Generate, decode, and beautify QR codes with customizable colors, logos, and formats. Works across all OpenClaw channels including WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zouyawen](https://clawhub.ai/user/zouyawen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill in OpenClaw to generate QR codes, decode QR code images, and restyle QR codes for messaging channels such as WhatsApp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended full-feature installation path executes an unpinned remote shell script.

Mitigation: Review the installer source, pin it to a trusted revision, and verify checksums or signatures before execution; avoid direct curl-to-shell installation.

Risk: Logo path handling can expose local files if workspace boundaries are bypassed.

Mitigation: Use only relative logo paths within the workspace and keep path traversal validation enabled.

## Reference(s):

- [ClawHub QR Code skill page](https://clawhub.ai/zouyawen/skills/openclaw-qr-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce QR code generation, decoding, beautification, installation, and channel-compatibility guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
