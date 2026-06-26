## Description: <br>
全网热榜追踪器，聚合微博、知乎、抖音、B站和小红书热搜榜单，支持趋势分析、话题监控和定时推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peterdog666](https://clawhub.ai/user/peterdog666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect public trending topics across major Chinese social platforms, compare trends against local history, monitor configured keywords, and generate recurring hotspot reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public and third-party trend APIs while collecting hot-list data. <br>
Mitigation: Install and run it only in environments where those outbound requests are acceptable. <br>
Risk: The skill saves local history, generated reports, and monitored keywords. <br>
Mitigation: Review the generated data and configuration directories, and avoid storing sensitive monitoring terms if local persistence is not appropriate. <br>
Risk: Optional cookies, scheduled runs, and push targets may expose sensitive session or notification data if misconfigured. <br>
Mitigation: Enable scheduled pushes intentionally, review webhook or email targets before use, and avoid providing real platform cookies unless they are required and protected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peterdog666/hotspot-radar) <br>
- [Artifact README](artifact/README.md) <br>
- [Weibo hot search API used by collector](https://weibo.com/ajax/statuses/hot_band) <br>
- [Luoying daily-hot API used by collector](https://apiserver.alcex.cn/daily-hot/) <br>
- [60s Rednote API used by collector](https://60s.viki.moe/v2/rednote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, interactive HTML reports, JSON history snapshots, local configuration files, and command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local history, trend, report, monitor, and optional push configuration files under the skill workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact package.json reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
