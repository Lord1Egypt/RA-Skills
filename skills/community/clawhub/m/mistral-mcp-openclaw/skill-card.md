## Description: <br>
Configure OpenClaw to use the community mistral-mcp stdio server for Mistral OCR, Codestral FIM, Voxtral audio, durable workflows, moderation, classification, files, batch, and model/voice resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swih](https://clawhub.ai/user/swih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw with a community Mistral MCP server when an agent needs Mistral-specific tool access for OCR, code completion, audio, workflow, moderation, classification, files, batch, model, or voice operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Mistral API key. <br>
Mitigation: Use environment variables or a secret manager, avoid pasting keys into chat, and prefer a dedicated or limited API key where possible. <br>
Risk: The skill configures a community npm MCP server package. <br>
Mitigation: Review the mistral-mcp package or source before installing it in sensitive workspaces, and consider pinning a trusted version. <br>
Risk: Mistral tool calls may process documents, audio, code, or other workspace data. <br>
Mitigation: Avoid processing sensitive files unless Mistral's terms and the workspace policy allow it. <br>
Risk: Batch and transcription workloads may incur cost or rate-limit exposure. <br>
Mitigation: Check the current Mistral plan, pricing, rate limits, and usage policies before running large workloads. <br>


## Reference(s): <br>
- [Mistral MCP homepage](https://github.com/Swih/mistral-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/swih/mistral-mcp-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, OpenClaw CLI, the mistral-mcp package, and a MISTRAL_API_KEY environment variable.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
