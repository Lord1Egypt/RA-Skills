## Description:

Retrieves structured public Kuaishou data for keyword video search, creator post listing, and video comment fetching to support content research, competitor monitoring, KOL screening, trend analysis, and comment insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content creators, data analysts, and agents use this skill to query public Kuaishou search results, creator posts, and video comments, then turn the returned structured data into summaries, comparisons, reports, or operational insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile URLs, video URLs, request limits, and GUAIKEI_API_TOKEN are sent to the GuAikei service.

Mitigation: Confirm the user accepts this external data sharing before execution, and avoid sending sensitive research topics, private URLs, or tokens outside approved environments.

Risk: The skill can retain fetched results in local logs, which may include comments, URLs, or competitive research topics.

Mitigation: Store logs in an approved location, restrict access when results are sensitive, and delete retained logs when they are no longer needed.

Risk: The skill is limited to public Kuaishou data and can return empty or error statuses when inputs are invalid, unavailable, rate-limited, or unauthorized.

Mitigation: Check the returned status and error_code before analysis, retry only when appropriate, and do not fill missing results with inferred data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishou-search-2)
- [Server-resolved GitHub provenance](https://github.com/why20261/kuaishou-search)
- [GuAikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Structured JSON results with concise Markdown summaries, shell command examples, and failure guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful runs may save JSON result logs locally.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact package and changelog report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
