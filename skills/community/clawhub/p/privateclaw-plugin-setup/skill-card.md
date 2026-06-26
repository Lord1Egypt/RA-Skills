## Description: <br>
Install, enable, verify, pair, and manage PrivateClaw OpenClaw sessions, preferring same-conversation /privateclaw QR replies and falling back to the local CLI when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topcheer](https://clawhub.ai/user/topcheer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and configure the PrivateClaw plugin, verify command registration, and choose the appropriate QR pairing flow for chat-backed or local sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default install path uses an unsafe-install override for an unpinned external plugin package. <br>
Mitigation: Install only when the publisher and package source are trusted, prefer a pinned version or reviewed local checkout, and avoid bypassing install safety checks unless the reason is understood. <br>
Risk: PrivateClaw pairing sessions can remain active in a background daemon after the QR is printed. <br>
Mitigation: Review active sessions after pairing and close or remove sessions that should no longer remain open. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/topcheer/privateclaw-plugin-setup) <br>
- [PrivateClaw provider homepage](https://github.com/topcheer/PrivateClaw/tree/main/packages/privateclaw-provider) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and configuration changes should be reviewed before execution in the user's OpenClaw environment.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
