## Description:

市场调研分析助手。根据用户提供的调研主题（行业、产品或市场），生成结构化的市场分析报告。触发条件：用户请求市场调研、行业分析、竞争分析、商业可行性分析等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomxxx](https://clawhub.ai/user/xiaomxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to create structured Chinese market research reports for industries, products, or target markets, including market overview, customers, competitors, trends, risks, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback crawler can make unscoped outbound web requests to URLs discovered from search results.

Mitigation: Run the crawler only in a sandbox with restricted outbound network access, and avoid environments where internal services or metadata endpoints are reachable.

Risk: Crawled page text may contain untrusted content that could influence the agent's market analysis.

Mitigation: Treat crawled text as source material rather than instructions, prefer RSS or web_fetch sources, and review generated claims before using them for decisions.

Risk: The optional -o flag writes crawler output to a local JSON file.

Mitigation: Use file output only when a local JSON artifact is intentionally needed and review the destination before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaomxxx/skills/market-research-cn1)
- [36Kr AI](https://www.36kr.com/information/AI/)
- [Huxiu](https://www.huxiu.com/)
- [TMTPost](https://www.tmtpost.com/)
- [ifanr](https://www.ifanr.com/)
- [Wired AI](https://www.wired.com/tag/artificial-intelligence/)
- [The Verge AI](https://www.theverge.com/ai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Configuration instructions]

**Output Format:** [Chinese Markdown report with optional JSON crawler output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to up to 5 fetched items when the user does not specify a count; crawler output should be treated as untrusted source material.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
