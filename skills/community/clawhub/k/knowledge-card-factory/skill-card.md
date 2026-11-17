## Description:

Knowledge Card Factory automates topic discovery, content research, AI-assisted visuals, and multi-platform publishing for knowledge-card content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, knowledge-sharing teams, and developers use this skill to turn a topic or trend into researched social content, knowledge-card visuals, captions, tags, and optional publishing output. It is intended for workflows that need search, cross-platform research, visual generation or rendering, and user-reviewed publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish content publicly through connected social-publishing skills.

Mitigation: Require a visible preview, verify the target account and platform, and obtain explicit approval immediately before each public post.

Risk: Search, cross-platform collection, and AI-generated content can introduce inaccurate, misleading, or rights-sensitive material.

Mitigation: Review sources, generated claims, captions, and images before use, and retain drafts when confidence is low.

Risk: Unpinned external skill dependencies may change behavior over time.

Mitigation: Prefer pinned or reviewed dependency versions where available and re-scan the workflow after dependency updates.

Risk: Notifications and workflow checkpoints may expose generated content or operational details to connected services.

Mitigation: Use only approved notification channels and avoid sending sensitive draft content unless the destination is authorized.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zlszhonglongshen/skills/knowledge-card-factory)
- [Publisher Profile](https://clawhub.ai/user/zlszhonglongshen)
- [brave-search Dependency](https://clawhub.ai/brave-search)
- [agent-reach Dependency](https://clawhub.ai/agent-reach)
- [nano-banana-pro Dependency](https://clawhub.ai/nano-banana-pro)
- [xiaohongshu-mcp Dependency](https://clawhub.ai/xiaohongshu-mcp)
- [card-renderer Optional Dependency](https://clawhub.ai/card-renderer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with code examples, JSON/YAML configuration snippets, generated content drafts, image file paths, tags, and publish URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal operation may depend on third-party search, scraping, image-generation, card-rendering, notification, and social-publishing skills; public posting should require preview and explicit user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter, workflow.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
