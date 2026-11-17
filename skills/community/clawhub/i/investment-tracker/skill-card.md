## Description:

Investment Tracker App helps an agent query and update portfolio holdings, cash balances, diary entries, equity curve data, benchmark comparisons, and screenshot-based holding imports through a local backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[20czy](https://clawhub.ai/user/20czy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to manage a local personal investment tracker: reviewing holdings and cash, recording diary and equity curve updates, comparing performance with HS300 data, and importing brokerage screenshots after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive portfolio data and brokerage screenshots may be handled by the local backend and configured AI vision provider.

Mitigation: Use only trusted AI provider settings, redact screenshots when possible, and avoid uploading unnecessary account identifiers.

Risk: The backend exposes financial data APIs on port 8000 when running.

Mitigation: Bind the backend to 127.0.0.1 or protect it with authentication and firewall controls; do not expose it directly to a network.

Risk: Write, rollback, delete, and reset operations can alter or remove investment records.

Mitigation: Require explicit user confirmation for write operations and keep independent backups of the local SQLite database.

Risk: The skill depends on an external backend that is not included in the artifact.

Mitigation: Install only a pinned, reviewed backend version from a trusted source before using the skill with real portfolio data.

## Reference(s):

- [Investment Tracker API Quick Reference](references/api-docs.md)
- [ClawHub Skill Page](https://clawhub.ai/20czy/skills/investment-tracker)
- [Publisher Profile](https://clawhub.ai/user/20czy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and structured API-response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, a running local backend, and DASHSCOPE_API_KEY for screenshot analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
