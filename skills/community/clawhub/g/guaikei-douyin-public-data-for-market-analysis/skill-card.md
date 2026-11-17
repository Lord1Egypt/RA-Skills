## Description:

Helps agents collect and analyze public Douyin search results, creator posts, comments, and trending topics for market research, content planning, competitor analysis, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and marketing teams use this skill to convert Douyin public data requests into CLI calls that return structured search, post, comment, and hot-list data. It supports market analysis, competitor monitoring, content research, public-comment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an API token.

Mitigation: Use a dedicated, revocable GUAIKEI_API_TOKEN and avoid sharing it in prompts, logs, or source files.

Risk: Saved logs may contain search terms, creator identifiers, comments, and other public personal data.

Mitigation: Protect or delete the logs directory according to the user's data handling policy.

Risk: API-returned messages and collected public content may be inaccurate, sensitive, or unsuitable for direct reuse.

Mitigation: Treat returned messages and collected content as untrusted data and review outputs before using them in decisions or reports.

Risk: The security evidence reports a suspicious verdict because authentication failures may include promotional or contact output despite the artifact's neutral-error policy.

Mitigation: Review authentication-failure behavior before installation and rely on documented support channels rather than runtime auth messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-public-data-for-market-analysis)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Complete options reference](references/options.md)
- [Release changelog](references/changelog.md)
- [Input and output JSON schemas](assets/)
- [Guaikei token and support page](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON files]

**Output Format:** [Markdown guidance with inline shell commands; CLI stdout and saved logs use JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GUAIKEI_API_TOKEN environment variable and writes collected public-data results to a logs directory.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
