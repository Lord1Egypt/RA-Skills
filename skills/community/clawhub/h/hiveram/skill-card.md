## Description:

Agent coordination layer via Workledger for shared work orders, claim and release leases, cross-machine memory sync, and handoff between OpenClaw instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppiankov](https://clawhub.ai/user/ppiankov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multiple OpenClaw agents through Workledger work orders, leases, shared context, and handoffs across sessions or machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command downloads a mutable latest Workledger release and extracts it into the system binary path.

Mitigation: Pin a specific Workledger release, verify a published checksum or signature, and install to a user-owned bin directory when possible.

Risk: Shared context sync can persist sensitive project, customer, or secret material beyond a single agent session.

Mitigation: Do not store secrets or customer data in shared context; keep the Workledger API key narrowly scoped, protected, and rotated.

Risk: Delete and context-put operations modify shared multi-agent state and can affect other agents' work.

Mitigation: Review destructive or shared-state updates before execution and use claim/release workflow discipline for coordinated changes.

## Reference(s):

- [Hiveram service](https://hiveram.com)
- [Workledger CLI distribution](https://github.com/ppiankov/hiveram-dist)
- [Hiveram on ClawHub](https://clawhub.ai/ppiankov/skills/hiveram)
- [ppiankov ClawHub profile](https://clawhub.ai/user/ppiankov)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the workledger CLI and a configured WORKLEDGER_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
