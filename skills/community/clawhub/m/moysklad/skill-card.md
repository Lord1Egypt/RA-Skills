## Description: <br>
МойСклад ERP — управление товарами, контрагентами, заказами, складами, остатками и документами через REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[monsterdeveloper](https://clawhub.ai/user/monsterdeveloper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query and update MoySklad ERP data, including products, counterparties, customer orders, invoices, warehouses, stock reports, and direct API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify live ERP records and the security review flags the raw API helper as able to leak credentials or perform unsafe production changes. <br>
Mitigation: Use a least-privilege MoySklad token, avoid raw full-URL API calls, and require human review before POST, PUT, PATCH, or DELETE operations. <br>
Risk: The skill handles sensitive ERP credentials and business data. <br>
Mitigation: Store credentials only in environment variables, prefer token authentication over login/password, and limit access to accounts and data required for the task. <br>


## Reference(s): <br>
- [MoySklad API Overview](references/api-overview.md) <br>
- [MoySklad Entities](references/entities.md) <br>
- [MoySklad API Examples](references/examples.md) <br>
- [MoySklad API Documentation](https://dev.moysklad.ru/doc/api/remap/1.2/) <br>
- [ClawHub Skill Page](https://clawhub.ai/monsterdeveloper/moysklad) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, optional JSON output, and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and MoySklad credentials via MOYSKLAD_TOKEN or MOYSKLAD_LOGIN and MOYSKLAD_PASSWORD.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
