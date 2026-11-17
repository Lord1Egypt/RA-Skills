## Description:

Batch-fetches detailed performance metrics for known TikTok video IDs or URLs, including engagement, sales, GMV, creator, media, and attribution fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and ecommerce analysts use this skill to compare known TikTok videos side by side by views, likes, comments, shares, estimated sales, GMV, publish date, creator, and video flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send TikTok URLs, video IDs, analytics queries, account data, and payment workflow data to LinkFox services.

Mitigation: Use it only when the user trusts LinkFox for that data and verify that requests go to official LinkFox domains before execution.

Risk: Feedback submission can transmit a description of user intent, results, or problems.

Mitigation: Show and approve any feedback payload before sending it.

Risk: Full API responses and cache files may be written locally and can contain sensitive or proprietary analytics data.

Mitigation: Review, protect, and clean up local LinkFox output and cache files after use.

Risk: API keys may be exposed if stored in shell startup files or pasted into shared contexts.

Mitigation: Prefer session-scoped environment variables or secret storage where possible and avoid sharing the key in prompts or logs.

Risk: Repeated or high-volume calls consume paid LinkFox credits.

Mitigation: Tell the user before repeated calls and batch only the video IDs or URLs needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-batch-video-detail)
- [EchoTik batch video detail API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown comparison summaries with JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large responses are summarized while full responses are retained in local LinkFox data files; results may include estimated analytics rather than exact platform figures.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
