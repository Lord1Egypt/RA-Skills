## Description: <br>
Nutrition MCP - wraps Open Food Facts API for free product nutrition lookups with no API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search product nutrition data and retrieve product details through Pipeworx's nutrition MCP connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup queries are sent to Pipeworx's remote nutrition gateway. <br>
Mitigation: Avoid sensitive query content and review the service before using it in restricted environments. <br>
Risk: The connection example uses npx with mcp-remote@latest, which can change over time. <br>
Mitigation: Pin the launcher version when stricter supply-chain control is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-nutrition) <br>
- [Pipeworx nutrition homepage](https://pipeworx.io/packs/nutrition) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and tool-result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides nutrition lookup guidance through search_products and get_product tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
