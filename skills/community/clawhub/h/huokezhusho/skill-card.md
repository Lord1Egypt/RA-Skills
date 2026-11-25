## Description:

抖音公域评论区精准获客工具。当用户需要「挖掘潜在客户/销售线索、竞品评论区截流、私域引流、按关键词找抖音高意向用户」时启用。标准流程：①关键词搜索视频拿到 aweme_id → ②用 aweme_id 拉取评论、提取客户信息（昵称/uid/sec_uid/地区/评论内容）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External marketing, sales, and content teams use this skill to search public Douyin videos, creators, comments, and trending topics for content ideas, audience needs, competitor research, and potential public-facing leads. It summarizes selected results and supports a search-to-comments workflow; it does not retrieve private contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and supplied Douyin links or IDs are sent to the third-party Guaikei API.

Mitigation: Use only public content identifiers relevant to the user's request, and make clear that the query is sent to Guaikei before running it. Do not send private data.

## Reference(s):

- [Customer acquisition workflow](artifact/references/customer-acquisition.md)
- [Demand mining workflow](artifact/references/demand-mining.md)
- [Command routing guide](artifact/references/routing.md)
- [Output contract](artifact/references/contract.md)
- [Guaikei service](https://www.guaikei.com)
- [ClawHub release](https://clawhub.ai/engheng-art/skills/huokezhusho)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown, Shell commands]

**Output Format:** [Structured JSON query results with concise Markdown summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarize selected fields instead of pasting full result payloads. Results concern public content and account data.]

## Skill Version(s):

1.4.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
