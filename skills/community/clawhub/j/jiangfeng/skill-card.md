## Description:

分析淘宝直播、超级直播和财务数据，自动识别文件、处理编码、计算投放指标，并生成报表和优化建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[18262202398-star](https://clawhub.ai/user/18262202398-star)

### License/Terms of Use:

MIT-0

## Use Case:

投放运营人员和数据分析人员可用该技能处理超级直播、淘宝直播和财务报表数据，计算 ROI、成本、转化率和收入等关键指标。该技能适合生成本地 HTML/CSV 分析报表并辅助制定投放优化建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute injected browser content when source spreadsheets or reports contain malicious or contaminated values.

Mitigation: Use trusted input files only, or update the report generator to escape dynamic values and apply a restrictive content security policy before opening generated reports.

Risk: Business and financial data is written to local report files in the configured output directory.

Mitigation: Choose a controlled output directory with appropriate access controls before processing sensitive data.

Risk: Unpinned Python dependencies may resolve to unexpected package versions.

Mitigation: Pin dependency versions in a controlled environment before using the skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18262202398-star/skills/jiangfeng)

## Skill Output:

**Output Type(s):** [text, files, guidance]

**Output Format:** [Console status text plus HTML and CSV report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local CSV/XLSX advertising, live-commerce, and finance reports from configured input directories.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
