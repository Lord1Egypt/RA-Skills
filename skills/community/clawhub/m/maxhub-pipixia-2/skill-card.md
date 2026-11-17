## Description:

皮皮虾数据查询助手。覆盖作品详情、用户数据、搜索、热搜、评论、话题等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, community researchers, and other users can query PiPiXia post, user, search, trending, comment, and topic data, then receive concise summaries or comparisons to inform content and community analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security assessment marks this release suspicious: its references describe capabilities beyond the stated data-query purpose, installation is unpinned, and analysis was partial; no clear malicious intent is reported.

Mitigation: Follow the server guidance: avoid installation until the publisher explains the extra capabilities and provides a version-pinned installation method; review the complete package before use.

Risk: The artifact describes an increase_post_view_count operation alongside its data-query features, while also describing the endpoints as read-only.

Mitigation: Clarify this documented capability with the publisher and avoid invoking it unless its behavior and intended use are confirmed.

## Reference(s):

- [Post and user API reference](artifact/references/api-post-user.md)
- [Search and trending API reference](artifact/references/api-search-trending.md)
- [Parameter mappings](artifact/references/param-mappings.md)
- [MaxHub API website](https://www.aconfig.cn)
- [Server-resolved source repository](https://github.com/XieWxx/maxhub-pipixia)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown summaries, tables, and follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese or English responses with API-backed query results; an API key is required for data access.]

## Skill Version(s):

3.6.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
