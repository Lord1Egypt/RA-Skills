## Description: <br>
Expert pandas skill for data manipulation, cleaning, analysis, and transformation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangruihan](https://clawhub.ai/user/yangruihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to clean, inspect, convert, merge, filter, and summarize tabular data with pandas workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleaning or conversion commands may overwrite files if the user supplies an important existing output path. <br>
Mitigation: Use explicit new output filenames and keep backups of original datasets before running file-writing commands. <br>
Risk: The skill processes user-selected local tabular data, which may contain sensitive or proprietary records. <br>
Mitigation: Run the scripts only on data the user is authorized to process and keep outputs in an appropriate local workspace. <br>
Risk: Python dependencies may affect the surrounding environment if installed globally. <br>
Mitigation: Install requirements in a virtual environment when dependency isolation is needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yangruihan/pandas-skill) <br>
- [Pandas common operations reference](references/common_operations.md) <br>
- [Data cleaning best practices](references/data_cleaning_best_practices.md) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated data/report files such as CSV, Excel, JSON, Parquet, HTML, or text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts read user-selected tabular files and write user-selected cleaned, transformed, or analysis outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
