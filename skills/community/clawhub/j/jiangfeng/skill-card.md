## Description: <br>
基于淘宝直播、超级直播和财务数据，自动识别广告与财务导出文件，计算关键投放指标，并生成多维分析报告和优化建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18262202398-star](https://clawhub.ai/user/18262202398-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and commerce operations users can analyze Taobao live commerce, Super Live, and finance exports for ROI, cost, conversion, refund, and margin trends. The skill helps turn local CSV or Excel exports into HTML and CSV reports for campaign review and optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes advertising and financial exports that may contain sensitive business data. <br>
Mitigation: Use a dedicated narrow input directory containing only the intended exports, and avoid pointing it at broad personal or shared folders. <br>
Risk: Generated HTML and CSV reports may persist raw or derived business records on disk. <br>
Mitigation: Write reports to a private output directory, review and redact them before sharing, and apply the same retention controls used for source exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18262202398-star/jiangfeng) <br>
- [Publisher profile](https://clawhub.ai/user/18262202398-star) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, HTML files, CSV files, guidance] <br>
**Output Format:** [Console status text plus generated HTML and CSV report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local advertising and financial data exports from a configured input directory and writes reports to a configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
