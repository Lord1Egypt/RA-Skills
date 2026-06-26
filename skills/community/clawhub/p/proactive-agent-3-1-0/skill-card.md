## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve, including WAL Protocol, Working Buffer, Autonomous Crons, and security hardening patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlackMCVN](https://clawhub.ai/user/BlackMCVN) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure agents with persistent memory, proactive check-ins, onboarding flows, self-improvement routines, and security guardrails. It provides reusable Markdown assets, guidance, and an audit script for agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad persistent memory and proactive behavior, which can capture sensitive user context or cause actions beyond the user's immediate request. <br>
Mitigation: Install only in a trusted, dedicated workspace; regularly inspect or delete USER.md, MEMORY.md, SESSION-STATE.md, and memory logs; and require explicit confirmation before external actions. <br>
Risk: Heartbeat and cron patterns can cause repeated or autonomous agent activity if enabled without clear limits. <br>
Mitigation: Disable or manually review heartbeats and crons by default, and set explicit limits before allowing scheduled checks or autonomous agent turns. <br>
Risk: Spawned agents, web access, CLI use, and reads from email or calendar can expand the data and action surface. <br>
Mitigation: Restrict spawned agents and web or CLI use, and require confirmation before reading sensitive sources or closing, moving, deleting, sending, posting, or publishing anything. <br>


## Reference(s): <br>
- [Proactive Agent 3.1.0 ClawHub page](https://clawhub.ai/BlackMCVN/proactive-agent-3-1-0) <br>
- [Publisher profile](https://clawhub.ai/user/BlackMCVN) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Hal 9001 profile](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with workspace asset templates and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional local workspace files for memory, onboarding, heartbeat checks, identity, tool notes, and a shell security audit script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); content version 3.1.0 (source: artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
