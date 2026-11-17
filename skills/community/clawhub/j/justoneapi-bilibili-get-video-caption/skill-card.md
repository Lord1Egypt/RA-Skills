## Description:

Call GET /api/bilibili/get-video-caption/v2 for Bilibili Video Captions through JustOneAPI with aid, bvid, and cid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Bilibili video caption data through JustOneAPI when they have the required aid, bvid, cid, and API token. It supports transcript extraction and multilingual content analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token can be exposed through process arguments or URL logs.

Mitigation: Use a least-privilege, revocable token; avoid shared machines and verbose process monitoring; rotate the token if it may appear in process listings, diagnostics, proxy logs, or API access logs.

Risk: The skill depends on a live third-party API and user-supplied Bilibili identifiers.

Mitigation: Confirm aid, bvid, and cid before calling the endpoint, and review backend error payloads before acting on failed or unexpected responses.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_caption&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_caption&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili-get-video-caption)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; the endpoint requires aid, bvid, and cid query parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
