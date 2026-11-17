## Description:

Run OpenClaw as a system-level LaunchDaemon on macOS for 24/7 operation across screen lock, logout, and user switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happydog-intj](https://clawhub.ai/user/happydog-intj)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to keep an OpenClaw gateway running persistently on macOS when a machine is locked, logged out, or used as an always-on host. It provides setup, verification, management, troubleshooting, and uninstall guidance for a LaunchDaemon-based configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer requires privileged LaunchDaemon installation and changes system service state.

Mitigation: Use it only when always-on system-level OpenClaw behavior is required, inspect a pinned installer before running it, and prefer a LaunchAgent when logged-in-only operation is sufficient.

Risk: The generated LaunchDaemon can expose the OpenClaw gateway token to local users through plist environment variables.

Mitigation: Rotate the gateway token after prior use of the installer and prefer a Keychain-backed token design for stronger local secret handling.

Risk: The documented one-line curl-to-bash install pattern executes remote code directly.

Mitigation: Download the installer first, verify its source and integrity, review its contents, and run only the reviewed copy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/happydog-intj/skills/openclaw-macos-always-on)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [Chinese README](artifact/README.zh-CN.md)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and LaunchDaemon plist configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides installation, verification, management, troubleshooting, and uninstall instructions for macOS systems.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
