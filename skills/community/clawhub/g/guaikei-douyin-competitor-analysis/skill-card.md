## Description:

Queries Douyin public data for keyword search, hot trends, creator post collection, comment retrieval, and competitor or content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, analysts, and operations teams use this skill to retrieve structured public Douyin data for topic research, competitor monitoring, sentiment review, hot-trend tracking, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin keywords, target URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use the skill only when third-party API processing is acceptable, and configure the token with the minimum access needed for the intended analysis.

Risk: Collected comments, competitor data, and search results may be retained locally as JSON logs.

Mitigation: Protect or delete the logs directory according to the sensitivity and retention needs of the research.

Risk: The skill is specific to Douyin data and can be over-applied to broader content research requests.

Mitigation: Confirm that the user wants Douyin public data before running the commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-competitor-analysis)
- [Guaikei API Token and Support](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON on stdout, with concise user-facing guidance when required inputs or token configuration are missing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save retrieved research data as JSON logs under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
