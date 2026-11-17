## Description:

Configure OpenClaw to use the community mistral-mcp stdio server for Mistral OCR, Codestral FIM, Voxtral audio, durable workflows, moderation, classification, files, batch, and model/voice resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swih](https://clawhub.ai/user/swih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw with Mistral-specific MCP tools for OCR, code completion, audio transcription and generation, moderation, classification, batch jobs, files, durable workflows, and live model or voice resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a community npm MCP server introduces supply-chain exposure.

Mitigation: Review or pin the mistral-mcp npm package version and avoid sudo or global installs in sensitive environments where possible.

Risk: The MCP server uses a Mistral API key and can access whatever that credential permits.

Mitigation: Provide the key through environment variables or a secret manager, and use a credential with only the access you are comfortable granting to this community server.

Risk: Batch, OCR, and transcription workflows can incur provider costs or encounter rate limits.

Mitigation: Check the current Mistral plan, pricing, and usage policies before running large or asynchronous workloads.

## Reference(s):

- [Mistral MCP GitHub repository](https://github.com/Swih/mistral-mcp)
- [ClawHub skill page](https://clawhub.ai/swih/skills/mistral-mcp-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command blocks and OpenClaw MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw CLI, Node.js, npm, mistral-mcp, and MISTRAL_API_KEY.]

## Skill Version(s):

0.3.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
