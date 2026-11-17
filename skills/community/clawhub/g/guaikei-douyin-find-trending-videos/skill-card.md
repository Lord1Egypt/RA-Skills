## Description:

This skill helps agents query public Douyin data for keyword search, creator posts, comments, and real-time trending lists, while excluding posting, editing, downloading, and non-Douyin platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to gather public Douyin content data for topic selection, competitor research, comment review, and trend monitoring through Node.js CLI commands. It requires a configured GUAIKEI_API_TOKEN before running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin queries, target URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com, and the token is placed in request URLs.

Mitigation: Install only if this data flow is acceptable, use a scoped token where possible, rotate tokens after use, and avoid sensitive investigations.

Risk: Collected public Douyin results may be saved locally by default.

Mitigation: Restrict access to the logs directory and clean up stored result files when they are no longer needed.

Risk: Broad trigger language can invoke the skill for generic research requests.

Mitigation: Use explicit Douyin-only prompts and confirm intent before running CLI commands.

## Reference(s):

- [Usage Documentation](readme.md)
- [Complete CLI Options](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI Request Schema](assets/search_cli_req.schema.json)
- [Search CLI Response Schema](assets/search_cli_resp.schema.json)
- [Post CLI Request Schema](assets/post_cli_req.schema.json)
- [Post CLI Response Schema](assets/post_cli_resp.schema.json)
- [Comment CLI Request Schema](assets/comment_cli_req.schema.json)
- [Comment CLI Response Schema](assets/comment_cli_resp.schema.json)
- [Hot CLI Response Schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Files]

**Output Format:** [JSON on stdout with stderr logs and optional local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single requests can return up to 10,000 public records; logs may be written under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
