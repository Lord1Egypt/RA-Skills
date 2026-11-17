## Description:

Raspberry Pi health monitor for CPU temperature, throttling status, voltage levels, memory and disk usage, fan RPM, overclock detection, and power issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josunlp](https://clawhub.ai/user/josunlp)

### License/Terms of Use:


## Use Case:

Developers, operators, and Raspberry Pi users use this skill to run a local read-only health check when monitoring device stability, diagnosing thermal throttling or under-voltage, and checking resource pressure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The health report may display local system configuration, resource usage, and kernel power-event information.

Mitigation: Run the skill only where that diagnostic output can be viewed by trusted users, and review logs before sharing them outside the device owner or operations team.

Risk: The script reports hardware and operating-system health signals but does not repair thermal, power, storage, or memory issues.

Mitigation: Treat warning or critical exit codes as prompts for operator review and follow-up remediation on the Raspberry Pi.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Terminal text health report with status lines and an exit code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 means healthy, 1 means warnings, and 2 means critical issues.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
