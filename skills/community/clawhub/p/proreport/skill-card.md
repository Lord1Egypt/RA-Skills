## Description: <br>
量化策略评估报告生成器，读取 Excel 净值数据，计算量化指标并生成图表、分析文字、PDF 和 Word 策略评估报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duanwei2028](https://clawhub.ai/user/duanwei2028) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agents supporting investment research use this skill to turn uploaded Excel net-value data into quantitative metrics, charts, AI-written commentary, and PDF/DOCX strategy reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided Excel performance data and generated JSON, charts, PDF, and DOCX files may contain sensitive financial information. <br>
Mitigation: Run the skill in a dedicated project or virtual environment, place only intended Excel files in the data folder, choose an output directory suitable for retention or sharing, and delete generated files when they contain sensitive data. <br>
Risk: Generated strategy analysis can be misleading if source data, computed metrics, or AI-written commentary are not reviewed before use. <br>
Mitigation: Review analysis.json, content.json, charts, and final PDF/DOCX reports for data quality, calculation consistency, and appropriate financial interpretation before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duanwei2028/proreport) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Files, Guidance] <br>
**Output Format:** [Markdown instructions with bash and Python snippets, plus local JSON, PNG, PDF, and DOCX report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local Excel files and writes analysis.json, content.json, chart PNGs, and PDF/DOCX reports under the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
