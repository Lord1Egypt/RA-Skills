## Description:

Generate, validate, export, and manage MOCI identities for OpenClaw agents, including memory-bound identity verification, identity portability, trust scoring, and gateway configuration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mociforge](https://clawhub.ai/user/mociforge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and assess memory-bound OpenClaw agent identities, verify agent continuity, plan secure identity export and import, and configure MOCI-related gateway workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates long-lived local identity and memory files under ~/.openclaw, which can become sensitive persistent state.

Mitigation: Install only in environments where local file access is controlled, use file systems that enforce owner-only permissions, restrict tools from reading identity files, and keep encrypted backups outside chats, logs, and shared diagnostics.

Risk: Server security evidence says the release needs review because key security promises are contradicted by the reference implementation.

Mitigation: Do not rely on this version for production trust, provenance, or identity recovery until caller-token authentication, encrypted export, import validation, nonce replay handling, and recovery-phrase guidance have been reviewed and fixed.

Risk: Passphrases and recovery phrases can cause identity compromise if exposed through chat, logs, shared files, or diagnostics.

Mitigation: Keep passphrases and recovery phrases out of agent conversations and logs, retrieve them through secure local secret mechanisms, and rotate or regenerate affected identities if secrets are exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mociforge/skills/moci)
- [Memory Chain Security](references/memory-security.md)
- [MOCI Reference Implementation](references/moci.ts)
- [MOCI Threat Matrix](references/threat-matrix.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration examples, and TypeScript reference material]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce identity lifecycle guidance, validation steps, threat-model notes, and OpenClaw Gateway configuration recommendations.]

## Skill Version(s):

0.1.0 (source: release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
