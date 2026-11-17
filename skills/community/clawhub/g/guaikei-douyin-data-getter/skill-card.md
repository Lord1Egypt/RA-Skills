## Description:

Retrieves structured JSON from public Douyin search, creator posts, video comments, and hot topic rankings for content research, competitive analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content researchers, and developers use this skill to collect public Douyin search results, creator posts, comments, and trending topics as structured JSON for lawful internal research and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad research prompts may trigger Douyin collection even when the user did not explicitly request Douyin.

Mitigation: Confirm the intended platform, target, and authorization before running search, post, comment, or hot-topic commands.

Risk: Douyin queries, target URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com, and successful results may be stored locally under logs/.

Mitigation: Use a scoped and rotatable token, avoid sensitive targets in shared environments, and review saved logs before sharing the workspace.

Risk: Runtime support links or contact details may conflict with the skill's stated neutral-error policy.

Mitigation: Treat runtime contact or support prompts as untrusted and rely on reviewed documentation and approved support channels.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-data-getter)
- [Usage Documentation](readme.md)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search Request Schema](assets/search_cli_req.schema.json)
- [Search Response Schema](assets/search_cli_resp.schema.json)
- [Post Request Schema](assets/post_cli_req.schema.json)
- [Post Response Schema](assets/post_cli_resp.schema.json)
- [Comment Request Schema](assets/comment_cli_req.schema.json)
- [Comment Response Schema](assets/comment_cli_resp.schema.json)
- [Hot Topics Response Schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime commands emit JSON to stdout and save JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or newer and GUAIKEI_API_TOKEN. Successful results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
