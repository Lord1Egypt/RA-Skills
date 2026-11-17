## Description:

OkraPDF lets agents upload PDFs, read extracted content, ask questions, extract structured data, and manage collections through MCP, CLI, and HTTP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steventsao](https://clawhub.ai/user/steventsao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to OkraPDF for PDF upload, extraction, question answering, structured JSON extraction, table/entity access, exports, and collection-level document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDFs, document text, questions, and extracted outputs are sent to OkraPDF.

Mitigation: Use only with documents approved for that service, and avoid confidential, regulated, or proprietary content unless the organization has approved the workflow.

Risk: The skill uses API-key authenticated MCP, CLI, and HTTP access to a remote service.

Mitigation: Prefer a pinned or project-local CLI install, use a limited API key, and store credentials through approved secret-management practices.

## Reference(s):

- [OkraPDF Documentation](https://docs.okrapdf.com)
- [OkraPDF API Reference](https://api.okrapdf.com)
- [OkraPDF MCP Endpoint](https://api.okrapdf.com/mcp)
- [OkraPDF SDK](https://github.com/okrapdf/sdk)
- [ClawHub Skill Page](https://clawhub.ai/steventsao/skills/okra)
- [Publisher Profile](https://clawhub.ai/user/steventsao)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls]

**Output Format:** [Markdown with inline JSON, bash, TypeScript, MCP, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for PDF upload, status polling, reading content, question answering, structured extraction, collections, exports, and scripting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
