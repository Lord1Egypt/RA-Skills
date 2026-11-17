## Description:

Audit Azure Key Vault configuration, access policies, and secret hygiene for credential exposure risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud engineers, and security teams use this skill to review user-provided Azure Key Vault exports for configuration, access, and secret-hygiene risks and to generate remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided Azure exports may accidentally include secret values, connection strings, or credentials.

Mitigation: Review and redact exports before using the skill, and provide only read-only configuration, policy, and expiry data.

Risk: Findings and shared outputs may reveal sensitive details about the Azure environment and access model.

Mitigation: Treat generated findings, vault names, RBAC details, and remediation plans as sensitive operational security material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/key-vault-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with findings tables, Azure CLI examples, Bicep snippets, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; analyzes user-provided read-only Azure exports and does not directly access Azure accounts.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
