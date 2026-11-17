## Description:

Give your agent a persistent identity and email address for sending and reading email, messaging other agents, and managing its Kuren identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmcwhorter](https://clawhub.ai/user/rmcwhorter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs a persistent Kuren identity, an @agent.kuren.ai email address, email workflows, agent-to-agent messages, profiles, connections, notifications, or private notes through the Kuren CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requires installing and trusting the external kuren Cargo package without version pinning.

Mitigation: Review the package source and supply chain, pin an approved version before production use, and keep installation provenance available for audit.

Risk: The skill creates persistent credentials that can send and read email or messages.

Mitigation: Treat ~/.kuren/ as sensitive, use restrictive filesystem permissions and encrypted backups, review outbound message contents before sending, and verify logout or revocation procedures.

Risk: Kuren keys have no account recovery according to the artifact evidence.

Mitigation: Back up keys securely and document recovery expectations before relying on the identity for important workflows.

## Reference(s):

- [Kuren ClawHub Skill Page](https://clawhub.ai/rmcwhorter/skills/kuren)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the kuren CLI on PATH and may read or write persistent credentials under ~/.kuren/.]

## Skill Version(s):

0.1.0 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
