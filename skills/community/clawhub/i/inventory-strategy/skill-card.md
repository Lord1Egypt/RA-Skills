## Description: <br>
零售库存健康诊断与行动策略生成，基于语义层指标完成品类四象限分类、问题商品定位和行动方案输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyujun](https://clawhub.ai/user/jackyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators, planners, and inventory analysts use this skill to diagnose inventory health from semantic-layer metrics, identify at-risk categories and brand-season combinations, and generate staged HTML reports plus an xlsx action plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries inventory, sales, stock-value, and discount metrics that may include sensitive business information. <br>
Mitigation: Install and run it only where metric-query access to those business metrics is approved. <br>
Risk: Generated HTML and spreadsheet reports may expose sensitive commercial data if shared broadly. <br>
Mitigation: Review generated report files before distributing them outside the intended business audience. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jackyujun/inventory-strategy) <br>
- [Final HTML report specification](references/report-html-spec.md) <br>
- [Step 2 output template](references/step2-output-template.html) <br>
- [Classification helper code](references/classify-code.py) <br>
- [Dynamic sensing reference](references/dynamic-sensing.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation output with generated HTML and xlsx report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires metric-query access to inventory, sales, stock-value, discount, and related semantic-layer metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
