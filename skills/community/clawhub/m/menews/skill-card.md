## Description:

AIMPACT provides AI morning reports, evening reports, 24-hour hot-news rankings, and curated AI content, sorted by AI score and optionally delivered on a schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesmenews](https://clawhub.ai/user/jamesmenews)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to fetch and format current AI industry news from ME News API sources. It supports manual report requests and optional scheduled delivery through a preconfigured message channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches content from external ME News API endpoints, so report quality and availability depend on those endpoints.

Mitigation: Review generated reports before relying on them, and treat API errors or stale content as a source-data issue rather than an agent conclusion.

Risk: Optional scheduled delivery can send recurring reports through preconfigured message channels.

Mitigation: Enable scheduled tasks only when recurring delivery is intended, and confirm OpenClaw message-channel credentials and recipients before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamesmenews/skills/menews)
- [ME News source configuration](artifact/sources.md)
- [Output format template](artifact/format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news reports with optional shell command examples for scheduling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are limited to the configured ME News sources, sorted by AI score when provided, deduplicated by title or ID, and formatted according to artifact/format.md.]

## Skill Version(s):

1.0.11 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
