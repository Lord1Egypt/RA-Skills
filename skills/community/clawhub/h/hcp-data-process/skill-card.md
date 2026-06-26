## Description: <br>
从 HCP 仪器结果文件中提取汇总表。适用于用户提供的 HCP 类 Excel 文件，其中第一个 sheet 或原始文本包含 Sample、QC、Standards 等 Group 分段，并希望按样例格式生成新的汇总 sheet。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cantonbio-skill](https://clawhub.ai/user/cantonbio-skill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Laboratory analysts and automation engineers use this skill to process HCP instrument result exports and generate standardized Excel summary workbooks from Group sections containing Sample, MeanResult, and CV fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing original HCP spreadsheets directly can overwrite generated output files when --overwrite is used. <br>
Mitigation: Run the skill on copies first and use --overwrite only when replacing an existing generated workbook is intended. <br>
Risk: The extraction depends on compatible HCP export structure and required Group, Sample, MeanResult, and CV fields. <br>
Mitigation: Confirm the input file follows the expected export layout and review the generated summary workbook before using it downstream. <br>
Risk: The local script requires Python dependencies such as openpyxl. <br>
Mitigation: Confirm Python and openpyxl are installed in the execution environment before processing files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes .xlsx, .xlsm, and UTF-16 tab-delimited .xls inputs; outputs _extracted.xlsx workbooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
