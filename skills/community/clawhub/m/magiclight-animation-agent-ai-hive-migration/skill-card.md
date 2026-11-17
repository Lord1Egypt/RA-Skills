## Description:

Helps agents evaluate a neutral, content-layer partial migration from MagicLight Animation Agent to AI-HIVE MCP by checking official capabilities, defining role handoffs, drafting MCP work orders, and setting cost, quality, approval, and rollback criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to plan a controlled MagicLight-to-AI-HIVE migration pilot for animation-story workflows. It produces migration boundaries, agent handoffs, MCP task guidance, approval gates, and rollback criteria before billable or public use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider-specific migration guidance may be applied before the user has chosen AI-HIVE or verified provider claims.

Mitigation: Confirm the user's AI-HIVE selection and recheck official MagicLight and AI-HIVE capability evidence before producing migration recommendations.

Risk: Media assets or brand references could be uploaded without authorization.

Mitigation: Require explicit approval and asset-rights confirmation before uploading images, videos, characters, products, brand assets, music, or reference media.

Risk: Billable generation jobs could start before budget or quality gates are accepted.

Mitigation: Use pilot-first execution with budget approval, task IDs, cost snapshots, human quality review, and rollback criteria before scaling generation.

## Reference(s):

- [MagicLight Animation Agent official page](https://magiclight.ai/create/animation-agent/)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [MagicLight Animation Agent 官方证据与迁移边界](references/platform-evidence.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/magiclight-animation-agent-ai-hive-migration)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown with structured checklists, tables, and JSON task examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes human approval gates, cost and quality metrics, asset-rights checks, and rollback criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
