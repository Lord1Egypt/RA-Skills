## Description:

Generates a comprehensive local hardware and system information report across macOS, Linux, and Windows, including system overview, CPU, memory, storage, GPU/display, network, battery, device, sensor, and real-time status details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[braveheartzjh](https://clawhub.ai/user/braveheartzjh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for a broad local hardware inventory and receive a structured Markdown report. It is intended for configuration checks, troubleshooting context, and device capability review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place a full local hardware inventory in the agent conversation, including sensitive identifiers such as serial numbers, UUIDs, and MAC addresses.

Mitigation: Use it only when a full inventory is needed, and redact identifiers before sharing or storing the report.

Risk: Some requested hardware fields may require elevated commands.

Mitigation: Do not approve sudo unless a specific requested field truly requires it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Analysis, Guidance]

**Output Format:** [Structured Markdown hardware report with command-derived findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive local device identifiers such as serial numbers, UUIDs, MAC addresses, storage details, and battery data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
