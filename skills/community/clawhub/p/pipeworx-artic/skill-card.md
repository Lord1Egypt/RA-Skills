## Description: <br>
Explore the Art Institute of Chicago collection, including artworks, artists, and exhibitions, through the ARTIC public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search ARTIC collection records, retrieve artwork and artist details, browse exhibitions, and pull structured art data for education, trip planning, analysis, or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls a remote MCP endpoint and ARTIC-derived data can affect downstream summaries or decisions. <br>
Mitigation: Use it only in trusted MCP client configurations, review returned records before reuse, and treat generated summaries as derived from external collection data. <br>
Risk: The security evidence notes that maintainer workflows and third-party releases should be installed only when the repository and publisher are trusted. <br>
Mitigation: Install from the server-resolved ClawHub release, review the skill contents and security verdict, and avoid invoking it in sensitive workflows without approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-artic) <br>
- [Pipeworx ARTIC pack](https://pipeworx.io/packs/artic) <br>
- [Pipeworx ARTIC MCP endpoint](https://gateway.pipeworx.io/artic/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON MCP client configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-RPC tool-call examples, ARTIC record summaries, image URLs, descriptions, and provenance returned by the remote MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
