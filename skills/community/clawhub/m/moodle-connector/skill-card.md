## Description:

Moodle REST API client, batch downloader, and MCP server for Claude Code integration. SSO-enabled with support for Azure AD, Google, and SAML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jabir-srj](https://clawhub.ai/user/jabir-srj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to connect to Moodle instances, retrieve courses, grades, assignments, announcements, materials, and summaries, and download Moodle-hosted files through CLI, Python, or MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling, downloads, and local persistence have serious under-disclosed security risks.

Mitigation: Review before installing and do not use real Moodle credentials until credential storage, caching, and data transmission behavior are accurately documented.

Risk: Downloads may use untrusted URLs or write outside an approved location.

Mitigation: Restrict downloads to the configured Moodle origin and contain output paths to an approved directory before deployment.

Risk: Default credential-password behavior can weaken protection for stored Moodle tokens or passwords.

Mitigation: Remove the test-pass default, require a strong deployment-specific password, and rotate Moodle tokens or stored passwords if the skill was already used with the default.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/jabir-srj/skills/moodle-connector)
- [Project Homepage](https://github.com/Jabir-Srj/moodle-connector)
- [Project Repository](https://github.com/Jabir-Srj/moodle-connector.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown and plain text responses, downloaded files, JSON configuration, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Moodle course data, grades, assignments, announcements, materials, summaries, cached API responses, and downloaded files.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
