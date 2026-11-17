## Description:

Manage Printful stores, products, variants, orders, files, webhooks, mockups, reports, and exports through the Printful REST API using a private API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to inspect and manage Printful account resources, build local integrations, and convert seller requests into safer Printful API calls. It supports read workflows, live mutations with confirmation, and product exports in markdown, CSV, or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Printful private token that may grant access to live account data and actions.

Mitigation: Use the minimum token scopes needed for the task and keep the token in PRINTFUL_API_KEY instead of saving it in files.

Risk: Order confirmation or cancellation, delete operations, webhook changes, and raw requests can affect live Printful data.

Mitigation: Review the target IDs, endpoint family, and payload before writes, and require user confirmation for live mutations.

Risk: Large or repeated account reads can expose sensitive store, order, customer, or product data in outputs.

Mitigation: Summarize account data first, keep raw JSON dumps small unless requested, and avoid storing private data in the skill package.

## Reference(s):

- [Printful API notes](references/printful-api-notes.md)
- [Printful request examples](references/request-examples.md)
- [ClawHub skill page](https://clawhub.ai/stanestane/skills/printful-management)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payload examples, and optional generated markdown, CSV, or JSON export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PRINTFUL_API_KEY for authentication and pretty-prints API responses as JSON; export-products can write markdown, CSV, or JSON files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
