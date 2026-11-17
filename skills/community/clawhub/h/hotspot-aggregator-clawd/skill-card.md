## Description:

Aggregates trending topics from Weibo, Baidu, Zhihu, and Douyin, generates daily hotspot reports, and supports keyword subscription checks for content operations, creation, market analysis, and public-opinion monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect Chinese social-platform trending-topic data, generate Markdown reports, and check configured keywords for matching hotspots. It is intended for content planning, market monitoring, and public-opinion tracking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place untrusted internet content into an agent memory folder without clear isolation or sanitization.

Mitigation: Review generated reports before allowing an agent to treat them as memory or instructions, and add sanitization or trust-boundary handling before automated monitoring.

Risk: Real API mode fetches content from listed external sources and may require proxy use.

Mitigation: Keep USE_REAL_API disabled unless the operator trusts the listed sources and any configured proxy.

Risk: Broad Chinese-language triggers could invoke monitoring behavior more often than intended.

Mitigation: Narrow triggers and keyword subscriptions to the intended monitoring scope before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/hotspot-aggregator-clawd)
- [Publisher profile](https://clawhub.ai/user/onlyloveher)
- [Baidu hot search API endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Weibo hot search API endpoint](https://weibo.com/ajax/side/hotSearch)
- [Zhihu hot list API endpoint](https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total)
- [Douyin hot search aggregate API endpoint](https://api.oioweb.cn/api/toutiao/douyinHot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON hotspot data files, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes hotspot data and reports under /root/clawd/memory/hotspots; defaults to demonstration data unless USE_REAL_API is enabled.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
