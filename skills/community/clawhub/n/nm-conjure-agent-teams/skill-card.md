## Description: <br>
Coordinates Claude agent teams via filesystem protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multiple Claude CLI agents across parallel implementation, review, refactoring, testing, and task handoff workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates multiple local Claude agents through ~/.claude files and terminal panes. <br>
Mitigation: Install it only in workspaces where local multi-agent coordination is intended, and review generated team/task files before relying on them for critical work. <br>
Risk: Automated health recovery can release stalled agents' tasks and restart or replace panes. <br>
Mitigation: Review health-monitoring behavior before enabling automated recovery, and require human approval for high-risk or critical task recovery. <br>
Risk: Team and task cleanup behavior can delete local coordination records. <br>
Mitigation: Confirm shutdown and deletion steps before purging team/task directories, especially when records are needed for audit or recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conjure-agent-teams) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure) <br>
- [Agent Teams skill definition](artifact/SKILL.md) <br>
- [Team management module](artifact/modules/team-management.md) <br>
- [Messaging protocol module](artifact/modules/messaging-protocol.md) <br>
- [Task coordination module](artifact/modules/task-coordination.md) <br>
- [Spawning patterns module](artifact/modules/spawning-patterns.md) <br>
- [Crew roles module](artifact/modules/crew-roles.md) <br>
- [Health monitoring module](artifact/modules/health-monitoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers local team and task files, tmux or terminal panes, message inboxes, and role-aware task coordination.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
