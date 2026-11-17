## Description:

Helps an agent install or configure RapidX CLI and MCP access, set production LTP credentials, locate workspace MCP configuration, review integration status, discover tools, and run read-only self-checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquiditytech](https://clawhub.ai/user/liquiditytech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare an agent host for RapidX CLI or MCP workflows, configure required LTP credentials, verify tool discovery, and report whether the runtime is MCP_READY, CLI_ONLY_READY, or NOT_VERIFIED before trading workflows begin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide installation of a mutable trading CLI and configuration of production credentials for tools that may perform high-impact account actions.

Mitigation: Install only from trusted RapidX CLI package sources, prefer pinned workspace-local installs, and use least-privilege credentials where possible.

Risk: Persisting full production credentials in MCP configuration can expose sensitive trading access through host retention, collaboration, or local file access.

Mitigation: Prefer host-supported secret references or a secret manager, avoid writing production secrets directly into MCP config, and mask credentials in logs and reviews.

Risk: Live trading, cancel-all, leverage, and close-position actions can materially affect an account if executed without adequate confirmation.

Mitigation: Require explicit previews, user confirmations, runtime self-checks, and readbacks before any live trading or high-impact account action.

## Reference(s):

- [RapidX Capability Overview](references/capability-overview.md)
- [RapidX Skills / CLI / MCP Best Practices](references/best-practices.md)
- [LTP RapidX Config on ClawHub](https://clawhub.ai/liquiditytech/skills/ltp-rapidx-config)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked credential references, read-only self-check results, MCP readiness classification, and integration review findings.]

## Skill Version(s):

1.0.17 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
