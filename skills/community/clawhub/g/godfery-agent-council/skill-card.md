## Description:

Creates and manages autonomous AI agents with workspaces and memory, plus Discord channel setup and organization for OpenClaw integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create OpenClaw agents, bind them to Discord channels, and maintain channel configuration and workspace references for multi-agent systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change Discord, OpenClaw, and workspace state by creating or renaming channels, updating gateway configuration, and generating agent files.

Mitigation: Review generated commands and configuration patches before running them; use least-privilege Discord bot credentials and keep the target workspace narrow and under version control.

Risk: Optional memory cron jobs can create persistent autonomous file writes.

Mitigation: Enable memory cron only for agents that need scheduled updates, set an explicit time zone, and periodically audit the generated cron jobs and memory files.

Risk: Channel names, context text, and system prompts flow into configuration.

Mitigation: Avoid untrusted inputs for channel names, context, and prompts; inspect generated prompts before applying gateway changes.

## Reference(s):

- [Complete setup guide](https://skillboss.co/skill.md)
- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/godfery-agent-council)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration patches, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenClaw gateway configuration, Discord channels, workspace Markdown files, and optional cron jobs when commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
