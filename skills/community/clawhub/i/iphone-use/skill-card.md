## Description:

Use when a task needs a real iPhone: operating iOS apps that have no API, exporting on-phone data, tapping, typing, scrolling, or taking phone screenshots through the iphone-use daemon's HTTP agent API over macOS iPhone Mirroring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent through real iPhone workflows where app APIs are unavailable, including UI automation, screenshots, data export, and repeatable task scripting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a real iPhone, including sensitive apps and actions with real-world consequences.

Mitigation: Use only with a phone and Mac you control, verify the screen before destructive actions, and avoid unattended payment or 2FA flows.

Risk: The daemon API is protected by a bearer token, so leaked credentials could allow unwanted phone control.

Mitigation: Protect the daemon token, keep it out of logs and shared files, and restrict access to trusted hosts and networks.

Risk: The documented installer path relies on a remote shell command that creates persistent software on the Mac.

Mitigation: Review or pin the installer before execution and confirm the LaunchAgent behavior before installing.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/leeguooooo/iphone-use/tree/main/skills/iphone-use)
- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/iphone-use)
- [Publisher profile](https://clawhub.ai/user/leeguooooo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request payloads, curl commands, troubleshooting guidance, and reusable script outlines.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
