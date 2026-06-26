## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs, preserve working context, and continuously improve with memory, heartbeat, onboarding, and security patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujiang817](https://clawhub.ai/user/liujiang817) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure an AI agent with proactive workflows, persistent memory files, onboarding, heartbeat checks, self-improvement routines, and security guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent memory and user profiling, which can accumulate sensitive personal or third-party information. <br>
Mitigation: Regularly review USER.md, MEMORY.md, SOUL.md, SESSION-STATE.md, daily notes, and working-buffer files; avoid storing secrets, health, financial, regulated, or third-party personal details. <br>
Risk: Heartbeat, email/calendar monitoring, autonomous cron, isolated-agent, and automatic profiling patterns may operate without clear consent boundaries. <br>
Mitigation: Remove these behaviors or explicitly opt into each one before use, and require human approval before any external action. <br>
Risk: Broad local-environment authority, including cleanup or maintenance behavior, can affect files or application state. <br>
Mitigation: Keep deletion, app cleanup, and environment changes behind explicit confirmation and run the included security audit before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liujiang817/my-proactive-agent) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Hal 9001 profile](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with workspace file templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reusable agent memory, onboarding, heartbeat, and security-audit artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
