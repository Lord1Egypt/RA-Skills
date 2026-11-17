## Description:

Manage PerfexCRM records from messaging apps through API-backed CRUD operations, filtering, pagination, search, and webhook-aware workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostasmm](https://clawhub.ai/user/kostasmm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators use this skill to let agents translate natural-language requests into PerfexCRM API calls for customers, invoices, leads, tickets, projects, and related business records. It supports conversational CRM administration across messaging surfaces while encouraging pagination, field filtering, search-first retrieval, summarization, and confirmation before destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad read and write access to sensitive CRM data including customer, invoice, ticket, staff, and payment records.

Mitigation: Install it only with a PerfexCRM API key scoped to the operations the agent should perform, and avoid exposing the key in chat logs or shell history.

Risk: Delete or other high-impact CRM operations can modify business records.

Mitigation: Require explicit user confirmation before destructive or high-impact CRM changes.

## Reference(s):

- [PerfexAPI Homepage](https://perfexapi.com)
- [PerfexAPI Documentation](https://perfexapi.com/docs)
- [PerfexCRM API Webhooks Module Repository](https://github.com/sattip/perfexcrm-api-webhooks-module)
- [PerfexAPI Changelog](https://perfexapi.com/changelog)
- [PerfexAPI MCP Integration](https://perfexapi.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PERFEXCRM_API_URL and PERFEXCRM_API_KEY; examples rely on curl and the X-API-KEY header.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
