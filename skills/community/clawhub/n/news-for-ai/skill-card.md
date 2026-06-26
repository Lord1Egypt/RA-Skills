## Description: <br>
Fetches real-time AI industry news, daily digests, and search results for AI topics, products, models, and MCP services, returning structured JSON with clean text and separated media resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sskun](https://clawhub.ai/user/sskun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content workflows use this skill to gather current AI news, daily summaries, and topic-specific AI source material for article drafting, monitoring, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python dependencies are declared with minimum versions rather than pinned versions. <br>
Mitigation: Install in a virtual environment and use a lockfile or pinned dependency set before production use. <br>
Risk: Search terms and article fetches are sent to AIBase domains. <br>
Mitigation: Avoid submitting confidential keywords or sensitive unpublished topics through this skill. <br>
Risk: Fetched news, product, model, and MCP information may be incomplete, stale, or shaped by the upstream site. <br>
Mitigation: Review returned sources and verify important facts before publishing or acting on the output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sskun/news-for-ai) <br>
- [Publisher profile](https://clawhub.ai/user/sskun) <br>
- [AIBase news](https://news.aibase.cn/news) <br>
- [AIBase daily](https://news.aibase.cn/daily) <br>
- [AIBase search](https://www.aibase.cn/search/) <br>
- [Output schemas](artifact/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON with Markdown text fields and separated image, video, and link arrays.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands write JSON to stdout and errors to stderr; --no-content omits article body and media fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
