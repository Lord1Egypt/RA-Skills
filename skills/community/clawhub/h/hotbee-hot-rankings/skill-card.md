## Description:

Retrieves HotBee hot-ranking data for Xiaohongshu, Douyin, Baidu, Weibo, and Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanye1402-hash](https://clawhub.ai/user/shanye1402-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to select confirmed HotBee hot-ranking endpoints and request trending-topic data for supported Chinese platforms while avoiding unsupported endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run a third-party GitHub-hosted package with local API-key access.

Mitigation: Install only after reviewing the package source, prefer a commit-pinned or registry-published version, and run dry-run mode before live calls.

Risk: HotBee API keys may be exposed through command history, local logs, or URL logging during live requests.

Mitigation: Provide HOTBEE_API_KEY through the local environment only, avoid echoing or persisting it, and use it only for approved live calls.

Risk: Hot-ranking calls may consume paid HotBee quota.

Mitigation: Start with dry-run mode, explain selected platforms and possible quota use, and confirm before making live paid requests.

## Reference(s):

- [Hot Rankings API](references/api.md)
- [HotBee Skills](https://www.hotbee.cn/skills)
- [ClawHub skill page](https://clawhub.ai/shanye1402-hash/skills/hotbee-hot-rankings)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown text with inline shell commands and API response field guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe HotBee API response fields such as title, score, word_type, rank_change, time, and tips when present.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
