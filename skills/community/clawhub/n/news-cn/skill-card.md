## Description:

中文新闻门户列表抓取，可输出 Markdown 简报或 JSON/RSS，无需新闻类 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect Chinese news links from supported portal list pages or RSS feeds and produce concise briefs for aggregation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch web content from URLs supplied to it.

Mitigation: Use NEWS_CN_ALLOW_HOSTS to restrict requests to trusted news domains and avoid arbitrary URLs from untrusted prompts.

Risk: Private-network protections are incomplete or can be configured off.

Mitigation: Keep NEWS_CN_BLOCK_PRIVATE enabled and review any environment changes before deployment.

Risk: Dependency behavior may change if beautifulsoup4 is installed without version control.

Mitigation: Pin beautifulsoup4 in the execution environment before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/news-cn)
- [Publisher profile: jisuapi](https://clawhub.ai/user/jisuapi)
- [JisuAPI website](https://www.jisuapi.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown digest, JSON item list, or JSON preset listing emitted to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch mode accepts JSON request parameters for sources, mode, limits, deduplication, timeout, and output format.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
