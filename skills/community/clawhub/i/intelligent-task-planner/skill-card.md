## Description:

Intelligent Task Planner analyzes natural-language requests, identifies task intent, plans skill chains, and guides agents through task execution and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethvs](https://clawhub.ai/user/ethvs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route broad natural-language requests into task plans, skill matches, execution steps, and review checkpoints. It is intended for agents that need centralized planning across creative, research, coding, business, and everyday task categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to act as a global planner that can intercept all inputs, enforce exclusive routing, and override normal agent prompts.

Mitigation: Use it only when that control model is intentional; disable intercept_all, exclusive mode, prompt override, and enforced skill chains unless an administrator has approved them.

Risk: Automatic installation of matched skills can introduce unreviewed third-party components into an agent workflow.

Mitigation: Disable autoInstall by default, restrict sources to trusted registries, and review and scan skills before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ethvs/skills/intelligent-task-planner)
- [Publisher profile](https://clawhub.ai/user/ethvs)
- [Project homepage](https://github.com/ethvs/Intelligent-Task-Planner#readme)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text with task plans, skill-chain recommendations, examples, code snippets, shell commands, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose multi-step plans, quality gates, and installation or routing changes for downstream agent execution.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
