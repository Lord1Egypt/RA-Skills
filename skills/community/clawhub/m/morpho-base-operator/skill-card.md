## Description:

Operate a Base-first Morpho vault workflow with registry-gated planning, external authorization, MCP execution, reconciliation, and archived reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walioo](https://clawhub.ai/user/walioo)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi operators and engineers use this skill to run controlled Morpho vault operations on Base by loading a registry, validating addresses and market status, preparing deterministic plans, collecting external signatures, executing through the pinned MCP stack, and reconciling reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private keys or authority signatures may be exposed if handled inside the agent host.

Mitigation: Keep signing outside the host, prefer hardware-backed or external signing, and provide local secrets outside the published skill bundle.

Risk: Executing against an unknown, paused, disabled, or address-mismatched market could produce unsafe writes.

Mitigation: Treat the registry as the source of truth, reject unsupported market state before execution, and stop on address or adapter mismatches.

Risk: Mainnet execution can move assets before operator review is complete.

Mitigation: Keep allowMainnetExecution false by default and require explicit operator signoff before enabling execution.

Risk: A revert or ambiguous receipt can leave operation status unclear.

Mitigation: Stop retries, reconcile the transaction outcome, preserve logs and reports under artifacts/, and archive the execution report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/walioo/skills/morpho-base-operator)
- [Runbook Reference](references/runbook.md)
- [Policy](references/policy.md)
- [Incident Response Reference](references/incident-response.md)
- [Registry](references/registry.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown operational guidance with ordered steps, risk checks, and configuration reminders.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires operator-supplied local RPC, signing key handling, registry data, and active vault identifiers outside the skill bundle.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
