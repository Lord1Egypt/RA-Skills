## Description: <br>
定时获取AI行业最新资讯，整理成每日早报发送给用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who want a scheduled AI industry briefing use this skill to collect recent AI news, summarize major developments and trends, and post a concise daily report to a configured messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically posts reports to an enterprise messaging channel. <br>
Mitigation: Confirm the target channel and recipients, test in a non-production channel first, and disable or edit the cron job when only manual reports are desired. <br>
Risk: News gathering and message delivery may send prompts or report content through external search and messaging providers. <br>
Mitigation: Use only approved providers and avoid including sensitive internal prompts or private data in the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrxparley/parley-ai-daily-news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown-style daily briefing with optional scheduled messaging configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for a daily 08:30 Asia/Shanghai cron schedule and manual invocation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
