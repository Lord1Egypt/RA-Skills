## Description:

Provides Odoo 19 module development guidance covering project structure, model definitions, view design, access control, business logic, automated actions, and development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft and review Odoo 19 module structure, Python models, XML views, ACL files, record rules, manifests, and installation or debugging steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included Odoo ACL example can grant broad create, edit, and delete permissions, including an all-users manager row if copied directly into a production module.

Mitigation: Review and replace the ACL template before production use: define explicit groups, avoid delete permission by default, and add record rules and tests for portal, public, internal, and manager users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-odoo19-module-dev)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, XML, CSV, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Odoo module file structures, manifest examples, model code, view definitions, ACL templates, record rules, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
