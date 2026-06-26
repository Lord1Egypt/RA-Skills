## Description: <br>
对中国移动"灵畿"平台工单数据进行全面分析，支持时效、满意度、热点问题评估并生成专业PDF运营报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengyusheng188](https://clawhub.ai/user/chengyusheng188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and support teams use this skill to analyze LingJi Excel ticket exports, review service timeliness and satisfaction trends, identify recurring issue categories, and produce terminal or PDF reports for internal operations review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LingJi ticket exports, generated PDFs, terminal output, and temporary report files may contain personal data, ticket identifiers, company details, or incident content. <br>
Mitigation: Use only authorized exports, keep generated artifacts confidential, redact sensitive fields before sharing, and prefer approved internal channels. <br>
Risk: Reports can be incomplete or misleading if the input workbook does not match the expected LingJi ticket schema. <br>
Mitigation: Confirm the Excel field names and export format before relying on the metrics, and review the generated report before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengyusheng188/lingji-yunying-gongdan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Terminal text report or PDF report generated from an Excel workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads authorized LingJi .xlsx exports and may create a temporary HTML file during PDF generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
