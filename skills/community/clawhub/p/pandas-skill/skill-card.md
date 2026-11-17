## Description:

Pandas Skill helps agents work with tabular data by providing pandas-based guidance and local scripts for data cleaning, analysis, transformation, and format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangruihan](https://clawhub.ai/user/yangruihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and data-focused agents use this skill to inspect, clean, transform, merge, and convert tabular datasets with pandas workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleaning or transformation options can produce incorrect dataset changes if applied without review.

Mitigation: Keep original datasets backed up, write cleaned or transformed data to new output files, and review results before using them downstream.

Risk: Dependency updates can change pandas or file-format behavior in production workflows.

Mitigation: Use pinned dependency versions when using the skill in production or with untrusted files.

## Reference(s):

- [Pandas Skill on ClawHub](https://clawhub.ai/yangruihan/skills/pandas-skill)
- [Common Pandas Operations](references/common_operations.md)
- [Data Cleaning Best Practices](references/data_cleaning_best_practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; scripts can also produce CSV, Excel, JSON, Parquet, HTML, and text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file reads and writes are disclosed; generated outputs should be reviewed before downstream use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
