## Description:

Retrieves public Douyin search results, creator posts, video comments, and hot-list data for topic research, competitive analysis, sentiment review, and trend monitoring; it does not support publishing, editing, or downloading media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and marketing analysts use this skill to collect public Douyin search, creator, comment, and hot-list data for content planning, competitor research, public-comment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan summary flags broad automatic activation for generic trend or search requests.

Mitigation: Invoke the skill only for intended Douyin public-data tasks, and ask a clarifying question when the user request could refer to another platform or a non-Douyin workflow.

Risk: The security guidance notes that Douyin search terms, account or video URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use only approved tokens and non-sensitive public inputs, and disclose the third-party API dependency before use in controlled environments.

Risk: The security scan summary flags local retention of collected social-media data, and the artifact documents automatic saved logs.

Mitigation: Treat saved logs as retained social-media data, review them before sharing, and delete or protect them according to the user's data-handling policy.

Risk: The security guidance warns against obtaining or redistributing downloadable media URLs.

Mitigation: Use results for analysis of public metadata and comments only, and do not use the skill output to redistribute media assets or bypass platform restrictions.

Risk: The security scan summary notes runtime promotional messages and token-related exposure concerns.

Mitigation: Prefer neutral error handling, avoid surfacing promotional contact text in agent responses, and never print or store token values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-intel-exchange)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei token and help site](https://www.guaikei.com)
- [Complete options](references/options.md)
- [Changelog](references/changelog.md)
- [JSON schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON on stdout, operational logs on stderr, and saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-run result sets are capped at 10000 records and require GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog, runtime constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
