## Description: <br>
Signed Protobuf packets over TCP for AI agent-to-agent communication with MCP tools, ed25519 authentication, discovery, routing, and memory sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nTEG-dev](https://clawhub.ai/user/nTEG-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect AI agents through signed TCP and Protobuf messages, discover available agents, route messages, and optionally expose the workflow through MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server helper can start server software through Docker or Go and may leave a local service running. <br>
Mitigation: Use keep_ensure_server only when local Docker or Go execution is acceptable; pin package, image, or Go module versions and stop the service when finished. <br>
Risk: Agents can exchange message bodies and optional memory data through the keep server. <br>
Mitigation: Keep the service bound to trusted local networks and avoid sending secrets or unreviewed memory through agent messages. <br>
Risk: Server evidence marks the release suspicious because it can run local services and remove or replace Docker containers on the target port. <br>
Mitigation: Review and scan the release before deployment, and monitor container or background process changes during use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nTEG-dev/keep-protocol) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Project README](artifact/README.md) <br>
- [Agent Integration Guide](artifact/AGENTS.md) <br>
- [Release Workflow](artifact/docs/release-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, JSON configuration, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke MCP tools that send or receive agent messages and may start a local keep server when explicitly used.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
