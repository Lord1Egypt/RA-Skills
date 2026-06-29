## Description: <br>
拼多多研究员 is a Pinduoduo-focused ecommerce research assistant that analyzes products, keywords, competitors, best sellers, shops, categories, pricing, and users, then generates an interactive HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and ecommerce analysts use this skill to research Pinduoduo products, categories, competitors, pricing, and customer signals from public web data and produce a local visual report for decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Report inputs may include sensitive proprietary data that becomes visible in the generated local HTML report. <br>
Mitigation: Use non-sensitive inputs where possible and review generated reports before sharing or publishing them. <br>
Risk: Opening the generated report may load Chart.js from a CDN. <br>
Mitigation: Open reports in an environment where loading that CDN is acceptable, or adapt the report generator to use a locally approved Chart.js copy before deployment. <br>
Risk: Market research based on public web data can be incomplete or time-sensitive. <br>
Mitigation: Treat report findings as decision support and verify key prices, sales signals, and platform metrics against current authoritative sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/pdd-researcher) <br>
- [Homepage from ClawHub metadata](https://github.com/bettermen/pdd-researcher) <br>
- [Pinduoduo platform knowledge reference](references/pdd_platform_knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown summary plus generated local HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local HTML report from JSON input and may reference public web-search data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
