## Description: <br>
基于Excel表格及指标定义，生成承运商维度的指数、行业平均数据，并支持历史趋势图展示与指标构成解析 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-vb](https://clawhub.ai/user/a-vb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Carrier operations teams use this skill to query a carrier's logistics index score for a specified date, compare it with the industry average, review ranking and warning labels, and identify the sub-metric that most affected the score. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local carrier spreadsheets and may use Jingwe portal pages to retrieve sub-metric and anomaly details. <br>
Mitigation: Use only authorized files and portal access, provide a narrow file path, verify the carrier and date before running, and trigger downloads only when anomaly details are intended. <br>
Risk: Carrier ranking, deviation labels, and operational suggestions may be misleading if the selected source data, carrier, or date is incorrect. <br>
Mitigation: Review the selected carrier, date, industry average, ranking, warning label, and largest-impact sub-metric before acting on the generated suggestions. <br>


## Reference(s): <br>
- [Jingwe Index Direction](http://jingwe.jdl.com/#/indexCenter/indexDirection) <br>
- [Jingwe Shipper Overview](http://jingwe.jdl.com/#/indexCenter/shipperOverview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Files, Guidance] <br>
**Output Format:** [Markdown with carrier metrics, trend-chart data, sub-metric analysis, operational suggestions, and optional anomaly details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local .xlsx or .csv carrier index file and authorized access to the Jingwe portal for sub-metric and anomaly-detail retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
