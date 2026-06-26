## Description: <br>
AI-powered HR Operating System for Southeast Asia. Full payroll with PH/SG/LK compliance, 9 AI agents (payroll specialist, compliance officer, leave advisor...), attendance with GPS geofencing, leave/OT/expense workflows, org intelligence with flight risk & burnout detection. Zero-setup via OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonypk](https://clawhub.ai/user/tonypk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams, managers, and employees use this skill to answer Southeast Asia HR compliance questions, manage local HR records, generate HR documents, calculate payroll contributions, and connect to HalaOS cloud APIs for employee, attendance, leave, payroll, approval, and analytics workflows. <br>

### Deployment Geography for Use: <br>
Southeast Asia (Philippines, Singapore, and Sri Lanka) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive employee, attendance, payroll, and HR analytics data when connected to HalaOS. <br>
Mitigation: Use a least-privilege or read-only HalaOS API key where possible, test first with non-production data, and store local HR records only in approved secured systems. <br>
Risk: Payroll, approvals, attendance changes, government filings, and employee-impacting analytics can materially affect employees. <br>
Mitigation: Require explicit human review and approval before acting on payroll, approvals, attendance updates, government filings, or flight-risk and burnout-risk analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonypk/halaos-hr) <br>
- [HalaOS website](https://halaos.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, API calls, guidance] <br>
**Output Format:** [Markdown responses with tables, JSON examples, configuration paths, and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HALAOS_API_KEY for cloud access and ~/.openclaw/skills/halaos-hr/config.json for local skill configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
