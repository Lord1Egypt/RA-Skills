## Description:

Run data quality checks on PMU (Phasor Measurement Unit) data, including frequency, voltage magnitude, phasor angles, missing values, and timestamp continuity against configurable limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clayutk](https://clawhub.ai/user/clayutk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate PMU CSV measurements, identify out-of-range electrical values, detect missing data or timestamp gaps, and review flagged rows for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads PMU CSV files and writes derived report files, so outputs may contain sensitive or operationally relevant source data.

Mitigation: Run it only on trusted input files and output directories, handle generated CSV and HTML reports with the same care as the source data, and review reports before opening them in spreadsheet tools.

Risk: Running file-processing scripts with elevated privileges can expand the impact of ordinary file-output mistakes.

Mitigation: Run the checker as a normal user in a controlled working directory and avoid elevated privileges.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; stdout summary reports, flagged-row CSV files, and optional HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local CSV input and optional JSON limits configuration; writes flagged-row output beside the input file or into a requested output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
