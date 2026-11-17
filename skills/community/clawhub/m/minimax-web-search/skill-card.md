## Description:

Uses the MiniMax MCP web_search tool to perform web searches when users ask for online lookup, current information, news, or MiniMax web_search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thincher](https://clawhub.ai/user/thincher)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to route user search requests through MiniMax MCP, configure the required API key, and return formatted web-search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow can execute mutable third-party code through uvx and curl-pipe-to-shell.

Mitigation: Review package sources before installation, pin trusted versions of uv and minimax-coding-plan-mcp, and avoid direct curl-pipe-to-shell installation.

Risk: The skill handles a MiniMax API key through an environment variable or local config file.

Mitigation: Store the API key in a secret manager or a tightly permissioned config file, and rotate it if exposed.

Risk: The MCP process inherits the surrounding environment when launched.

Mitigation: Run the skill in a constrained environment without unrelated sensitive environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thincher/skills/minimax-web-search)
- [Publisher profile](https://clawhub.ai/user/thincher)
- [MiniMax coding plan subscription](https://platform.minimaxi.com/subscribe/coding-plan?code=GjuAjhGKqQ&source=link)
- [MiniMax API host](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and shell commands, with search results printed as formatted JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a search query and a MiniMax API key supplied through MINIMAX_API_KEY or a local config file.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
