## Description: <br>
Records OpenClaw tool calls before and after execution for auditing, debugging, usage statistics, and error tracking with sensitive data redaction guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add audit logging around OpenClaw tool calls so they can investigate tool usage, failures, sessions, and usage patterns. It is most relevant where tool-call logs are intentionally collected and handled as sensitive operational data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit logs can record sensitive tool inputs, outputs, session IDs, and user IDs. <br>
Mitigation: Treat audit logs as sensitive data, restrict read access, define retention and cleanup, and redact or avoid logging parameters, results, session identifiers, and user identifiers by default. <br>
Risk: Broad tool-call auditing can collect more operational data than intended. <br>
Mitigation: Install only when broad auditing is intentional, review logged fields before deployment, and keep the hook scoped to the minimum information needed for auditing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanxiao-bot/openclaw-audit-log-hook) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript, JSON, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces hook implementation guidance and log-analysis commands; it does not create log files unless the user implements the hook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
