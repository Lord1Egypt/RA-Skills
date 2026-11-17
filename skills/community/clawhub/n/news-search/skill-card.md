## Description:

Searches Baidu News, Toutiao, Bing News, Google News, and Sina News, then aggregates and deduplicates news results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlutwuwei](https://clawhub.ai/user/dlutwuwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to run keyword-based news searches across multiple news search services and receive deduplicated result lists with titles, links, sources, channels, and times when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives a headless browser against third-party search sites and the security evidence flags this as suspicious.

Mitigation: Install only when this behavior is acceptable for the intended environment and review the dependency set before deployment.

Risk: The skill disables Chromium sandboxing while visiting external sites.

Mitigation: Run it in an isolated, non-root environment and consider removing the no-sandbox launch flags before use on systems with sensitive files or credentials.

Risk: The skill uses an anti-bot stealth plugin.

Mitigation: Confirm that use of browser automation and stealth behavior is acceptable for the target sites and deployment policy; consider removing the stealth plugin when it is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlutwuwei/skills/news-search)
- [Baidu News search](https://www.baidu.com/s?tn=news&word={keyword})
- [Toutiao news search](https://so.toutiao.com/search?keyword={keyword}&pd=news)
- [Bing News search](https://www.bing.com/news/search?q={keyword})
- [Google News search](https://news.google.com/search?q={keyword})
- [Sina News search](https://search.sina.com.cn/?q={keyword}&c=news)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown or JSON news result list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are deduplicated by link; caller can choose engine, per-engine maximum result count, and output format.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
