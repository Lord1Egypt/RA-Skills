## Description:

Get all CI/CD flows from Open-C3 platform. Returns the complete list of flows in the system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinfeng2011](https://clawhub.ai/user/lijinfeng2011)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to list Open-C3 CI/CD flows across service trees, including IDs, names, source addresses, total counts, and grouping statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Open-C3 application key and can expose sensitive configuration if setup is insecure.

Mitigation: Keep config.env private with restrictive permissions, never commit or share APP_KEY, and prefer a least-privileged read-only application key.

Risk: Using an untrusted Open-C3 endpoint or untrusted config.env can expose credentials or cause the script to use unsafe configuration.

Mitigation: Use only trusted Open-C3 instances, configure OPEN_C3_URL with HTTPS, and inspect any config.env file before use.

Risk: The generated flow listing can reveal CI/CD pipeline names, service-tree structure, and source repository addresses.

Mitigation: Share output only with users who are authorized to view Open-C3 flow and service-tree metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinfeng2011/skills/openc3-flow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown table and summary text, with shell commands and configuration guidance when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, OPEN_C3_URL, APP_NAME, and APP_KEY; the Open-C3 API response is parsed into a flow table grouped by service tree.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
