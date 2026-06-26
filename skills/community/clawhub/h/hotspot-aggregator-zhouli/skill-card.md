## Description: <br>
Hotspot Aggregator helps an agent collect trending topics from Weibo, Baidu, Zhihu, and Douyin, generate daily hotspot reports, and check subscribed keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, creators, market analysts, and public-opinion monitoring teams use this skill to collect social trend data, produce daily markdown reports, and track keyword matches across supported platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports, fetched hotspot data, and keyword lists can be retained locally under /root/clawd/memory/hotspots. <br>
Mitigation: Review local retention expectations before use, restrict access to that directory, and delete reports or keyword lists when they are no longer needed. <br>
Risk: Real API mode can contact external trend APIs and may require a proxy for some platforms. <br>
Mitigation: Leave real API mode disabled unless external network calls are intended, and verify proxy and API access policies before enabling it. <br>
Risk: Adding the suggested cron entry creates ongoing daily execution. <br>
Mitigation: Install the cron entry only when recurring collection is desired, and monitor scheduled runs for volume and API-rate impact. <br>


## Reference(s): <br>
- [Hotspot Aggregator ClawHub listing](https://clawhub.ai/onlyloveher/hotspot-aggregator-zhouli) <br>
- [Publisher profile](https://clawhub.ai/user/onlyloveher) <br>
- [Weibo hot search API](https://weibo.com/ajax/side/hotSearch) <br>
- [Baidu hot search API](https://top.baidu.com/api/board?platform=wise&tab=realtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON hotspot data, and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports and keyword data under /root/clawd/memory/hotspots when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, skill.yaml, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
