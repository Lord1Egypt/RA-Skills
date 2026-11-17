## Description:

Kindle Claude Monitor helps developers turn a Kindle, phone, tablet, or spare display into a Claude Code status monitor for session state and confirmation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heavenchenggong](https://clawhub.ai/user/heavenchenggong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code on macOS use this skill to set up a local status dashboard on a Kindle, phone, tablet, or spare display. The monitor helps them notice when sessions are thinking, running tools, waiting for confirmation, or done.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The monitor exposes unauthenticated Claude activity data and state controls on the local network.

Mitigation: Use it only on a trusted LAN, avoid router port forwarding, and consider adding authentication or binding the event receiver to localhost.

Risk: The skill installs persistent Claude Code hooks and a launchd service.

Mitigation: Review the hook changes before installing and remove the hooks and service when the monitor is no longer needed.

Risk: The runtime can retain hook event history in ~/.claude/kindle-monitor/events.jsonl.

Mitigation: Delete the event log after uninstalling if hook history should not be retained.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heavenchenggong/skills/kindle-claude-monitor)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local monitor URLs and macOS setup steps.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
