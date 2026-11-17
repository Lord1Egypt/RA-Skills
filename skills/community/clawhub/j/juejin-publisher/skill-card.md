## Description:

Publishes Markdown articles to Juejin through Juejin's official Cookie-authenticated API, with support for categories, tags, summaries, and cover images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devilwwj](https://clawhub.ai/user/devilwwj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to publish Markdown articles to Juejin from an agent or command line. It can create drafts or publish posts with frontmatter-driven title, summary, cover image, category, and tag settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a full Juejin browser Cookie that can act on the user's account.

Mitigation: Use a protected environment variable or local credential file, avoid passing the Cookie on the command line, and rotate it if it may have appeared in shell history or logs.

Risk: The default publishing flow can publish content immediately rather than only creating a draft.

Mitigation: Run in draft-only mode first to verify the article, category, tags, summary, and cover image before publishing.

## Reference(s):

- [Juejin Publisher ClawHub Listing](https://clawhub.ai/devilwwj/skills/juejin-publisher)
- [Juejin](https://juejin.cn)
- [Juejin Common Category IDs](artifact/references/category_ids.md)
- [Juejin Common Tag IDs](artifact/references/tag_ids.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance and terminal text with Juejin draft or post links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a draft or publish immediately depending on draft-only usage.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
