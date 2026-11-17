## Description:

Analyze Bilibili workflows with JustOneAPI, including video Details, user Published Videos, and user Profile across 9 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content operations teams use this skill to retrieve API-backed Bilibili video, user, comment, danmaku, caption, search, and share-link data when they have the required Bilibili identifiers or filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command-line arguments and URL query parameters, which may expose it in command logs, process telemetry, traces, or URL logs.

Mitigation: Use a scoped or low-privilege token when available, avoid sharing logs or traces that may contain the token, and rotate the token if exposure is suspected.

Risk: The skill depends on user-provided Bilibili identifiers and filters; incorrect inputs can produce irrelevant API-backed results.

Mitigation: Ask for missing required parameters and echo key filters such as aid, bvid, cid, page, uid, keyword, or shareUrl when presenting results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili&utm_content=project_link)
- [Just One API dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with selected JSON API results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and operation-specific Bilibili identifiers or filters.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
