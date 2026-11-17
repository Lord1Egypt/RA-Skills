## Description:

Retrieves structured public Xiaohongshu note, comment, keyword-search, and creator-post data for content research and marketing analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, marketers, and analysts use this skill to collect public Xiaohongshu keyword results, note details, comments, and creator post lists for trend research, competitive monitoring, KOL screening, and follow-on analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords or URLs and GUAIKEI_API_TOKEN-dependent requests to the Guaikei API.

Mitigation: Use only when the user is comfortable sharing the requested public Xiaohongshu inputs with Guaikei, and keep the API token scoped and protected.

Risk: Generated logs can contain searched terms, Xiaohongshu URLs, returned content, comments, and other analysis inputs.

Mitigation: Treat the logs directory as sensitive output; avoid syncing, publishing, or sharing it without review.

Risk: Tokenized Xiaohongshu URLs and API-token-dependent activity may appear in command inputs, saved outputs, or process history.

Mitigation: Avoid pasting sensitive links into shared channels, redact tokenized URLs before sharing results, and prefer future versions that redact sensitive values by default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-detail)
- [Guaikei API service](https://www.guaikei.com)
- [Options and invocation reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands; runtime commands return structured JSON and write task logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; outputs may include Xiaohongshu keywords, URLs, interaction metrics, author details, comments, and saved logs.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, artifact metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
