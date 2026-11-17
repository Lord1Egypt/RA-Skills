## Description:

Durable, signature-verified webhooks for OpenClaw agents and other consumers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[7schmiede](https://clawhub.ai/user/7schmiede)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Hookaido as a durable webhook ingress for OpenClaw agents and other consumers. It provides guidance for signature verification, event delivery or pull relays, queue operations, and MCP diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook payloads can contain untrusted content that reaches an agent.

Mitigation: Use a restricted agent for incoming events and keep its allowed agent IDs narrow.

Risk: Webhook credentials and stored event data could be exposed through insecure connections or broad access.

Mitigation: Use dedicated tokens, HTTPS for remote connections, and protect stored webhook data; keep MCP read-only unless performing an intentional maintenance task.

Risk: The security review did not verify the downloaded upstream binary or establish publisher identity.

Mitigation: Verify the upstream release signatures and checksums before installing the binary.

## Reference(s):

- [OpenClaw integration guide](references/openclaw.md)
- [Hookaido operations guide](references/operations.md)
- [Skill homepage](https://github.com/7schmiede/claw-skill-hookaido)
- [Hookaido project](https://github.com/nuetzliches/hookaido)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code]

**Output Format:** [Markdown with configuration examples, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.15.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
