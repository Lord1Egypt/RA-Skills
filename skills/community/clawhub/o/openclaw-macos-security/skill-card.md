## Description:

macOS security monitoring for OpenClaw

This skill is ready for commercial/non-commercial use.

## Publisher:

[drg3nz0](https://clawhub.ai/user/drg3nz0)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to ask an OpenClaw agent for local macOS security checks, including camera, microphone, firewall, VPN, open-port, and WiFi status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad execution, file-read, and network permissions for local macOS diagnostics.

Mitigation: Review the requested permissions before installing and run the skill only in a trusted macOS environment where local diagnostic command execution is acceptable.

Risk: The documentation advertises app-blocking and a larger command set than the reviewed code provides.

Mitigation: Treat block-app and unsupported advertised commands as non-protective in this version and verify important security findings with independent system tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drg3nz0/skills/openclaw-macos-security)
- [npm package](https://www.npmjs.com/package/openclaw-macos-security)
- [MaclawPro website](https://maclawpro.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses summarize local macOS diagnostic command results and may include links to MaclawPro.]

## Skill Version(s):

1.0.4 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
