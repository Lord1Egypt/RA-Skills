## Description:

Google Analytics API integration with managed OAuth for managing accounts, properties, and data streams through the Admin API and running reports through the Data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rich-song](https://clawhub.ai/user/rich-song)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure Google Analytics OAuth connections, inspect GA4 account and property structure, and run analytics reports from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Analytics requests are routed through Maton's gateway and require access through MATON_API_KEY.

Mitigation: Install only when that routing is acceptable, protect MATON_API_KEY as a secret, and use a least-privilege Google account where possible.

Risk: Admin API create, update, patch, or delete operations can modify production analytics properties.

Mitigation: Manually confirm mutating Admin API requests before running them against production properties.

Risk: When multiple Google Analytics connections exist, omitted connection selection may use the default active connection.

Mitigation: Specify the intended connection with the Maton-Connection header for sensitive or multi-account workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rich-song/skills/google-analytics-api)
- [Publisher profile](https://clawhub.ai/user/rich-song)
- [Google Analytics Admin API Overview](https://developers.google.com/analytics/devguides/config/admin/v1)
- [Google Analytics Data API Overview](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [Google Analytics Data API Run Report](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport)
- [Maton](https://maton.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, HTTP examples, and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces API request guidance that requires network access, MATON_API_KEY, and valid Google Analytics OAuth connections.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
