## Description:

Analyzes a numeric column in a CSV file by calculating its maximum, minimum, and average.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdmseven](https://clawhub.ai/user/fdmseven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to inspect a local CSV file and get basic descriptive statistics for one numeric column.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debug mode may print the first few rows of the CSV file.

Mitigation: Use --debug only when it is acceptable to expose sample CSV contents in terminal output.

Risk: Unpinned pandas installations can affect reproducibility over time.

Mitigation: Install the dependency in a virtual environment and pin pandas when repeatable results matter.

Risk: Non-numeric or unintended columns can produce failed or misleading analysis.

Mitigation: Run the skill only on CSV files and numeric columns that are intended for analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fdmseven/skills/mini-analysis-column)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pandas and a CSV file with a numeric target column; debug mode may print file shape and sample rows.]

## Skill Version(s):

0.1.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
