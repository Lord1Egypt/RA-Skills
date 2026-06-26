## Description: <br>
IP Address Management and DNS record reconciliation audit covering subnet utilization analysis, DNS forward/reverse consistency, IP conflict detection, and DHCP scope health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers, DNS administrators, and security or compliance teams use this skill to compare IPAM records, live subnet activity, DHCP state, and DNS records so they can identify stale records, duplicate assignments, subnet exhaustion, and reconciliation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auditing networks or DNS zones without authorization can expose sensitive infrastructure data. <br>
Mitigation: Install and use the skill only for authorized targets and scope the audit to approved networks and zones. <br>
Risk: Credentials or API tokens used for IPAM, DNS, or network device access could be exposed in prompts or shell history. <br>
Mitigation: Use scoped read-only credentials and avoid placing real secrets directly in prompts, transcripts, or shell history. <br>
Risk: TLS verification bypass patterns can normalize insecure access to management APIs. <br>
Mitigation: Do not copy curl patterns that disable certificate checks unless explicitly approved by the organization. <br>
Risk: Remediation advice such as deleting DNS records or changing network ports could disrupt production systems if applied automatically. <br>
Mitigation: Treat remediation as manual change guidance and require separate human-reviewed change control before making changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vahagn-madatyan/ipam-dns-audit) <br>
- [IPAM/DNS Audit CLI Reference](references/cli-reference.md) <br>
- [Subnet and DNS Reference](references/subnet-dns-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, audit tables, and report structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only audit guidance and remediation recommendations for human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
