## Description:

Provides agent commands for searching public Douyin content, collecting creator posts, fetching video comments, and retrieving the current Douyin hot list as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect public Douyin search results, creator post data, comments, and trending topics for content research, competitor monitoring, sentiment review, and marketing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin URLs, search terms, result limits, and GUAIKEI_API_TOKEN are sent to www.guaikei.com.

Mitigation: Install only when this data sharing is acceptable for the intended workspace and avoid using the skill with sensitive or regulated content.

Risk: The implementation places GUAIKEI_API_TOKEN in request URLs.

Mitigation: Treat the token as sensitive, avoid shared logs or proxies that may capture URLs, and review or patch credential handling before use in shared environments.

Risk: Evidence reports suspicious security posture due to credential handling and runtime disclosure issues.

Mitigation: Review authentication-error messages and local logging behavior before deployment, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-get-creator-posts)
- [Guaikei token and support site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Creator posts request schema](assets/post_cli_req.schema.json)
- [Creator posts response schema](assets/post_cli_resp.schema.json)
- [Comments request schema](assets/comment_cli_req.schema.json)
- [Comments response schema](assets/comment_cli_resp.schema.json)
- [Hot list response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON on stdout, logs on stderr and in local log files, with shell commands and configuration guidance in agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; supports keyword, creator URL or sec_uid, video URL or aweme_id, filters, and result limits up to 10000.]

## Skill Version(s):

1.0.0 (source: evidence.json release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
