## Description:

Call GET /api/xiaohongshu/share-url-transfer/v1 for Xiaohongshu (RedNote) Share Link Resolution through JustOneAPI with shareUrl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to resolve Xiaohongshu (RedNote) share links through JustOneAPI and extract data such as note IDs for downstream note or comment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent as a URL query parameter and may be exposed through chat, logs, screenshots, or request traces if mishandled.

Mitigation: Use the narrowest token available, avoid pasting token values into chat or logs, and rotate the token if exposure is possible.

## Reference(s):

- [JustOneAPI API homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_share_url_transfer&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a shareUrl query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
