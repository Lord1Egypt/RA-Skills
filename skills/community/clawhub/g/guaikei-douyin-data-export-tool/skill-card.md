## Description:

This skill helps an agent collect and export public Douyin data for keyword search, creator posts, video comments, and real-time hot lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and content research teams use this skill to gather public Douyin search results, creator posts, comments, and hot-list data for content research, competitor analysis, public-opinion review, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, profile or video URLs, and a Guaikei API token to the provider service.

Mitigation: Install only when this data sharing is acceptable, keep the token in an environment variable, and review or patch token handling before use.

Risk: Remote error messages and authentication-failure behavior may expose unreviewed provider text or promotional support paths.

Mitigation: Review or patch error handling so authentication failures stop immediately and return neutral, non-promotional messages.

Risk: Exported logs may retain public comments or profile data that can include personal information.

Mitigation: Treat logs as retained datasets, restrict access, and delete or protect them after the research task is complete.

Risk: Broad activation for short-video research could run the skill when the user has not clearly chosen Douyin as the data source.

Mitigation: Confirm the intended platform and data scope before running commands for ambiguous short-video or competitor-analysis requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-data-export-tool)
- [Usage documentation](readme.md)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/*.schema.json)
- [Guaikei API token documentation](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI commands emit JSON to stdout and save JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the GUAIKEI_API_TOKEN environment variable and Node.js 16.14 or newer; command output follows the bundled JSON schemas.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
