## Description: <br>
An OpenClaw memory system skill that organizes persistent memories into user, feedback, project, and reference categories, supports Dream Agent log consolidation, team memory sharing, auto capture, session state management, and task progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to preserve preferences, feedback, project context, references, session state, and asynchronous task progress across conversations and agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may retain private user, project, or workspace content across OpenClaw sessions. <br>
Mitigation: Review stored memories regularly, avoid storing secrets or raw credentials, and back up the ~/.openclaw workspace before installation, migration, rollback, or team synchronization. <br>
Risk: Team memory features can share selected memories between agents and workspaces. <br>
Mitigation: Share only reviewed entries, keep the built-in secret scan enabled, and run team synchronization only for intended workspaces. <br>
Risk: MiniMax integration can send log or prompt content to an external API using bundled credentials and unsafe TLS settings. <br>
Mitigation: Remove or review MiniMax scripts before use, replace bundled credentials with user-managed configuration, and re-enable TLS certificate verification. <br>
Risk: Batch installation, migration, rollback, and snapshot scripts can broadly mutate ~/.openclaw workspace files. <br>
Mitigation: Create a backup first, verify the target workspace variables, and run broad mutation commands only after reviewing their planned scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-memory-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory files, JSON indexes, configuration files, shell command output, and guidance text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent memory, index, team-memory, session-state, snapshot, and task-progress files under OpenClaw workspaces.] <br>

## Skill Version(s): <br>
3.4.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
