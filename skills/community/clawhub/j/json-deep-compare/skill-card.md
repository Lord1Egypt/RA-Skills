## Description:

Compares two JSON files deeply, supports unordered list matching and ignored fields, and produces a structured Excel difference report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanw2039](https://clawhub.ai/user/hanw2039)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to compare expected and actual JSON payloads, configuration files, or migration outputs and review differences in an Excel report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Excel reports from untrusted JSON may carry spreadsheet-related risk.

Mitigation: Do not open generated reports from untrusted JSON in a spreadsheet app unless formula-like values have been neutralized.

Risk: Installing dependencies from an untrusted source may introduce package supply-chain risk.

Mitigation: Install only from a trusted Python package index and consider pinning openpyxl.

Risk: The generated .xlsx output path could overwrite an important existing file.

Mitigation: Choose output paths deliberately and avoid overwriting important .xlsx files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanw2039/skills/json-deep-compare)
- [Publisher profile](https://clawhub.ai/user/hanw2039)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate an .xlsx comparison report when the provided code is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
