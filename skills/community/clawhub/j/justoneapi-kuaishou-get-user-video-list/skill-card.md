## Description:

Call GET /api/kuaishou/get-user-video-list/v2 for Kuaishou User Published Videos through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve a Kuaishou user's published video metadata through JustOneAPI for creator monitoring and content performance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through the command line and URL query string, where it may appear in logs or process metadata.

Mitigation: Use narrowly scoped or disposable tokens when available, avoid sharing command output or process listings, and rotate the token if exposure is suspected.

Risk: The skill retrieves third-party Kuaishou creator video metadata and returns backend response JSON.

Mitigation: Confirm the requested userId is appropriate for the task and avoid sharing response JSON beyond the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-kuaishou-get-user-video-list)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_video_list&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_video_list&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Short Markdown summary followed by raw JSON from the JustOneAPI response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; userId is required and pcursor is optional.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
