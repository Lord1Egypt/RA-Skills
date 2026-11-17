## Description:

Drafts Midea Group-style internal communications, including weekly or monthly reports, project updates, incident reports, cross-department emails, FAQ answers, newsletters, and general internal messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and internal communications teams use this skill to draft concise, structured Midea Group-style internal documents from provided context or approved enterprise sources. It routes common communication requests to templates for reports, newsletters, project updates, incidents, cross-department coordination, FAQs, and general messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to search company email, chat, calendars, and documents broadly when drafting newsletters, FAQs, or weekly reports.

Mitigation: Scope enterprise searches to approved channels, folders, date ranges, and audiences before generation.

Risk: Generated internal communications may include sensitive, stale, or misleading information if source context is not reviewed.

Mitigation: Require human review, redaction, and source validation before sharing generated output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/internal-comms-midea)
- [3P weekly report template](artifact/examples/3p-weekly-report.md)
- [Company newsletter template](artifact/examples/company-newsletter.md)
- [Project update template](artifact/examples/project_update.md)
- [Incident report template](artifact/examples/incident_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text using the selected communication template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include structured sections, tables, placeholders for missing user-supplied details, and source links when available.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
