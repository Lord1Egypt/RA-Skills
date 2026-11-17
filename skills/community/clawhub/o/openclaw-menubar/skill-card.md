## Description:

Enables OpenClaw as a macOS-only native menu bar app with quick chat popup access to a local OpenClaw gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prab002](https://clawhub.ai/user/prab002)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users on macOS use this skill to install and run a lightweight Electron menu bar app for quick chat access without opening the full dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles OpenClaw gateway credentials and authentication tokens.

Mitigation: Review token handling before installing; remove token logging and prefer secure OS credential storage such as Keychain.

Risk: The Electron app loads local gateway web content and uses unsafe defaults in parts of the window configuration.

Mitigation: Harden Electron settings before production use, including context isolation, Node integration, remote module access, external navigation, and OAuth callback validation.

Risk: The bundled dependency set may include vulnerable packages.

Mitigation: Run npm audit or equivalent dependency review and update vulnerable dependencies before deployment.

Risk: The app runs as a background macOS menu bar process connected to the local gateway.

Mitigation: Install only on trusted macOS hosts and use the provided stop script when the background app is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prab002/skills/openclaw-menubar)
- [Publisher profile](https://clawhub.ai/user/prab002)
- [Artifact skill instructions](artifact/SKILL.md)
- [OpenClaw Menu Bar package metadata](artifact/assets/openclaw-menubar/package.json)
- [menubar package reference](https://github.com/maxogden/menubar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and packaged Electron app files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; requires a local OpenClaw gateway and Node.js.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
