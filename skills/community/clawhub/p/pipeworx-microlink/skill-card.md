## Description: <br>
Microlink MCP wraps the Microlink API for metadata extraction and webpage screenshots without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect an MCP server that retrieves URL metadata and takes webpage screenshots through Microlink. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs are sent to an external Microlink service. <br>
Mitigation: Avoid internal sites, private pages, signed URLs, tokens in query strings, and other sensitive identifiers unless that external processing is acceptable. <br>
Risk: The connection runs through the remote mcp-remote package and Pipeworx endpoint. <br>
Mitigation: Install only when the publisher, package, and external endpoint are trusted for the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-microlink) <br>
- [Pipeworx Microlink pack](https://pipeworx.io/packs/microlink) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, images] <br>
**Output Format:** [Markdown instructions with JSON MCP server configuration; tool results may include metadata and screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mcp-remote to call the external Pipeworx Microlink MCP endpoint; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
