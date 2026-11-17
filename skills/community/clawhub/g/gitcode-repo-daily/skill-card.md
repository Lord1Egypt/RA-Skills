## Description:

Generate daily operations reports for GitCode repositories with key metrics, AI summaries, and Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoxj](https://clawhub.ai/user/autoxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to collect GitCode repository activity for a selected day, summarize PR and issue activity, and render a daily operations report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GitCode token to call repository APIs.

Mitigation: Use a least-privileged GitCode token and avoid sharing generated reports or logs that could expose sensitive repository activity.

Risk: The skill persists repository lists, metrics, and summaries under the skill directory.

Mitigation: Review the configured repositories and generated local files before retaining, sharing, or committing the skill directory.

Risk: PR and issue text from repositories is untrusted content that can appear in generated Markdown.

Mitigation: Review generated Markdown before publishing or opening it in rich renderers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoxj/skills/gitcode-repo-daily)
- [README](README.md)
- [Usage examples](examples.md)
- [Daily report template](resources/daily_report.md)
- [GitCode API endpoint](https://api.gitcode.com/api/v5)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON status and summary inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITCODE_TOKEN, reads configured repositories, writes report artifacts under the skill directory, and stores report metrics and summaries in SQLite.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
