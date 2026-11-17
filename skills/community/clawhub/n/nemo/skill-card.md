## Description:

Nemo helps agents search for MCP tools and agent skills, retrieve full skill instructions, and invoke tools on indexed remote MCP servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mootbing](https://clawhub.ai/user/mootbing)

### License/Terms of Use:


## Use Case:

Developers and agents use Nemo to discover available MCP tools and agent skills across remote servers, inspect skill instructions, and route selected tool calls through the Nemo service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote skill instructions and externally selected MCP tools may cross trust boundaries.

Mitigation: Use only with a trusted Nemo service and trusted indexed MCP servers, and require explicit review before following retrieved instructions or invoking remote tools.

Risk: Tool arguments may expose secrets or private file contents to remote services.

Mitigation: Do not send secrets, credentials, private files, or sensitive user data as search queries or tool arguments.

## Reference(s):

- [Nemo ClawHub Skill Page](https://clawhub.ai/mootbing/skills/nemo)
- [Nemo Service Base URL](https://nemo.25chenghua.workers.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and text with API examples and tool invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote responses may be truncated by the service response limits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
