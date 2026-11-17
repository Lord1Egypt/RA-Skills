## Description:

Runs a multi-model deliberation across models from different labs (Claude, GPT, Gemini, Grok, DeepSeek, Kimi, and more) via mumo's MCP server, returning full responses plus typed cross-model reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericatmumo](https://clawhub.ai/user/ericatmumo)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this Hermes skill to request independent cross-model review for architecture decisions, product tradeoffs, design plans, launch risks, and other high-regret choices. It is especially relevant before acting on changes involving auth, security, tokens, payments, data exposure, or migrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deliberation prompts may include sensitive designs, auth flows, security findings, customer data, personal data, or proprietary material and are sent to mumo and potentially downstream model providers.

Mitigation: Redact secrets and personal data, include only the minimum excerpts needed for the review, and avoid sending highly sensitive material unless that disclosure is acceptable.

Risk: Sharing a session can expose deliberation content beyond the local operator.

Mitigation: Use share_session only when intentionally creating a public session link.

Risk: The MCP server requires a mumo API key, and mishandling that key can expose access to the service.

Mitigation: Store MUMO_API_KEY in the Hermes .env file with restricted permissions, reference it from configuration as an environment variable, and avoid placing literal keys in shell commands or config files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericatmumo/skills/mumo-hermes)
- [mumo Product](https://mumo.chat)
- [mumo Hermes Install Guide](https://mumo.chat/install/hermes)
- [mumo MCP Reference](https://mumo.chat/docs/mcp)
- [mumo REST API](https://mumo.chat/docs/api)
- [mumo Hermes Repository](https://github.com/mumo-chat/mumo-hermes)
- [Claim Maps](references/claim-maps.md)
- [Model Selection](references/model-selection.md)
- [Operating Notes](references/operating-notes.md)
- [Snippets](references/snippets.md)
- [Synthesis](references/synthesis.md)
- [Takeaway](references/takeaway.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown synthesis with tool-call guidance and occasional shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cross-model claim-map interpretation, typed snippets, follow-up deliberation prompts, and public session links only when intentionally shared.]

## Skill Version(s):

0.6.3 (source: frontmatter, changelog, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
