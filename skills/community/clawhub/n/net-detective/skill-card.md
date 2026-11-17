## Description:

Run structured network diagnostics across DNS, ping, traceroute, MTU, speed, and history baselines, then produce a plain-English diagnosis with actionable next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and support engineers use Net Detective to diagnose slow or broken connectivity and turn raw network measurements into a clear report with next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs active network diagnostics against public hosts and resolvers.

Mitigation: Run it only on networks where diagnostics are authorized, and skip optional speed, traceroute, or MTU checks when active probing is inappropriate.

Risk: Raw diagnostic JSON can include local host, local IP, gateway, DNS, traceroute, and performance details from a sensitive network.

Mitigation: Share only the plain-English findings when possible, and redact or avoid sharing raw diagnostic JSON from sensitive environments.

Risk: Documented examples write diagnostic outputs under /tmp, which may be less private on shared systems.

Mitigation: Use a private temporary directory with restrictive permissions, such as one created with mktemp -d, for diagnostic JSON and history comparison outputs.

Risk: Running network tools with elevated privileges can increase the impact of any local execution mistake.

Mitigation: Run the skill as a normal user and avoid sudo unless a reviewer explicitly determines it is required for the environment.

## Reference(s):

- [Net Detective diagnostic guide](artifact/references/diagnostic-guide.md)
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/skills/net-detective)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON diagnostic inputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally record local history for baseline comparison; no external Python packages are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
