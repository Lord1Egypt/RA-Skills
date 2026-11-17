## Description:

Lovefromio Garmin Health Analysis lets an agent query Garmin Connect health, recovery, activity, sleep, and time-series metrics, download FIT/GPX files, and generate interactive health dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and agents use this skill to authenticate to Garmin Connect, retrieve personal health and activity data, analyze recovery, sleep, and training trends, and produce summaries or dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published package includes plaintext Garmin credentials in config.json.

Mitigation: Do not install this release as-is; remove config.json from the package, rotate the exposed Garmin password, and invalidate existing sessions before use.

Risk: The skill can access and export sensitive health, profile, and GPS activity data.

Mitigation: Store credentials and tokens outside the package, restrict token and export-file permissions, and review generated files before sharing or retaining them.

Risk: Unpinned dependencies or external dashboard JavaScript can change behavior after installation.

Mitigation: Install in an isolated environment, pin Python dependencies, and bundle or integrity-pin dashboard JavaScript assets.

Risk: Health trend interpretation could be mistaken for medical advice.

Mitigation: Keep responses informational, include a medical disclaimer for health insights, and direct users to a clinician for health concerns.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lovefromio/skills/lovefromio-garmin-health-analysis)
- [Garmin Connect API Reference](references/api.md)
- [Health Data Analysis Guide](references/health_analysis.md)
- [Extended Garmin Capabilities](references/extended_capabilities.md)
- [MCP Server Setup Notes](references/mcp_setup.md)
- [python-garminconnect Library](https://github.com/cyberjunky/python-garminconnect)
- [Garmin Connect](https://connect.garmin.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON command output, and generated HTML dashboard files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local FIT, GPX, TCX, JSON, and HTML files containing health, profile, activity, or GPS data.]

## Skill Version(s):

1.2.4 (source: server release evidence; artifact frontmatter remains 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
