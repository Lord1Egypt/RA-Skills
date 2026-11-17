## Description:

Provides CLI-assisted access to public Douyin keyword search, author post, video comment, and hot-trend data for structured JSON export and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content analysts use this skill to collect public Douyin search results, creator posts, comments, and trend lists for content research, competitor analysis, topic planning, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports unsafe API token handling.

Mitigation: Review before installing and use a low-privilege or disposable GUAIKEI_API_TOKEN.

Risk: Douyin queries, URLs, and returned public data may be sent to Guaikei and saved locally under logs/.

Mitigation: Avoid sensitive inputs, limit use to public Douyin data, and remove local logs when retention is not needed.

Risk: Security evidence flags overbroad activation guidance for vague trend questions.

Mitigation: Invoke only for explicit Douyin public-data requests or clearly scoped Douyin content research.

Risk: Security evidence reports a contradiction between promised runtime behavior and promotional output.

Mitigation: Inspect stderr and runtime messages before automated deployment, especially around authentication errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-author-posts-to-feed-export)
- [Usage documentation](artifact/readme.md)
- [Command options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Search request schema](artifact/assets/search_cli_req.schema.json)
- [Search response schema](artifact/assets/search_cli_resp.schema.json)
- [Author posts response schema](artifact/assets/post_cli_resp.schema.json)
- [Guaikei token and service site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands plus structured JSON CLI output and optional JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; stdout is intended for JSON results, stderr carries runtime logs, and successful search/post/comment commands may save JSON files under logs/.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog, and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
