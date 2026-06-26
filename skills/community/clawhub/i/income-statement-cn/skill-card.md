## Description: <br>
根据明细表数据自动生成规范格式的利润表，按收入和支出分类汇总并输出 Excel 工作簿。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[courage-zen](https://clawhub.ai/user/courage-zen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
财务、运营和开发人员可用此技能从含“明细”工作表的财务 Excel 文件生成标准化利润表，用于按分类 2/分类 3 汇总收入、支出并计算经营利润。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script writes to a hard-coded local /Users/zhengyong/.openclaw output path when no output path is supplied. <br>
Mitigation: Pass an explicit output path or edit the default path before running the script. <br>
Risk: Running the workbook conversion directly on financial data can overwrite or transform local outputs unexpectedly. <br>
Mitigation: Test on a copy of the spreadsheet and review the generated workbook before using it for reporting. <br>
Risk: Execution depends on the local Python environment having openpyxl installed. <br>
Mitigation: Install and verify openpyxl in the intended environment before running the generator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/courage-zen/income-statement-cn) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [generate_income_statement.py](artifact/generate_income_statement.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with Python code and local Excel workbook output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Excel workbook with a 明细 worksheet and the openpyxl Python package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
