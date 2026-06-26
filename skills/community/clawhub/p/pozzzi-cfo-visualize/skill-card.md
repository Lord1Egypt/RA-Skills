## Description: <br>
噗滋（pozzzi）报表官 - 图表代码生成工具。接收 pozzzi-cfo-analyze 返回的 viz_specs，生成目标工具（Excel/WPS/钉钉/腾讯文档）的图表代码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Spreadsheet and reporting users use this skill to turn analyzed dataset visualization specs into chart-generation code for Excel, WPS, DingTalk, or Tencent Docs. It supports common chart types for dashboards, comparisons, trends, pivots, and funnel-style reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated VBA, Office Script, WPS JSAPI, DingTalk macro, or Tencent Docs script output is executable code that may alter spreadsheets or produce incorrect charts. <br>
Mitigation: Review generated code before running it, test on a copy of the spreadsheet when possible, and avoid using it in sensitive or production files unless the changes are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/pozzzi-cfo-visualize) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, guidance] <br>
**Output Format:** [Markdown with spreadsheet automation code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates target-tool chart code for Excel, WPS, DingTalk, or Tencent Docs; output should be reviewed and tested before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
