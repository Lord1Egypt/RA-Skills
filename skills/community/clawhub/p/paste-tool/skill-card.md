## Description:

Merge lines from multiple files side by side to create columnar output from separate sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to combine corresponding lines from separate text files into aligned, table-like output for comparison or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads whichever files it is asked to merge and prints their combined contents.

Mitigation: Run it only on files whose contents are intended to be exposed in the resulting output.

Risk: The documented delimiter and serial merge options may not work as described in the current bundled script.

Mitigation: Validate behavior with non-sensitive sample files before relying on custom delimiters or serial merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/paste-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text columnar output with tab-delimited rows by default]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads requested input files or stdin and prints merged rows; documented delimiter and serial options may not work as described in the current bundled script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
