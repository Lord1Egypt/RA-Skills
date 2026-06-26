## Description: <br>
工资审核助手 helps payroll, HR, and finance reviewers generate monthly payroll audit checklists and reports with cross-source validation across personnel, attendance, performance, bonus, social insurance, tax, housing, and calculation checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Payroll reviewers, HR COE teams, and finance auditors use this skill to prepare monthly payroll audit checklists and reports, identify data mismatches, and track materials needed for domestic and overseas payroll review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive payroll and employee data. <br>
Mitigation: Install only in approved payroll or HR environments, minimize employee identifiers where possible, and treat all inputs and generated reports as sensitive. <br>
Risk: Generated reports may be written to local output paths, including /tmp examples. <br>
Mitigation: Use approved storage locations for real payroll data and avoid /tmp for production payroll files. <br>
Risk: Feishu sharing can expose payroll reports to unintended recipients. <br>
Mitigation: Verify recipients before sending any payroll report or generated file. <br>
Risk: Automated audit outputs can influence payroll release decisions. <br>
Mitigation: Require human review before payroll release or any data-changing action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tuobadaidai/payroll-audit) <br>
- [README.md](README.md) <br>
- [USER-GUIDE.md](USER-GUIDE.md) <br>
- [Core payroll audit checks](rules/core-checks.md) <br>
- [Regional payroll audit rules](rules/regional-rules.md) <br>
- [Required audit materials](rules/materials-list.md) <br>
- [Cross-validation script](scripts/cross_validate.py) <br>
- [HTML report generator](scripts/generate_html_report.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit reports, HTML reports, JSON validation inputs, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local report files and Feishu-ready content; generated payroll data and reports should be treated as sensitive.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
