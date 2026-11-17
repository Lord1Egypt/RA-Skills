## Description:

Collects structured JSON data from Douyin public search results, creator posts, video comments, and real-time hot lists for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, marketers, and developers use this skill to collect structured Douyin public data for content research, competitor monitoring, public-comment analysis, and hot-topic tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends supplied Douyin URLs, keywords, and returned public result data to guaikei.com.

Mitigation: Use it only for intended Douyin public-data tasks and avoid submitting sensitive internal topics, private identifiers, or confidential research terms.

Risk: The skill depends on a GUAIKEI_API_TOKEN credential for access.

Mitigation: Use a dedicated, revocable token with limited quota, pass it through the environment, and rotate it if it is exposed.

Risk: The skill writes local JSON logs that may contain public user identifiers, comments, monitored topics, and analysis inputs.

Mitigation: Review, restrict access to, or delete the logs directory after use according to the user's data-handling requirements.

Risk: Broad activation guidance may cause the skill to run for general short-video research requests.

Mitigation: Constrain use to explicit Douyin public-data collection tasks before executing CLI commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-data-funnel)
- [Usage documentation](readme.md)
- [Complete CLI options](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/*.schema.json)
- [Guaikei service documentation](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Files, Guidance]

**Output Format:** [Pure JSON on stdout, operational messages on stderr, and optional JSON log files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or newer and a GUAIKEI_API_TOKEN environment variable; single-command result limits are documented as up to 10000 records.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog, runtime constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
