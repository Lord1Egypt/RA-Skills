## Description:

Provides command-line access to public Douyin search, creator post, comment, and hot-list data for content planning, competitor research, public-opinion review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to collect structured JSON from public Douyin search results, creator posts, video comments, and hot lists for short-video research workflows. It does not support private or login-only Douyin data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin URLs, keywords, limits, and the GUAIKEI_API_TOKEN are sent to guaikei.com during execution.

Mitigation: Use only a token intended for this provider, avoid sensitive research terms, and rotate or revoke the token if exposure is suspected.

Risk: Search, post, comment, and hot-list results are saved locally under logs/.

Mitigation: Review generated log files for sensitive or regulated content and remove them when they are no longer needed.

Risk: The security evidence reports that runtime authentication failures may display external promotional contact information.

Mitigation: Treat authentication failures as a prompt to check the environment variable and provider documentation rather than relying on runtime contact text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-lookup-tool)
- [Usage documentation](readme.md)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/)
- [Guaikei token and service documentation](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with Node.js shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands write JSON responses to stdout and save timestamped JSON logs under logs/.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
