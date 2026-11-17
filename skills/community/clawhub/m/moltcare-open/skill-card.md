## Description:

Installs and configures the MoltCare-Open framework for OpenClaw, including agent configuration templates, trigger workflows, memory templates, and token-audit automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[useens](https://clawhub.ai/user/useens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install a structured agent configuration framework with reusable behavior, memory, preference, constraint, and audit templates. It is intended for configuring agent behavior and operational workflows in a local OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent agent behavior and scheduled automation with insufficient confirmation, rollback, and safety controls.

Mitigation: Review the skill before installing, prefer the ClawHub install path, back up ~/.openclaw/workspace and the crontab, and enable the weekly audit only when recurring automation is intended.

Risk: Auto-loaded behavior and memory templates can change how the agent records preferences, constraints, and long-term memory.

Mitigation: After installation, inspect and edit AGENTS.md, SOUL.md, USER.md, and MEMORY.md so memory writes require explicit confirmation and unwanted behavioral triggers are removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/useens/skills/moltcare-open)
- [ClawHub publisher profile](https://clawhub.ai/user/useens)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local OpenClaw workspace configuration guidance and templates; installation may copy files and configure scheduled audit behavior.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
