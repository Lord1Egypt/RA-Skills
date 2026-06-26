## Description: <br>
Global biodiversity data -- search species, retrieve taxonomy, and find georeferenced occurrence records via GBIF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and conservation teams use this skill to add GBIF species search, taxonomy lookup, and georeferenced occurrence retrieval to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are routed through the Pipeworx remote MCP gateway. <br>
Mitigation: Review network policy and data sensitivity requirements before sending lookup requests through the gateway. <br>
Risk: The sample MCP configuration uses mcp-remote@latest, which may change over time. <br>
Mitigation: Pin the mcp-remote package version in environments that require reproducible installs. <br>


## Reference(s): <br>
- [Pipeworx GBIF Pack](https://pipeworx.io/packs/gbif) <br>
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/pipeworx-gbif) <br>
- [Pipeworx GBIF MCP Gateway](https://gateway.pipeworx.io/gbif/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP configuration, JSON-RPC examples, or GBIF lookup results for species, taxonomy, and occurrences.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
