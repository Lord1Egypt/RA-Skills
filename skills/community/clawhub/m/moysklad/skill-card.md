## Description:

МойСклад ERP helps agents work with products, counterparties, customer orders, warehouses, stock reports, invoices, and related records through the MoySklad JSON API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monsterdeveloper](https://clawhub.ai/user/monsterdeveloper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to read MoySklad ERP data, create or update business records, and produce stock or sales-oriented reports through REST API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generic API command can send ERP credentials to a user-supplied full URL.

Mitigation: Use a scoped bearer token, prefer documented relative paths against the official MoySklad API, and fix or review the helper before using it with real business data.

Risk: Some commands can create, update, or delete business records.

Mitigation: Review generated commands and request bodies before execution, and validate changes with least-privilege credentials or a test account where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monsterdeveloper/skills/moysklad)
- [MoySklad API overview](references/api-overview.md)
- [MoySklad entities reference](references/entities.md)
- [MoySklad API code examples](references/examples.md)
- [MoySklad JSON API 1.2](https://api.moysklad.ru/api/remap/1.2)
- [MoySklad API error reference](https://dev.moysklad.ru/doc/api/remap/1.2/#error_1002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript snippets, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke MoySklad API operations that read or mutate business records when credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
