## Description: <br>
Helps agents find, recommend, mark, and review hot topics while tracking prior topic usage in a local SQLite history database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Linus995](https://clawhub.ai/user/Linus995) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators and external users use this skill to discover topic ideas, check or mark whether a topic has been used, get freshness-aware recommendations, and review recent topic history. It is not a real-time news or crisis-monitoring tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores topic history locally, which can expose sensitive content ideas or research topics on the user's machine. <br>
Mitigation: Avoid recording sensitive topics unless local storage under ~/.openclaw/data/topic_history.db is acceptable, and periodically review or remove stored history when needed. <br>
Risk: The artifact should not be relied on for live Weibo, Zhihu, Douyin, or other real-time trend monitoring. <br>
Mitigation: Use it for local topic inspiration and usage tracking, and verify current trends with an appropriate live source before publishing time-sensitive content. <br>
Risk: The topic-check script behavior is limited and may not reflect arbitrary user-provided topics as documented. <br>
Mitigation: Confirm check results against the stored topic history before treating a topic as unused. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Linus995/hot-topic-finder) <br>
- [Publisher profile](https://clawhub.ai/user/Linus995) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Console text and concise Markdown with Python script commands and local SQLite topic-history records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and stores topic history under ~/.openclaw/data/topic_history.db.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
