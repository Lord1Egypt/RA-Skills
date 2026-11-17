## Description:

Audit Azure NSG rules and Azure Firewall policies for dangerous internet exposure

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to review user-provided Azure NSG, effective rule, and Azure Firewall policy exports for risky internet exposure and to receive prioritized findings with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription-wide Network Contributor access is broader than the skill's stated read-only audit purpose.

Mitigation: Use Reader or a narrowly scoped custom audit role where possible, and reserve broader access only for review steps that require it.

Risk: User-provided Azure exports or pasted console output could contain credentials, access keys, or secret keys.

Mitigation: Confirm supplied data contains no credentials or secrets before processing it with the agent.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with findings tables, JSON snippets, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided exports or topology descriptions; does not request credentials or directly access Azure.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
