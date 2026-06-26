## Description: <br>
从Kettle作业（.kjb/.ktr）中提取SQL脚本，支持批量提取、合并SQL组件和简洁输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjunhan633-glitch](https://clawhub.ai/user/chenjunhan633-glitch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to extract, review, merge, and batch-process SQL embedded in Kettle ETL job and transformation files. It is suited for SQL backup, migration preparation, code review, documentation, and troubleshooting workflows where the original SQL should be preserved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL and reports may contain sensitive business logic or database details. <br>
Mitigation: Run the skill in a controlled project workspace, treat generated SQL and reports as sensitive, and avoid committing reports or extracted SQL accidentally. <br>
Risk: Executable SQL generated from Kettle files may be unsafe or unsuitable for a target production database without review. <br>
Mitigation: Manually review and test generated executable SQL in a non-production database before considering production use. <br>
Risk: Broad input paths can process more Kettle files than intended. <br>
Mitigation: Point the tool at specific Kettle files or narrowly scoped directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjunhan633-glitch/kettle-sql-extractor) <br>
- [README](README.md) <br>
- [Quick Start Guide](docs/QUICK_START.md) <br>
- [Usage Examples](docs/USAGE_EXAMPLES.md) <br>
- [Merge SQL Quickstart](docs/MERGE_SQL_QUICKSTART.md) <br>
- [Batch Extract Quickstart](docs/BATCH_EXTRACT_QUICKSTART.md) <br>
- [Troubleshooting Case](docs/troubleshooting_case_kettle_extract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated artifacts may include SQL, JSON, text summaries, and HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in simple-output mode for SQL-only files or full report mode for analysis summaries and HTML reports.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
