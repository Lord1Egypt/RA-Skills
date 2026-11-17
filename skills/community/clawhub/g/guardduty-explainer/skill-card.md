## Description:

Translate GuardDuty findings into plain-English incident summaries with actionable response steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Security engineers and incident responders use this skill to interpret exported AWS GuardDuty findings, assess severity and false-positive likelihood, map activity to MITRE ATT&CK, and produce prioritized response steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GuardDuty exports can contain sensitive operational identifiers.

Mitigation: Review exports before use and remove unnecessary account IDs, resource IDs, IP addresses, hostnames, bucket or object names, usernames, and similar identifiers.

Risk: Credentials or session material could be pasted alongside security findings.

Mitigation: Do not include credentials, access keys, secret keys, or session tokens in the provided data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with incident summaries, response playbooks, and inline AWS CLI command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only analysis of user-provided GuardDuty exports or console text; no direct AWS account access.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
