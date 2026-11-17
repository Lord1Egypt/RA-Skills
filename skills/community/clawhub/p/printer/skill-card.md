## Description:

Manage printers via CUPS on macOS, including discovery, adding printers, printing files, queue management, status checks, wake commands, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhvanilpatel](https://clawhub.ai/user/dhvanilpatel)

### License/Terms of Use:


## Use Case:

Developers and macOS users use this skill to operate CUPS printer workflows from an agent, including discovering printers, creating queues, printing files, managing jobs, and diagnosing status issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Printer administration commands can have broad effects, including canceling jobs, rejecting new jobs, disabling queues, or removing a printer queue.

Mitigation: Confirm the printer name and intended scope before running queue-wide or administrative commands such as cancel -a, cupsreject, cupsdisable, or lpadmin -x.

Risk: Commands that use sudo or lpadmin can change server-side printer configuration.

Mitigation: Review printer URIs, queue names, and option values before applying changes, and prefer narrower per-user settings when server-side defaults are not needed.

Risk: Status, wake, and SNMP examples contact printer network addresses.

Mitigation: Run network probes only against authorized printers and verify the target IP address or hostname first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dhvanilpatel/skills/printer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target macOS CUPS tooling; some examples require sudo privileges or optional SNMP utilities.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
