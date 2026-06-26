## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs, maintain persistent memory, and continuously improve through onboarding, heartbeats, security checks, and recovery patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp33333333333](https://clawhub.ai/user/cp33333333333) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an agent that can preserve working context, learn user preferences, perform proactive check-ins, and apply safety routines before tool use or external actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent personal memory and broad transcript logging can store sensitive user context longer than intended. <br>
Mitigation: Limit what the agent records, review generated memory files regularly, and remove broad transcript logging unless the user explicitly wants it. <br>
Risk: Proactive autonomy and unattended background crons can trigger work without timely human review. <br>
Mitigation: Disable or restrict unattended crons by default and require human approval before enabling recurring background actions. <br>
Risk: Monitoring, browser or app cleanup, tool use, and spawned-agent behavior can change local state or expand activity beyond the current conversation. <br>
Mitigation: Gate external, destructive, cleanup, and spawned-agent actions behind explicit review and keep an auditable record of what was changed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cp33333333333/proactive-agent1) <br>
- [Publisher Profile](https://clawhub.ai/user/cp33333333333) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes starter agent memory files, onboarding templates, heartbeat routines, and a security audit script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
