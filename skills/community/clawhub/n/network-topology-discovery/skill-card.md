## Description: <br>
Iterative network topology discovery using CDP/LLDP neighbor protocols, ARP/MAC table correlation, and routing table analysis across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and incident responders use this skill to map device adjacencies, routing boundaries, endpoints, and anomalies inside an authorized discovery scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes that the read-only label conflicts with remediation guidance that could change live network device configuration. <br>
Mitigation: Use the skill for discovery only, and route enablement, VLAN, trunk, routing-policy, clearing, and port-security changes through normal change approval. <br>
Risk: Topology, routing, MAC, and ARP outputs can expose sensitive infrastructure details. <br>
Mitigation: Define a strict discovery boundary, use least-privilege read-only device accounts, and protect collected topology outputs as sensitive data. <br>


## Reference(s): <br>
- [Network Topology Discovery on ClawHub](https://clawhub.ai/vahagn-madatyan/network-topology-discovery) <br>
- [CLI Reference](artifact/references/cli-reference.md) <br>
- [Discovery Workflow](artifact/references/discovery-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with network CLI command examples and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized SSH or console access to devices in the discovery scope; topology outputs can contain sensitive network information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
