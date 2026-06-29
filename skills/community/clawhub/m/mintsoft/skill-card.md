## Description: <br>
Mintsoft warehouse-management API wrapper - query warehouses, orders, products, stock levels, ASNs, and the Product Usage stock-flow report from a single ms-apikey credential. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berkgungor](https://clawhub.ai/user/berkgungor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and warehouse-support agents use this skill to inspect Mintsoft warehouse, order, product, stock, ASN, and stock-flow data through a JSON-emitting command-line wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read tenant-scoped Mintsoft warehouse, order, product, ASN, inventory, and stock-flow data through the configured API credential. <br>
Mitigation: Install and run it only for users or agents that are authorized to access that Mintsoft tenant data. <br>
Risk: The optional auth flow caches a Mintsoft API key locally for up to 24 hours. <br>
Mitigation: Prefer a pre-issued MINTSOFT_API_KEY in the environment; if the cache is used, treat ~/.config/mintsoft-skill/token.json as a secret and rely on its restrictive file permissions. <br>
Risk: Passing Mintsoft passwords as command-line arguments can expose credentials through shell history or process listings. <br>
Mitigation: Use environment variables for credentials and avoid command-line password flags where possible. <br>


## Reference(s): <br>
- [Mintsoft API endpoint reference](https://api.mintsoft.co.uk/swagger/index.html) <br>
- [Mintsoft API base URL](https://api.mintsoft.co.uk/api) <br>
- [httpx documentation](https://www.python-httpx.org/) <br>
- [ClawHub skill page](https://clawhub.ai/berkgungor/mintsoft) <br>
- [Publisher profile](https://clawhub.ai/user/berkgungor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [List commands return JSON objects with a count and resource array; single-record commands return one JSON resource; errors return JSON and a non-zero exit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
