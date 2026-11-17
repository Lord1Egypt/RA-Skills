## Description:

Deploy a remote MCP server on Vercel with Next.js and mcp-handler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaperret](https://clawhub.ai/user/lucaperret)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, deploy, test, and publish Vercel-hosted MCP endpoints for Next.js applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated MCP tools may expose sensitive APIs or perform create, update, or delete operations without adequate review.

Mitigation: Review each generated tool before deployment, use accurate MCP safety annotations, and require authentication for sensitive APIs.

Risk: Vercel serverless constraints can break deployments that depend on files outside the configured root directory or writable local storage.

Mitigation: Keep runtime dependencies inside the deployed project root and handle filesystem writes defensively for serverless execution.

## Reference(s):

- [Project homepage](https://github.com/lucaperret/agent-skills)
- [mcp-handler](https://github.com/vercel/mcp-handler)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Vercel MCP docs](https://vercel.com/docs/mcp)
- [Smithery](https://smithery.ai)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP route examples, tool annotations, deployment checks, and publishing guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
