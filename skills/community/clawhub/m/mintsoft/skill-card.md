## Description:

Mintsoft warehouse-management API wrapper - query warehouses, orders, products, stock levels, ASNs, and the Product Usage stock-flow report from a single ms-apikey credential.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berkgungor](https://clawhub.ai/user/berkgungor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to let an agent query Mintsoft warehouse, order, product, inventory, ASN, and product-usage data through the bundled CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mintsoft credentials and cached API keys are sensitive business secrets.

Mitigation: Prefer MINTSOFT_API_KEY, keep token caches in private user directories, restrict file permissions, and rotate keys when access is no longer needed.

Risk: The skill can expose warehouse, order, product, stock, ASN, and product-usage data to an agent.

Mitigation: Install it only for agents and users authorized to access the connected Mintsoft tenant and operational data.

Risk: The runtime depends on httpx for outbound API calls.

Mitigation: Install httpx in a pinned or isolated Python environment when possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/berkgungor/skills/mintsoft)
- [Mintsoft API Swagger](https://api.mintsoft.co.uk/swagger/index.html)
- [Mintsoft API Base Endpoint](https://api.mintsoft.co.uk/api)
- [httpx Documentation](https://www.python-httpx.org/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [List commands support summary output; long pagination has a default 90-second deadline.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
