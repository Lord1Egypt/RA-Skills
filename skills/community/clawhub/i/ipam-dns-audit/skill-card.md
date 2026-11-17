## Description:

IP Address Management and DNS record reconciliation audit covering subnet utilization analysis, DNS forward/reverse consistency, IP conflict detection, and DHCP scope health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network, DNS, and infrastructure engineers use this skill to audit IPAM records against live subnet activity and DNS records, then produce reconciliation findings for conflicts, stale records, DHCP scope health, and capacity planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is marked read-only but includes remediation examples such as deleting DNS records or disabling network ports.

Mitigation: Treat remediation as recommendations only and require operator review plus normal change-management approval before changing DNS or network state.

Risk: Credential-handling examples can expose API tokens or passwords if pasted directly into shells, history, or logs.

Mitigation: Use least-privileged read-only accounts and pass secrets through approved secret-management or environment mechanisms rather than inline command arguments.

Risk: Some IPAM examples use disabled TLS certificate verification for Infoblox API calls.

Mitigation: Use validated TLS for production access and reserve disabled certificate checks for controlled tests only.

## Reference(s):

- [IPAM/DNS Audit CLI Reference](references/cli-reference.md)
- [Subnet and DNS Reference](references/subnet-dns-reference.md)
- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/skills/ipam-dns-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples and structured audit report tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audit and remediation guidance; it does not execute changes by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
