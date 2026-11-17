## Description:

Generates structured Chinese workplace weekly reports from user-provided work notes and outputs them as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoheizp](https://clawhub.ai/user/xiaoheizp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, team leads, freelancers, and students can use this skill to turn short work notes into a structured weekly status report for workplace or project reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates functionality by advertising monthly reports, Word/PPT output, charts, and file-output options that the current code does not implement.

Mitigation: Treat the current release as a basic Markdown weekly-report generator and verify advertised features before relying on them.

Risk: The package may install Pandoc even though the current code does not use it.

Mitigation: Review the Pandoc dependency before installation and omit it where the deployment only needs Markdown text output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoheizp/skills/ke-weekly-report)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The current code emits a basic weekly report; server security evidence notes that advertised Word/PPT, monthly, chart, and file-output features are not implemented.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
