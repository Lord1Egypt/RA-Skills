## Description: <br>
AI HR Copilot for Southeast Asia that works with the HalaOS MCP Server for live employee, attendance, leave, payroll, compliance, and org intelligence data, or standalone with built-in PH/SG/LK labor law knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonypk](https://clawhub.ai/user/tonypk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams, managers, and authorized employees use this skill to ask HR questions, review live HalaOS data, manage leave and attendance workflows, inspect payroll and compliance information, and generate HR documents through conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose or change sensitive employee, payroll, leave, attendance, and workforce-risk data from broad natural-language prompts. <br>
Mitigation: Install only for authorized HR users, use the narrowest HalaOS API key available, and avoid admin credentials for routine questions. <br>
Risk: Payroll runs, approvals, attendance changes, government-form generation, flight-risk reviews, and org-wide employee access can have operational or privacy impact. <br>
Mitigation: Require explicit confirmation before executing high-impact actions or retrieving organization-wide sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonypk/halaos-hr-copilot) <br>
- [HalaOS website](https://halaos.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown with tables, summaries, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured HalaOS MCP tools or use standalone labor-law knowledge depending on available credentials and configuration.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
