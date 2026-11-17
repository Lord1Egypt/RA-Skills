## Description:

InfluxDB Cloud (influxdata.com). Use this skill for ANY InfluxDB Cloud request — reading, creating, and updating data. Whenever a task involves InfluxDB Cloud, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to list and retrieve InfluxDB Cloud buckets, run InfluxQL queries, and write line protocol data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote installers that were not verified.

Mitigation: Install a verified oo CLI version yourself before use.

Risk: The CLI can make persistent changes to other agent skills through startup synchronization.

Mitigation: Disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1 before agent use.

Risk: InfluxDB access can expose more data or write access than the task needs.

Mitigation: Use a limited-scope InfluxDB token and retain the required write confirmations.

Risk: A write action can change InfluxDB Cloud data.

Mitigation: Confirm the exact payload and effect with the user before running a write action.

## Reference(s):

- [InfluxDB Cloud Serverless API documentation](https://docs.influxdata.com/influxdb3/cloud-serverless/api/)
- [InfluxDB Cloud product page](https://www.influxdata.com/products/influxdb-cloud/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [InfluxDB Cloud skill release](https://clawhub.ai/oomol/skills/oo-influxdb-cloud)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas; writes require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
