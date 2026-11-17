## Description:

PC game deals from 30+ stores - search sales, compare prices, and track cheapest-ever prices via CheapShark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search current PC game deals, compare prices across supported storefronts, inspect price history, and build game deal alert workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP configuration uses `npx -y mcp-remote@latest`, which can execute a changing npm package without an interactive approval step.

Mitigation: Pin `mcp-remote` to a reviewed version, remove automatic `-y` approval where possible, and install only after trusting the Pipeworx endpoint and npm bridge.

## Reference(s):

- [Pipeworx Game Deals Pack](https://pipeworx.io/packs/gamedeals)
- [ClawHub Skill Listing](https://clawhub.ai/b-gutman/skills/pipeworx-gamedeals)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns game deal search results, price comparisons, store listings, and MCP setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
