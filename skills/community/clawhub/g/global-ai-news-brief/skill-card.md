## Description:

Searches 11 social and media platforms from one keyword, standardizes the results, and helps an agent produce AI news briefings with topic clusters, sentiment analysis, platform comparisons, source tables, and an interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, market researchers, media teams, content creators, and agent builders use this skill to gather cross-platform AI and social-media news signals, compare platform narratives, and generate concise intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and API-key-authenticated requests are sent to RedFox.

Mitigation: Avoid confidential keywords, secrets, and personal investigations; use an API key whose scope, validity, and revocation process are understood.

Risk: Untrusted social-media content may be included in generated HTML reports without documented escaping or URL validation.

Mitigation: Treat generated reports as untrusted, validate links, and ensure user-provided and platform-provided text is escaped before opening or sharing the report.

Risk: Automatically opening generated HTML can expose the user to unsafe embedded links or rendered content.

Mitigation: Require confirmation before opening reports automatically and inspect the output in a controlled browser context.

Risk: Default temporary output paths can expose collected results on shared systems.

Mitigation: Use a private, access-controlled output path instead of shared temporary directories when storing JSON results or reports.

## Reference(s):

- [API interface reference](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/global-ai-news-brief)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown and terminal text with generated JSON data and an interactive HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; can write standardized JSON search results and an HTML report with source links and engagement metrics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
