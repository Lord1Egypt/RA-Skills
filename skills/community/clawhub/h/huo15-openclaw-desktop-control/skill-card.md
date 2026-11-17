## Description:

Guides an agent to use the desktop-control MCP server for macOS automation with accessibility-tree-first interaction, post-action verification, and session-state checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate macOS applications through OpenClaw's desktop-control MCP server, favoring accessibility-tree element targeting over pixel clicks and verifying each desktop action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for macOS desktop automation involving screen, accessibility, clipboard, app-control, and shell-capable MCP tools.

Mitigation: Install it only when that desktop-control capability is intended, grant macOS permissions deliberately, and review proposed actions before execution.

Risk: The included installer replaces existing copies of this skill in discovered OpenClaw workspace skill directories.

Mitigation: Review the installer before rerunning it and back up any locally customized copy of the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-desktop-control)
- [Skill homepage](https://cnb.cool/huo15/ai/huo15-skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline command examples and automation patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the desktop-control MCP server and appropriate macOS Accessibility, Screen Recording, and Automation permissions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
