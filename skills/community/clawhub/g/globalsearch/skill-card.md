## Description:

Global Search helps agents run multi-source web searches through clb.ciglobal.cn and return aggregated references from live search and indexed sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzsn402](https://clawhub.ai/user/zzsn402)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to gather current web results, news, article references, and research leads across Baidu, Google, Baidu AI Search, and an indexed warehouse source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to clb.ciglobal.cn and may be associated with the API-key account.

Mitigation: Use only non-sensitive, redacted, or generalized queries and confirm the provider's privacy and retention practices before deployment.

Risk: The skill requires GLOBAL_SEARCH_API_KEY for external API access.

Mitigation: Store the key in environment variables or managed secrets and do not hardcode it in scripts or prompts.

Risk: Search results from multiple external sources may be incomplete, outdated, or misleading.

Mitigation: Review returned references and verify important claims against authoritative sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzsn402/skills/globalsearch)
- [Provider homepage](https://clb.ciglobal.cn)
- [API key portal](https://clb.ciglobal.cn/apiKey/login)
- [Search API endpoint](https://clb.ciglobal.cn/web_search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code examples and JSON-like search result references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GLOBAL_SEARCH_API_KEY and sends queries to an external search service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
