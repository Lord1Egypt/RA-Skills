## Description:

OpenClaw AgentOS onboarding bootstrapper for initializing, diagnosing, upgrading, repairing, and health-checking an OpenClaw setup with baseline skills, memory architecture, a Markdown knowledge base, agent team profiles, self-evolution workflows, and context hygiene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xb19960921](https://clawhub.ai/user/xb19960921)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to bootstrap a fresh or underpowered OpenClaw environment into a personal AgentOS, including safe install planning, diagnostics, memory setup, knowledge-base setup, and health reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent unpinned package and skill installs from mutable third-party sources can change after review.

Mitigation: Review every proposed install before approval and prefer pinned versions or commit hashes.

Risk: Backup archives or third-party install sources may lack independent integrity guarantees.

Mitigation: Avoid backup ZIPs unless the publisher provides an independent checksum or signature, and test new skills in a restricted environment before granting access to private files, memory, credentials, or production workspaces.

Risk: Onboarding actions may alter workspace, memory, or knowledge-base files when the user approves setup or repair steps.

Mitigation: Use backups, patch review, and explicit confirmation for protected files and other risky writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xb19960921/skills/openclaw-agent-onboarding)
- [Skill baseline](references/skill-baseline.md)
- [Safety policy](references/safety-policy.md)
- [Memory architecture](references/memory-architecture.md)
- [Knowledge base](references/knowledge-base.md)
- [Agent team profiles](references/agent-team.md)
- [Self-evolution workflow](references/self-evolution.md)
- [Health checks](references/health-checks.md)
- [Context hygiene](references/context-hygiene.md)
- [Obsidian](https://obsidian.md)
- [nuwa-skill repository](https://github.com/alchaincyf/nuwa-skill)
- [darwin-skill repository](https://github.com/alchaincyf/darwin-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans and reports with inline shell commands, generated Markdown templates, and JSON diagnostic output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates actions into safe-fix, needs-confirm, and manual categories; confirms risky writes or installs before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
