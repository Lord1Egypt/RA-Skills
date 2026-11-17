## Description:

Collects public Douyin data for keyword video search, creator post fetching, video comment reading, and real-time hot ranking queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content researchers, and marketing teams use this skill to gather structured public Douyin data for short-video research, competitive analysis, sentiment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable API token may be sent in URLs.

Mitigation: Use a scoped token, keep it in the GUAIKEI_API_TOKEN environment variable, rotate it if exposed, and avoid sharing command output or logs that may reveal request details.

Risk: Fetched results are saved locally by default.

Mitigation: Review and clean the logs/ directory after use, and avoid running the skill in directories where retained public-data exports would be inappropriate.

Risk: The skill may activate on broad short-video research prompts.

Mitigation: Confirm the target platform and task before running commands when the user did not explicitly ask for Douyin data collection.

Risk: Authentication failures may display promotional contact details despite documentation saying runtime errors stay neutral.

Mitigation: Review authentication failure output before deployment and avoid exposing runtime error text directly to end users without moderation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-comprehensive-feed-grabber)
- [Usage Documentation](readme.md)
- [Complete Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei Token and Support Site](https://www.guaikei.com)
- [Search Request Schema](assets/search_cli_req.schema.json)
- [Search Response Schema](assets/search_cli_resp.schema.json)
- [Post Request Schema](assets/post_cli_req.schema.json)
- [Post Response Schema](assets/post_cli_resp.schema.json)
- [Comment Request Schema](assets/comment_cli_req.schema.json)
- [Comment Response Schema](assets/comment_cli_resp.schema.json)
- [Hot Ranking Response Schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON written to stdout with logs on stderr and saved result files under logs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command outputs follow the bundled JSON Schemas.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
