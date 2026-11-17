## Description:

Helps operators inspect and troubleshoot Oracle Linux Virtualization Manager and oVirt 4.5 environments through read-only inventory and diagnostic tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Virtualization administrators and engineers use the skill to review OLVM or oVirt inventory, health, capacity, events, and jobs, and to investigate engine, host, storage, or VM issues. It returns read-only findings and suggested next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Engine credentials and local configuration and audit data are sensitive.

Mitigation: Use a dedicated ReadOnlyAdmin account, protect the master password, and restrict access to local files.

Risk: Disabling TLS verification weakens checks on the engine connection.

Mitigation: Keep TLS verification enabled and configure the engine CA.

Risk: The documented package installation command is unpinned.

Mitigation: Pin a reviewed package version before installation.

Risk: An unhealthy audit store can leave the activity trail incomplete.

Mitigation: Check audit health before relying on a complete audit trail.

Risk: The external runtime code was unavailable for inspection, so its security guarantees could not be verified.

Mitigation: Review the runtime package and use a least-privilege engine account.

## Reference(s):

- [Capabilities](references/capabilities.md)
- [Setup and security guide](references/setup-guide.md)
- [CLI reference](references/cli-reference.md)
- [Agent guardrails](references/agent-guardrails.md)
- [Project homepage](https://github.com/AIops-tools/OLVM-AIops)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON results with concise Markdown findings and suggested actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are ranked and include measured signals, causes, and suggested actions; results may be partial when a scan is truncated.]

## Skill Version(s):

0.7.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
