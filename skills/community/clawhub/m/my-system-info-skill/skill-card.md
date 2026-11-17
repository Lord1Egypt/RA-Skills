## Description:

Generates Markdown system operations reports that capture operating system, CPU, memory, disk, network, process, and service status information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viztazeng](https://clawhub.ai/user/viztazeng)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and system administrators use this skill to collect a local snapshot of host health and environment details for diagnostics, troubleshooting, and routine operations checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include sensitive host details such as hostnames, usernames, IP addresses, mounted filesystems, running processes, and services.

Mitigation: Generate reports in a trusted working directory and review or redact the Markdown output before sharing it.

Risk: The skill writes local report files and may be run in directories where generated diagnostics are easy to expose accidentally.

Mitigation: Confirm the output location is appropriate and avoid unnecessary privileged execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viztazeng/skills/my-system-info-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown report file with terminal text identifying the generated file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped .md report files to system-tool-results by default.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
