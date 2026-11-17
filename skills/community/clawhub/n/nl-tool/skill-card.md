## Description:

Number lines of text files, showing line numbers alongside content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to number text files for code review, document reference, indexing, and log analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script has an undisclosed no-argument mode that can read a file path from stdin instead of numbering stdin text.

Mitigation: Review before installing, use only explicit intended filenames, and fix or document the no-argument behavior before relying on stdin workflows.

Risk: Advertised command options may not match the bundled script behavior.

Mitigation: Verify option support before operational use and update the script or documentation so expected line-numbering modes are accurate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/nl-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with line numbers and concise markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script emits a single numbered text stream.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
