## Description:

Logs risky OpenClaw agent actions, conducts activity audits, and reviews OpenClaw configs for security risks without blocking operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n0nu](https://clawhub.ai/user/n0nu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to log risky agent actions, review recent security activity, and run OpenClaw configuration audits with recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security logs can retain sensitive command details when detailed logging is used.

Mitigation: Do not include API keys, bearer tokens, private key contents, full request bodies, or secret-bearing commands in log details; review log file permissions on shared machines.

Risk: Notifications and scheduled audits may send security summaries to external or shared channels.

Mitigation: Enable message notifications or cron-based audits only after confirming which channel receives alerts and when audits run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/n0nu/skills/n0nu-security-audit)
- [Audit Guide](references/audit-guide.md)
- [OpenClaw Config Security Reference](references/config-risks.md)
- [Dangerous Patterns Reference](references/dangerous-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Observer-only audit reports and local security logs; notification behavior depends on user configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
