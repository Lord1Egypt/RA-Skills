## Description:

Query Prometheus monitoring data to check server metrics, resource usage, and system health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akellacom](https://clawhub.ai/user/akellacom)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill to query one or more Prometheus instances for server health, resource usage, alerts, labels, targets, and time-series data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local .env files and use environment Basic Auth credentials as fallbacks.

Mitigation: Run it from trusted workspace directories and prefer explicit per-instance credentials with scoped access.

Risk: Prometheus credentials can be stored in plaintext configuration files.

Mitigation: Restrict configuration file permissions and avoid storing credentials with broader access than required.

Risk: Using aggregated queries across mixed-trust Prometheus endpoints can broaden credential exposure.

Mitigation: Avoid --all with mixed-trust endpoints until credential scoping is reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries may aggregate results across multiple configured Prometheus instances.]

## Skill Version(s):

1.1.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
