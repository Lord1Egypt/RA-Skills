## Description: <br>
Generate, review, and optimize Ansible automation artifacts such as playbooks, roles, inventories, Jinja2 templates, variable files, and CI/CD-ready project layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klima911](https://clawhub.ai/user/klima911) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to produce Ansible playbooks, role scaffolds, inventories, templates, variables, project structures, and validation commands for YAML-based configuration management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Ansible YAML and shell commands can change infrastructure if run without review. <br>
Mitigation: Review generated artifacts before execution, run syntax checks, ansible-lint, and check mode first, and limit runs to the intended inventory or hosts. <br>
Risk: Inventory, vault, and configuration examples may involve secrets or privileged host access. <br>
Mitigation: Use ansible-vault for sensitive values, avoid committing plaintext passwords or vault password files, and keep host-key checking enabled unless there is a documented reason to disable it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, INI, Jinja2, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes file paths, validation commands, idempotency notes, lint guidance, and vault handling reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
