## Description: <br>
PC game deals from 30+ stores - search sales, compare prices, and track cheapest-ever prices via CheapShark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search PC game sales, compare prices across digital storefronts, inspect price history, and configure an MCP connection for game deal lookup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and filters are sent to the disclosed Pipeworx remote MCP endpoint. <br>
Mitigation: Avoid sending sensitive or private queries through the remote endpoint unless that data sharing is acceptable for the user's environment. <br>
Risk: The provided MCP configuration uses mcp-remote@latest, which can change over time. <br>
Mitigation: Pin or review the mcp-remote package version when strict supply-chain reproducibility is required. <br>


## Reference(s): <br>
- [Pipeworx Gamedeals Homepage](https://pipeworx.io/packs/gamedeals) <br>
- [Pipeworx Gamedeals MCP Endpoint](https://gateway.pipeworx.io/gamedeals/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/pipeworx-gamedeals) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return game deal search results, store comparisons, price history, and MCP setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
