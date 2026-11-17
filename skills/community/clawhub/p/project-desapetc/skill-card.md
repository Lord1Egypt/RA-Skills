## Description:

Project Desapetc helps agents create and manage Billions Network decentralized identities, link them to human owners, and sign or verify authentication challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desapetc](https://clawhub.ai/user/desapetc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create local DID identities, link an agent identity to a human owner, and verify ownership proofs for authentication-sensitive workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates durable identity secrets and can store private keys in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not configured.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities; if the skill already ran without encryption, treat stored keys as potentially exposed depending on host permissions and backups.

Risk: Using the skill on an untrusted host can expose identity material or weaken authentication-sensitive workflows.

Mitigation: Install and run the skill only on trusted hosts and review the security posture before using it for identity verification.

Risk: Passing real private keys through the --key option can expose sensitive material through shell history, process inspection, or logs.

Mitigation: Avoid passing production private keys with --key; prefer generating a new identity or importing secrets through a reviewed secure process.

Risk: Security evidence recommends updating vulnerable dependencies before relying on this skill for authentication-sensitive workflows.

Mitigation: Review and update npm dependencies before production use, then rerun the relevant security checks.

## Reference(s):

- [Project Desapetc ClawHub Skill Page](https://clawhub.ai/desapetc/skills/project-desapetc)
- [Billions Network](https://billions.network/)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local identity files under $HOME/.openclaw/billions and may return DID strings, challenge values, verification URLs, or success/error messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
