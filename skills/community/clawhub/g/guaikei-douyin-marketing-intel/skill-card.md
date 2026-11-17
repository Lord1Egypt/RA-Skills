## Description:

Guides an agent to fetch public Douyin data for keyword search, creator post collection, video comment analysis, and real-time trending topic checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketing teams use this skill to collect public Douyin search results, creator posts, comments, and trending topics for content research, competitor monitoring, sentiment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GUAIKEI API token and Douyin query inputs may be sent to the Guaikei backend, including through URL parameters.

Mitigation: Use the skill only after confirming that this data sharing is acceptable, keep tokens scoped and private, and rotate the token if URL or query logs may have exposed it.

Risk: Generated logs may contain research topics, public comments, profile identifiers, media URLs, and timestamps.

Mitigation: Treat the logs directory as sensitive output; restrict access, retain logs only as needed, and delete them when analysis is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-marketing-intel)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Usage documentation](readme.md)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands; CLI stdout is pure JSON and logs may be written as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and a GUAIKEI_API_TOKEN environment variable; command outputs cover search, post, comment, and hot-list workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
