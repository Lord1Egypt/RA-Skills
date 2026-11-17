## Description:

Extracts SQL scripts from Kettle .kjb and .ktr ETL jobs, with support for batch extraction, SQL component merging, and simple SQL-file output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjunhan633-glitch](https://clawhub.ai/user/chenjunhan633-glitch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to extract, inspect, merge, and archive SQL embedded in Kettle ETL job and transformation files without modifying the SQL content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated executable SQL can change database state if run without review.

Mitigation: Review extracted and generated SQL before database execution, and test against non-production data first.

Risk: Cleanup commands and broad output directories can remove or overwrite unintended files.

Mitigation: Use an explicit output directory, inspect cleanup candidates, and avoid running cleanup from a repository root, home directory, or shared workspace.

Risk: HTML reports and parsed Kettle content may be unsafe when inputs come from untrusted sources.

Mitigation: Treat generated reports as untrusted, process external Kettle files in an isolated workspace, and use reviewed, pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjunhan633-glitch/skills/kettle-sql-extractor)
- [ClawHub homepage metadata](https://clawhub.com/skills/kettle-sql-extractor)
- [README](artifact/README.md)
- [Quick start guide](artifact/docs/QUICK_START.md)
- [Merge SQL quickstart](artifact/docs/MERGE_SQL_QUICKSTART.md)
- [Batch extract quickstart](artifact/docs/BATCH_EXTRACT_QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash and Python commands; generated artifacts may include SQL, JSON, text, and HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce simple SQL-only output or fuller batch analysis reports depending on selected command options.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
