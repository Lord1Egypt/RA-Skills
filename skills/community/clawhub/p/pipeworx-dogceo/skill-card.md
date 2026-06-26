## Description: <br>
Random dog photos by breed — 120+ breeds with sub-breeds from the Dog CEO API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve random or breed-specific dog image URLs and breed lists for chatbots, UI placeholders, pet-themed responses, and reference-photo workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dog image and breed queries are sent to a remote Pipeworx gateway. <br>
Mitigation: Use only for non-sensitive image lookup workflows and avoid sending confidential context in tool arguments. <br>
Risk: The sample MCP configuration installs mcp-remote@latest at runtime. <br>
Mitigation: Pin mcp-remote to a reviewed version for reproducible deployments. <br>


## Reference(s): <br>
- [Pipeworx Dog CEO Pack](https://pipeworx.io/packs/dogceo) <br>
- [Pipeworx Dog CEO MCP Gateway](https://gateway.pipeworx.io/dogceo/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples; MCP tool responses return dog image URLs or breed lists as text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented API example and can be configured through mcp-remote for MCP clients.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
