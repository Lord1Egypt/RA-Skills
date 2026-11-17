## Description:

Moodle REST API client, batch downloader, and MCP server for Claude Code integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jabir-srj](https://clawhub.ai/user/jabir-srj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and education-technology users use this skill to connect agents or scripts to Moodle for course lists, grades, assignments, materials, announcements, summaries, and controlled file downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real Moodle credentials or tokens could be exposed or mishandled during setup or use.

Mitigation: Use an isolated, non-admin environment and store credentials outside plaintext config files with restrictive permissions.

Risk: File download behavior could write untrusted content or unexpected paths if URLs and destinations are not constrained.

Mitigation: Restrict downloads to trusted Moodle URLs and a dedicated download directory before using real credentials.

Risk: Default or weak credential passwords can reduce protection for stored Moodle credentials.

Mitigation: Remove the default test password path and require a strong user-supplied credential password.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jabir-srj/skills/moodle-connector-skill)
- [Moodle Connector repository metadata](https://github.com/Jabir-Srj/moodle-connector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown summaries, CLI text output, MCP text responses, Python code examples, JSON configuration, and downloaded Moodle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Moodle configuration and credentials; downloads write to local cache or configured output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
