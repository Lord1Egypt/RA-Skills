## Description: <br>
NaviOffice Skill connects an agent to NaviOffice OA modules for system administration, HR, attendance, finance, CRM, sales, purchasing, inventory, projects, manufacturing, and calibration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaowb82](https://clawhub.ai/user/zhaowb82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and business operators use this skill to query and perform NaviOffice OA workflows across HR, finance, CRM, sales, purchasing, inventory, project, production, and calibration modules. It is intended for environments where the agent has a trusted, least-privilege NaviOffice API token and user confirmation for sensitive write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a NaviOffice API token to read or change sensitive business data. <br>
Mitigation: Use a least-privilege token, avoid production admin tokens, and confirm write operations involving HR, finance, sales, contracts, purchasing, inventory, or other business records before execution. <br>
Risk: The raw API path and custom API domain setting can send the API token outside the official service if misused. <br>
Mitigation: Keep the default official API domain unless the endpoint is controlled and trusted, and avoid raw commands that use full external URLs. <br>
Risk: Purchasing, sales, finance, inventory, and contract actions can create operational or commercial consequences. <br>
Mitigation: Review generated requests and require explicit human approval before creating suppliers, orders, contracts, receivables, reimbursements, stock movements, or related records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaowb82/navi-office) <br>
- [System management tools](references/system.md) <br>
- [Human resources tools](references/hr.md) <br>
- [Attendance tools](references/attendance.md) <br>
- [Finance tools](references/finance.md) <br>
- [CRM tools](references/crm.md) <br>
- [CRM API reference](references/crm-api.md) <br>
- [Sales tools](references/sales.md) <br>
- [Purchasing tools](references/purchase.md) <br>
- [Inventory tools](references/inventory.md) <br>
- [Project tools](references/project.md) <br>
- [Manufacturing tools](references/mes.md) <br>
- [Calibration tools](references/calibration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline JSON arguments, shell commands, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue authenticated NaviOffice API requests and business write operations when invoked with a valid token.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
