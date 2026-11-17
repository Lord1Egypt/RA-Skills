## Description:

妈妈网爬虫按分类或关键词抓取 mama.cn PC 端育儿文章，并将标题、来源、日期、链接和正文保存为本地 Markdown 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zton100](https://clawhub.ai/user/zton100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to collect mama.cn parenting articles by category or keyword and save them as local Markdown files for later review or indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler disables HTTPS certificate verification while fetching web pages.

Mitigation: Remove curl -k, fail closed on HTTPS errors, and run only on trusted networks until certificate verification is restored.

Risk: Fetched articles are saved into a persistent local knowledge folder and may contain untrusted web content.

Mitigation: Treat saved Markdown as data, review it before reuse, and avoid feeding it back into an agent as instructions.

Risk: Crawling and persistent writes can collect and store more content than intended.

Mitigation: Require explicit user approval for crawl scope and local writes, and use conservative max-pages and max-articles limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zton100/skills/mama-crawler)
- [Mama.cn parenting site](https://www.mama.cn/)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, guidance]

**Output Format:** [Markdown files saved locally, with terminal progress text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saved articles include title, source, date, URL, and extracted body text.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
