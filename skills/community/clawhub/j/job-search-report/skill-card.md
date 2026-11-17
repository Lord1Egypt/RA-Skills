## Description:

Generate a comprehensive job search progress report by analyzing sent applications and received replies from Gmail and producing a structured markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxty](https://clawhub.ai/user/xiaoxty)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review their job-search activity from Gmail in one structured report, including application counts, recruiter replies, status categories, action items, and weekly updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches authenticated Gmail for recent job applications and recruiter messages, which may expose sensitive personal and employment information.

Mitigation: Install and run it only when that Gmail access is intended, and review the generated report before saving or sharing it.

Risk: The optional Google Docs saving path may place job-search data into another Google service.

Mitigation: Use the Google Docs option only when the user explicitly wants the report handled through Google Docs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoxty/skills/job-search-report)
- [ClawHub publisher profile](https://clawhub.ai/user/xiaoxty)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated Gmail access through gog; optionally saves the report as a local Markdown file or Google Doc.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
