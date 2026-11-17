## Description:

Cocktail recipes from TheCocktailDB - search by name, browse by ingredient, or discover a random drink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to search for cocktail recipes, retrieve ingredient lists and preparation instructions, browse drinks by ingredient, or request a random cocktail suggestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP client configuration runs npm code through npx using mcp-remote@latest.

Mitigation: Pin mcp-remote to a reviewed exact version and run the client in a restricted environment before installation.

Risk: Secrets or unnecessary environment data could be exposed to the external MCP process if the agent environment is configured broadly.

Mitigation: Avoid placing unnecessary secrets in the agent environment and scope any credentials to the minimum required.

Risk: Cocktail recipe data is retrieved from an external service and may be unavailable or unsuitable for a specific audience or setting.

Mitigation: Review returned recipe content before serving it to end users and handle endpoint failures gracefully.

## Reference(s):

- [Pipeworx Cocktails Pack](https://pipeworx.io/packs/cocktails)
- [Pipeworx Cocktails MCP Endpoint](https://gateway.pipeworx.io/cocktails/mcp)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-cocktails)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [MCP tool responses with cocktail recipe details, ingredient lists, preparation instructions, and client configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the documented example; MCP client setup uses npx with mcp-remote.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
