## Description:

Guides an agent in controlling a user's local Chrome browser through the MCP chrome-devtools protocol for browser navigation, Outlook mail access, content search, and webpage automation after the user enables Chrome remote debugging and configures OpenClaw MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyun2000](https://clawhub.ai/user/yuyun2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare OpenClaw and a local Chrome session for browser automation tasks, including navigating pages, reading Outlook mail, searching X, clicking elements, filling forms, waiting for page content, and taking snapshots or screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose logged-in browser sessions through broad local Chrome control.

Mitigation: Use a dedicated Chrome profile with only the accounts needed for the task and avoid exposing personal or administrative tabs.

Risk: The setup uses an unpinned MCP package install.

Mitigation: Pin and review the MCP package version instead of using `@latest`.

Risk: Chrome remote debugging remains available after automation work is complete.

Mitigation: Turn off remote debugging when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyun2000/skills/m5stack-chrome-browser-control)
- [Publisher profile](https://clawhub.ai/user/yuyun2000)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with JSON configuration examples and tool-call workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
