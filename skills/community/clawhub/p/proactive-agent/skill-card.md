## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve, with WAL, working buffer, autonomous cron, and security-hardening patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halthelobster](https://clawhub.ai/user/halthelobster) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent memory, proactive check-ins, onboarding, self-improvement routines, and security review habits to an AI agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent proactive behavior can create background work, memory retention, local cleanup, and external account activity without enough user control. <br>
Mitigation: Require explicit opt-in for heartbeats and autonomous crons, confirm each cleanup action, scope email and calendar access, and define what memory may be stored, reviewed, redacted, and deleted. <br>
Risk: The artifact includes patterns for proactive execution that could act before the user has reviewed the intended behavior. <br>
Mitigation: Constrain or remove auto-follow and delete behavior before enabling the skill, and require human approval before external sends, posts, purchases, or irreversible changes. <br>


## Reference(s): <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/halthelobster/proactive-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and reusable configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operating patterns, checklists, starter memory files, heartbeat routines, and a security audit script.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
