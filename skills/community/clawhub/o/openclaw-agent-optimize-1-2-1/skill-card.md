## Description:

Provides structured audit, planning, and approval-gated optimization guidance for OpenClaw workspaces focused on cost, model routing, context discipline, delegation, and reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to audit agent workspaces and produce prioritized optimization plans with exact proposed changes, expected impact, rollback steps, and verification steps. It is intended for advisory use before approving persistent configuration, cron, memory, or routing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow may use an unpinned npx command, and optional companion components can introduce separate supply-chain or operational risk.

Mitigation: Review the install command before use, prefer a trusted manual install path when appropriate, and evaluate optional tools such as openclaw-mem or context-clean-up separately.

Risk: Optimization proposals can affect persistent configuration, cron behavior, memory files, or routing choices if approved without review.

Mitigation: Require the exact proposed change, expected impact, rollback plan, and verification step before approving any persistent change.

Risk: Reducing monitoring frequency or coverage can lower cost while missing signals that a user expects to keep.

Mitigation: Present coverage trade-offs as options and require the user to choose before applying a reduced-monitoring profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouhuihui008/skills/openclaw-agent-optimize-1-2-1)
- [OpenClaw](https://openclaw.ai)
- [Optimization Playbook](references/optimization-playbook.md)
- [Model Selection](references/model-selection.md)
- [Context Management](references/context-management.md)
- [Agent Orchestration](references/agent-orchestration.md)
- [Cron Optimization](references/cron-optimization.md)
- [Heartbeat Optimization](references/heartbeat-optimization.md)
- [Memory Patterns](references/memory-patterns.md)
- [Continuous Learning](references/continuous-learning.md)
- [Safeguards](references/safeguards.md)
- [openclaw-mem](https://github.com/phenomenoner/openclaw-mem)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with proposed commands or configuration patches when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory-first output with approval gates, rollback steps, and verification steps before persistent changes.]

## Skill Version(s):

1.2.1 (source: artifact/SKILL.md frontmatter and artifact/_meta.json; ClawHub release package version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
