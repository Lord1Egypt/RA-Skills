## Description:

Provides MCP-backed semantic search for cross-border legal compliance, foreign and Chinese regulations, judicial interpretations, and guiding cases for legal research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xltxai](https://clawhub.ai/user/xltxai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, enterprise compliance teams, and legal researchers use this skill to retrieve domestic and international legal materials for cross-border compliance, contract review, regulatory research, sentencing references, and compensation calculations. It is not intended for real-time legal news or case-specific litigation strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Legal research queries may be routed to aixllaw's remote MCP service.

Mitigation: Avoid sending confidential case facts, privileged attorney-client material, trade secrets, or personal data unless the provider's terms and data handling have been reviewed.

Risk: The skill returns legal research and analysis that may be incomplete, stale, or unsuitable for a specific matter.

Mitigation: Treat outputs as research support and have qualified counsel review important legal conclusions before relying on them.

Risk: Optional API-key use can expose credentials if MCP configuration is copied broadly or stored in the wrong place.

Mitigation: Store AIXLLAW_API_KEY only in the intended MCP configuration, limit access to that file, and review the configuration periodically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xltxai/skills/mcp-law-search)
- [SkillHub homepage](https://skillhub.cn/skills/org-tz5v519f/mcp-law-search-skill)
- [MCP legal search setup guide](references/mcp-setup-guide.md)
- [search_law advanced search reference](references/search-patterns.md)
- [aixllaw MCP service endpoint](https://mcp.aixllaw.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown legal-analysis responses with retrieved legal-source summaries, plus JSON configuration snippets and shell commands when setup guidance is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the search_law MCP tool; responses may include source type, validity status, disclaimers, retry guidance, and setup instructions for optional AIXLLAW_API_KEY authentication.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
