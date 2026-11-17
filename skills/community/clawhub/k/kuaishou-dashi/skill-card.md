## Description:

Kuaishou Dashi helps agents search Kuaishou public videos by keyword, retrieve public creator posts, and fetch video comments as structured JSON for content research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketing teams, MCN operators, and analysts use this skill to collect public Kuaishou video, creator, and comment data for topic research, competitor monitoring, KOL screening, comment analysis, and trend reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile URLs, video URLs, requested limits, and the GUAIKEI_API_TOKEN are sent to the Guaikei API.

Mitigation: Use the skill only when sharing those inputs with the third-party API is acceptable, and configure the token through the environment rather than including it in prompts or saved outputs.

Risk: Local logs may retain business-sensitive research, public comments, account URLs, or analysis outputs.

Mitigation: Review and delete the logs directory when collected results should not remain on disk.

Risk: The skill depends on a third-party API and can return empty results, rate-limit responses, token errors, or temporary service failures.

Mitigation: Check the returned status and error code before using results, reduce limits or retry later for rate limits and transient server errors, and avoid treating empty results as successful evidence.

## Reference(s):

- [Kuaishou Dashi ClawHub page](https://clawhub.ai/engheng-art/skills/kuaishou-dashi)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save task results to the local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog released 2026-08-29; artifact frontmatter metadata lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
