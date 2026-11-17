## Description:

Test network connectivity to remote hosts by sending ICMP echo requests. Use for network diagnostics and latency measurement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check basic network reachability and latency to a specified hostname or IP address with ICMP ping diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send ICMP network probes to hostnames or IP addresses supplied by the user.

Mitigation: Use it only against systems you are authorized to test and review target hosts before execution.

Risk: The current implementation is narrower than the documented options and executes a fixed four-packet ping.

Mitigation: Confirm runtime behavior in the target environment and update the documentation or script before relying on unsupported options.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ping diagnostic commands or guidance for a single target host; the bundled script executes four ICMP echo requests.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
