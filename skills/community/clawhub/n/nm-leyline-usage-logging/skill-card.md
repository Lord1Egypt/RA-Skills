## Description: <br>
Implements structured usage logging and audit trails for cost and session tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to add session-aware JSONL usage logs, audit trails, cost tracking, and analytics patterns to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local usage logs and metadata may contain sensitive prompts, customer data, secrets, or regulated personal data if callers include them. <br>
Mitigation: Avoid recording sensitive metadata, review what is written under ~/.claude/leyline/usage, and delete or rotate logs when retention matters. <br>


## Reference(s): <br>
- [Leyline homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Skill page](https://clawhub.ai/athola/nm-leyline-usage-logging) <br>
- [Session Patterns](modules/session-patterns.md) <br>
- [Log Formats](modules/log-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON, Python, YAML, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local logging patterns and examples; it does not execute code by itself.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
