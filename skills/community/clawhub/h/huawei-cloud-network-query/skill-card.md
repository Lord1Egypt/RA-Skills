## Description: <br>
Queries Huawei Cloud network resources across VPC, EIP, ELB, NAT, VPN, and DNS using packaged read-only Python query scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and operations teams use this skill to inspect Huawei Cloud network topology, configuration, identifiers, dependencies, and status without creating, modifying, or deleting resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Huawei Cloud access credentials and can query account resource data. <br>
Mitigation: Use temporary, least-privilege, read-only Huawei Cloud credentials and avoid exposing credential environment variable values in prompts, logs, or outputs. <br>
Risk: Security evidence flags TLS verification bypasses and runtime dependency/bootstrap behavior. <br>
Mitigation: Review the packaged scripts before installation, remove TLS verification bypasses, pin dependencies, and require explicit user consent before environment changes. <br>
Risk: Returned inventory can include sensitive network topology, security group, load balancer, VPN, DNS, and resource identifier data. <br>
Mitigation: Limit queries to necessary regions and resources, redact sensitive fields before sharing, and cache or store outputs only where access is controlled. <br>


## Reference(s): <br>
- [DNS Python Script Usage Guide](artifact/references/dns/guide.md) <br>
- [EIP Python Script Usage Guide](artifact/references/eip/guide.md) <br>
- [ELB Python Script Usage Guide](artifact/references/elb/guide.md) <br>
- [NAT Gateway Python Script Usage Guide](artifact/references/nat/guide.md) <br>
- [VPC Python Script Usage Guide](artifact/references/vpc/guide.md) <br>
- [VPN Python Script Usage Guide](artifact/references/vpn/guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON query results from packaged scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cloud resource IDs, names, status, topology, quotas, and dependency information returned by Huawei Cloud APIs.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
