## Description: <br>
Network forensics evidence collection and analysis during security incidents, including volatile evidence preservation, lateral movement detection from flow and ARP/MAC/CAM data, and containment verification across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, incident responders, and network engineers use this skill to collect and analyze network artifacts during active or post-incident investigations, including flow records, packet captures, forwarding state, routing state, device logs, and containment verification evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled read-only, but packet capture, export, support-bundle, and running-configuration commands can affect live network devices or write sensitive evidence files. <br>
Mitigation: Use only for authorized incident-response work, obtain approval before capture or export steps, limit packet count and duration, monitor device CPU and storage, and define evidence transfer, retention, and cleanup steps. <br>
Risk: Collected packet captures, running configurations, support bundles, logs, and flow data may contain sensitive network, credential, or payload information. <br>
Mitigation: Protect evidence as sensitive data, compute and record hashes, preserve chain of custody, restrict access to authorized responders, and follow approved retention policies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/incident-response-network) <br>
- [Network Forensics CLI Reference](references/cli-reference.md) <br>
- [Network Forensics Workflow](references/forensics-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with inline network CLI commands and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are scoped to network forensics evidence collection, analysis, containment verification, timeline reconstruction, and documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
