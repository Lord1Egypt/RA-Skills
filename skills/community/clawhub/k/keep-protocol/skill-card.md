## Description:

Keep Protocol helps agents exchange signed Protobuf packets over TCP with MCP tools, discovery, routing, and memory sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nteg-dev](https://clawhub.ai/user/nteg-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Keep Protocol to coordinate multi-agent workflows by sending signed messages, discovering connected agents, listening for routed packets, and sharing optional memory payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bootstrap a Keep server and may affect Docker containers or execute mutable remote software through Docker or Go startup paths.

Mitigation: Install and run it only in a trusted local development environment; review and constrain server startup behavior before allowing autonomous agents to call keep_ensure_server.

Risk: The TCP server and routed message bodies can expose agent communication if used on untrusted networks or with sensitive content.

Mitigation: Keep the server on localhost or trusted networks, avoid sending secrets or sensitive memory, and do not treat src names as strong authenticated identities.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nteg-dev/skills/keep-protocol)
- [README](artifact/README.md)
- [Agent Integration Guide](artifact/AGENTS.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code, shell commands, JSON configuration, and MCP tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tools may return plain text or JSON-encoded strings from a configured Keep server.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
