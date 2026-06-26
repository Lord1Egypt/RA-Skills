## Description: <br>
Provides real estate market intelligence through an Altos Research MCP server, including market snapshots, inventory trends, listing searches, pending sales, new listings, and downloadable data catalog lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real-estate professionals, analysts, and agents use this skill to query regional market statistics and listing activity through the Altos MCP connector when preparing market reports, client guidance, or local inventory analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and responses are routed through an external Pipeworx/Altos MCP service whose server implementation is not included in the artifact. <br>
Mitigation: Use the skill for non-sensitive market lookups and avoid submitting confidential client details, private transaction information, or sensitive business plans unless the provider is trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/brucegutman/pipeworx-altos) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>
- [Altos MCP endpoint](https://gateway.pipeworx.io/altos/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or text responses with MCP configuration JSON when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return real-estate market statistics, listing summaries, file catalog details, and links or identifiers for downloadable regional data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
