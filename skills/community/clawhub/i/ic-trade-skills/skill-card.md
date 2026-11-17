## Description:

Connects local ERP inventory with the IC Trade Navigator API for real-time IC pricing, risk scores, and trade advice without exposing financial pricing data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oppstie](https://clawhub.ai/user/oppstie)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, sales, and operations users connect Claude Desktop or another MCP-compatible client to local IC inventory and a remote quote service. The skill supports single-part quotes, batch inventory quoting, and combined local stock plus market intelligence views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector handles API keys and calls a remote quote endpoint.

Mitigation: Use only a trusted HTTPS quote endpoint, scope and rotate the API key, and avoid sharing the credential outside the MCP server configuration.

Risk: Inventory files and optional customer identifiers may expose sensitive procurement context.

Mitigation: Run the connector with access only to the intended inventory file and avoid sending real customer identifiers unless they are required and approved.

Risk: Remote quote advisory text may be incorrect or unsuitable for direct procurement action.

Mitigation: Treat advisory text as untrusted market data and require human review before procurement decisions or customer-facing commitments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oppstie/skills/ic-trade-skills)
- [Publisher profile](https://clawhub.ai/user/oppstie)
- [IC Trade Navigator API endpoint](https://api.ic-navigator.com/v1/quote)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown tool responses, JSON quote data, and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include quoted price, quote action, availability, risk level, advisory language, local stock quantity, and merged recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
