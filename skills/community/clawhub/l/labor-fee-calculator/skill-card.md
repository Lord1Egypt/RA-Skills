## Description: <br>
劳动法费用计算路由技能，根据用户问题自动分发到补偿金及赔偿金、加班工资、未休年休假补偿或工伤赔偿子技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, legal practitioners, HR teams, and agents use this skill to route Chinese labor-law fee questions to calculators for work injury compensation, unused annual leave pay, overtime pay, and termination-related compensation or damages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Python scripts that can read JSON payload files, write Excel files to caller-specified paths, cache policy data, and call Delilegal policy APIs with an API key. <br>
Mitigation: Run it in a dedicated sandbox or workspace, review generated file paths before execution, keep config.json protected, and avoid passing sensitive absolute-path @ files. <br>
Risk: API credentials may be sent with persistent session metadata to policy API endpoints. <br>
Mitigation: Use a scoped API key, rotate it if exposed, and do not override API endpoint environment variables unless the destination is trusted. <br>
Risk: Labor-law calculations can be affected by incomplete facts, jurisdiction-specific policy data, and changing wage or compensation standards. <br>
Mitigation: Verify input facts and cited policy data before relying on results, and treat outputs as calculation support rather than legal advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolalam/labor-fee-calculator) <br>
- [Delilegal API key portal](https://open.delilegal.com/personal/keys) <br>
- [Compensation and damages formulas](compensation-damages-calculator/references/formulas.md) <br>
- [Overtime pay formulas](overtime-pay-calculator/references/formulas.md) <br>
- [Unused annual leave formulas](unused-annual-leave-calculator/references/formulas.md) <br>
- [Unused annual leave law articles](unused-annual-leave-calculator/references/law_articles.md) <br>
- [Work injury compensation formulas](work-injury-compensation-calculator/references/formulas.md) <br>
- [Work injury retirement age reference](work-injury-compensation-calculator/references/retirement_age.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with calculation tables, legal basis notes, and optional shell commands or Excel export instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call bundled Python calculators, request policy data with an API key, and optionally write Excel files when the user asks for export.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
