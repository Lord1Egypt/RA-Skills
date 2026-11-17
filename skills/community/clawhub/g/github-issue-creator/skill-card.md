## Description:

Convert raw notes, error logs, voice dictation, or screenshots into crisp GitHub-flavored markdown issue reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegovind](https://clawhub.ai/user/thegovind)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to turn informal bug reports, logs, voice notes, screenshots, or GIF references into structured GitHub-style issue reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated issue reports can contain sensitive user, project, or environment details from the original bug report.

Mitigation: Review the issue text before publishing and replace sensitive values with placeholders such as [PROJECT_NAME] or [USER_ID].

Risk: The skill writes generated reports into an /issues/ directory in the repository.

Mitigation: Confirm the target repository, generated filename, and issue content before relying on the file in a workflow with stricter path controls.

Risk: Inferred environment, reproduction, or severity details may be incomplete or incorrect when the source report is informal.

Mitigation: Verify environment fields, reproduction steps, and severity classification before submitting the issue.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [GitHub-flavored Markdown issue report saved as a dated file under /issues/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the naming convention YYYY-MM-DD-short-description.md and may include inline references to attached images or GIFs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
