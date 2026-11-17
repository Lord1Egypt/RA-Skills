## Description:

guaikei-comment helps agents collect public Xiaohongshu search results, note details, comments, and creator posts for content research, competitor monitoring, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, marketers, and analysts use this skill to retrieve public Xiaohongshu data for topic research, comment analysis, competitor monitoring, KOL screening, and report preparation. It is intended to gather structured source data for later summarization or analysis, not to access private content or perform account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note URLs, profile URLs, and the GUAIKEI_API_TOKEN to a third-party service.

Mitigation: Use only approved public-data inputs, avoid sensitive or private URLs and keywords, and keep the token in environment or secret storage rather than prompts or shared logs.

Risk: The security review says the short description understates the broader collection features.

Mitigation: Treat the release as a broader Xiaohongshu research and monitoring tool; confirm the intended route, scope, and result limit before running commands.

Risk: The security review flags avoidable API token handling risk.

Mitigation: Restrict token access to trusted environments, rotate the token if it may have been exposed, and avoid copying command output or logs into public channels without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-comment)
- [engheng-art ClawHub profile](https://clawhub.ai/user/engheng-art)
- [GUAIKEI website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with bash commands and structured JSON command output; command results may also be saved under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN. Inputs can include Xiaohongshu keywords, note URLs, creator profile URLs, result limits, content type, sort order, and time range.]

## Skill Version(s):

1.0.0 (source: release evidence, skill metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
