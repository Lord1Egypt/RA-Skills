## Description: <br>
Fetches daily hot-topic rankings from Weibo, Zhihu, Baidu, Bilibili, Douyin, and Toutiao, then formats the results for Discord delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to collect trending-topic summaries from configured public news and social platforms and prepare a concise Discord-ready daily briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external news APIs and prepares output for a configured Discord thread. <br>
Mitigation: Confirm that the external API endpoints and Discord destination are intended before installing or scheduling the skill. <br>
Risk: The optional international-news module uses Currents and GNews API keys when provided. <br>
Mitigation: Provide only the intended API keys, and avoid running the optional module if international news is not needed. <br>
Risk: The fetch script stores a backup copy of generated Markdown under /tmp. <br>
Mitigation: Review host retention expectations for /tmp files or remove the backup behavior if local copies are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/hot-topics-daily) <br>
- [60s API project](https://github.com/vikiboss/60s) <br>
- [60s API endpoint](https://60s.viki.moe/v2) <br>
- [Currents API endpoint](https://api.currentsapi.services/v1) <br>
- [GNews API endpoint](https://gnews.io/api/v4) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text formatted for Discord, with configuration-driven platform selection and item limits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a temporary Markdown backup to /tmp/hot-topics-message.md when the Node.js fetch script runs.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
