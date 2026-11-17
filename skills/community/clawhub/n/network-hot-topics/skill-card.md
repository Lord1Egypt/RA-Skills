## Description:

Fetches current online hot topics from public search results or trend sources such as Weibo, Zhihu, and Baidu, then summarizes the selected topics as concise title-and-summary items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akang943578](https://clawhub.ai/user/akang943578)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create a brief current-events digest from public online trend sources when they need a quick multi-platform hot-topic summary rather than deep analysis of a single topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing through a mutable npx @latest command can expose users to package-version supply-chain risk.

Mitigation: Prefer ClawHub's trusted import flow or verify and pin the clawhub CLI package and version before installation.

Risk: Trend summaries depend on public web search or public trend APIs and may be incomplete, stale, or unavailable.

Mitigation: Show retrieval timing when useful, avoid inventing topics, and fall back to additional public sources when one source has insufficient data.

Risk: The skill may return Chinese-formatted summaries by default.

Mitigation: Honor the user's requested language or explicitly state the language used in the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akang943578/skills/network-hot-topics)
- [Publisher profile](https://clawhub.ai/user/akang943578)
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch)
- [Zhihu hot list](https://www.zhihu.com/hot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown numbered list of hot-topic titles with one-sentence summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normally produces 10 concise items; requires current web search or public trend-source access and may use Chinese wording by default.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
