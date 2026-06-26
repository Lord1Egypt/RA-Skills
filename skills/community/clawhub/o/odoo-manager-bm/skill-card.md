## Description: <br>
Manage Odoo contacts, business objects, and metadata through the External XML-RPC API, including generic CRUD operations, model introspection, and context-aware instance, database, and credential resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernhmueller](https://clawhub.ai/user/bernhmueller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Odoo records across contacts, business models, and metadata from an agent workflow. It is intended for environments where the agent is allowed to use configured Odoo credentials and perform read or write operations through XML-RPC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete Odoo business records through configured credentials. <br>
Mitigation: Use a dedicated least-privilege Odoo account and require explicit approval before create, update, or delete actions. <br>
Risk: Context switching can point the agent at the wrong Odoo instance or database. <br>
Mitigation: Verify the resolved URL and database before every write or delete operation and reset session context after sensitive work. <br>
Risk: Odoo passwords or API keys grant account-level access to business data. <br>
Mitigation: Store credentials in environment variables or a secrets manager, avoid admin credentials, and never display full secrets in responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bernhmueller/odoo-manager-bm) <br>
- [Odoo External API documentation](https://www.odoo.com/documentation/18.0/fr/developer/reference/external_api.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Python, shell, and XML-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include Odoo connection context summaries, record data, CRUD operation plans, and troubleshooting guidance; secrets should not be displayed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
