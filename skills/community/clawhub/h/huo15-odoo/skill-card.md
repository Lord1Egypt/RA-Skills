## Description: <br>
Provides Odoo 19 XML-RPC guidance, configuration prompts, and examples for querying and operating Huo15 Odoo business models, including projects, tasks, CRM, inventory, sales, Knowledge, and local Docker development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Odoo connection details and generate XML-RPC examples for common ERP workflows. It is intended for agents that need guidance, code snippets, shell commands, and configuration steps for Huo15 Odoo 19 integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide live ERP credentials and may store them in local OpenClaw configuration files. <br>
Mitigation: Install only from a trusted publisher, use a least-privilege Odoo account, and confirm where credential files are stored and who can read them. <br>
Risk: The artifact documents disabling TLS certificate verification for Odoo connections. <br>
Mitigation: Avoid production credentials until TLS verification is fixed or certificate trust is handled safely. <br>
Risk: The Odoo API examples include create, update, and delete operations against business records. <br>
Mitigation: Review generated operations before execution, test with non-production data when possible, and restrict the Odoo account to only the required models and permissions. <br>


## Reference(s): <br>
- [Odoo Docker Configuration Repository](https://cnb.cool/huo15/tools/odoo19_docker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Odoo XML-RPC examples and configuration guidance; no structured machine-readable output contract is specified.] <br>

## Skill Version(s): <br>
1.7.1 (source: skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
