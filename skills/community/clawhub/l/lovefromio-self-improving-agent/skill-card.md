## Description: <br>
Captures learnings, errors, corrections, feature requests, and recurring workflow patterns so agents can record and promote durable improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to log command failures, user corrections, missing capabilities, knowledge gaps, and better approaches into structured markdown files. It also provides optional hooks and promotion workflows for turning proven learnings into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages long-lived agent memory and broad logging of conversation or error context. <br>
Mitigation: Prefer project-local setup, redact secrets and personal data before logging, and periodically review or delete .learnings and workspace memory files. <br>
Risk: Always-on hooks can add persistent reminders and capture workflow context more broadly than intended. <br>
Mitigation: Inspect scripts before enabling hooks, avoid global hooks, and use narrow hook matchers. <br>
Risk: Promoting unreviewed learnings into prompt or workspace files can preserve incorrect or sensitive guidance. <br>
Mitigation: Require explicit approval before promoting content into prompt files. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Self-Improvement Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entry formats for agent-maintained markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
