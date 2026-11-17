## Description:

This skill helps agents collect and analyze public Douyin data through keyword search, creator post retrieval, video comment retrieval, and real-time hot-list lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for short-video market research, competitor account monitoring, public comment analysis, and Douyin trend tracking. It is intended for public Douyin data only and does not support private data, posting, editing, downloading, or other short-video platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags misleading token-error behavior and insecure token handling.

Mitigation: Review before installing, use a dedicated low-privilege Guaikei token, and rotate the token if it may have been exposed.

Risk: Search keywords and Douyin URLs are sent to the Guaikei service during normal operation.

Mitigation: Avoid submitting confidential research terms, private URLs, or sensitive identifiers through the skill.

Risk: Result files are saved locally under logs/ by default.

Mitigation: Review local log contents, apply workspace access controls, and delete or redact logs that contain sensitive analysis inputs or outputs.

Risk: Runtime contact and website messages do not match the manifest's stated neutral auth-error policy.

Mitigation: Validate auth-error behavior in the target environment and do not rely on runtime support messages as trusted security guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-public-records)
- [Usage Documentation](readme.md)
- [Command Options](references/options.md)
- [Changelog](references/changelog.md)
- [Search Request Schema](assets/search_cli_req.schema.json)
- [Search Response Schema](assets/search_cli_resp.schema.json)
- [Post Request Schema](assets/post_cli_req.schema.json)
- [Post Response Schema](assets/post_cli_resp.schema.json)
- [Comment Request Schema](assets/comment_cli_req.schema.json)
- [Comment Response Schema](assets/comment_cli_resp.schema.json)
- [Hot List Response Schema](assets/hot_cli_resp.schema.json)
- [Guaikei Service Website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [JSON responses on stdout, operational logs on stderr, and concise text or Markdown guidance when the agent summarizes results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; sends search terms and Douyin URLs to the Guaikei service; writes result logs under logs/ by default; individual requests support up to 10000 public records.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
