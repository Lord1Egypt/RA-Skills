## Description:

Nex Reports creates, schedules, and delivers automated business reports by combining data from Nex tools and configured local sources into markdown, HTML, Telegram, or JSON briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators, managers, and teams use this skill to create recurring operational briefings that combine health checks, CRM pipeline status, expenses, deliverables, domain alerts, vault alerts, email, calendar, task, and custom command results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored report configurations can invoke high-impact arbitrary shell commands through the CUSTOM module.

Mitigation: Use the CUSTOM module only for fully trusted commands, restrict who can edit ~/.nex-reports/reports.db, and run scheduled reports with minimal privileges.

Risk: Telegram deliveries and saved report files may contain sensitive business data.

Mitigation: Limit recipients and file access, and review generated report content before broad distribution.

## Reference(s):

- [Nex AI homepage](https://nex-ai.be)
- [ClawHub skill page](https://clawhub.ai/nexaiguy/skills/nex-reports)
- [ClawHub publisher profile](https://clawhub.ai/user/nexaiguy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide creation of scheduled reports and delivery to files or Telegram; generated reports may be markdown, HTML, Telegram text, or JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
