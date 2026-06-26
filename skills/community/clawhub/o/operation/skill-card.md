## Description: <br>
Provides a data analysis toolkit for Excel and CSV files, including data profiling, column comparison, data cleaning, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lqiuee](https://clawhub.ai/user/lqiuee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to inspect tabular files, compare columns, clean duplicate or missing data, and generate analysis reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill may install Python packages from the package index if dependencies are missing. <br>
Mitigation: Review the scripts and run them only in an isolated Python environment or disposable workspace. <br>
Risk: Cleaning workflows can produce transformed datasets and reports in output paths chosen at runtime. <br>
Mitigation: Confirm output paths before execution and keep original datasets backed up before using any cleaning workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lqiuee/operation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifacts may be Excel, text, Markdown, or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create analysis reports, comparison workbooks, or cleaned datasets in user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
