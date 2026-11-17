## Description:

Collects public Douyin search results, creator posts, video comments, and real-time hot-list data as structured JSON for content research, competitor analysis, public opinion monitoring, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run Node.js CLI collectors for public Douyin content research, competitor monitoring, trend tracking, and comment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API tokens, search terms, and Douyin URLs to guaikei.com.

Mitigation: Use a dedicated token, avoid sensitive queries, and rotate the token if it may have been exposed.

Risk: The trigger guidance is broad enough to run on vague short-video research requests.

Mitigation: Confirm the user intends Douyin collection before executing commands for ambiguous requests.

Risk: Successful collection results are saved under the local logs directory.

Mitigation: Review, protect, or delete generated logs on shared machines or when queries contain sensitive research topics.

Risk: Response schemas include media URL fields while the skill says downloading is out of scope.

Mitigation: Treat returned media URLs as research metadata only and do not download or redistribute media unless separately authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-snapshot-collector)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Full option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)
- [Hot-list response schema](assets/hot_cli_resp.schema.json)
- [Guaikei service site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, text guidance]

**Output Format:** [JSON on stdout with operational messages on stderr and timestamped JSON logs under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; collection limits are controlled by CLI parameters and documented schemas.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
