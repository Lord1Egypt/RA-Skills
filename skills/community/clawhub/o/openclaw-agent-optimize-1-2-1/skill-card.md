## Description: <br>
Provides advisory OpenClaw workspace audits and optimization plans for cost-aware routing, context discipline, delegation, and reliability without making persistent changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw workspaces, identify cost, context, model-routing, delegation, cron, and reliability issues, and receive prioritized change proposals with rollback and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed heartbeat, cron, configuration, or memory changes could affect cost, monitoring coverage, or retained workspace details. <br>
Mitigation: Review the exact diff, files written, expected impact, rollback plan, and post-change verification before approving any persistent change. <br>
Risk: Optional external tools mentioned by the skill may have separate security and operational properties. <br>
Mitigation: Review and approve optional tools such as openclaw-mem separately before installation or use. <br>


## Reference(s): <br>
- [Optimization Playbook](references/optimization-playbook.md) <br>
- [Model Selection](references/model-selection.md) <br>
- [Context Management](references/context-management.md) <br>
- [Agent Orchestration](references/agent-orchestration.md) <br>
- [Cron Optimization](references/cron-optimization.md) <br>
- [Heartbeat Optimization](references/heartbeat-optimization.md) <br>
- [Memory Patterns](references/memory-patterns.md) <br>
- [Continuous Learning](references/continuous-learning.md) <br>
- [Safeguards](references/safeguards.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [everything-claude-code inspiration](https://github.com/affaan-m/everything-claude-code) <br>
- [openclaw-mem optional companion](https://github.com/phenomenoner/openclaw-mem) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown with exact change proposals, rollback steps, verification plans, and optional inline commands or configuration patches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory-first output; persistent configuration, cron, heartbeat, or memory changes require explicit user approval.] <br>

## Skill Version(s): <br>
1.2.1 (source: SKILL.md frontmatter; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
