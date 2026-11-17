## Description:

Generate realistic synthetic test data - relational JSON/CSV/SQL fixtures, seed data, and QA datasets - via the MockHero MCP server or REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinosaur24](https://clawhub.ai/user/dinosaur24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to generate realistic synthetic users, orders, invoices, fixtures, seed data, and multi-table QA datasets with valid foreign keys. It is useful when an agent needs JSON, CSV, or SQL test data without hand-writing fixtures or faker scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local stdio MCP server is run through an npm package.

Mitigation: Prefer the remote MCP endpoint unless local stdio is required; if local stdio is used, pin and review the npm package version before running it.

Risk: API keys can be exposed through headers, MCP arguments, or environment variables.

Mitigation: Provide only the needed MockHero API key, store it securely, and avoid exposing unrelated credentials in the agent environment.

Risk: The service creates synthetic data and does not provide de-identification guarantees for real production data.

Mitigation: Do not send real production data for anonymization or masking; use it only to create synthetic fixtures, seed data, and QA datasets.

Risk: Large generation jobs can incur metered usage costs.

Mitigation: Estimate usage before generating and use the free preview for small jobs when it fits the documented limits.

## Reference(s):

- [MockHero homepage](https://mockhero.dev)
- [MockHero remote MCP endpoint](https://mockhero.dev/mcp/agent)
- [Mockhero ClawHub skill page](https://clawhub.ai/dinosaur24/skills/mockhero)
- [dinosaur24 publisher profile](https://clawhub.ai/user/dinosaur24)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, API paths, MCP tool names, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents toward synthetic data generation through MockHero MCP or REST workflows; generated datasets may be JSON, CSV, or SQL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
