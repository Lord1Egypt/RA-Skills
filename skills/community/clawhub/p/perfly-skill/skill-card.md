## Description:

Summarize local coding work and submit selected worklog items to Perfly through the hosted Agent Sync MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levi840714](https://clawhub.ai/user/levi840714)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Perfly to turn approved local coding metadata into concise worklog items and submit selected items to Perfly through MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Worklog metadata such as branch names, issue keys, or commit titles can reveal sensitive project information.

Mitigation: Review the preview before submission and omit confidential identifiers or summarize them at a higher level.

Risk: Fallback bearer token setup can expose credentials if tokens are pasted into chat or logs.

Mitigation: Prefer MCP OAuth discovery and configure fallback ingestion tokens only in the MCP client or Perfly setup flow.

## Reference(s):

- [Perfly ClawHub package](https://clawhub.ai/levi840714/skills/perfly-skill)
- [Perfly homepage](https://perfly.dev)
- [Hosted Perfly MCP endpoint](https://api.perfly.dev/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration]

**Output Format:** [Concise Markdown summaries and MCP tool calls containing worklog metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview before write, user confirmation by default, and metadata-only evidence references.]

## Skill Version(s):

1.0.1 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
