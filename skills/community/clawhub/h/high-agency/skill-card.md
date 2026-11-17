## Description:

High Agency gives an agent always-on task coaching for initiative, self-review, troubleshooting, recovery from stalled work, and cross-session lesson reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yu-xiao-sheng](https://clawhub.ai/user/yu-xiao-sheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, researchers, and other agent users can use this skill to bias an assistant toward proactive task ownership, verification, and structured recovery during complex work sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation may affect all tasks with an always-on coaching style.

Mitigation: Review the skill before installation and enable it only in workspaces where this behavior is desired.

Risk: The artifact directs the agent to save and reuse cross-session notes such as builder-journal.md.

Mitigation: Disable persistence or require review of memory writes in sensitive projects.

Risk: Pressure-oriented rhetoric may be unsuitable for some users or teams.

Mitigation: Assess tone and user impact before enabling it in shared or production agent environments.

## Reference(s):

- [High Agency on ClawHub](https://clawhub.ai/yu-xiao-sheng/skills/high-agency)
- [OpenPUA homepage](https://openpua.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with checklists, prompts, and occasional shell-command suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to read and write persistent notes such as builder-journal.md when memory is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
