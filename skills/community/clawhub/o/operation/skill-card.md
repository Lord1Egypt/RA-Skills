## Description:

A data analysis and operations toolkit for analyzing Excel, CSV, and TSV files, comparing columns, cleaning data, and generating reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lqiuee](https://clawhub.ai/user/lqiuee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to inspect tabular files, compare columns, clean common data issues, and produce Excel, text, or Markdown reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts may install unpinned Python packages at runtime.

Mitigation: Preinstall dependencies in a controlled environment and avoid running the scripts where pip can modify a sensitive Python installation.

Risk: Generated Excel or CSV files from untrusted input may preserve formula-like content as active spreadsheet content.

Mitigation: Treat generated spreadsheet files from untrusted datasets as potentially active content and review them before opening in spreadsheet software.

Risk: The tool reads selected local spreadsheets and writes derived reports or cleaned copies.

Mitigation: Run it only on intended files and direct outputs to a controlled location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lqiuee/skills/operation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts produce Excel, CSV, text, and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local spreadsheet or delimited text files and writes derived reports or cleaned copies.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
