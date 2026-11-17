## Description:

Tracks updates to Chinese national GB/GB/T standards for a selected ICS category, compares them with local records, reports new, removed, or status-changed standards, and can download newly available PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sereinone](https://clawhub.ai/user/sereinone)

### License/Terms of Use:

MIT-0

## Use Case:

Standards, compliance, and engineering teams use this skill to monitor a chosen ICS category for national standard changes and review generated JSON reports. Agents can also help run the bundled Python script and, with user approval, download newly available standard PDFs into a selected work directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts openstd.samr.gov.cn and writes JSON reports and optional PDF files to a user-selected directory.

Mitigation: Review the target directory before running the script or downloads, and only install if outbound access to openstd.samr.gov.cn and local file creation are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sereinone/skills/national-standard-monitor-skill)
- [Publisher Profile](https://clawhub.ai/user/sereinone)
- [National Public Service Platform for Standards Information](https://openstd.samr.gov.cn/bzgk/gb)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes standards_metadata.json, latest_check.json, update_report.json, and optional PDF files in the user-selected directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
