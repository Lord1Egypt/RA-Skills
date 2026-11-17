## Description:

Distributed agent mesh for OpenClaw gateways with ring-of-trust admission, CRDT-synced coordination, capability-contract routing, and governed delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likesjx](https://clawhub.ai/user/likesjx)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw operators and developers use this skill to coordinate work across multiple gateways, manage trust and routing policies, and keep delegated tasks visible and auditable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task-controlled inputs can trigger code installation or command execution on an OpenClaw gateway.

Mitigation: Run only in administrator-controlled environments with authenticated task creation, caller allowlists, and deployment or command execution disabled unless explicitly approved.

Risk: Untrusted package sources or mutable plugin references could introduce unintended code.

Mitigation: Require signed or allowlisted artifacts, pin plugin identities and versions, verify SHA-256 hashes, and use trusted package sources.

Risk: Package-provided smoke tests may execute code after deployment.

Mitigation: Review deployment artifacts before installation and avoid automatic execution of package-provided smoke tests unless the artifact source is trusted.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/likesjx/skills/openclaw-skill-ansible)
- [OpenClaw](https://openclaw.ai/)
- [OpenClaw Ansible Plugin](https://github.com/likesjx/openclaw-plugin-ansible)
- [Ansible Skill Source Repository](https://github.com/likesjx/openclaw-skill-ansible)
- [Operator Runbook](docs/operator-runbook.md)
- [Plugin Capability Inventory](docs/plugin-capabilities-actual-v2026-03-03.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and JSON task artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce operational status updates, command output summaries, and artifact logs when paired with OpenClaw gateway actions.]

## Skill Version(s):

0.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
