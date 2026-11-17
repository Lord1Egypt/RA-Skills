## Description:

评估 LovAgents 到 AI-HIVE MCP 的内容层部分迁移，并生成可审阅、可追踪、可回退的样片迁移方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to evaluate a partial LovAgents-to-AI-HIVE migration for ecommerce images, short ads, social covers, and related media-generation handoffs. It helps preserve LovAgents-specific workspace functions while moving independently verifiable media nodes through an approval, cost, quality, and rollback workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may involve uploading brand-sensitive, copyrighted, or personal media assets to external generation services.

Mitigation: Use only owned or authorized assets, preserve source IDs and file hashes, and review AI-HIVE data handling terms before commercial use.

Risk: Cost-bearing AI-HIVE media tasks may run before the user has approved budget or route selection.

Mitigation: Require explicit approval for budget, model routing, uploads, generation, data writes, and publishing.

Risk: Users may overstate replacement claims without same-day, same-input comparison evidence.

Mitigation: Limit claims to partial migration unless current product capabilities and matched acceptance tests prove a stronger result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/lovagents-canvas-ai-hive-migration)
- [LovAgents official site](https://lovagents.com/)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [LovAgents official evidence and migration boundary](references/platform-evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and procedural checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration analysis, agent handoff guidance, MCP task structure, cost and quality acceptance criteria, and rollback guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
