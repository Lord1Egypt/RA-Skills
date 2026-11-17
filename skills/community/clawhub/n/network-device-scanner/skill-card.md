## Description:

Scans a local network for active devices and common open ports, then returns a formatted Markdown table with IP addresses, MAC addresses, open ports, and inferred device types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doooxu](https://clawhub.ai/user/doooxu)

### License/Terms of Use:

MIT-0

## Use Case:

Network administrators and developers use this skill to inventory devices and identify common exposed services on networks they own or are authorized to assess.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill actively probes network hosts.

Mitigation: Use it only on networks the user owns or has explicit permission to assess.

Risk: The scan scope is hardcoded to 172.16.10.x and can be broadened through SCAN_EXTRA_IPS without clear confirmation.

Mitigation: Confirm the target network before execution and remove or constrain SCAN_EXTRA_IPS and hardcoded network assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doooxu/skills/network-device-scanner)
- [ClawHub publisher profile](https://clawhub.ai/user/doooxu)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands]

**Output Format:** [Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports discovered IP addresses, MAC addresses, common open ports, and inferred device types.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
