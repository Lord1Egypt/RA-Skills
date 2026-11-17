## Description:

OpenClaw 文档知识库 - 搜索与同步 / OpenClaw Documentation Knowledge Base - Search & Sync

This skill is ready for commercial/non-commercial use.

## Publisher:

[sushengbuyu](https://clawhub.ai/user/sushengbuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search a bundled OpenClaw documentation index, browse documentation categories, and optionally refresh the local documentation cache from the OpenClaw docs site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional sync command contacts docs.openclaw.ai and updates generated documentation files in the skill directory.

Mitigation: Run sync only when refreshing the bundled documentation index, and review generated file changes before relying on updated results.

Risk: Search results depend on the bundled documentation index and may lag behind the live OpenClaw documentation.

Mitigation: Use the sync command before workflows that require current documentation, or cross-check important answers against the OpenClaw documentation site.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text search results or JSON result objects, with Markdown and bash examples in the skill instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output can be filtered by category, limited by result count, or returned as JSON for agent consumption.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
