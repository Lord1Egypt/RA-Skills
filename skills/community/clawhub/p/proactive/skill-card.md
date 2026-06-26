## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makaronz](https://clawhub.ai/user/makaronz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add proactive behavior, persistent memory practices, heartbeat checks, self-healing routines, and verification habits to an AI agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad proactive authority and persistent memory without enough consent, scoping, or safety controls. <br>
Mitigation: Make memory logging opt-in, keep memory files private and out of shared repositories, and require explicit user approval before external actions or destructive cleanup. <br>
Risk: Autonomous crons, sub-agents, and credential-adjacent integrations can act beyond the user's immediate attention if configured too broadly. <br>
Mitigation: Disable autonomous crons and sub-agents unless intentionally configured, and grant email, calendar, or credential-adjacent access only with narrow account and action limits. <br>


## Reference(s): <br>
- [Proactive on ClawHub](https://clawhub.ai/makaronz/proactive) <br>
- [makaronz Publisher Profile](https://clawhub.ai/user/makaronz) <br>
- [Onboarding Flow](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional workspace files and scripts for onboarding, memory, heartbeat checks, and security auditing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports proactive-agent 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
