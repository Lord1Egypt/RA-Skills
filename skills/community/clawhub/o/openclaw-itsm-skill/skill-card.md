## Description:

Analyzes Jiawei BlueKing ITSM ticket exports to map fields, recommend handling for new tickets, generate trend reports, identify recurring issues, and monitor SLA risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaeljochen](https://clawhub.ai/user/michaeljochen)

### License/Terms of Use:

MIT-0

## Use Case:

IT service desk, operations, and support teams use this skill to analyze exported ITSM ticket data, advise on routing and resolution for new tickets, generate daily or weekly reports, detect recurring issues, and monitor SLA risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ITSM ticket exports and generated reports may contain sensitive business data, secrets, or regulated personal data.

Mitigation: Install and use the skill only when authorized to analyze the tickets involved; minimize exported fields and redact secrets or regulated personal data where possible.

Risk: Enterprise WeChat webhooks or scheduled report sends could disclose ticket information to unintended recipients.

Mitigation: Verify webhook destinations and scheduled report recipients, and send only sanitized summaries to approved channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michaeljochen/skills/openclaw-itsm-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and structured text summaries, with optional shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ticket metrics, SLA status, handling recommendations, report content, and sanitized notification summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
