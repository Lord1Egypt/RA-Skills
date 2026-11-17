## Description:

Generates daily WeChat official account short-drama trend reports by querying RedFoxHub data, ranking articles by read count, clustering genres, and producing creative insights plus a local HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External short-drama writers, content operators, MCN teams, and WeChat official account owners use this skill to request trend reports, investigate genres or time ranges, and get data-backed topic and title guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report HTML is built from remote article metadata and may include unescaped upstream values.

Mitigation: Review generated reports before sharing or deploying them, and sanitize or escape remote metadata before broader use.

Risk: The skill needs a RedFoxHub API key and includes an --api-key option that could expose credentials through command history or process listings.

Mitigation: Use a scoped, revocable REDFOX_API_KEY environment variable and avoid passing secrets on the command line.

Risk: The script contacts redfox.hk, writes local report and cache files, and opens generated HTML in the browser.

Mitigation: Run it in a controlled environment, review the configured output locations, and only open reports from trusted runs.

## Reference(s):

- [Core workflow](references/core_workflow.md)
- [Usage examples](references/examples.md)
- [RedFoxHub](https://redfox.hk/)
- [RedFoxHub playlet message API endpoint](https://redfox.hk/story/api/parseWork/queryPlayletMsgs)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/playlet-gzh-feed)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report text with a generated local HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; writes HTML reports to ~/Downloads/QoderReports and cache data to ~/.workbuddy/cache.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
