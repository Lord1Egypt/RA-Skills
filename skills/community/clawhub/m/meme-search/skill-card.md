## Description:

搜索表情包图片，帮助 Agent 在回复中用图片表达情绪、状态和场景反应。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laizhenjie0107](https://clawhub.ai/user/laizhenjie0107)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate natural-language mood or context queries and embed returned meme image URLs in Markdown replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-generated mood and context queries may be sent to an unauthenticated third-party HTTP service.

Mitigation: Install only when that disclosure is acceptable, and avoid including sensitive context in meme queries.

Risk: Copying the SOUL.md block can make the meme reply behavior persist across future sessions.

Mitigation: Copy the block only when persistence is intended, and remove it later to fully disable the behavior.

Risk: Markdown image embeds load content from the third-party HTTP service and may fail or be rate limited silently.

Mitigation: Treat images as optional presentation and allow responses to continue without an image.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laizhenjie0107/skills/meme-search)
- [Meme search API endpoint](http://101.200.84.220/api/v1/meme/search?query={query})

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown image embeds with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return empty output when the API fails or is rate limited; images load from a third-party HTTP service.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
