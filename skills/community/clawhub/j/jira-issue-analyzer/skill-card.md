## Description:

Jira Issue Analyzer fetches Jira issue details and attachments, delegates evidence-based log analysis, and produces a local Markdown issue analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimos92](https://clawhub.ai/user/dimos92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to gather Jira issue context, download related attachments, analyze logs and reproduction evidence, and generate a structured Markdown report for triage or root-cause review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira credentials could be exposed or misused if broad tokens or insecure Jira hosts are configured.

Mitigation: Use HTTPS Jira endpoints and a narrowly scoped read-only token stored outside shared project files.

Risk: Downloaded attachments or report paths could overwrite local files or introduce untrusted content into analysis.

Mitigation: Review destination paths before download or cleanup, and inspect attachments from untrusted issues before opening or processing them.

## Reference(s):

- [Jira Issue Analyzer README](README.md)
- [Jira Issue Fetcher README](jira/README.md)
- [Report Template](report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/dimos92/skills/jira-issue-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON issue data, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Markdown reports to a local project directory and may download Jira attachments to a local temporary directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
