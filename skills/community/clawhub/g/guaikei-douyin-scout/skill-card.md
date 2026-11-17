## Description:

Searches Douyin public content, retrieves creator posts and video comments, and checks the real-time hot list for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather structured public Douyin data for content planning, competitor monitoring, comment review, and trend tracking. It is limited to Douyin search, creator-post retrieval, video-comment retrieval, and hot-list lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication failure handling may show promotional contact details.

Mitigation: Before deployment, confirm invalid-token paths return only neutral remediation guidance and do not display promotional contact information at runtime.

Risk: The API token may be sent in URL query strings.

Mitigation: Treat the token as sensitive, avoid sharing logs or captured URLs, and ask the publisher to move token transmission to an Authorization header.

Risk: Broad natural-language triggers may run the skill for ambiguous short-video research requests.

Mitigation: Use the skill only for explicit Douyin public-data tasks and confirm the platform and operation before collecting data.

Risk: Results may be stored locally as JSON logs.

Mitigation: Avoid sensitive research terms or private target URLs, and review log retention or disable/manage logs before use in sensitive environments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-scout)
- [Usage documentation](artifact/readme.md)
- [Command options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Search request schema](artifact/assets/search_cli_req.schema.json)
- [Search response schema](artifact/assets/search_cli_resp.schema.json)
- [Post request schema](artifact/assets/post_cli_req.schema.json)
- [Post response schema](artifact/assets/post_cli_resp.schema.json)
- [Comment request schema](artifact/assets/comment_cli_req.schema.json)
- [Comment response schema](artifact/assets/comment_cli_resp.schema.json)
- [Hot-list response schema](artifact/assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON on stdout, operational logs on stderr, and optional timestamped JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN. Supports search, creator-post, comment, and hot-list command modes with documented filters and limits up to 10000 results.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
