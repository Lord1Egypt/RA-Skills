## Description:

An AI-powered guide to scaffolding, configuring, debugging, and integrating MCP servers that connect agents with external tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use it to plan MCP integrations, draft server code and configuration, and troubleshoot connections across common tools. Its outputs are guidance and drafts; users review and apply setup and authorization changes themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence, but scan coverage was incomplete and did not establish whether setup guidance or referenced materials are safe.

Mitigation: Review server setup instructions and referenced materials before use, and validate them in the intended environment.

Risk: Integration examples may involve credentials and tools capable of reading or changing external systems.

Mitigation: Keep real credentials out of prompts and drafts, use least-privilege access, and require human review and approval for write operations.

## Reference(s):

- [MCP Tool Integrator on ClawHub](https://clawhub.ai/gechengling/skills/mcp-tool-integrator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Markdown with tables, code blocks, configuration examples, and diagnostic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft guidance only; does not connect to servers or execute changes.]

## Skill Version(s):

4.0.6 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
