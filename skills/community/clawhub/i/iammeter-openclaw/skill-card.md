## Description:

Query and export IAMMETER device and site data, including real-time meter readings, historical energy data, CSV exports, power analysis, and offline analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iammeter](https://clawhub.ai/user/iammeter)

### License/Terms of Use:


## Use Case:

Developers, energy operators, and OpenClaw users can use this skill to inspect IAMMETER sites and devices, retrieve energy readings, export history, and run meter analysis from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs an IAMMETER API token and sends it to IAMMETER over the network for intended API calls.

Mitigation: Use a revocable token, store it only in the documented Skills UI or environment variable, and rotate it if exposed.

Risk: Generated CSV exports may be unsafe to open directly in spreadsheet software if upstream data contains formula-like values.

Mitigation: Review or sanitize CSV files before opening them in spreadsheet applications.

Risk: The package uses semver ranges for dependencies rather than exact pinned versions.

Mitigation: Pin and audit dependencies before deployment in controlled environments.

## Reference(s):

- [IAMMETER API Reference](references/api.md)
- [IAMMETER Swagger API](https://www.iammeter.com/swaggerui/swagger.json)
- [IAMMETER Cloud API](https://www.iammeter.com/docs/system-api)
- [IAMMETER Device Communication Protocols](https://www.iammeter.com/newsshow/blog-fw-features)
- [IAMMETER ClawHub Skill Page](https://clawhub.ai/iammeter/skills/iammeter-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON API responses, CSV files, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an IAMMETER API token and network access to IAMMETER endpoints.]

## Skill Version(s):

0.2.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
