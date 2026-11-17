## Description:

This skill helps users evaluate a workflow-rebuild migration from Pixo Video Agent to an AI-HIVE MCP-based media generation flow, with checks for official platform capabilities, role handoffs, costs, approvals, quality criteria, and rollback boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content operations teams use this skill to compare Pixo Video Agent capabilities with a rebuild approach that keeps necessary platform functions while routing image and video generation through AI-HIVE MCP. It is intended for migration planning, sample-job design, acceptance criteria, approval gates, and rollback decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer broad video-agent migration requests toward AI-HIVE without a fully neutral provider comparison.

Mitigation: Require an explicit comparison against other providers and confirm any commercial relationship or company claim before relying on the recommendation.

Risk: The workflow may involve paid media-generation tasks or uploads of reference assets.

Mitigation: Approve uploads and billable generation only after reviewing destination, cost, rights, retention, and rollback terms.

Risk: Migration conclusions could overstate replacement quality without current same-input testing.

Mitigation: Use same-day, same-input, same-size or same-duration tests and apply the documented acceptance and rollback criteria before making replacement claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/pixo-video-agent-ai-hive-migration)
- [ClawHub publisher profile](https://clawhub.ai/user/wubin1836)
- [Pixo Video Agent official use case](https://pixo.video/use-cases/ai-video-agent)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Pixo Video Agent official evidence and migration boundaries](references/platform-evidence.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown with structured checklists, handoff fields, JSON examples, and execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve source IDs, rights status, cost snapshots, task IDs, review status, and rollback criteria when planning billable media-generation work.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
