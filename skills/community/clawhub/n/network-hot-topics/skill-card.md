## Description: <br>
Gets current online hot topics from platforms such as Weibo, Zhihu, and Baidu, then summarizes them into 10 concise items with a title and one-sentence summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akang943578](https://clawhub.ai/user/akang943578) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather a brief daily snapshot of public online trends across multiple platforms. It is intended for hot-topic summaries, trend briefs, and quick news-awareness checks rather than deep analysis of a single topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts search providers or public hot-topic APIs, so results may depend on provider availability and freshness. <br>
Mitigation: Review the generated list for stale or missing topics and include the retrieval time when using the summary for time-sensitive decisions. <br>
Risk: Trend queries may be sent to external search providers or public APIs. <br>
Mitigation: Do not include sensitive private information in prompts that trigger live searches. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/akang943578/network-hot-topics) <br>
- [Weibo hot search API](https://weibo.com/ajax/side/hotSearch) <br>
- [Zhihu hot list](https://www.zhihu.com/hot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown numbered list with 10 topic titles and one-sentence summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May note the retrieval time or source availability because public trend data may not be real-time to the second.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
