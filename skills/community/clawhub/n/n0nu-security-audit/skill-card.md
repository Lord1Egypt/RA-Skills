## Description: <br>
Logs risky OpenClaw agent actions, conducts activity audits, and reviews OpenClaw configs for security risks without blocking operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n0nu](https://clawhub.ai/user/n0nu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to log risky agent actions, summarize recent activity, and review OpenClaw configuration for security issues. It supports audit visibility without acting as a runtime enforcement layer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit logs can include sensitive command details, file paths, or operational context. <br>
Mitigation: Avoid logging raw secrets and review audit logs before sharing them outside trusted channels. <br>
Risk: Notification forwarding can expose security audit details to external messaging channels. <br>
Mitigation: Enable notifications only for trusted channels and keep notifications limited to the information needed for review. <br>
Risk: Running configuration audits with automatic fixes can modify local OpenClaw settings. <br>
Mitigation: Run config audits without --fix first, review findings, and apply fixes only after confirming the intended changes. <br>


## Reference(s): <br>
- [Audit Guide](references/audit-guide.md) <br>
- [Config Risks](references/config-risks.md) <br>
- [Dangerous Patterns](references/dangerous-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/n0nu/n0nu-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audit log entries and human-readable security audit summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
