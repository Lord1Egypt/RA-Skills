## Description:

Provides MCP tools for listing and retrieving Chargebee subscriptions, customers, and invoices through the Pipeworx Chargebee API v2 integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Chargebee subscription, customer, and invoice records from a Pipeworx-hosted MCP gateway. It supports billing and customer-status inspection workflows that need filtered, read-only Chargebee data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive customer, invoice, address, and payment-method metadata may be exposed through tool responses.

Mitigation: Limit Chargebee credentials to the minimum read-only scopes needed, avoid unnecessary lookups, and treat returned billing data as sensitive.

Risk: Chargebee data is routed through an unverified third-party MCP gateway with limited disclosure about privacy, access controls, logging, retention, and subprocessors.

Mitigation: Confirm the gateway operator's credential handling and data-processing practices before using the skill with production data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-chargebee)
- [Pipeworx Chargebee MCP gateway](https://gateway.pipeworx.io/chargebee/mcp)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration]

**Output Format:** [MCP tool responses and JSON configuration snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Chargebee subscription, customer, and invoice lookups with optional filtering and pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
