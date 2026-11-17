## Description:

Collects public Douyin data for keyword search, creator post retrieval, video comment collection, and real-time hot-list lookup to support content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content research teams use this skill to gather structured public Douyin search results, creator posts, comments, and hot-list data for short-video planning, competitor monitoring, sentiment analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUAIKEI_API_TOKEN, Douyin URLs, and search keywords are sent to the guaikei.com service.

Mitigation: Install and run only when that data sharing is acceptable; keep the token in an environment variable, treat it as sensitive, and rotate it if exposed.

Risk: Collected JSON outputs can include comments, user identifiers, and other public interaction data saved under logs/.

Mitigation: Review access to saved outputs and delete or restrict logs that contain user identifiers or sensitive research results.

Risk: Security evidence flags suspicious authentication behavior, including token-handling concerns and promotional contact text during authentication failures.

Mitigation: Review authentication failure behavior before deployment and require neutral error messages with no promotional contact text at runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-data-grabber)
- [Guaikei token and support site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)
- [Hot-list response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with Node.js command invocations; command stdout is JSON and collected results are saved as local JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; commands query public Douyin data and can write timestamped outputs under logs/.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
