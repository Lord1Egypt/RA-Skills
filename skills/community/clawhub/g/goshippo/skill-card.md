## Description: <br>
A shipping and logistics skill for Shippo that helps agents get multi-carrier rates, buy domestic and international labels with customs, validate addresses, track packages, run bulk CSV batches, and provide shipping-cost and integration guidance through Shippo's hosted OAuth MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shippo](https://clawhub.ai/user/shippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, shipping operations teams, and agents use this skill to integrate Shippo shipping workflows, compare carrier rates, purchase labels with explicit approval, handle customs details, track packages, and analyze shipping activity. It is intended for users who want an agent to operate on an authorized Shippo account through hosted OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that charge the authorized Shippo account, including label and batch purchases. <br>
Mitigation: Require explicit user approval before purchases and show carrier, service, cost, ETA, origin, and destination before proceeding. <br>
Risk: The skill operates through a per-user OAuth session with access to live shipping account data and actions. <br>
Mitigation: Install only for users who want an agent to operate on their Shippo account, and re-authorize OAuth only through Shippo when needed. <br>
Risk: Refunds, manifests, webhook or account changes, deletes, and direct REST fallback can affect account state or integrations. <br>
Mitigation: Gate those operations behind explicit approval and review the proposed account change before execution. <br>
Risk: Local shipping analysis reports or support-ticket drafts may contain sensitive shipping, billing, or customer data. <br>
Mitigation: Choose the output location deliberately and minimize personally identifiable information, especially names and street-level address fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shippo/goshippo) <br>
- [Publisher profile](https://clawhub.ai/user/shippo) <br>
- [Homepage](https://github.com/goshippo/ai) <br>
- [Shippo MCP server](https://mcp.shippo.com) <br>
- [API Concepts](https://docs.goshippo.com/docs/api_concepts/apiversioning) <br>
- [Address Validation Guide](https://docs.goshippo.com/docs/addresses/address_validation) <br>
- [Customs Reference](https://docs.goshippo.com/docs/exporting/internationalshipments) <br>
- [Carrier Accounts](https://docs.goshippo.com/docs/shipping/carrieraccounts) <br>
- [Webhooks](https://docs.goshippo.com/docs/tracking/webhooks) <br>
- [Carrier Guide](references/carrier-guide.md) <br>
- [CSV Batch Format Specification](references/csv-format.md) <br>
- [Customs Declaration Guide](references/customs-guide.md) <br>
- [Shippo MCP Tool Reference](references/tool-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown, JSON snippets, configuration blocks, code examples, and structured shipping summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include carrier rate tables, label or tracking URLs, CSV validation summaries, customs checklists, support-ticket drafts, and integration guidance.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
