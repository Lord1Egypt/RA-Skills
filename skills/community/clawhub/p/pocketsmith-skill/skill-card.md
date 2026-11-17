## Description:

Manage PocketSmith transactions, categories, and financial data via the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lextoumbourou](https://clawhub.ai/user/lextoumbourou)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect PocketSmith financial data, search transactions, manage categories, review budgets, and optionally create, update, delete, or refresh financial records through PocketSmith API-backed CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete PocketSmith financial records, and the security review notes that advertised write protection is not enforced across the public API layer.

Mitigation: Keep POCKETSMITH_ALLOW_WRITES unset for read-only use. If writes are enabled, require manual confirmation before create, update, delete, category deletion, or forecast refresh actions.

Risk: The required PocketSmith developer key gives the agent access to financial data.

Mitigation: Install only when agent access to PocketSmith financial data is acceptable, provide the key through a controlled environment variable, and avoid exposing command output or credentials in shared logs.

Risk: Direct imports of the Python API can bypass the CLI's write guard.

Mitigation: Prefer CLI execution for write operations until write protection is enforced at the client or API layer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lextoumbourou/skills/pocketsmith-skill)
- [PocketSmith developer API reference](https://developers.pocketsmith.com/reference)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON from CLI commands, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POCKETSMITH_DEVELOPER_KEY. Write operations require POCKETSMITH_ALLOW_WRITES=true and should receive manual confirmation before execution.]

## Skill Version(s):

v1.0.0 (source: ClawHub release metadata; package version 1.0.0 in pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
