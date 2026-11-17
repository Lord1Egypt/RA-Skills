## Description:

Manage Odoo contacts, business objects, and metadata through Odoo's XML-RPC External API with generic CRUD operations and context-aware instance, database, and credential resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willykinfoussia](https://clawhub.ai/user/willykinfoussia)

### License/Terms of Use:


## Use Case:

Developers and business operators use this skill to inspect and manage Odoo records across configured instances and databases, including contacts, arbitrary business models, and model metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad authority over business data through generic Odoo CRUD operations.

Mitigation: Use a least-privileged Odoo account or API key, test in staging first, and require explicit confirmation before create, update, or delete operations.

Risk: Odoo credentials could be sent to an unintended or user-supplied endpoint when context overrides change the resolved URL or database.

Mitigation: Verify the exact Odoo URL and database before authenticating, and avoid session or temporary overrides unless the target instance is trusted.

## Reference(s):

- [Odoo External API documentation](https://www.odoo.com/documentation/18.0/fr/developer/reference/external_api.html)
- [Odoo documentation](https://www.odoo.com/documentation/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with XML-RPC examples, shell snippets, configuration details, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ODOO_URL, ODOO_DB, ODOO_USERNAME, and ODOO_PASSWORD; ODOO_API_KEY may replace the password when configured.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
