## Description:

Use when an agent needs to operate RapidX through MCP or CLI for portfolio reads, market reads, order preview, order submit/replace/cancel, position management, algo orders, or explicit live trading verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquiditytech](https://clawhub.ai/user/liquiditytech)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading operators use this skill to guide an agent through RapidX portfolio reads, market reads, previewed order actions, position management, algo order workflows, automation sessions, and explicit live trading verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents that have scoped access to live trading credentials and real trade-write authority.

Mitigation: Install only from a trusted RapidX CLI publisher, prefer a pinned and reviewed CLI version, use the host secret store, begin with read-only checks, and keep trading scope narrow.

Risk: Automation sessions can authorize multiple order lifecycle actions within the approved scope.

Mitigation: Enable automation only with explicit authorization for symbols, notional caps, duration, allowed actions, and allowed order types; use short sessions and stop automation when it is no longer needed.

## Reference(s):

- [RapidX Capability Overview](references/capability-overview.md)
- [RapidX Skills / CLI / MCP Best Practices](references/best-practices.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown guidance with inline command and tool examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trade-write guidance requires preview evidence, explicit consent or scoped automation authorization, and readback before final claims.]

## Skill Version(s):

1.0.17 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
