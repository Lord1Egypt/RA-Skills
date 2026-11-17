## Description:

Guaikei XHS Author Tracker helps agents retrieve public Xiaohongshu keyword search results, note details, author posts, and note comments through Node.js CLI commands for downstream content, marketing, and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, and data analysts use this skill to collect public Xiaohongshu data for keyword research, competitor monitoring, author-post tracking, note inspection, and comment analysis. The skill is intended to gather structured source data that an agent can summarize, compare, cluster, or turn into reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers broader Xiaohongshu search, note-detail, author-post, and comment collection workflows than a single-note comment retriever.

Mitigation: Review requested tasks against the documented routing rules and install only when these broader data-collection capabilities are acceptable.

Risk: The API token is sent to a third-party API service in request parameters.

Mitigation: Use a dedicated GUAIKEI_API_TOKEN, rotate it when needed, and avoid sharing tokens across unrelated workflows.

Risk: Public-profile, note, and comment data is sent to the third-party API service and saved locally in logs.

Mitigation: Avoid submitting sensitive or private links, confirm the data-sharing posture before use, and manage generated log files according to local retention rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-author-tracker)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI execution returns structured JSON and writes JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; outputs include request metadata, status, error_code, message, execution metadata, and results.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter, constants, changelog, and package.json report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
