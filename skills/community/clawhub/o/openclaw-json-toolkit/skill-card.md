## Description:

OpenClaw JSON Toolkit helps agents format, validate, diff, query, transform, and generate schemas for JSON through a hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yedanyagamiai-cmd](https://clawhub.ai/user/yedanyagamiai-cmd)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to process JSON payloads, debug syntax errors, compare configuration changes, extract nested values, transform structures, and generate draft-07 JSON Schema from examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted JSON is processed by a hosted remote MCP service, and the package evidence cannot verify its privacy assurances.

Mitigation: Use only data that is acceptable to send to the hosted service; redact secrets, personal data, customer data, and internal configuration before use.

Risk: Production secrets, regulated data, or proprietary API responses may require stronger control than this hosted service provides.

Mitigation: Prefer a local or self-hosted JSON tool for those data classes.

Risk: Large payloads and non-JSON formats are outside the skill's stated operating bounds.

Mitigation: Split large JSON into smaller chunks and decode binary formats to JSON before processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yedanyagamiai-cmd/skills/openclaw-json-toolkit)
- [OpenClaw Homepage](https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers)
- [JSON Toolkit MCP Endpoint](https://json-toolkit-mcp.yagami8095.workers.dev/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, code, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hosted MCP calls return bounded JSON or text results; users should redact sensitive content before use.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
