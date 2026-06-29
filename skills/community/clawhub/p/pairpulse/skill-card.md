## Description: <br>
购物篮关联分析工具，输入 Excel 订单数据，输出 Apriori 商品关联规则、结构化 JSON 和业务策略建议，并支持本地运行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucetam-sino](https://clawhub.ai/user/brucetam-sino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and operations teams use this skill to run local market-basket analysis on order spreadsheets and turn association rules into recommendations, bundles, merchandising ideas, and customer-segment insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install or upgrade the external PyPI package named pairpulse. <br>
Mitigation: Confirm that the package source and version are trusted before running pip install or pip install --upgrade. <br>
Risk: Input spreadsheets may contain customer IDs, order history, or other business-sensitive data. <br>
Mitigation: Use only spreadsheets intended for local analysis and follow the organization's data handling rules before running the commands. <br>
Risk: Association rules and strategy suggestions can be misleading when input columns, product names, or customer segments are incomplete or incorrectly standardized. <br>
Mitigation: Review the generated JSON, reports, charts, and recommendations before using them for business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucetam-sino/pairpulse) <br>
- [PairPulse project link](https://github.com/brucetam-sino/PairPulse) <br>
- [PairPulse PyPI package](https://pypi.org/project/pairpulse/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Analysis, Guidance, Files] <br>
**Output Format:** [Markdown instructions with bash examples; PairPulse command output can include JSON, Excel reports, and PNG charts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local commands against user-provided Excel order data; JSON output is intended for agent consumption and follow-up analysis.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
