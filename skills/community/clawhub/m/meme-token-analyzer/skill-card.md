## Description:

Analyzes meme and community tokens using recent web sentiment and LLM reasoning to produce a token rating, risk warning, data freshness status, sources, and educational report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request entertainment and educational analysis of meme tokens, including community sentiment, narrative strength, rating, and risk context. It is not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opaque remote MCP backend may process requests outside the local artifact.

Mitigation: Install or enable the skill only when the publisher and remote backend are trusted, and document the MCP API surface before deployment.

Risk: Bundled executable code may conflict with the published remote-MCP architecture and expose unauthenticated paid AI, search, or image workflows if run locally.

Mitigation: Treat the remote MCP tool as authoritative unless the local implementation is reviewed, fixed, authenticated, and explicitly selected for use.

Risk: Full request-body logging, eval-based shell execution, and unlocked dependency installation can increase operational and supply-chain exposure.

Mitigation: Remove sensitive request logging, avoid eval-based shell execution, and install dependencies from a locked, hash-verified path.

## Reference(s):

- [Repository metadata](https://github.com/AntalphaAI/meme-token-analyzer)
- [MCP endpoint metadata](https://mcp-skills.ai.antalpha.com/mcp)
- [Publisher profile](https://clawhub.ai/user/deanpeng-dotcom)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON response fields and a Markdown-style token analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes token identifier, major-coin handling, rating, report sections, search summary, data freshness, sources, and disclaimer when returned by the MCP tool.]

## Skill Version(s):

2.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
