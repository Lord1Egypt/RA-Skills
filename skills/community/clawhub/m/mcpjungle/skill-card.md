## Description: <br>
Manage MCPJungle gateway through its CLI for listing, registering, deregistering, enabling, disabling, invoking, and inspecting MCP servers, tools, prompts, and tool groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctxinf](https://clawhub.ai/user/ctxinf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage a running MCPJungle registry from an agent-assisted workflow, including server lifecycle operations, tool and prompt visibility, direct tool invocation, and configuration export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disable or deregister commands can change MCP server, tool, or prompt availability. <br>
Mitigation: Confirm the target registry, server name, and expected impact before running disable or deregister commands. <br>
Risk: Invoked MCP tools may receive sensitive prompts, files, credentials, or private data. <br>
Mitigation: Use only trusted MCP servers and avoid passing sensitive data unless that disclosure is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ctxinf/mcpjungle) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are command-oriented guidance for interacting with an existing MCPJungle CLI and registry.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
