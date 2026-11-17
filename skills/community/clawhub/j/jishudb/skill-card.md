## Description:

Helps install, locate, connect, and troubleshoot JishuDB Desktop or a remote JishuDB service for an agent client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to set up JishuDB Desktop, find an existing service, configure an MCP client, and recover connection or authorization failures. It verifies the actual client connection rather than answering knowledge-base questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can download and launch JishuDB Desktop and change the selected MCP client configuration.

Mitigation: Approve the helper's release source, paths, and client profile before execution; install only when these local changes are intended.

Risk: The Windows installer may show an unsigned publisher notice.

Mitigation: Review the publisher notice and installation plan before consenting.

Risk: Sharing authorization codes or tokens in chat can expose credentials.

Mitigation: Complete authorization in the intended browser or client flow; never provide OAuth codes or tokens in chat.

## Reference(s):

- [JishuDB skill homepage (listed in release metadata)](https://github.com/x-aijishu/jishudb-skills/tree/main/skills/jishudb)
- [Installation contract](references/installation-contract.md)
- [Connection recovery](references/connection-recovery.md)
- [macOS CNB installation](references/cnb-macos-installation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with setup steps, commands, and connection status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a verified client connection or the next required user action.]

## Skill Version(s):

0.1.22 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
