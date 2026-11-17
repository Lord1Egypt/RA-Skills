## Description:

Provides Chinese-language guidance for evaluating and planning an OiiOii-to-AI-HIVE MCP workflow migration, including capability verification, pilot production handoffs, cost and quality metrics, approvals, and rollback boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, creative teams, and migration planners use this skill to assess whether OiiOii production workflows can be rebuilt with host-agent roles and AI-HIVE MCP image/video generation. It helps produce scoped migration plans, sample-production acceptance criteria, approval gates, and rollback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OiiOii or AI-HIVE capabilities, availability, or pricing may change after the skill's evidence snapshot.

Mitigation: Re-verify current platform capabilities and pricing before production use or comparative claims.

Risk: Paid generation or external media processing could occur without proper approval.

Mitigation: Require manual approval for paid generation, uploads, publishing, and other external actions.

Risk: Uploaded reference media, people, brands, music, or IP may be unauthorized.

Mitigation: Use only owned or explicitly authorized assets and preserve source IDs, rights notes, and file hashes.

Risk: Broad AI-video or storyboard requests may be steered toward this vendor-specific migration workflow.

Mitigation: Confirm that the user's intent is an OiiOii-to-AI-HIVE migration before applying the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/oiioii-agent-studio-ai-hive-migration)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)
- [OiiOii How It Works](https://www.oiioii.ai/how-it-works)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [OiiOii Official Evidence and Migration Boundaries](references/platform-evidence.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with structured checklists, tables, and JSON work-order examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language migration-planning output with approval, cost, quality, and rollback controls]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
