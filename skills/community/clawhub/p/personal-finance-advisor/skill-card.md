## Description: <br>
Personal Finance Advisor helps users analyze spending, plan budgets, compare tax scenarios, plan retirement, review insurance coverage, and generate investment allocation suggestions across multiple accounts and currencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this skill to process local personal finance records and receive planning guidance for income, spending, budgets, investing, taxes, retirement, and insurance. <br>

### Deployment Geography for Use: <br>
Global; default examples and configuration are oriented to China with CNY and tax_region: cn. <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to process personal financial records that can contain sensitive account, income, spending, and tax information. <br>
Mitigation: Provide only the minimum data needed, keep imported CSV/OFX/QIF files local, and verify that sensitive fields are removed or masked before sharing outputs. <br>
Risk: Investment, tax, retirement, and insurance suggestions may be incomplete, outdated, or unsuitable for a user's jurisdiction and financial situation. <br>
Mitigation: Treat outputs as planning assistance, review assumptions and calculations, and consult qualified financial, tax, legal, or insurance professionals before acting. <br>
Risk: Imported statements may expose identifiers or detailed transaction history even when the skill has no executable code or hidden installation behavior. <br>
Mitigation: Sanitize source files before use, avoid direct bank API connections, and preserve the documented local-processing workflow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured financial analysis, recommendations, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include budget categories, financial calculations, investment allocation suggestions, tax-planning comparisons, retirement targets, insurance coverage priorities, and local-data handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
