## Description: <br>
Manage Odoo contacts, business objects, and metadata via the official External XML-RPC API, including generic CRUD operations, partner workflows, model introspection, and dynamic instance, database, and credential resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willykinfoussia](https://clawhub.ai/user/willykinfoussia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, administrators, and operations teams use this skill to inspect and manage Odoo records through XML-RPC while switching between configured instances, databases, and credentials. It is suited for contact management, generic model CRUD tasks, and metadata discovery when the agent has authorized Odoo access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority to modify or delete live Odoo business records. <br>
Mitigation: Use a dedicated least-privilege Odoo API key, verify the active URL, database, and user before write or delete actions, test changes in staging first, and avoid broad bulk operations. <br>
Risk: Session or temporary context can point the agent at a sensitive or unintended Odoo environment. <br>
Mitigation: Review the resolved connection context before sensitive work and clear session context after completing tasks. <br>


## Reference(s): <br>
- [Odoo Documentation](https://www.odoo.com/documentation/) <br>
- [Odoo External API Documentation](https://www.odoo.com/documentation/18.0/fr/developer/reference/external_api.html) <br>
- [ClawHub Odoo Manager Release](https://clawhub.ai/willykinfoussia/odoo-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with XML-RPC examples, configuration snippets, and structured operation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Odoo record summaries, resolved non-secret connection context, and error-handling guidance.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
