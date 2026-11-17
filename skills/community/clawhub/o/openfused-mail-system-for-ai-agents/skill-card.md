## Description:

OpenFuse helps AI agents manage decentralized context stores, signed or encrypted messages, peer synchronization, and cryptographic trust.

This skill is ready for commercial/non-commercial use.

## Publisher:

[velinxs](https://clawhub.ai/user/velinxs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize and operate OpenFuse context stores, exchange messages between agents, manage peer trust, and synchronize context over configured peers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send data and sync peer-controlled context into persistent agent state.

Mitigation: Use a dedicated store or sandbox, configure only trusted peers, and treat inbox content as untrusted even when it is signed or verified.

Risk: Peer synchronization uses SSH-based access and existing SSH configuration.

Mitigation: Use least-privilege SSH accounts and review configured peer destinations before running sync or watch operations.

Risk: The skill installs and invokes a global third-party CLI package.

Mitigation: Install only if the openfused npm package is trusted, and pin or review the package before use.

Risk: Watch and tunnel modes can repeatedly transfer data or expose access paths if enabled unnecessarily.

Mitigation: Avoid watch, reverse SSH tunnel, and cloudflared tunnel modes unless they are required for the deployment.

Risk: Files placed in shared/ are plaintext and visible to synced peers.

Mitigation: Do not place sensitive files in shared/, especially when peers are not fully trusted.

## Reference(s):

- [OpenFuse GitHub repository](https://github.com/wearethecompute/openfused)
- [openfused npm package](https://www.npmjs.com/package/openfused)
- [ClawHub skill listing](https://clawhub.ai/velinxs/skills/openfused-mail-system-for-ai-agents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through OpenFuse CLI setup and operations for context stores, peers, keys, inboxes, shared files, sync, and watch mode.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
