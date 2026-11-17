## Description:

皮皮虾数据查询助手。覆盖作品详情、用户数据、搜索、热搜、评论、话题等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and community operators use this skill to query and analyze PiPiXia posts, user profiles, comments, search results, trending boards, and topics through MaxHub APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises a read-only posture while also referencing view-count increase behavior.

Mitigation: Review the skill before installing, do not rely on it as purely read-only, and remove or clarify the mismatched behavior before production use.

Risk: The artifact includes non-PiPiXia fallback routes that do not match the stated PiPiXia data-query purpose.

Mitigation: Constrain use to documented PiPiXia endpoints and verify endpoint paths before allowing API calls.

Risk: The short-link feature could receive private or token-bearing URLs.

Mitigation: Avoid submitting private, sensitive, or credential-bearing URLs to the short-link endpoint.

Risk: The skill requires a MaxHub API key for API-backed queries.

Mitigation: Use only a MaxHub API key scoped to this provider and keep credential values out of prompts and outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/new-ironman/skills/pipixia-aggregate-scraper)
- [MaxHub API Website](https://www.aconfig.cn)
- [Post & User API Reference](artifact/references/api-post-user.md)
- [Search & Trending API Reference](artifact/references/api-search-trending.md)
- [Parameter Mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, bullet lists, and inline shell commands; API response data may be summarized from JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English responses; requires MAXHUB_API_KEY and curl for API-backed queries.]

## Skill Version(s):

3.6.1 (source: server release metadata, skill frontmatter, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
