## Description: <br>
Run OpenClaw as a system-level macOS LaunchDaemon for continuous operation through screen lock, logout, reboot, and user switching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happydog-intj](https://clawhub.ai/user/happydog-intj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure an always-on macOS gateway service for bots that should keep responding while the screen is locked, the user is logged out, or the machine restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow creates a persistent sudo-managed macOS LaunchDaemon that runs OpenClaw after lock, logout, and reboot. <br>
Mitigation: Install only on Macs intended for always-on OpenClaw operation, review the generated plist before loading it, and uninstall or disable the LaunchDaemon when continuous background operation is no longer required. <br>
Risk: The documented one-line curl-to-bash install path can execute remote shell content without local review. <br>
Mitigation: Download a pinned release or artifact first, inspect install.sh and the LaunchDaemon plist, then run the reviewed copy locally. <br>
Risk: The gateway token may be stored in the LaunchDaemon plist, which can expose it to local users who can read the plist. <br>
Mitigation: Prefer a restricted secret store such as macOS Keychain where practical, limit use on shared Macs, and rotate the gateway token after testing, uninstalling, or any suspected exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happydog-intj/openclaw-macos-always-on) <br>
- [Publisher profile](https://clawhub.ai/user/happydog-intj) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [install.sh](artifact/install.sh) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and XML plist configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, verification, management, troubleshooting, and uninstall guidance for a macOS LaunchDaemon.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
