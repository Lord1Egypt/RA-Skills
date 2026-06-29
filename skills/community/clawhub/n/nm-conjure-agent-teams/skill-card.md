## Description: <br>
Coordinates Claude agent teams via filesystem protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multiple Claude Code agents for parallel implementation, code review, refactoring, and task dependency management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup or shutdown actions can remove team/task state or kill panes for the wrong team. <br>
Mitigation: Confirm the team name, pane ID, and target path before deleting teams, removing lock files, or killing panes; back up important ~/.claude team/task state first. <br>
Risk: Local coordination state can be damaged if agents write inboxes or task files without the documented locking and atomic write patterns. <br>
Mitigation: Use the documented fcntl locks and atomic file replacement patterns for task, inbox, and team config updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conjure-agent-teams) <br>
- [Conjure plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure) <br>
- [Team management module](artifact/modules/team-management.md) <br>
- [Task coordination module](artifact/modules/task-coordination.md) <br>
- [Messaging protocol module](artifact/modules/messaging-protocol.md) <br>
- [Spawning patterns module](artifact/modules/spawning-patterns.md) <br>
- [Health monitoring module](artifact/modules/health-monitoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local team coordination through Claude CLI, tmux or iTerm panes, JSON task files, inbox messages, and health monitoring.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
