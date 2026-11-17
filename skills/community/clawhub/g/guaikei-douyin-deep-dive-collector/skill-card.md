## Description:

Collects public Douyin search results, creator posts, video comments, and hot-list data for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, marketers, and analysts use this skill to collect public Douyin search results, creator posts, comments, and hot-list entries for topic discovery, competitor analysis, sentiment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill sends Douyin URLs, search terms, and GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Use a dedicated token in a trusted environment, avoid sensitive search terms, and rotate the token after use with this version.

Risk: The security review says collected JSON is saved locally and should be handled carefully.

Mitigation: Review and periodically clean the logs directory, and avoid storing sensitive or unnecessary research data.

Risk: The security review says the skill can trigger too broadly on generic research requests.

Mitigation: Use it only for clearly Douyin-specific public-data tasks and confirm the target platform before running collection commands.

Risk: The security review says authentication-error behavior needs review.

Mitigation: Stop on token errors, do not retry invalid credentials, and keep user-facing remediation neutral.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-deep-dive-collector)
- [Usage documentation](readme.md)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search input schema](assets/search_cli_req.schema.json)
- [Search output schema](assets/search_cli_resp.schema.json)
- [Creator posts input schema](assets/post_cli_req.schema.json)
- [Creator posts output schema](assets/post_cli_resp.schema.json)
- [Comments input schema](assets/comment_cli_req.schema.json)
- [Comments output schema](assets/comment_cli_resp.schema.json)
- [Hot-list output schema](assets/hot_cli_resp.schema.json)
- [Guaikei token and support site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [JSON data from CLI stdout, with logs and collected results saved as JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; supports search, creator posts, comments, and hot-list commands with documented limits up to 10000 records.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
