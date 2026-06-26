## Description: <br>
Manage PocketSmith transactions, categories, and financial data via the API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lextoumbourou](https://clawhub.ai/user/lextoumbourou) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and finance-focused agents use this skill to read PocketSmith account data, search and categorize transactions, manage categories, labels, budgets, and optionally perform write operations after explicit opt-in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive PocketSmith financial data using POCKETSMITH_DEVELOPER_KEY. <br>
Mitigation: Install only from a trusted release and provide the developer key only in environments where the agent is authorized to access that financial data. <br>
Risk: Optional write operations can create, update, delete, or recategorize real financial records. <br>
Mitigation: Keep POCKETSMITH_ALLOW_WRITES unset for read-only use, enable it only for intended changes, and verify transaction or category IDs before executing write commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lextoumbourou/pocketsmith-skill) <br>
- [PocketSmith API reference](https://developers.pocketsmith.com/reference) <br>
- [PocketSmith API base URL](https://api.pocketsmith.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON command output with Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses YYYY-MM-DD dates and requires POCKETSMITH_DEVELOPER_KEY for authenticated PocketSmith API access.] <br>

## Skill Version(s): <br>
v1.0.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
