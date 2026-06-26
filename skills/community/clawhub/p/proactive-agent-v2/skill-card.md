## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eathon](https://clawhub.ai/user/eathon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an AI agent for proactive planning, persistent memory, self-improvement routines, security checks, and user onboarding. It provides operating rules, reference files, and audit guidance for agents that monitor context and propose useful work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables a persistent proactive agent with broad memory, monitoring, cleanup, self-editing, and delegation authority without enough user control. <br>
Mitigation: Install only when a persistent proactive agent is intended, and require explicit approval before enabling email or calendar access, browser or app cleanup, file deletion, spawned agents, autonomous cron work, or edits to core agent files. <br>
Risk: The skill stores and updates personal context in memory and profile files. <br>
Mitigation: Define what personal data may be stored, how long it is retained, and how the user can review, correct, or delete it. <br>
Risk: Autonomous routines and self-improvement behavior can change agent behavior over time. <br>
Mitigation: Keep self-improvement changes reviewable, scan skill and configuration changes before deployment, and require approval for security-related changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/eathon/proactive-agent-v2) <br>
- [Publisher profile](https://clawhub.ai/user/eathon) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Creator profile](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with reference files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent operating guidance, starter memory files, onboarding prompts, heartbeat checklists, and a local security-audit script.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
