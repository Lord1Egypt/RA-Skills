## Description:

Provides a Windows-oriented wrapper for MiniMax Token Plan web search and image understanding, with fallback options when the subscription is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godiao](https://clawhub.ai/user/godiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to run MiniMax-powered web search and image understanding through a Node.js wrapper around the MiniMax MCP server. It is especially aimed at Windows environments where the documented uvx path has asyncio DLL issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the executable dependency and credential or data handling are under-scoped and partly inconsistent.

Mitigation: Review before installing, pin and review the minimax-coding-plan-mcp dependency version, and keep credentials in environment variables or a secret manager.

Risk: Search and image-understanding workflows may send private screenshots, documents, internal URLs, or secrets to external services.

Mitigation: Avoid submitting sensitive screenshots, documents, internal URLs, or secrets through the search or image features.

Risk: The wrapper can run a Python executable selected by MINIMAX_PYTHON.

Mitigation: Set MINIMAX_PYTHON only to a trusted absolute Python executable path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/godiao/skills/minimax-mcp-tool)
- [Publisher Profile](https://clawhub.ai/user/godiao)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results, plain-text image descriptions, and Markdown usage guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment variables for credentials and Python executable selection; image understanding may process local image files or image URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
