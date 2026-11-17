## Description:

Interpersonal Knowledge Layer is a per-contact permission system that helps an agent decide what personal information it may share with other agents or users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smartinelle](https://clawhub.ai/user/smartinelle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure contact, permission, knowledge, and audit JSON files so an agent can gate personal-information disclosures by requester and context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal facts, contact mappings, permission rules, and disclosure history in local plaintext JSON files.

Mitigation: Restrict the IKL directory and files to the user's account and avoid storing highly sensitive values unless necessary.

Risk: The privacy gate is under-scoped as a hard security boundary.

Mitigation: Do not rely on the skill alone for high-assurance authorization; pair it with an external authorization component for sensitive deployments.

Risk: Audit logs can retain sensitive disclosure history and shared values.

Mitigation: Use log-redaction controls and review audit retention before deploying the skill.

Risk: Default relationship permissions may share more information than a user expects.

Mitigation: Review and adjust the default relationship permissions before adding personal knowledge entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smartinelle/skills/ikl)
- [contacts.json schema](artifact/references/schema-contacts.md)
- [permissions.json schema](artifact/references/schema-permissions.md)
- [knowledge.json schema](artifact/references/schema-knowledge.md)
- [audit log format](artifact/references/audit-format.md)
- [security design](artifact/references/security-design.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON files]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local plaintext IKL files for contacts, permissions, knowledge, and audit entries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
