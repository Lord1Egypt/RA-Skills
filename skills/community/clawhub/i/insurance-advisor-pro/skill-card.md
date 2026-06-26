## Description: <br>
健康保险顾问助手，帮助保险从业人员按标准SOP为客户进行需求分析、风险评估、保障缺口计算、平安健康险产品推荐，并生成方案建议书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[918774384lwt-pixel](https://clawhub.ai/user/918774384lwt-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance advisors use this skill to run customer KYC conversations, assess health and financial protection gaps, match Ping An health-insurance products, and prepare customer-facing insurance proposal materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects sensitive health, family, income, debt, policy, and budget details during insurance KYC. <br>
Mitigation: Use it only in approved client workflows, obtain explicit client consent first, and avoid collecting unnecessary identifiers. <br>
Risk: Generated proposal materials or Feishu documents may contain sensitive customer data. <br>
Mitigation: Create documents only in approved workspaces with reviewed sharing permissions, and store or retain outputs under organizational privacy and security rules. <br>
Risk: Insurance recommendations may be unsuitable if health disclosures, product availability, budgets, or underwriting constraints are incomplete or outdated. <br>
Mitigation: Have a qualified insurance professional review recommendations, verify current product terms, and confirm health告知 and underwriting requirements before presenting or binding coverage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/918774384lwt-pixel/insurance-advisor-pro) <br>
- [Insurance advisor SOP guide](references/sop-guide.md) <br>
- [Ping An product catalog](assets/pingan_products.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Conversational guidance, Markdown proposal content, JSON inputs, Python helper commands, and generated PDF report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create customer insurance proposal documents or PDF reports after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
