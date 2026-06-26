## Description: <br>
Guides agents through collecting, processing, verifying, and packaging Chinese macroeconomic indicators such as GDP, CPI, PPI, and output gap data from National Bureau of Statistics sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingjie-zhang-dev](https://clawhub.ai/user/yingjie-zhang-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, analysts, and developers use this skill to guide agents through collecting National Bureau of Statistics macroeconomic data, computing derived indicators, validating sources, and preparing Excel-based deliverables with data notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The main data-collection script may produce empty or mislabeled economic datasets while presenting them as collected National Bureau of Statistics data. <br>
Mitigation: Review helper scripts before use, verify generated GDP, CPI, and PPI outputs against official NBS sources, and inspect labels before relying on results. <br>
Risk: Running the link checker on untrusted workbooks can process private or internal links. <br>
Mitigation: Use the link checker only on workbooks intended for review and avoid spreadsheets that contain private or internal URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yingjie-zhang-dev/nbs-data-collection) <br>
- [Workflow reference](references/workflow.md) <br>
- [Indicator reference](references/indicators.md) <br>
- [Data source reference](references/sources.md) <br>
- [National Bureau of Statistics](https://www.stats.gov.cn) <br>
- [NBS data platform](https://data.stats.gov.cn) <br>
- [NBS data releases](https://www.stats.gov.cn/sj/zxfb/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; workflow execution may produce Excel, CSV, and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected deliverables include source links, validation notes, charted Excel sheets, checkpoints, and raw data folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
