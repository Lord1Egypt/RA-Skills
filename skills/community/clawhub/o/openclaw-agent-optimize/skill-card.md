## Description: <br>
Provides an advisory audit and prioritized optimization plan for OpenClaw workspaces, covering cost, model routing, context discipline, delegation, and reliability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phenomenoner](https://clawhub.ai/user/phenomenoner) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit agent workspaces and receive reversible optimization recommendations for cost control, context management, automation reliability, model tiering, and delegation. The skill is advisory-first and should present exact proposals, expected impact, rollback steps, and verification plans before persistent changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optimization advice may lead to persistent configuration, heartbeat, cron, sub-agent, or memory-file changes that affect monitoring coverage, reliability, or cost. <br>
Mitigation: Review proposed changes before applying them, require explicit approval, and confirm rollback and post-change verification steps. <br>
Risk: Optional companion tools such as openclaw-mem may add behavior outside this skill's documentation-only scope. <br>
Mitigation: Evaluate optional tools separately before installation or configuration. <br>


## Reference(s): <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub listing](https://clawhub.ai/phenomenoner/openclaw-agent-optimize) <br>
- [Optimization Playbook](references/optimization-playbook.md) <br>
- [Model Selection](references/model-selection.md) <br>
- [Context Management](references/context-management.md) <br>
- [Agent Orchestration](references/agent-orchestration.md) <br>
- [Cron Optimization](references/cron-optimization.md) <br>
- [Heartbeat Optimization](references/heartbeat-optimization.md) <br>
- [Memory Patterns](references/memory-patterns.md) <br>
- [Continuous Learning](references/continuous-learning.md) <br>
- [Safeguards](references/safeguards.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with exact change proposals, command snippets, rollback steps, and verification plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output only; persistent configuration or cron changes require explicit user approval.] <br>

## Skill Version(s): <br>
1.2.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
