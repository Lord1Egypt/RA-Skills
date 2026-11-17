## Description:

Openclaw Agent Optimize provides advisory audits and prioritized optimization plans for OpenClaw workspaces focused on cost-aware model routing, context discipline, delegation, reliability, rollback, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phenomenoner](https://clawhub.ai/user/phenomenoner)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to audit workspace cost, context bloat, model routing, delegation, cron, and heartbeat behavior, then receive a prioritized plan with exact proposed changes, rollback notes, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimization advice may propose config, cron, heartbeat, memory, or skill-surface changes that alter cost, reliability, or monitoring coverage.

Mitigation: Review the exact proposed change, expected impact, rollback plan, and post-change verification before approving any persistent mutation.

Risk: Installing through an unpinned package command can introduce npm supply-chain exposure.

Mitigation: Use a pinned or otherwise verified installer path when supply-chain assurance is required.

Risk: Reducing heartbeat or cron frequency can lower monitoring coverage.

Mitigation: Choose among explicit cost-versus-coverage profiles and approve reductions only after reviewing the trade-off.

## Reference(s):

- [Optimization Playbook](artifact/references/optimization-playbook.md)
- [Model Selection](artifact/references/model-selection.md)
- [Context Management](artifact/references/context-management.md)
- [Agent Orchestration](artifact/references/agent-orchestration.md)
- [Cron Optimization](artifact/references/cron-optimization.md)
- [Heartbeat Optimization](artifact/references/heartbeat-optimization.md)
- [Memory Patterns](artifact/references/memory-patterns.md)
- [Continuous Learning](artifact/references/continuous-learning.md)
- [Safeguards](artifact/references/safeguards.md)
- [OpenClaw](https://openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/phenomenoner/skills/openclaw-agent-optimize)
- [everything-claude-code Inspiration](https://github.com/affaan-m/everything-claude-code)
- [openclaw-mem](https://github.com/phenomenoner/openclaw-mem)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with structured audit sections, exact change proposals, rollback steps, and verification plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory-first output; persistent config, cron, heartbeat, memory, or skill-surface changes require explicit user approval.]

## Skill Version(s):

1.2.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
