## Description:

Network forensics evidence collection and analysis during security incidents, scoped to packet captures, flow data, forwarding tables, routing state, and device logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Security responders and network engineers use this skill during authorized incidents to collect network artifacts, analyze lateral movement, verify containment, and reconstruct network timelines across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packet captures, support bundles, and saved configurations can contain sensitive incident evidence.

Mitigation: Collect evidence only with authorization, use narrow filters and time or packet limits, transfer files to approved encrypted evidence storage, and remove temporary on-device copies according to policy.

Risk: On-device packet capture and evidence export can affect network device performance.

Mitigation: Monitor device health during collection and prefer bounded captures with explicit packet or duration limits.

Risk: The skill is labeled read-only while some evidence preservation steps write files to device storage.

Mitigation: Treat file export and save operations as evidence collection actions that require incident-response approval and documented chain of custody.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vahagn-madatyan/skills/incident-response-network)
- [Network Forensics CLI Reference](references/cli-reference.md)
- [Network Forensics Workflow](references/forensics-workflow.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with vendor-labeled CLI commands and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only containment verification guidance; evidence collection may create packet capture, support bundle, and configuration files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
