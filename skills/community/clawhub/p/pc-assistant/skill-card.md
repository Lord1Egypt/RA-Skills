## Description:

PC Assistant runs local PC healthcheck diagnostics across Linux, macOS, and Windows and produces system information with actionable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningtoba](https://clawhub.ai/user/ningtoba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and end users use this skill to collect local system diagnostics, identify storage, memory, service, network, and security-log issues, and receive maintenance recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Healthcheck reports may contain sensitive local system details and are saved as plaintext.

Mitigation: Run as a regular user, write reports to a private directory with restrictive permissions, and do not share generated reports publicly.

Risk: Security-audit sections can collect environment, shell history, SSH, login, package, process, network, and log details.

Mitigation: Review and redact reports before any transfer, avoid collecting sections that are not needed, and prefer publisher-provided opt-in or redacted modes before routine use.

Risk: Scheduled runs can repeatedly inventory a host and store reports in default temporary locations.

Mitigation: Configure a private output path, enable retention cleanup, and audit generated files after scheduled runs.

Risk: The scheduler sources a shell configuration file before execution.

Mitigation: Use only a trusted configuration file with limited variables, keep it writable only by the intended user, and inspect it before enabling cron execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningtoba/skills/pc-assistant)
- [Publisher profile](https://clawhub.ai/user/ningtoba)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plaintext healthcheck reports, JSON summaries, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are timestamped and may be written to configurable local output directories.]

## Skill Version(s):

1.2.5 (source: server release metadata and artifact install.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
