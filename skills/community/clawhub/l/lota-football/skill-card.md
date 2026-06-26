## Description: <br>
查询足球比赛列表和单场特征报告。使用两个独立脚本：lota_football_matches.sh 处理列表查询，lota_compact_fet.sh 获取特征文本, lota_fetch_future_24h自动化获取未来24小时内数据. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingvergil](https://clawhub.ai/user/kingvergil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query Lota football match lists, identify specific matches by date or ID, and retrieve compact single-match feature reports through local cache files or bash API clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed through shell history, crontab entries, logs, or process environments. <br>
Mitigation: Store LOTA_API_KEY outside command history and crontab lines where possible, limit log exposure, and remove scheduled jobs when continuous updates are no longer needed. <br>
Risk: The bundled scripts default to an unencrypted HTTP API base URL. <br>
Mitigation: Set LOTA_API_BASE_URL to an HTTPS endpoint if the service supports it before running live API calls. <br>
Risk: Cached match data and logs are written under lota_data and may include operational details. <br>
Mitigation: Restrict filesystem permissions on lota_data and generated logs, and review retention needs for cached data. <br>
Risk: Scheduled fetching can consume API quota or continue after it is no longer needed. <br>
Mitigation: Monitor quota usage, keep the cache-first workflow enabled, and remove cron entries when automated updates are not required. <br>


## Reference(s): <br>
- [Lota Football ClawHub release](https://clawhub.ai/kingvergil/lota-football) <br>
- [Publisher profile: kingvergil](https://clawhub.ai/user/kingvergil) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with bash commands and JSON or plain-text football data outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOTA_API_KEY for live API calls; prefers local lota_data cache files before making requests.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
