## Description:

Fetches public Kuaishou video, creator post, and comment data through the Guaikei API so agents can support competitor monitoring, topic discovery, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content operators, analysts, and agents use this skill to retrieve public Kuaishou search results, creator posts, and video comments for competitor analysis, topic research, trend monitoring, KOL selection, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, profile URLs, video URLs, and query parameters are sent to guaikei.com with the user's GUAIKEI_API_TOKEN.

Mitigation: Use the skill only when the data-sharing path is acceptable, keep the API token scoped and protected, and avoid submitting sensitive topics or identifiers.

Risk: Task outputs are retained locally in the logs directory and may contain queried topics, profiles, comments, or analysis results.

Mitigation: Delete or protect the logs directory when outputs are sensitive, and avoid sharing retained logs outside the intended team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/kuaishou-guaikei-competitor-analysis)
- [Guaikei API and token site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include status, error_code, query parameters, public Kuaishou records, and optional summaries; task outputs are saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: server release, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
