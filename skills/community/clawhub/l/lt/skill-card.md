## Description:

Agents can sign plugins, rotate credentials without losing identity, and publicly attest to behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltte](https://clawhub.ai/user/ltte)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure access to the 0.protocol MCP service, sign plugin artifacts, record behavior attestations, query identity state, and transfer task handoffs with witnessed receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plugin hashes, attestations, identity metadata, and handoff payloads may be sent to the 0.protocol MCP service, and public claims may be durable.

Mitigation: Avoid secrets, private customer data, sensitive incident context, and confidential operational details; choose claim and transfer visibility deliberately.

Risk: Signed expressions are recorded claims, not authentication, reputation, consensus, payments, or mandatory execution controls.

Mitigation: Treat expressions as provenance and handoff signals while continuing to use existing authentication, review, and trust processes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ltte/skills/lt)
- [README / Spec](https://github.com/0isone/0protocol)
- [API Reference](https://github.com/0isone/0protocol/blob/main/API.md)
- [Migration Guide](https://github.com/0isone/0protocol/blob/main/migration.md)
- [Why](https://github.com/0isone/0protocol/blob/main/WHY.md)
- [0.protocol MCP Endpoint](https://mcp.0protocol.dev/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP server configuration, mcporter commands, and guidance for signed claims, identity queries, and authenticated handoffs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
