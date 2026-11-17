## Description:

Guides agents in creating, finding, editing, formatting, exporting, and sharing Google Docs through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams can use the connector to automate document creation and editing, produce reports and templates, and manage document sharing through AgentPMT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation examples use an unpinned installer and source, so the downloaded content can change after review.

Mitigation: Use a reviewed, version-pinned installer and source revision.

Risk: Scanner coverage is partial because some local path-like references could not be resolved, leaving the review incomplete.

Mitigation: Review the unresolved references in the release and treat the security assessment as incomplete until they are understood.

## Reference(s):

- [Google Docs Connector product page](https://www.agentpmt.com/marketplace/google-docs-connector)
- [Google Docs Connector on ClawHub](https://clawhub.ai/agentpmt/skills/google-docs-connector)
- [AgentPMT account and MCP REST API setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Documents]

**Output Format:** [JSON action parameters and Google Docs content, with optional PDF, DOCX, HTML, or other supported exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AgentPMT-hosted remote tool calls and an authorized Google Docs account.]

## Skill Version(s):

1.0.3 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
