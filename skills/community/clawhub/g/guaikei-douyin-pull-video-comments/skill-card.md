## Description:

Helps agents retrieve public Douyin search results, creator posts, video comments, and real-time hot-list data for operations, competitor research, public-opinion review, and topic monitoring; it does not support publishing, editing, downloads, or non-Douyin data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, operators, analysts, and developers use this skill to collect structured public Douyin data for content research, competitor monitoring, comment analysis, and trend tracking. It requires a GUAIKEI API token and is intended for lawful use of public data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the GUAIKEI token plus Douyin search terms or target URLs to a third-party service.

Mitigation: Use a scoped token where possible, keep it in the environment only, and rotate it immediately if it is exposed.

Risk: Fetched comments and profile or video data are saved under the skill logs directory by default.

Mitigation: Review log contents after runs and delete stored data that is no longer needed.

Risk: Security evidence reports that runtime auth errors contradict the skill's no-promotion rule.

Mitigation: Review authentication error output before deployment and avoid exposing promotional or contact text to end users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-pull-video-comments)
- [Full options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI request schema](assets/post_cli_req.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Comment CLI request schema](assets/comment_cli_req.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)
- [Hot CLI response schema](assets/hot_cli_resp.schema.json)
- [GUAIKEI service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON on stdout with stderr logs and optional saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command outputs can include up to 10,000 records per request when service limits permit.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, references/changelog.md, src/config/constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
