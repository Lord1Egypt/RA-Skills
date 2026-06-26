## Description: <br>
Audit Azure NSG rules and Azure Firewall policies for dangerous internet exposure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Cloud security engineers and Azure administrators use this skill to review user-supplied NSG, effective-rule, and Azure Firewall exports for risky internet exposure and remediation recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to share detailed Azure infrastructure exports and topology information. <br>
Mitigation: Before sharing exports, redact subscription IDs, resource IDs, hostnames, public and private IP addresses, NIC IDs, topology details, unrelated resources, and any credentials, keys, or secrets. <br>
Risk: The skill references broad Azure permissions for some effective-rules queries. <br>
Mitigation: Use Reader-level access or a minimal custom role when possible, and grant broader permissions only when the specific query requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/nsg-firewall-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with findings tables, JSON snippets, and inline Azure CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes user-provided exports and does not access Azure directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
