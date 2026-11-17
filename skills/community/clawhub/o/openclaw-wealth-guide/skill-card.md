## Description:

Openclaw Wealth Guide is an OpenClaw skill for collecting data from web pages, APIs, databases, and files, processing it, and exporting structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxg852621787](https://clawhub.ai/user/dxg852621787)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to automate collection from authorized web, API, database, and file sources, then clean, transform, schedule, and export the resulting data. It is especially oriented toward Chinese-language OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access broad data sources.

Mitigation: Use it only with data sources you are authorized to access and restrict outbound network access where possible.

Risk: Unsafe URL and credential handling can expose secrets or send them to untrusted endpoints.

Mitigation: Avoid credentials unless the endpoint is trusted and uses HTTPS; review source URLs and authentication settings before use.

Risk: Exports may create or overwrite files.

Mitigation: Review export paths before running collection or export jobs.

Risk: Scheduled collection jobs can continue unattended.

Mitigation: Do not run scheduled jobs unattended until targets, credentials, and storage locations are confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dxg852621787/skills/openclaw-wealth-guide)
- [Repository README](https://gitee.com/du-xuegong/openclaw-wealth-guide/blob/main/README.md)
- [Repository Homepage](https://gitee.com/du-xuegong/openclaw-wealth-guide)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime exports can be JSON, CSV, Excel, SQLite, or PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied data source, processing, scheduling, and export configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
