## Description: <br>
Provides an MCP filesystem server through mcporter so an agent can read files, list directories, search by pattern, and inspect file metadata inside a configured workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudedamir-art](https://clawhub.ai/user/claudedamir-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give Jarvis controlled filesystem access for reading, listing, searching, and inspecting files within a configured workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent read, listing, search, and metadata access to files under the configured workspace, which can expose secrets or unrelated private data if the root is too broad. <br>
Mitigation: Configure the workspace root narrowly, keep secrets and unrelated private data outside that root, and review access before deployment. <br>
Risk: The skill depends on external command-line packages for filesystem access. <br>
Mitigation: Verify or pin the required packages before using the skill in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/claudedamir-art/jarvis-mcp-filesystem) <br>
- [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filesystem access is scoped to the configured workspace root.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
