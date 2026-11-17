## Description:

Hot Topics Daily fetches trending topics from Weibo, Zhihu, Baidu, Bilibili, Douyin, and Toutiao and formats a Discord-oriented daily roundup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation operators use this skill to fetch daily trending topics from configured Chinese platforms and produce a Discord-ready roundup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled outbound retrieval and Discord-oriented posting can send current-topic content to an unintended destination.

Mitigation: Confirm the Discord destination before enabling automation and run the skill as an unprivileged account.

Risk: The backup news module uses Currents and GNews API keys that are not central to the described hot-topic roundup.

Mitigation: Document or remove the backup module, and use only limited API keys if it remains enabled.

Risk: The push script writes a backup to a fixed path under /tmp.

Mitigation: Remove the backup write or change it to a safer per-run path before scheduled use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/hot-topics-daily)
- [60s API repository](https://github.com/vikiboss/60s)
- [60s API base URL](https://60s.viki.moe/v2)
- [Currents API](https://api.currentsapi.services/v1)
- [GNews API](https://gnews.io/api/v4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-formatted Discord message and concise shell or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads configurable platform settings, emits one roundup message, and may write a local backup message file.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
