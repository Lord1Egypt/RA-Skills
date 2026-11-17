## Description:

Manage MCPJungle gateway through its CLI for listing, registering, deregistering, enabling, disabling, invoking, and inspecting MCP servers, tools, prompts, and tool groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctxinf](https://clawhub.ai/user/ctxinf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer a running MCPJungle registry through CLI commands, including server registration, tool and prompt lifecycle management, configuration export, and direct tool invocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing registry administration commands could affect MCP servers, tools, prompts, or groups if run against the wrong target.

Mitigation: Confirm the registry URL, server, tool, and prompt names before running state-changing commands.

Risk: Tool invocations may pass sensitive input to target MCP servers.

Mitigation: Avoid passing secrets or sensitive data into tool invocations unless the target server is trusted.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for operating an installed MCPJungle CLI against a running registry.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
