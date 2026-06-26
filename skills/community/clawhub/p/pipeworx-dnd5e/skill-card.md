## Description: <br>
D&D 5th Edition reference — spells, monsters, classes, and spell lists from the official SRD <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players, game masters, and developers use this skill to look up D&D 5e SRD spells, monsters, class details, and spell lists through Pipeworx MCP/API calls during game prep, play, or companion-app development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: D&D lookup queries are sent to a Pipeworx-hosted gateway. <br>
Mitigation: Install only if sending those queries to Pipeworx is acceptable for the user's environment. <br>
Risk: The optional MCP configuration runs npx mcp-remote@latest, which downloads code at runtime. <br>
Mitigation: Review and pin the remote MCP package or otherwise approve runtime package downloads before using the optional MCP configuration. <br>


## Reference(s): <br>
- [Pipeworx D&D 5e Pack](https://pipeworx.io/packs/dnd5e) <br>
- [Pipeworx D&D 5e MCP Endpoint](https://gateway.pipeworx.io/dnd5e/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-dnd5e) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown and JSON examples with D&D reference lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for direct examples; optional MCP configuration uses npx mcp-remote to connect to the Pipeworx gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
