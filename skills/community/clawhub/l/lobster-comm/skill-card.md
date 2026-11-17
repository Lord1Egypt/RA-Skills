## Description:

Bot-to-bot P2P communication over Tailscale using the LCP/1.1 UDP protocol for signed, reliable messages between agents on different machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffchang2024](https://clawhub.ai/user/jeffchang2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Lobster Comm to configure and run peer-to-peer messaging between AI agents over a Tailscale network for cross-machine task delegation and distributed orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages cross the user's Tailnet and are stored on disk.

Mitigation: Do not send secrets through this skill; review storage locations, retention, and cleanup before use.

Risk: Authentication and local control boundaries are weak for trusted agent-to-agent use without review.

Mitigation: Require peer key pinning, source validation, authenticated IPC, and restrictive key storage before trusted or autonomous use.

Risk: Auto-start or Windows service use can keep the messaging daemon active on shared machines.

Mitigation: Avoid auto-start and service mode on shared systems unless access controls and an operational disable path are reviewed.

## Reference(s):

- [LCP/1.1 Protocol Specification](references/protocol-spec.md)
- [PyNaCl](https://pypi.org/project/PyNaCl/)
- [Tailscale](https://tailscale.com/)
- [NSSM](https://nssm.cc/)
- [ClawHub skill page](https://clawhub.ai/jeffchang2024/skills/lobster-comm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe daemon status, inbox/outbox message files, and LCP message JSON.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
