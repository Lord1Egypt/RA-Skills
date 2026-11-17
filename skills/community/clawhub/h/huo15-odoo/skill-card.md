## Description:

Provides a Chinese-language Odoo 19 XML-RPC access guide for configuring connections, querying and changing Odoo business records, troubleshooting common errors, and running a local Docker development setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business-system operators use this skill to guide Odoo 19 XML-RPC setup, authentication, model operations, CRM activity workflows, reporting examples, troubleshooting, and local Docker development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses Odoo credentials for access to business data.

Mitigation: Use a least-privileged, revocable Odoo account and avoid granting production access without review.

Risk: The skill recommends bypassing TLS certificate verification for SSL troubleshooting.

Mitigation: Use the SSL verification bypass only in controlled non-production troubleshooting; fix certificate trust for normal use.

Risk: The skill includes examples for write, delete, bulk conversion, and activity-creation operations on Odoo records.

Mitigation: Require confirmation before allowing an agent to run data-changing or bulk operations, especially in production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-odoo)
- [Odoo Docker configuration repository](https://cnb.cool/huo15/tools/odoo19_docker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes XML-RPC request examples, configuration prompts, troubleshooting notes, and Docker commands.]

## Skill Version(s):

1.7.1 (source: artifact/skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
