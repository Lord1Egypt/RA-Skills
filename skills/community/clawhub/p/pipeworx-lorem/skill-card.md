## Description: <br>
Lorem MCP — wraps loripsum.net (free, no auth) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to connect an MCP server that generates Lorem Ipsum text from loripsum.net without requiring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connection example launches npx with mcp-remote@latest and connects to a remote MCP gateway, so the executed package or remote service behavior may change over time. <br>
Mitigation: Review the command before adding it to an agent, consider pinning the mcp-remote package version, and use the skill only in environments where remote MCP access is allowed. <br>


## Reference(s): <br>
- [Pipeworx Lorem homepage](https://pipeworx.io/packs/lorem) <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-lorem) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration] <br>
**Output Format:** [Plain text MCP tool responses and JSON MCP server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides generate_paragraphs and generate_with_options tools; no API key is documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
