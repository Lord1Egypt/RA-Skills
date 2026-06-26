## Description: <br>
Captures learnings, errors, corrections, and feature requests so agents can preserve useful session knowledge and promote broadly applicable lessons into project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IngJoseMendez](https://clawhub.ai/user/IngJoseMendez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, and feature requests as markdown learning records. They can review those records and promote durable lessons to project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session learnings may preserve sensitive details from private code, customer data, secrets, or proprietary plans. <br>
Mitigation: Keep .learnings local or gitignored by default and redact sensitive details before saving or sharing entries. <br>
Risk: Incorrect or overly broad lessons can spread into future agent context if promoted without review. <br>
Mitigation: Require human review before promoting any learning into agent prompt files or sharing it across sessions. <br>
Risk: Always-on hooks can inject reminders into more sessions than intended. <br>
Mitigation: Use hooks only as explicit opt-in configuration and avoid global always-on hooks unless the workspace owner has approved them. <br>


## Reference(s): <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Entry Examples](artifact/references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/IngJoseMendez/jose-self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional hook reminder text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates .learnings markdown entries and can emit lightweight reminders when opt-in hooks are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
