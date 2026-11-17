## Description:

Jarvis Mission Control for OpenCLAW AIS v2.1.1 is an instruction-only skill for setting up or connecting a self-hosted command center for OpenCLAW AI systems, including kanban tasks, real-time chat, OpenClaw Sessions, cost metrics, Claude Code session tracking, GitHub Issues sync, webhook monitoring, CLI guidance, and agent file editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to install, configure, or connect a Mission Control dashboard for coordinating OpenCLAW agent teams. It helps users track tasks, sessions, costs, GitHub issues, webhooks, team activity, and local command-center data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linked command-center service can expose local agent and session information through a dashboard.

Mitigation: Audit the linked project before running it, review what it reads from local agent directories, and restrict dashboard access.

Risk: Setup guidance includes cloning, installing dependencies, and running a local service from an external project.

Mitigation: Review the linked source code and dependency manifest before executing install or startup commands.

Risk: Cloud connection and GitHub sync workflows can involve API keys or tokens.

Mitigation: Use environment variables or secret storage where possible, avoid placing API keys directly on command lines, and scope tokens narrowly.

Risk: Reset instructions can delete local Mission Control state.

Mitigation: Back up the .mission-control directory before running reset or cleanup commands.

Risk: Editing agent SOUL, MEMORY, or IDENTITY files can change agent behavior.

Mitigation: Review and back up agent files before edits, and treat changes as behavior-affecting configuration.

## Reference(s):

- [Setup Guide - Self-Hosted Mission Control](references/1-setup.md)
- [MissionDeck.ai Cloud Connection](references/2-missiondeck-connect.md)
- [mc CLI Reference](references/3-mc-cli.md)
- [Data Population Guide](references/4-data-population.md)
- [Security Notes](SECURITY.md)
- [ClawHub Skill Page](https://clawhub.ai/asif2bd/skills/jarvis-mission-control)
- [GitHub Self-Hosted Project](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw)
- [MissionDeck.ai Cloud](https://missiondeck.ai)
- [Live Demo](https://missiondeck.ai/mission-control/demo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, URLs, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only package; commands and configuration snippets are reference material and do not execute automatically.]

## Skill Version(s):

2.1.1 (source: server release, target metadata, SKILL.md frontmatter, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
