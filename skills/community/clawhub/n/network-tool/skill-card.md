## Description:

Display and manage network interfaces, connections, and routing information. Use for network diagnostics and configuration analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to inspect network state and run diagnostics such as DNS lookups, connectivity checks, HTTP requests, port checks, and speed tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented scope understates active network probing and arbitrary HTTP request capabilities.

Mitigation: Review and approve the implemented command set before deployment, and update public documentation so users understand the actual network authority granted.

Risk: Port scans and HTTP requests can affect systems that the user does not own or have permission to test.

Mitigation: Require explicit consent, allowed target ranges, and rate or port-range limits before enabling active checks.

Risk: Public IP and speed-test commands contact third-party services.

Mitigation: Disclose third-party network calls and allow operators to disable those commands in restricted environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and terminal-style diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network operations can contact user-specified hosts and third-party IP or speed-test services.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
