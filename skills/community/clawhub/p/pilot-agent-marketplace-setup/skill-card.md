## Description:

Deploy a decentralized agent marketplace with directory, matchmaker, escrow, and gateway agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up a four-agent marketplace where capabilities are discovered, requests are matched, transactions are escrowed, and gateway traffic is handled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run broad install and setup commands with under-specified safety controls.

Mitigation: Review commands before execution, use a strict hostname-safe prefix, quote generated arguments, and confirm the full hostname and handshake list before running setup.

Risk: Setup may overwrite or conflict with an existing marketplace manifest.

Mitigation: Check whether ~/.pilot/setups/agent-marketplace.json already exists before writing it, and run setup from a least-privileged account.

Risk: Dependent skills and binaries may change behavior across versions.

Mitigation: Prefer pinned or verified versions of dependent skills and required binaries such as pilotctl and clawhub.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-agent-marketplace-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific setup steps, hostnames, handshake commands, manifest templates, and verification guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
