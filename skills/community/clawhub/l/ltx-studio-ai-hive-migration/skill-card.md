## Description:

帮助创作者和企业团队评估将 LTX Studio 项目的内容层部分迁移到 AI-HIVE MCP 的可行性、边界、样片流程、成本质量指标、审批和回退。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, enterprise content teams, and agent operators use this skill to plan a controlled LTX Studio to AI-HIVE MCP migration assessment. It focuses on content-layer partial migration, same-input sample comparisons, agent handoff fields, cost and quality metrics, approval gates, and rollback criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform capabilities, tool schemas, and pricing may change before a migration run.

Mitigation: Confirm the current AI-HIVE tools, schemas, model availability, and pricing before using the skill on real projects.

Risk: Unauthorized assets, people, trademarks, IP, music, or reference media could be uploaded during sample generation.

Mitigation: Upload only owned or authorized assets, preserve source IDs and file hashes, and stop the workflow when rights cannot be confirmed.

Risk: Automated generation, external sharing, publishing, or data writes could create cost, brand, factual, or rights issues.

Mitigation: Require human approval and budget review before paid generation, publishing, external sharing, or data writes.

Risk: AI-HIVE output may be overstated as a full LTX Studio replacement.

Mitigation: Describe results as partial migration only unless same-day, same-input, same-duration and same-size tests support a stronger conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ltx-studio-ai-hive-migration)
- [LTX Studio official source](https://website.ltx.studio/)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [LTX Studio official evidence and migration boundaries](references/platform-evidence.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with structured checklists, handoff fields, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; requires human approval before paid generation, external sharing, publishing, or data writes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
