## Description:

li-Record-lecture-video generates day-by-day Excel study plans from recorded course video titles and durations, with built-in and user-supplied Excel template modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and training coordinators use this skill to turn recorded-course video lists into daily study plan spreadsheets. It supports built-in templates, placeholder-based custom templates, and automatic template column detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted course data, config JSON, or Excel templates can influence workbook content, and some workbook text fields are not fully formula-sanitized.

Mitigation: Use trusted inputs and avoid untrusted guide, homework, exam, registration, learning-method, or placeholder text until sanitization is applied across all workbook text fields.

Risk: The skill writes an .xlsx workbook to disk.

Mitigation: Confirm the requested output path before execution and keep outputs outside system directories.

## Reference(s):

- [Template specification](references/template-spec.md)

## Skill Output:

**Output Type(s):** [Files, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples; generated workbook output is .xlsx]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an Excel study-plan workbook from user-provided course metadata, video titles, durations, and optional template files.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
