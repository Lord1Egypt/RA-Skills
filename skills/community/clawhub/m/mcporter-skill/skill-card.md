## Description: <br>
Use the mcporter CLI to list, configure, authenticate, and call MCP servers and tools over HTTP or stdio, including ad-hoc servers, configuration edits, and CLI/type generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Livvux](https://clawhub.ai/user/Livvux) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to operate MCP servers from an agent workflow: listing configured servers, authenticating, calling tools, editing mcporter configuration, and generating typed CLI wrappers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured MCP servers, authentication flows, tool calls, and configuration edits may handle credentials, change local mcporter state, or send arguments and context to local or remote servers. <br>
Mitigation: Install mcporter only from a trusted source, configure only trusted MCP servers, and review auth, config, ad-hoc server, and tool-call commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Livvux/mcporter-skill) <br>
- [mcporter homepage](https://github.com/pdxfinder/mcporter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose mcporter commands that interact with local or remote MCP servers and local mcporter configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
