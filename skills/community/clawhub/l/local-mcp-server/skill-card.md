## Description: <br>
Run a full Model Context Protocol (MCP) server in Termux. Exposes Read, Bash, Grep, glob tools for local Ollama models. Privacy-first, offline-capable, ~10MB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wizelements](https://clawhub.ai/user/wizelements) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a local MCP server in Termux or Linux, giving local Ollama-connected agents controlled access to file reading, shell execution, grep search, and glob matching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An MCP-connected model can receive local file and shell tool access through this server. <br>
Mitigation: Keep the server bound to localhost, restrict allowed paths to a test or project directory, and avoid secrets directories. <br>
Risk: Shell command execution can cause unintended system or data changes if commands are run without review. <br>
Mitigation: Require confirmation before command execution and do not rely on command blocklists as the only control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wizelements/local-mcp-server) <br>
- [Publisher profile](https://clawhub.ai/user/wizelements) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides local MCP tool access for reading files, executing shell commands, and searching or matching file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
