## Description:

Guidance for installing, configuring, and operating Open Computer Use, an open-source Computer Use MCP service for macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifuryst](https://clawhub.ai/user/ifuryst)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install, configure, verify, troubleshoot, and operate the Open Computer Use MCP service from compatible agent runtimes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures a desktop-control MCP tool with broad access to the user's local computer session.

Mitigation: Install only trusted package and repository versions, grant OS permissions only when needed, and revoke permissions or remove MCP/plugin configuration when no longer used.

Risk: Desktop automation can send messages, submit forms, delete data, install software, change system settings, make purchases, or expose sensitive local information.

Mitigation: Require user approval before sensitive actions and re-read application state after important actions before continuing.

## Reference(s):

- [Open Computer Use ClawHub page](https://clawhub.ai/ifuryst/skills/open-computer-use)
- [Open Computer Use repository](https://github.com/iFurySt/open-codex-computer-use)
- [open-computer-use npm package](https://www.npmjs.com/package/open-computer-use)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON configuration examples, and operating guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes safety guidance for desktop-control permissions and MCP/plugin configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
