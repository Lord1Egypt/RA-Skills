## Description:

Generate, review, and optimize Ansible automation artifacts, including playbooks, roles, inventories, Jinja2 templates, ansible.cfg files, Galaxy dependencies, AWX-related guidance, and YAML-based infrastructure automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klima911](https://clawhub.ai/user/klima911)

### License/Terms of Use:


## Use Case:

Developers, infrastructure engineers, and DevOps teams use this skill to draft, review, and organize Ansible automation for server configuration, application deployment, inventory management, reusable roles, templates, and validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Ansible defaults may weaken infrastructure security if used unchanged against real systems.

Mitigation: Review and change security defaults before use: keep SSH host key checking enabled, avoid defaulting to ~/.ssh/id_rsa, require explicit approval for root become, pin dependencies to reviewed versions or commits, restrict fact cache storage, and encrypt or redact Vault values before committing them.

Risk: Generated playbooks, roles, inventories, and templates can change managed hosts if run without review.

Mitigation: Review generated artifacts before execution and run syntax checks, dry runs with --check --diff, and ansible-lint as applicable.

## Reference(s):

- [EZ Ansible Skill release page](https://clawhub.ai/klima911/skills/klimatex911)
- [Publisher profile](https://clawhub.ai/user/klima911)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML, INI, Jinja2, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces generated Ansible artifacts with file paths, validation commands, run instructions, and security notes for human review before execution.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
