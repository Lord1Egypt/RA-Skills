## Description:

Control a real phone from OpenClaw via a local MCP relay for actions such as opening apps, tapping, entering text, taking screenshots, checking device status, and querying or aborting phone-agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobileaiuse](https://clawhub.ai/user/mobileaiuse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect OpenClaw to a local MCP relay and operate a connected Android or iPhone device through natural-language tasks. It is suited for supervised phone automation, screenshots, device-status checks, task-result review, and emergency aborts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact actions on a connected phone, including sending messages, making purchases, changing settings, deleting data, and running multi-step automation.

Mitigation: Require explicit user approval before messaging, purchases, data deletion, or critical settings changes; supervise the phone session and use abort_task if behavior diverges.

Risk: The provided security evidence says the release depends on unaudited local server code and a mutable hosted browser page for device actions.

Mitigation: Install only when the MCP server source and hosted Mobile AI Agent page are trusted, and stop the local relay when the session is finished.

## Reference(s):

- [Mobile AI Agent page](https://mobile-ai-use.xyz/mobileAi)
- [ClawHub mobile-agent release page](https://clawhub.ai/mobileaiuse/skills/mobile-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also direct MCP tool calls that return screenshots, device status, task results, or task-abort outcomes.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
