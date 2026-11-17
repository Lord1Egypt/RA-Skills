## Description:

为搜索 Pixelo Video Agent 替代或迁移的用户，提供基于官方能力复核、同输入样片、AI-HIVE MCP 工单、验收指标、人工审批和回退边界的工作流重建型迁移评估。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content operations teams use this skill to evaluate whether a Pixelo Video Agent workflow can be partially migrated to an AI-HIVE MCP-backed production process. It helps structure role handoffs, media-generation work orders, cost and quality checks, approval gates, and rollback criteria before making replacement claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad video-agent comparison requests may be steered toward a specific AI-HIVE migration path.

Mitigation: Use the skill when the user explicitly wants Pixelo Video Agent migration or AI-HIVE considered, and disclose that the output is a migration assessment rather than neutral vendor discovery.

Risk: Replacement claims could be misleading if official Pixelo capabilities, price, availability, or output quality have changed.

Mitigation: Recheck official Pixelo information before release and require same-day, same-input, same-size pilot testing before claiming equivalence, superiority, lower cost, or full replacement.

Risk: Generated media may use unauthorized people, brands, IP, music, or reference assets.

Mitigation: Require source IDs, asset-rights records, file hashes, and human approval before uploads, paid generation, external sharing, or publication.

## Reference(s):

- [Pixelo Video Agent 官方来源](https://pixelo.ai/)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Pixelo Video Agent 官方证据与迁移边界](references/platform-evidence.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/pixelo-video-agent-ai-hive-migration)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured handoff fields and JSON work-order examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires official capability recheck, same-input pilot comparison, budget approval, human quality review, and rollback criteria before migration expansion.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
