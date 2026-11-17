## Description:

全网热榜追踪器，聚合微博、知乎、抖音、B站和小红书热搜榜单，支持趋势分析、话题监控和定时推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterdog666](https://clawhub.ai/user/peterdog666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect public trending topics across major Chinese social platforms, compare trends over time, monitor configured keywords, and generate daily hotspot reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute unsafe browser code from external trend data or an unaudited CDN script.

Mitigation: View generated HTML in a contained environment, avoid sharing reports without review, and fix inline JSON serialization and external CDN loading before broad deployment.

Risk: The skill fetches public trend data from third-party endpoints and may use optional account cookies or push webhooks.

Mitigation: Use without account cookies where possible, treat cookies and webhook settings as credentials, and limit local report retention to what users need.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peterdog666/skills/hotspot-radar)
- [Weibo hot search endpoint](https://weibo.com/ajax/statuses/hot_band)
- [Luoying daily hot API](https://apiserver.alcex.cn/daily-hot/)
- [60s rednote API](https://60s.viki.moe/v2/rednote)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, HTML reports, JSON snapshots, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local history, trend snapshots, reports, monitor keywords, and optional push configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact package.json lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
