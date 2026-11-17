## Description:

Buildable Bring Your Own Context system for AI agents that helps create owned context vaults, scaffold typed memory systems, generate MCP-native context layers, build portable bundle workflows, migrate context across runtimes, and audit long-running agent memory systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, audit, or migrate owned agent context systems with typed memory objects, governance policies, evaluation scorecards, portable bundle manifests, and MCP-accessible context workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated MCP server operations can mutate or delete durable memory.

Mitigation: Use the skill only in an isolated workspace that is safe to modify, back up existing directories before scaffolding into them, and review deletion and writeback behavior before connecting persistent memory.

Risk: Unsafe server or context names may affect generated Python source.

Mitigation: Avoid untrusted or unusual values for --name and --server-name, and review generated source before running it.

Risk: Exposing the generated MCP server over streamable HTTP can make memory operations reachable by untrusted clients.

Mitigation: Keep the server on STDIO or localhost unless authentication and authorization have been added.

Risk: Unpinned runtime dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin dependencies before installation and scan the generated workspace before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danielfoojunwei/skills/hot-swap-context)
- [Context Architecture Guide](references/context_architecture.md)
- [Evaluation and Governance Guide](references/evaluation_and_governance.md)
- [Paradigm Shifts for Portable Context Systems](references/paradigm_shifts.md)
- [Model Context Protocol Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration files, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate editable governance, evaluation, memory-object, bundle, and MCP server scaffold files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
