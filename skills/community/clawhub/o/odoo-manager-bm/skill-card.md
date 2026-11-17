## Description:

Manage Odoo contacts, business objects, and metadata through the official External XML-RPC API, including generic CRUD operations, partner workflows, model introspection, and context-aware instance, database, and credential resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernhmueller](https://clawhub.ai/user/bernhmueller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect and manage Odoo records across configured instances and databases. It supports connection checks, partner management, generic model CRUD, and Odoo model metadata discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly create, update, or delete live Odoo business data.

Mitigation: Use a dedicated least-privilege Odoo account or API key, verify the resolved URL, database, model, and record count before mutations, and avoid production mutations without explicit confirmation and preview steps.

Risk: Saved credentials may be reused with a changed Odoo server URL or database context.

Mitigation: Restrict use to trusted Odoo URLs, review context overrides before each sensitive operation, and reset temporary or session context after cross-instance work.

## Reference(s):

- [Odoo External API documentation](https://www.odoo.com/documentation/18.0/fr/developer/reference/external_api.html)
- [ClawHub skill page](https://clawhub.ai/bernhmueller/skills/odoo-manager-bm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline text, JSON examples, Python XML-RPC snippets, and shell environment-variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Odoo XML-RPC call patterns and operational guidance; does not expose full secrets when describing resolved context.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
